import pika
import threading
import json
import uuid
import time

lock = threading.Lock()

class RabbitMQConsumer:
    def __init__(self, host='rabbitmq', port=5672, vhost='/', user='admin', password='password', queue_name='frontend_queue'):
        with lock:
            self.messages = {}
        
        self.queue_name = queue_name
        host = 'localhost'

        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host,
                port,
                vhost,
                pika.PlainCredentials(user, password),                
            )
        )
        self.channel = self.connection.channel()

        # Объявляем очередь
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        # Запуск потребления сообщений в отдельном потоке
        self._stop_event = threading.Event()
        threading.Thread(target=self.start_consuming, daemon=True).start()


    def _callback(self, ch, method, properties, body):
        """Обработчик входящих сообщений."""
        try:
            # Парсим тело сообщения
            message = json.loads(body.decode())
            correlation_id = properties.correlation_id

            # Сохраняем в статическом словаре
            if correlation_id:
                self.add_message(correlation_id, message)
                print(f"[x] Received message with correlation_id={correlation_id}")
            else:
                print(f"[!] Received message without correlation_id")
        except json.JSONDecodeError:
            print(f"[!] Failed to decode message: {body.decode()}")


    def start_consuming(self):
        """Start listen"""
        pass
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._callback,
            auto_ack=True
        )
        print("[x] Waiting for messages. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("[x] Consumer stopped manually.")


    def add_message(self, correlation_id, message):
        with lock:
            self.messages[correlation_id] = message


    def get_message(self, correlation_id):
        """Returns by correlation_id."""
        with lock:
            res = self.messages.get(correlation_id)
            a = self.messages
            # del RabbitMQConsumer.messages[correlation_id]
            return res


    def is_messege_arrived(self, correlation_id):
        with lock:
            d = self.messages
            return correlation_id in self.messages.keys()


    def get_all_messages(self):
        """Returns all meseges"""
        with lock:
            return self.messages


    def __del__(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


class RabbitMQProducer:
    def __init__(self, host='rabbitmq', port=5672, vhost='/', user='admin', password='password'):
        self.channel = None
        self.connection = None
        self.consumer = None
        
        host = 'localhost'
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host,
                port,
                vhost,
                pika.PlainCredentials(user, password)
            )
        )
        self.channel = self.connection.channel()

    
    def start_consumer(self):
        self.consumer = RabbitMQConsumer()


    def __del__(self):
        print('[ERROR]: delete producer')
        self.connection.close()

    
    def send_message_with_response(self, queue_name, message: dict):
        reply_to_queue = 'frontend_queue'

        # Генерируем уникальный идентификатор для сообщения
        correlation_id = str(uuid.uuid4())

        # Отправляем сообщение с указанной очередью для ответа
        retries = 0
        max_retries = 10
        retry_interval = 0.1
        while retries < max_retries:
            try:
                # Попытка отправить сообщение
                self.channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    properties=pika.BasicProperties(
                        reply_to=reply_to_queue,
                        correlation_id=correlation_id,
                        content_type='application/json'
                    ),
                    mandatory=True,
                    body=json.dumps(message)
                )
                print(f"Message sent successfully: {message}")
                return True  # Сообщение успешно отправлено
            except pika.exceptions.AMQPError as e:
                retries += 1
                print(f"Error sending message. Attempt {retries} of {max_retries}. Error: {e}")
                if retries < max_retries:
                    time.sleep(retry_interval)  # Задержка перед повторной попыткой
                else:
                    print("Max retries reached, message sending failed.")
                    return False  # Все попытки исчерпан


        print(f"[x] Sent message with correlation_id: {correlation_id}")

        # Чекаем на ответ в очереди frontend_queue

        while not self.consumer.is_messege_arrived(correlation_id):
            pass
        return self.consumer.get_message(correlation_id)


import pika
import uuid

class RpcClient(object):
    def __init__(self, host='rabbitmq', port=5672, vhost='/', user='admin', password='password'):
        host = 'localhost'
        # Подключаемся к RabbitMQ
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host,
                port,
                vhost,
                pika.PlainCredentials(user, password),                
            )
        )
        self.channel = self.connection.channel()

        # Создаем уникальную очередь для получения ответа
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # Настроим получение ответа
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, msg):
        self.response = None
        self.corr_id = str(uuid.uuid4())  # Уникальный ID для отслеживания ответа

        # Отправляем запрос в очередь "rpc_queue"
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,  # Указываем, куда отправить ответ
                correlation_id=self.corr_id    # Сообщаем уникальный ID для ответа
            ),
            body=msg
        )
        while self.response is None:
            self.connection.process_data_events()  # Ожидаем ответа
        return self.response


