import pika
from minio import Minio
import os
from minio.error import S3Error
from dotenv import load_dotenv
load_dotenv("../../.env")

# Replace these with your AWS credentials and S3 bucket and file information
S3_ACCESS_KEY = os.environ.get("S3_KEY_ID")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
S3_HOST = os.environ.get("S3_HOST")
S3_SECURE = os.environ.get("S3_SECURE")

RABBIT_HOST = os.environ.get("RABBIT_HOST")
RABBIT_PORT = os.environ.get("RABBIT_PORT")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST,port=RABBIT_PORT))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()

def upload_file(file_key, file_s3_name,bucket_name):
    try:
        os.chdir("temp/")
        client = Minio(S3_HOST,
                access_key=S3_ACCESS_KEY,
                secret_key=S3_SECRET_KEY,
                secure=S3_SECURE
        )
        client.fput_object(
                bucket_name, file_key, file_s3_name,
        )
        print(f"File uploaded successfully to S3 key: {file_key}")
        os.chdir("..")
    except Exception as e:
        print(f"Error uploading file: {e}")

upload_file("test.mp4","test.mp4","videos")

body = '{"file_bucket_name":"videos","file_name":"test.mp4","emoji":true,"silence":true}'
channel.basic_publish(exchange='', routing_key='task_queue', body=body)

print(" [x] Sent 'Hello World!'")

channel.close()
connection.close()