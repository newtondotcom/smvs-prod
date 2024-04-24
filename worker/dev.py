import pika
from s3 import *
from utils import *
from gen import *
from silent import *
from s3 import *
from emojis import *
from processing import *
import json

videos_bucket_name = "videos"
thumbnails_bucket_name = "thumbnails"

def main():
    ## Default parameters
    emoji = True
    lsilence = False

    #Download file from S3
    local_file_path = "../inputs/palma.mp4"

    #Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4","_out.mp4")

    video_aligned = False

    time_encoding,time_transcription,time_alignment = process_video(path_in,path_out,emoji,lsilence,video_aligned)

    print("File processed: "+path_out)

    thumbnail_path = local_file_path.replace(".mp4", ".jpg")
    generate_thumbnail(path_in,thumbnail_path)

    
    body = {
        "task_id": key_db,
        "time_transcription": time_transcription,
        "time_encoding": time_encoding,
        "time_alignment": time_alignment,
        "done_at": datetime.datetime.now().isoformat(),
        "thumbnail": thumbnail_url
    }
    print(body)

    try:
        #os.remove(file_name)
        None
    except OSError:
        pass

    #clean_temporary_directory()
    
    print(" Done")

main()