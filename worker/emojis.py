import subprocess
from utils import *

path_emojis = "emojis/images/"

#define this two values depending on video heigh and width 
emoji_size = 72
y_offset = 10

def overlay_images_on_video(in_path, out_path, width, height,ass,emojis_list=None):
    swidth = (width-emoji_size)/2
    sheight = (height-emoji_size)/2 - y_offset
    filter_complex = ""
    if emojis_list!=None :
        emojis_list = [(path_emojis + image + ".png", start_time, end_time) for image, start_time, end_time in emojis_list]
        for idx, (image_name, start_time, end_time) in enumerate(emojis_list):
            previous_video = f"[{idx}v]" if idx > 0 else "[0:v]"
            filter_complex += f"{previous_video}[{idx + 1}:v]overlay={swidth}:{sheight}:enable='between(t,{start_time},{end_time})'"
            if idx < len(emojis_list) - 1:
                filter_complex += f"[{idx + 1}v];"
            else:
                filter_complex += f"[last];[last]ass='{ass}'[out]"

        # Build the complete ffmpeg command
        cmd = (
            f"ffmpeg -i {in_path} {' '.join(['-i ' + image for image, _, _ in emojis_list])} "
            f"-filter_complex \"{filter_complex}\" -map [out] -map 0:a -c:a copy {out_path} -y"
        )

    else:
        cmd = f"ffmpeg -i {in_path} -vf 'ass={ass}' -c:a copy -y {out_path}"
    subprocess.run(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)



