import pika
from s3 import *
from utils import *
from gen import *
from silent import *
from s3 import *
from emojis import *
from processing import *
import json
from dotenv import load_dotenv
load_dotenv()

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

videos_bucket_name = "videos"
thumbnails_bucket_name = "thumbnails"
s3_videos = S3(videos_bucket_name)
s3_minia = S3(thumbnails_bucket_name)

print(' Waiting for messages...')

def callback(ch, method, properties, body):
    bodyjson = json.loads(body)

    ## Parameters
    #file_bucket_name = bodyjson['file_bucket_name']
    file_name = bodyjson['file_name']
    emoji = bodyjson['emoji']
    lsilence = bodyjson['silence']
    video_aligned = bodyjson['video_aligned']
    key_db = bodyjson['key_db']

    ## Default parameters
    #file_bucket_name = "videos"
    #file_name = "test.mp4"
    #emoji = True
    #lsilence = True

    #Download file from S3
    local_file_path = "temp/"+file_name
    s3_videos.download_file(file_name, local_file_path)

    print("File downloaded: "+local_file_path)

    #Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4","_out.mp4")

    time_encoding,time_transcription,time_alignment = process_video(path_in,path_out,emoji,lsilence,video_aligned)

    print("File processed: "+path_out)

    #Upload video to S3
    file_key = path_out
    blc = s3.upload_file(file_key.replace("temp/",""), file_key.replace("temp/",""))

    print("File uploaded: "+file_key)

    s3.remove_file(file_name)

    print("File removed: "+file_name)

    #add minia with very low resolution    
    thumbnail_path = local_file_path.replace(".mp4", "_thumbnail.jpg")
    generate_thumbnail(path_in,thumbnail_path)
    thumbnail_url = s3_minia.upload_file("minia",thumbnail_path)


    # construction of the body for the frontend
    body = {
        "task_id": key_db,
        "time_transcription": time_transcription,
        "time_encoding": time_encoding,
        "time_alignment": time_alignment,
        "done_at": datetime.datetime.now().isoformat(),
        "thumbnail": thumbnail_url
    }
    #request.post("http://localhost:5000/api/v1/tasks", json=body)

    try:
        os.remove(file_name)
    except OSError:
        pass

    clean_temporary_directory()

    #Advice server that file is ready
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    print(" Done")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()