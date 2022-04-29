#amqp://guest:guest@rabbitmq:5672
from turtle import title
import pika, json

from main import Product, db

params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Received in main')
    data =  json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(id=data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product updated')
    
    if properties.content_type == 'product_created':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')


channel.start_consuming()

channel.close()