import pika
from minio import Minio
import os
from minio.error import S3Error

# Replace these with your AWS credentials and S3 bucket and file information
aws_access_key_id = 'oJTJnZIz0lJ8RblZMLbb'
aws_secret_access_key = 'nyAeRaWm1vo9mBBwgKqhLzP1Yjws7V5IpVrfKPEe'

print(' Connecting to server ...')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="141.145.217.120",port=5672))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()

def upload_file(file_key, file_s3_name,bucket_name):
    try:
        os.chdir("temp/")
        client = Minio("144.91.123.186:32771",
                access_key=aws_access_key_id,
                secret_key=aws_secret_access_key,
                secure=False
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