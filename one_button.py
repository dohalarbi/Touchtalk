# Touchtalk
#!/usr/bin/python


from PIL import *
from Tkinter import *	#library for gui
from time import sleep
import os, sys
import pyaudio
import wave
#import RPi.GPIO as GPIO

master = Tk()
master.minsize(600,600)
master.geometry("320x100")


# GP1 = 1
# GP2 = 2
# GP3 = 3
# GP4 = 4

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(GP1, GPIO.IN)
# GPIO.setup(GP2, GPIO.IN)
# GPIO.setup(GP3, GPIO.IN)
# GPIO.setup(GP4, GPIO.IN)


#if (GPIO.input(GP1) == True):
#    print("Do somthing")


#stoping audio
def stop():
	print("stoping audio")
	os.system('pkill mpg321')


#playing audio
def play():
	print("playing audio")
	os.system('mpg321 piano2.wav &')
	sleep(1);


#quit the script
def Exit():
	sys.exit()


#record audio wav file the 5 seconds
def record():
        print("recording !!!")
        os.system("python record_audio1_1.py")

	


#Test buttons
#img = PhotoImage(file="Kingdom.png")
#img1 = img.subsample(4, 4)	#create a new image 1/4 as large as the original
#b = Button(master, image=img1, text="Play audio", command=play)
        
b = Button(master, text="Play audio", command=play)
b.pack(side=LEFT)

c = Button(master, text="Stop audio", command=stop)
c.pack(side=RIGHT)


c = Button(master, text="Closing the program!!", command=Exit)
c.pack(side=TOP)


d = Button(master, text="Record audio", command=record)
d.pack(side=TOP)

mainloop()




# You can resize a PhotoImage using the zoom and subsample methods. Both methods return a new PhotoImage object.

# from tkinter import *
# root = Tk()     #you must create an instance of Tk() first

# image = PhotoImage(file='path/to/image.gif')
# larger_image = image.zoom(2, 2)         #create a new image twice as large as the original
# smaller_image = image.subsample(2, 2)   #create a new image half as large as the original
