import random
import os
import re
from typing import Iterator, TextIO
import subprocess
from styles import *
from utils import *
from silent import *
from emojis import *
from gen import *

# http://www.looksoftware.com/help/v11/Content/Reference/Language_Reference/Constants/Color_constants.htm
# rouge, jaune, vert
colors = ["\\2c&&H000000FF&","\\2c&H0000FFFF&","\\2c&H0000FF00&"]
colors2 = ["\\1c&H0000FF&","\\1c&H00FFFF&","\\1c&H00FF00&"]
tab = []
new_tab = []
styles = gen_styles()
words = []


def write_ass(words):
    for s in words:
        for i in range(len(s['words'])):
            word = s['words'][i]['word']
            if len(s['words'][i])==1:
                break
            start = s['words'][i]['start']
            end = s['words'][i]['end']
            if i == len(s['words']) - 1 :
                tab.append([start,end,word,True])
            else :
                tab.append([start,end,word,False])

def analyse_tab_durations():
    moyenne_time = 0
    moyenne_lenght = 0
    for j in tab:
        start = j[0]
        end = j[1]
        word= j[2]
        moyenne_time += (end-start)
        moyenne_lenght += len(word)
    moyenne_lenght = moyenne_lenght/len(tab)
    moyenne_time = moyenne_time/len(tab)
    
    retenue = 0
    seuil = 0.05
    for j in range(len(tab)):
        if retenue > 0:
            retenue -= 1
        else :
            retenue = juxtaposer_mots(tab, new_tab, seuil, j, moyenne_time, moyenne_lenght)

def write_ass_file(file : TextIO):
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
        localtext =  ""
        globalstart = s[0][0]
        globalend = s[-1][1]
        color = colors[i_color]
        i_color = (i_color+1)%len(colors)
        
        boiler = "{\\k40\\fad(0,0)\\be1\\b\\bord2\\shad1\\1c&&HFFFFFF&\\3c&H000000&\\q1\\an5\\b700"+color+"} "
        localtext = boiler
        if len(s)==4:
            boiler = "{\\fad(0,0)\\be1\\b\\bord2\\shad1\\1c&&HFFFFFF&\\3c&H000000&\\q1\\an5\\b700"+color+"} "
            localtext = boiler
            first_start = s[0][0]
            first_end = s[1][1]
            second_start = s[2][0]
            second_end = s[3][1]
            diff = abs(round(float(first_end-first_start)*100))
            #duration = "{\\1c&HFFFFFF&\\t("+str(0)+","+str(diff)+","+colors2[i_color]+")}"
            duration = "{"+colors[i_color]+"\\k"+str(diff)+"}"
            localtext += duration+s[0][2].upper()+" "+s[1][2].upper()+"\\N "
            i_color = (i_color+1)%len(colors)
            color=colors[i_color]
            diff2 = abs(round(float(second_end-second_start)*100))
            diff3 = abs(round(float(second_start-first_start)*100))
            diff4 = abs(round(float(second_end-first_start)*100))
            duration2 = "{"+colors[i_color]+"\\k"+str(diff2)+"\\t("+str(diff3)+","+str(diff4)+",\\fscx110)"+"\\t("+str(diff3)+","+str(diff4)+",\\fscy110)}"
            localtext += duration2+s[2][2].upper()+" "+s[3][2].upper()
        else :
            for segment in s:
                word = segment[2]
                start = segment[0]
                end = segment[1]
                delta = end - start
                duration = "{\\k"+str(abs(round(delta*100)))+"}"
                #boiler = " {\\be0\\b1\\move(100, 100, 200, 200,["+str(start)+","+str(int(delta))+"])\\blur2}"
                #localtext += boiler+word.upper().replace(" "," "+boiler)
                localtext += duration+word.upper()+" "
        
        style = "s"+str(random.randint(0,len(styles)-1))
            
        words = localtext.split("{\q1")
        if len(words)==5:  ## add a line break if there are more than 4 words
            localtext = "{\q1"+words[1]+"{\q1"+words[2]+"\\N{\q1"+words[3]+"{\q1"+words[4]

        file.write(f"""Dialogue: 0,{time_to_hhmmss(globalstart)},{time_to_hhmmss(globalend)},{style},,50,50,20,fx,{localtext}"""+  "\n")

def process_video(path_in,path_out,emoji,lsilence):
    width = 0
    heigh = 0  
    ass_path = "temp/"
    width,heigh = get_dimensions(path=path_in)
    ass_path = os.path.join(ass_path, f"{filename(path_in)}.ass")  

    audio_path = get_audio([path_in])[path_in]

    words = get_transcribe(audio_path)

    write_ass(words=words)

    analyse_tab_durations() 
        
    with open(ass_path,"w", encoding="utf-8") as ass:
        write_ass_file(file=ass)

    emojis_list = [("1", 1.523, 5.518), ("2", 10.5, 15.5), ("3", 20.5, 25.5)]

    if emoji:
        overlay_images_on_video(in_path=path_in,out_path=path_out,emojis_list=emojis_list,width=width,height=heigh,ass=ass_path)
    else:
        overlay_images_on_video(in_path=path_in,out_path=path_out,emojis_list=None,width=width,height=heigh,ass=ass_path)

    if lsilence:
        rm_silent_parts(path_out,path_out)
        
    return path_out
        