import pika
import os
from dotenv import load_dotenv
load_dotenv()

print('Connecting to server ...')

RABBIT_HOST = os.environ.get("RABBIT_HOST")
RABBIT_PORT = os.environ.get("RABBIT_PORT")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST,port=RABBIT_PORT))
except pika.exceptions.AMQPConnectionError:
    print("Failed to connect to RabbitMQ service. Message won't be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print('Waiting for messages...')

channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Received %r" % body)

channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
