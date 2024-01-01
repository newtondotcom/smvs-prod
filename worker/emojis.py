import subprocess
from utils import *

path_emojis = "emojis/images/"
image_list = [("1", 1.523, 5.518), ("2", 10.5, 15.5), ("3", 20.5, 25.5)]

emoji_size = 72

y_offset = 10

def overlay_images_on_video(in_path, out_path, width, height,ass,image_list=None):
    swidth = (width-emoji_size)/2
    sheight = (height-emoji_size)/2 - y_offset
    filter_complex = ""
    if image_list!=None :
        image_list = [(path_emojis + image + ".png", start_time, end_time) for image, start_time, end_time in image_list]
        for idx, (image_name, start_time, end_time) in enumerate(image_list):
            previous_video = f"[{idx}v]" if idx > 0 else "[0:v]"
            filter_complex += f"{previous_video}[{idx + 1}:v]overlay={swidth}:{sheight}:enable='between(t,{start_time},{end_time})'"
            if idx < len(image_list) - 1:
                filter_complex += f"[{idx + 1}v];"
            else:
                filter_complex += f"[last];[last]ass='{ass}'[out]"

        # Build the complete ffmpeg command
        cmd = (
            f"ffmpeg -i {in_path} {' '.join(['-i ' + image for image, _, _ in image_list])} "
            f"-filter_complex \"{filter_complex}\" -map [out] -map 0:a -c:a copy {out_path} -y"
        )

    else:
        cmd = f"ffmpeg -i {in_path} -vf 'ass={ass}' -c:a copy -y {out_path}"
    print(cmd)
    subprocess.run(cmd, shell=True)



