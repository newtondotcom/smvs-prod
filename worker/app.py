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

apikey = os.environ.get("API_KEY")

RABBIT_HOST = os.environ.get("RABBIT_HOST")
RABBIT_PORT = os.environ.get("RABBIT_PORT")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST,port=RABBIT_PORT))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")
    exit()
    
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

thumbnails_bucket = "thumbnails"
s3_minia = S3(thumbnails_bucket)

print(' Waiting for messages...')

def callback(ch, method, properties, body):
    global s3_minia
    bodyjson = json.loads(body)

    ## Parameters
    file_name = bodyjson['file_name']
    emoji = bodyjson['emoji']
    lsilence = bodyjson['lsilence']
    video_aligned = bodyjson['video_aligned']
    key_db = bodyjson['key_db']
    position = bodyjson['position']

    S3_name = bodyjson['s3_name']
    s3_videos = S3(S3_name)

    print("Trying to download file: "+file_name)

    #Download file from S3
    local_file_path = "temp/"+file_name
    s3_videos.download_file(file_name, local_file_path)

    print("File downloaded: "+local_file_path)

    #Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4","_out.mp4")

    time_encoding,time_transcription,time_alignment = process_video(path_in,path_out,emoji,lsilence,video_aligned,position)

    print("File processed: "+path_out)

    #Upload video to videos S3
    file_key = path_out
    s3_videos.upload_file(file_key)

    print("File uploaded: "+file_key)

    s3_videos.remove_file(file_name)

    print("File removed: "+file_name)

    #add minia with very low resolution    
    thumbnail_path = path_in.replace(".mp4", ".jpg")
    generate_thumbnail(path_in,thumbnail_path)
    s3_minia.upload_file(thumbnail_path)

    print("Thumbnail uploaded: " + thumbnail_path.replace("temp/",""))


    # construction of the body for the frontend
    body = {
        "task_id": key_db,
        "time_transcription": time_transcription,
        "time_encoding": time_encoding,
        "time_alignment": time_alignment,
        "done_at": datetime.datetime.now().isoformat(),
        "thumbnail": file_name.replace(".mp4", ".jpg")
    }
    headers = {'Authorization': 'Bearer '+apikey}
    requests.post("http://localhost:3000/api/dashboard/tasks",headers=headers, json=body)

    try:
        clean_temporary_directory()
    except OSError:
        pass


    #Advice server that file is ready
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    print(" Done")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()