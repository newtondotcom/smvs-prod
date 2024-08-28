import pika
import time
import json
from dotenv import load_dotenv
load_dotenv("../../.env")

print(' Connecting to server ...')

RABBIT_HOST = os.environ.get("RABBIT_HOST")
RABBIT_PORT = os.environ.get("RABBIT_PORT")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST,port=RABBIT_PORT))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


print(' Waiting for messages...')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    bodyjson = json.loads(body)
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()