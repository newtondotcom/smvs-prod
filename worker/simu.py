import pika
from s3 import *
import json
import datetime
import requests
from dotenv import load_dotenv
load_dotenv()

print(' Connecting to server ...')

RABBIT_HOST = os.environ.get("RABBIT_HOST")
RABBIT_PORT = os.environ.get("RABBIT_PORT")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST,port=RABBIT_PORT))
except pika.exceptions.AMQPConnectionError:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

videos_bucket_name = "videos"
thumbnails_bucket_name = "thumbnails"
s3_videos = S3(videos_bucket_name)
s3_minia = S3(thumbnails_bucket_name)

print(' Waiting for messages...')

def callback(ch, method, properties, body):
    bodyjson = json.loads(body)

    print(bodyjson)

    ## Parameters
    key_db = bodyjson['key_db']

    #time.sleep(5)

    # construction of the body for the frontend
    body = {
        "task_id": key_db,
        "time_transcription": 10,
        "time_encoding": 100,
        "time_alignment": 10,
        "done_at": datetime.datetime.now().isoformat(),
        "thumbnail": "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80"
    }
    requests.post("http://localhost:3000/api/dashboard/tasks", json=body)

    #Advice server that file is ready
    ch.basic_ack(delivery_tag=method.delivery_tag)
    exit()
    print(" Done")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()