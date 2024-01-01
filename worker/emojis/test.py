import subprocess
import cv2

emoji_size = 72

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
    
def overlay_images_on_video(video_path, image_list):
    width,height = get_dimensions(video_path)
    swidth = (width-emoji_size)/2
    sheight = (height-emoji_size)/2
    filter_complex = ""
    for idx, (image_name, start_time, end_time) in enumerate(image_list):
        previous_video = f"[{idx}v]" if idx > 0 else "[0:v]"
        filter_complex += f"{previous_video}[{idx + 1}:v]overlay={swidth}:{sheight}:enable='between(t,{start_time},{end_time})'"
        if idx < len(image_list) - 1:
            filter_complex += f"[{idx + 1}v];"
        else:
            filter_complex += ";"

    # Build the complete ffmpeg command
    cmd = (
        f"ffmpeg -i {video_path} {' '.join(['-i ' + image for image, _, _ in image_list])} "
        f"-filter_complex \"{filter_complex}\" -c:a copy output_video.mp4 -y"
    )
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    image_list = [("images/1.png", 1.523, 5.518), ("images/2.png", 10.5, 15.5), ("images/3.png", 20.5, 25.5)]
    video_path = "../input/mbf.mp4" 
    overlay_images_on_video(video_path, image_list)
