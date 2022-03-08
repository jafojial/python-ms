#amqp://guest:guest@rabbitmq:5672
import pika

params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish():
    channel.basic_publish(exchange='', routing_key='admin', body='hello')