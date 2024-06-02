import pika
import json
import sys

print('Connecting to server ...')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="144.91.123.186", port=15672))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message won't be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print('Waiting for messages...')

channel.basic_qos(prefetch_count=1)

i = 0
nbclear = sys.argv[1]

def callback(ch, method, properties, body):
    global i
    ch.basic_ack(delivery_tag=method.delivery_tag)
    i += 1
    if i == nbclear:
        ch.stop_consuming()
        print("Done")
        return
    print("Done")

channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
