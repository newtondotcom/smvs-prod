#!/usr/bin/env python3
import os
import pika
import json
import requests
import datetime
import time
from dotenv import load_dotenv
from s3 import *
from utils import *
from gen import *
from silent import *
from emojis import *
from processing import *

load_dotenv()
webhook = os.environ.get("DISCORD_WEBHOOK")

task_id= "cm695swsi0007l4qfy3wny4qk"
file_name="1737626173697_bszxf9.mp4"

thumbnails_bucket = "thumbnails2"
s3_minia = S3(thumbnails_bucket)
path_in = f"temp/{file_name}"
thumbnail_path = path_in.replace(".mp4", ".jpg")
generate_thumbnail(path_in, thumbnail_path)
#s3_minia.upload_file(thumbnail_path)
#exit()

# Construction of the body for the frontend
body = {
            "task_id": task_id,
            "time_transcription": 12.399791726000103,
            "time_encoding": 0.9623507700000573,
            "time_alignment": 1.0396214889999555,
            "done_at": datetime.datetime.now().isoformat(),
            "thumbnail": file_name.replace(".mp4", ".jpg"),
}
headers = {"Authorization": "Bearer " + apikey}
requests.post(
            "https://app.yogocap.com/api/dashboard/tasks", headers=headers, json=body
)

try:
    clean_temporary_directory()
except OSError:
        pass

print(" Done")
