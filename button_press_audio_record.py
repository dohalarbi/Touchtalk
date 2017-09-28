import RPi.GPIO as gpio
import os
import subprocess
import psutil
import time


gpio.setmode(gpio.BCM)

gpio.setup(4, gpio.IN, pull_up_down=gpio.PUD_DOWN) #theoretical page switch
gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_DOWN) #mode switch 

procname = 'arecord'

recording = 0 #default state
killed = 0

try:
    while True:
        if (gpio.input(17) == 1):
            if (gpio.input(4)==1 and recording == 0): #press grid switch to start recording
                recording = 1
                process = subprocess.Popen("arecord -f S16_LE -t wav -c 2 -d 10 -Dplug:default recording.wav", shell=True)
                print("recording")
                
            elif (gpio.input(4)==0 and recording == 1): #grid switch has been released and recording is done
                print("recording stopped")
                os.system('pkill arecord')
                print('Playback in 5 seconds')
                time.sleep(5)
                process = subprocess.Popen("aplay -f S16_LE -t wav -c 2 -d 10 -Dplug:default recording.wav", shell=True)
                killed = 1
                
            elif (recording == 1 and killed == 1):
                print("break")
                recording = 0
                killed = 0
                break

except KeyboardInterrupt:
	gpio.cleanup()
