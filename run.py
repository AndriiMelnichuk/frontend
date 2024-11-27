from app import create_app
from app.rabbitMq.consumer import RabbitMQConsumer
from app.rabbitMq.producer import RabbitMQProducer

app = create_app()
app.config["SECRET_KEY"] = 'your_secret_key'
RabbitMQConsumer()
RabbitMQProducer()
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
