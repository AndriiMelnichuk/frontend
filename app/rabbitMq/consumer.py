import pika
import threading
import json
import threading

lock = threading.Lock()

class RabbitMQConsumer:
    _instance = None
    messages = {}  

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self, host='rabbitmq', port=5672, vhost='/', user='admin', password='password', queue_name='frontend_queue'):
        if not hasattr(self, '_initialized'):  
            self._initialized = True
            self.queue_name = queue_name
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
                self.messages[correlation_id] = message
                print(f"[x] Received message with correlation_id={correlation_id}: {message}")
            else:
                print(f"[!] Received message without correlation_id: {message}")
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


    
    @staticmethod
    def get_message(correlation_id):
        """Returns by correlation_id."""
        with lock:
            res = RabbitMQConsumer.messages.get(correlation_id)
            a = RabbitMQConsumer.messages
            print(a)
            del RabbitMQConsumer.messages[correlation_id]
            return res


    
    @staticmethod
    def is_messege_arrived(correlation_id):
        with lock:
            return correlation_id in RabbitMQConsumer.messages.keys()


    
    @staticmethod
    def get_all_messages():
        """Returns all meseges"""
        with lock:
            return RabbitMQConsumer.messages


    def __del__(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


