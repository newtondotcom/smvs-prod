import os
from s3 import *
from utils import *
from gen import *
from silent import *
from s3 import *
from emojis import *
from processing import *
import json

def main(local_file_path):
    ## Default parameters
    emoji = False
    lsilence = False

    # Process file
    path_in = local_file_path
    path_out = local_file_path.replace(".mp4", "_out.mp4")

    position = "chips"

    video_aligned = True

    time_encoding, time_transcription, time_alignment = process_video(path_in, path_out, emoji, lsilence, video_aligned, position)

    print("File processed: " + path_out)

    try:
        clean_temporary_directory()
    except OSError:
        pass
    
    print(" Done")

def process_all_videos_in_folder(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".mp4"):
            file_path = os.path.join(folder_path, file)
            output_file_path = file_path.replace(".mp4", "_out.mp4")
            if not os.path.exists(output_file_path):
                print(f"Processing {file_path}...")
                main(file_path)
            else:
                print(f"Skipping {file}, output file already exists.")

# Specify the folder containing the .mp4 videos
folder_path = "/home/robebs/Downloads/baffie/"

# Process all videos in the folder
process_all_videos_in_folder(folder_path)
