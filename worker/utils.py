import os
import ffmpeg
import random
import cv2

def extract_filename_without_extension(file_path):
    """Extracts the filename without extension from a given file path."""
    return os.path.splitext(os.path.basename(file_path))[0]

def format_seconds_to_hhmmss(time_seconds):
    """Converts time in seconds to the 'hh:mm:ss.ms' format."""
    total_seconds = int(time_seconds)
    milliseconds = int((time_seconds - total_seconds) * 100)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"00:{minutes}:{seconds}.{milliseconds}" 

def extract_audio_from_videos(video_paths):
    """
    Extracts audio from video files and saves them as WAV files in a temporary directory.
    Returns a dictionary with original video paths as keys and corresponding audio paths as values.
    """
    audio_paths = {}
    temp_directory = "temp/"

    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)
        
    for video_path in video_paths:
        print(f"Extracting audio from {extract_filename_without_extension(video_path)}...")
        output_audio_path = os.path.join(temp_directory, f"{extract_filename_without_extension(video_path)}.wav")
        
        # Use ffmpeg to extract audio
        ffmpeg.input(video_path).output(
            output_audio_path,
            acodec="pcm_s16le", ac=1, ar="16k"
        ).run(quiet=True, overwrite_output=True)

        audio_paths[video_path] = output_audio_path

    return audio_paths
    
def clean_temporary_directory():
    """Cleans the contents of the temporary directory."""
    temp_directory = "temp/"
    try:
        if not os.path.exists(temp_directory):
            print(f"The directory '{temp_directory}' does not exist.")
            return

        # Remove all files and directories inside the temp directory
        for item in os.listdir(temp_directory):
            item_path = os.path.join(temp_directory, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        print(f"Cleaned the contents of '{temp_directory}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_video_dimensions(video_path):
    """Gets the width and height dimensions of a video file."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return None
    
    width = int(cap.get(3))  # 3 corresponds to CV_CAP_PROP_FRAME_WIDTH
    height = int(cap.get(4))  # 4 corresponds to CV_CAP_PROP_FRAME_HEIGHT

    print(f"Video Dimensions (Width x Height): {width} x {height}")

    # Release the video capture object
    cap.release()
    return width, height
    

def group_words_based_on_threshold(tab, new_tab, proximity_threshold, index, average_time, average_length):
    """
    Groups words based on specified thresholds and criteria.
    """
    def is_word_below_threshold(word, next_word=None):
        """Checks if a word meets the threshold criteria."""
        if next_word is None:
            # Check if the word ends with "." or meets time/length criteria
            if "." in word[2]:
                return True
            return word[1] - word[0] < average_time or len(word[2]) < average_length
        else:
            # Check proximity threshold between current word and next word
            return next_word[0] - word[1] < proximity_threshold and "." not in word[2]

    # Initialize a new group with the current word
    group = [tab[index]]

    # If the current word does not meet the threshold or is the last word in the list, append the group to new_tab
    if not is_word_below_threshold(tab[index]) or index == len(tab) - 1:
        new_tab.append(group)
        return 0

    # Determine the number of words to juxtapose
    words_to_juxtapose = min(4, len(tab) - index)
    retenue = 0

    # Loop through subsequent words to form a group based on the threshold criteria
    for i in range(1, words_to_juxtapose):
        current_word = tab[index + i]
        previous_word = tab[index + i - 1]

        if is_word_below_threshold(current_word) and is_word_below_threshold(previous_word, current_word):
            group.append(current_word)
            retenue += 1
        elif "." in current_word[2]:
            # Include the sentence-ending word in the group
            group.append(current_word)
            retenue += 1
        else:
            break  # Stop adding words to the group if threshold is not met and not a sentence-ending word

    # Append the final group to the new_tab list
    new_tab.append(group)
    return retenue


def generate_thumbnail(path_in, thumbnail_path):
    """Generates a thumbnail from the input video at 1 second."""
    try:
        # Open the input video file and extract thumbnail
        probe = ffmpeg.probe(path_in)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        if not video_stream:
            raise ValueError("Input file is not a valid video file.")

        # Use ffmpeg to extract thumbnail with specified dimensions and parameters
        (
            ffmpeg
            .input(path_in, ss=1)
            .output(
                thumbnail_path,
                vframes=1,
                vf='scale=200:100:force_original_aspect_ratio=decrease,pad=200:100:(ow-iw)/2:(oh-ih)/2,crop=200:100'
            )
            .run(overwrite_output=True, quiet=True)  # Suppress output to console
        )

        print(f"Thumbnail generated successfully: {thumbnail_path}")
    except ffmpeg.Error as e:
        print(f"Error generating thumbnail: {e.stderr}")
    except Exception as e:
        print(f"Error: {e}")