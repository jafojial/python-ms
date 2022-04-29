#amqp://guest:guest@rabbitmq:5672
import pika, json

params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)