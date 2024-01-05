import pika
import time
import json

print(' Connecting to server ...')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="144.91.123.186",port=15672))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


print(' Waiting for messages...')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    bodyjson = json.loads(body)
    taskData = bodyjson['taskData']
    silence = bodyjson['silence']
    print(" [x] Silence %r" % silence)
    print(" [x] Task Data %r" % taskData)
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()