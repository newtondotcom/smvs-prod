import random
import os
from typing import TextIO
from styles import *
from utils import *
from silent import *
from emojis import *
from gen import *

overlap_offset = 0.01

font_size_pt = 18
# http://www.looksoftware.com/help/v11/Content/Reference/Language_Reference/Constants/Color_constants.htm
# rouge, jaune, vert

# Constants for subtitle colors
colors = ["\\2c&&H000000FF&", "\\2c&H0000FFFF&", "\\2c&H0000FF00&"]
colors2 = ["\\1c&H0000FF&", "\\1c&H00FFFF&", "\\1c&H00FF00&"]

# Global variables (consider avoiding global variables if possible)
tab = []       # Stores extracted words and timings
new_tab = []   # Stores grouped and formatted subtitle segments
words = []     # Placeholder for extracted transcriptions
styles = gen_styles(font_size_pt)  # List of predefined subtitle styles

def populate_tabs(words):
    """Extracts words and timings from transcriptions and populates 'tab'."""
    for s in words:
        for i in range(len(s['words'])):
            word = s['words'][i]['word']
            if len(s['words'][i]) == 1:
                break
            start = s['words'][i]['start']
            end = s['words'][i]['end']
            if i == len(s['words']) - 1:
                tab.append([start, end, word, True])  # Last word in a sentence
            else:
                tab.append([start, end, word, False])  # Intermediate word

def analyse_tab_durations():
    """Calculates average time and length of words in 'tab' for grouping."""
    moyenne_time = 0
    moyenne_length = 0
    for j in tab:
        start = j[0]
        end = j[1]
        word = j[2]
        moyenne_time += (end - start)
        moyenne_length += len(word)
    moyenne_length = moyenne_length / len(tab)
    moyenne_time = moyenne_time / len(tab)
    
    retenue = 0
    seuil = 0.10  # Proximity threshold for grouping words
    # Contain words within a group based on specified criteria
    for j in range(len(tab)):
        if retenue > 0:
            retenue -= 1
        else:
            retenue = group_words_based_on_threshold(tab, new_tab, seuil, j, moyenne_time, moyenne_length)

def write_ass_file_aligned(file: TextIO, position):
    """Writes formatted subtitles to an ASS file."""

    position_subtitle = "\\an5" if position == "center" else "\\an2"

    file.write("[Script Info]\n")
    file.write("ScriptType: v4.00\n")
    file.write("Collisions: Normal\n")
    file.write("PlayDepth: 0\n")
    file.write("\n")
    file.write("[V4+ Styles]\n")
    file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColor, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding, WrapStyle\n")
    for j in styles:
        file.write(j)
    file.write("\n")
    file.write("[Events]\n")
    file.write("Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n")
    
    i_color = 0
    for s in new_tab:
        localtext = ""
        globalstart = s[0][0]
        globalend = s[-1][1]
        color = colors[i_color]
        i_color = (i_color + 1) % len(colors)
        
        boiler = "{\\k40\\fad(0,0)\\be1\\b\\bord2\\shad1\\1c&HFFFFFF&\\3c&H000000&\\q1\\b700" + position_subtitle + color + "} "
        localtext = boiler
        
        if len(s) == 4:
            boiler = "{\\fad(0,0)\\be1\\b\\bord2\\shad1\\1c&HFFFFFF&\\3c&H000000&\\q1\\b700" + position_subtitle + color + "} "
            localtext = boiler
            
            first_start = s[0][0]
            first_end = s[1][1]
            second_start = s[2][0]
            second_end = s[3][1]

            # Ensure no overlap
            if second_start < first_end:
                second_start = first_end + overlap_offset
            if s[2][0] < s[1][1]:
                s[2] = (s[1][1] + overlap_offset, s[2][1], s[2][2])
            if s[3][0] < s[2][1]:
                s[3] = (s[2][1] + overlap_offset, s[3][1], s[3][2])
            
            diff = abs(round(float(first_end - first_start) * 100))
            duration = "{" + colors[i_color] + "\\k" + str(diff) + "}"
            localtext += duration + s[0][2].upper() + " " + s[1][2].upper() + "\\N "
            
            i_color = (i_color + 1) % len(colors)
            color = colors[i_color]
            diff2 = abs(round(float(second_end - second_start) * 100))
            diff3 = abs(round(float(second_start - first_start) * 100))
            diff4 = abs(round(float(second_end - first_start) * 100))
            duration2 = "{" + colors[i_color] + "\\k" + str(diff2) + "\\t(" + str(diff3) + "," + str(diff4) + ",\\fscx110)" + "\\t(" + str(diff3) + "," + str(diff4) + ",\\fscy110)}"
            localtext += duration2 + s[2][2].upper() + " " + s[3][2].upper()
        else:
            previous_end = None
            for segment in s:
                start = segment[0]
                end = segment[1]
                word = segment[2]
                if previous_end and start < previous_end:
                    start = previous_end + overlap_offset
                delta = end - start
                duration = "{\\k" + str(abs(round(delta * 100))) + "}"
                localtext += duration + word.upper() + " "
                previous_end = end
        
        style = "s" + str(random.randint(0, len(styles) - 1))
            
        words = localtext.split("{\\q1")
        if len(words) == 5:
            localtext = "{\\q1" + words[1] + "{\\q1" + words[2] + "\\N{\\q1" + words[3] + "{\\q1" + words[4]

        file.write(f"Dialogue: 0,{format_seconds_to_hhmmss(globalstart)},{format_seconds_to_hhmmss(globalend)},{style},,50,50,20,fx,{localtext}\n")

def write_ass_file_non_aligned(contents,file: TextIO):
    """Writes formatted subtitles to an ASS file."""
    file.write("[Script Info]\n")
    file.write("ScriptType: v4.00\n")
    file.write("Collisions: Normal\n")
    file.write("PlayDepth: 0\n")
    file.write("\n")
    file.write("[V4+ Styles]\n")
    file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColor, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding, WrapStyle\n")
    # file.write 
    file.write("\n")
    file.write("[Events]\n")
    file.write("Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n")
    
    i_color = 0
    for s in contents:            
        #f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
        #f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
        #f"{segment['text'].strip().replace('-->', '->')}\n",

        file.write(f"Dialogue: 0,{format_seconds_to_hhmmss(s['start'])},{format_seconds_to_hhmmss(s['end'])},,,50,50,20,fx,{s['text'].strip().replace('-->', '->')}\n")

def process_video(path_in, path_out, emoji, lsilence, isVideoAligned, position):
    """Processes a video based on specified parameters."""
    global tab, new_tab, words
    tab = []       # Reset tab for each video processing task
    new_tab = []   # Reset new_tab for each video processing task
    words = []     # Reset words for each video processing task

    ass_path = os.path.join("temp", f"{extract_filename_without_extension(path_in)}.ass")  # Define ASS file path
    
    audio_path = extract_audio_from_videos([path_in])[path_in]  # Get audio file path from video

    words, langage , time_transcription, time_alignment = get_transcribe(audio_path)  # Transcribe audio to extract words

    time_encoding = 0
    if isVideoAligned:
        time_encoding = video_aligned(words, ass_path, emoji, path_in, path_out, lsilence,position,langage)  # Process aligned video
    else:
        time_encoding = video_non_aligned(words, ass_path, emoji, path_in, path_out)  # Process non-aligned video

    return time_encoding,time_transcription,time_alignment

def video_non_aligned(words, ass_path, emoji, path_in, path_out):
    """Processes a non-aligned video with generated subtitles."""

    # Write the ass file with content from faster-whipser transcription
    with open(ass_path, "w", encoding="utf-8") as srt:
        write_ass_file_non_aligned(words, file=srt)  # Write transcript to SRT file

    # Get the dimensions (width and height) of the input video
    width, height = get_video_dimensions(video_path=path_in)
    
    set_font_size(width,height)

    # simply overlay the ASS script on the video
    time_encoding = overlay_images_on_video(
        in_path=path_in,
        out_path=path_out,
        emojis_list=None,
        width=width,
        height=height,
        font_size_pt = font_size_pt,
        ass=ass_path
    )
    return time_encoding

def compute_emojis():
    array_for_emojis_processing = []
    for i in new_tab:
        words = [i[j][2] for j in range(len(i))]
        array_for_emojis_processing.append([i[0][0],i[-1][1],words])
    return array_for_emojis_processing


def video_aligned(words, ass_path, emoji, path_in, path_out, lsilence, position,langage):
    # Get the dimensions (width and height) of the input video
    width, height = get_video_dimensions(video_path=path_in)

    populate_tabs(words=words)

    # Analyze and process the durations and grouping of words
    analyse_tab_durations() 
        
    # Write the ASS script to a file at the specified path
    with open(ass_path, "w", encoding="utf-8") as ass:
        write_ass_file_aligned(file=ass,position=position)

    time_encoding = 0

    # Overlay emojis on the input video if emoji flag is True
    if emoji:
        array_for_emojis_processing = compute_emojis()
        emojis_list = fetch_similar_emojis(array_for_emojis_processing, langage)
        time_encoding = overlay_images_on_video(
            in_path=path_in,
            out_path=path_out,
            emojis_list=emojis_list,
            width=width,
            height=height,
            position=position,
            font_size_pt = font_size_pt,
            ass=ass_path
        )
    else:
        # If no emojis are provided, simply overlay the ASS script on the video
        time_encoding = overlay_images_on_video(
            in_path=path_in,
            out_path=path_out,
            emojis_list=None,
            width=width,
            height=height,
            position=position,
            font_size_pt = font_size_pt,
            ass=ass_path
        )

    # Remove silent parts from the output video if lsilence flag is True
    if lsilence:
        rm_silent_parts(path_out, path_out)
        
    return time_encoding

def set_font_size(width,height):
    global font_size_pt
    if (width < 380 or height < 720):
        font_size_pt = 14
    else :
        font_size_pt = 18
    print('Font size has been set to ',font_size_pt)