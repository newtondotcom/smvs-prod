import subprocess
import time
from utils import *

emojis_dir = "emojis/images/"

def overlay_images_on_video(in_path, out_path, width, height, ass, emojis_list=None):
    """
    Overlays images on a video using ffmpeg.

    Args:
        in_path (str): Path to the input video.
        out_path (str): Path to save the output video.
        width (int): Width of the video.
        height (int): Height of the video.
        ass (str): Path to the ASS subtitle file.
        emojis_list (list, optional): List of tuples (IMAGE_WORKER_NAME, start_time, end_time)
            specifying images to overlay and their display times.

    Returns:
        None
    """
    emoji_size = height / 10
    y_offset = width / 100
    swidth = (width - emoji_size) / 2
    sheight = (height - emoji_size) / 2 - y_offset

    filter_complex = ""

    if emojis_list is not None:
        # Prepare emoji input list for ffmpeg
        emojis_list = [(emojis_dir + image + ".png", start_time, end_time) for image, start_time, end_time in emojis_list]

        for idx, (IMAGE_WORKER_NAME, start_time, end_time) in enumerate(emojis_list):
            previous_video = f"[{idx}v]" if idx > 0 else "[0:v]"
            # Build overlay filter for each emoji image
            filter_complex += f"{previous_video}[{idx + 1}:v]overlay={swidth}:{sheight}:enable='between(t,{start_time},{end_time})'"
            if idx < len(emojis_list) - 1:
                filter_complex += f"[{idx + 1}v];"
            else:
                filter_complex += f"[last];[last]ass='{ass}'[out]"

        # Construct the complete ffmpeg command
        cmd = (
            f"ffmpeg -i {in_path} {' '.join(['-i ' + image for image, _, _ in emojis_list])} "
            f"-filter_complex \"{filter_complex}\" -map [out] -map 0:a -c:a copy {out_path} -y"
        )
    else:
        # If no emojis, use ASS subtitles directly with video overlay
        cmd = f"ffmpeg -i {in_path} -vf 'ass={ass}' -c:a copy -y {out_path}"

    # Execute the ffmpeg command
    tic = time.perf_counter()
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    toc = time.perf_counter()

    # Measure and print execution time
    print(f"ffmpeg processing for video took: {toc - tic} seconds")

# Example usage:
# overlay_images_on_video('input.mp4', 'output.mp4', 1280, 720, 'subtitles.ass', emojis_list=[('emoji1', 5.0, 10.0), ('emoji2', 15.0, 20.0)])
# overlay_images_on_video('input.mp4', 'output.mp4', 1280, 720, 'subtitles.ass')
