import os
import subprocess
import psutil
import time

def audio_playback(page_select,grid_select):
    fname = "/home/pi/touchtalk/Sounds"
    if  (page_select == 1):
        fname = fname + "/P1"
    elif(page_select == 2):
        fname = fname + "/P2"
    elif(page_select == 3):
        fname = fname + "/P3"
    elif(page_select == 4):
        fname = fname + "/P4"
        
    if  (grid_select == 1):
        fname = fname + "B1"
    elif (grid_select == 2):
        fname = fname + "B2"
    elif (grid_select == 3):
        fname = fname + "B3"
    elif (grid_select == 4):
        fname = fname + "B4"
        
    fname = fname + ".wav"
        
    popen_string = "aplay -f S16_LE -t wav -c 2 -d 10 -Dplug:default " + fname
    process = subprocess.Popen(popen_string, shell=True)