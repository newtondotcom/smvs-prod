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

videos_bucket_name = "videos"
thumbnails_bucket_name = "thumbnails"

print(' Waiting for messages...')

def main():
    ## Default parameters
    emoji = False
    lsilence = False

    #Download file from S3
    local_file_path = "../fakerabbitmq/python/temp/palma.mp4"

    print("File downloaded: "+local_file_path)

    #Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4","_out.mp4")

    process_video(path_in,path_out,emoji,lsilence,video_aligned=False)

    print("File processed: "+path_out)

    thumbnail_path = local_file_path.replace(".mp4", ".jpg")
    generate_thumbnail(path_in,thumbnail_path)

    try:
        #os.remove(file_name)
        None
    except OSError:
        pass

    #clean_temp()
    
    print(" Done")

main()