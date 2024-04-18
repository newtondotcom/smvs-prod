import pika
from s3 import *
from utils import *
from gen import *
from silent import *
from s3 import *
from emojis import *
from processing import *
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
    bodyjson = json.loads(body)

    ## Parameters
    file_bucket_name = bodyjson['file_bucket_name']
    file_name = bodyjson['file_name']
    emoji = bodyjson['emoji']
    lsilence = bodyjson['silence']

    #email = bodyjson['email']

    ## Default parameters
    #file_bucket_name = "videos"
    #file_name = "test.mp4"
    #emoji = True
    #lsilence = True

    #Download file from S3
    local_file_path = "temp/"+file_name
    download_file(file_name, local_file_path,file_bucket_name)

    print("File downloaded: "+local_file_path)

    #Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4","_out.mp4")

    process_video(path_in,path_out,emoji,lsilence)

    print("File processed: "+path_out)

    #Upload file to S3
    file_key = path_out
    upload_file(file_key.replace("temp/",""), file_key.replace("temp/",""),file_bucket_name)

    print("File uploaded: "+file_key)

    remove_file(file_bucket_name,file_name)

    print("File removed: "+file_name)

    #add minia with very low resolution
    # CREATE THE MINIA WITH VERY LOW RESOLUTION
    upload_file("minia",file_name.replace(".mp4",".png"))

    try:
        os.remove(file_name)
    except OSError:
        pass

    clean_temp()

    #Advice server that file is ready
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    print(" Done")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()