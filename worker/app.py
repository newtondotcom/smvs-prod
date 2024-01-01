import pika
from s3 import *
from utils import *
from gen import *
from silent import *
from s3 import *
from emojis import *
from treat import *

print(' Connecting to server ...')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="141.145.217.120",port=5672))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


print(' Waiting for messages...')

#channel.basic_publish(exchange='', routing_key='task_queue', body='Hello World!')

def callback(ch, method, properties, body):
    print(" Received %s" % body.decode())

    ## Parameters
    file_bucket_name = "videos"
    file_name = "test.mp4"
    emoji = True
    lsilence = True

    #Download file from S3
    local_file_path = "temp/"+file_name
    download_file(file_name, local_file_path,file_bucket_name)

    #Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4","_out.mp4")

    trat_video(path_in,path_out,emoji,lsilence)

    #Upload file to S3
    file_key = path_out
    upload_file(file_key.replace("temp/",""), file_key.replace("temp/",""),file_bucket_name)

    remove_file(file_bucket_name,file_name)
    #remove minia
    #remove_file(file_bucket_name,file_name.replace(".mp4",".png"))

    os.remove(file_name)

    #Advice server that file is ready
    ch.basic_ack(delivery_tag=method.delivery_tag)

    clean_temp()
    print(" Done")
    #exit()

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()