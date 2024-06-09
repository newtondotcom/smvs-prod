import pika
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()

print('Connecting to server ...')

host = os.environ.get("RABBIT_HOST")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="144.91.123.186", port=15672))
except pika.exceptions.AMQPConnectionError as exc:
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
