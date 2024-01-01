import os
import ffmpeg
from typing import TextIO
import random
import subprocess
import cv2
from styles import *

def filename(path):
    return os.path.splitext(os.path.basename(path))[0]

def time_to_hhmmss(date):
    data = str(date)
    second = int(date)
    ms = int((date - second) * 100)
    minutes = int(second) // 60
    second = int(second) % 60
    return f"00:{minutes}:{second}.{ms}" 

def get_audio(paths):
    audio_paths = {}

    if not os.path.exists("temp/"):
        os.makedirs("temp/")
        
    for path in paths:
        print(f"Extracting audio from {filename(path)}...")
        output_path = os.path.join("temp/", f"{filename(path)}.wav")
        ffmpeg.input(path).output(
            output_path,
            acodec="pcm_s16le", ac=1, ar="16k"
        ).run(quiet=True, overwrite_output=True)

        audio_paths[path] = output_path

    return audio_paths


styles = gen_styles()
    
def clean_temp():
    temp_dir_path = "temp/"
    try:
        # Check if the provided directory path exists
        if not os.path.exists(temp_dir_path):
            print(f"The directory '{temp_dir_path}' does not exist.")
            return

        # Delete all files and directories inside the temp directory
        for item in os.listdir(temp_dir_path):
            item_path = os.path.join(temp_dir_path, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        print(f"Cleaned the contents of '{temp_dir_path}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_dimensions(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
    else:
        width = int(cap.get(3))  # 3 corresponds to CV_CAP_PROP_FRAME_WIDTH
        height = int(cap.get(4))  # 4 corresponds to CV_CAP_PROP_FRAME_HEIGHT

        print(f"Video Dimensions (Width x Height): {width} x {height}")

        # Release the video capture object
        cap.release()
        return width,height
    

def juxtaposer_mots(tab, new_tab, seuil, j, moyenne_time, moyenne_length):
    def is_below_threshold(word, next_word=None):
        if next_word is None:
            if word[2].endswith("."):
                return True
            return word[1] - word[0] < moyenne_time or len(word[2]) < moyenne_length
        else:
            return next_word[0] - word[1] < seuil

    group = [tab[j]]
    if not is_below_threshold(tab[j]) or j == len(tab) - 1:
        new_tab.append(group)
        return 0

    mots_a_juxtaposer = min(4, len(tab) - j)
    retenue = 0

    for i in range(1, mots_a_juxtaposer):
        current_word = tab[j + i]
        previous_word = tab[j + i - 1]

        if is_below_threshold(current_word) and is_below_threshold(previous_word, current_word):
            group.append(current_word)
            retenue += 1
        else:
            break

    new_tab.append(group)
    return retenue
    