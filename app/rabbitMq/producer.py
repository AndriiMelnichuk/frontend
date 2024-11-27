import pika
import json
import uuid
from .consumer import RabbitMQConsumer

class RabbitMQProducer:
    _instance = None
    channel = None
    connection = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host='rabbitmq', port=5672, vhost='/', user='admin', password='password'):
        if not hasattr(self, '_initialized'):  
            host = 'localhost'
            RabbitMQProducer.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host,
                    port,
                    vhost,
                    pika.PlainCredentials(user, password)
                )
            )
            RabbitMQProducer.channel = RabbitMQProducer.connection.channel()

    def __del__(self):
        self.connection.close()

    
    def send_message_with_response(self, queue_name, message: dict):
        reply_to_queue = 'frontend_queue'

        # Генерируем уникальный идентификатор для сообщения
        correlation_id = str(uuid.uuid4())

        # Отправляем сообщение с указанной очередью для ответа
        RabbitMQProducer.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=reply_to_queue,
                correlation_id=correlation_id,
                content_type='application/json'
            ),
            body=json.dumps(message)
        )
        print(f"[x] Sent message: {message}")

        # Чекаем на ответ в очереди frontend_queue

        while not RabbitMQConsumer.is_messege_arrived(correlation_id):
            pass
        return RabbitMQConsumer.get_message(correlation_id)
