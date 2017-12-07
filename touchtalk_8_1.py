#!/usr/bin/python3
#client Mode setup

import Adafruit_GPIO as GPIO
import time
from datetime import datetime
import signal

from mode_operation_6 import *
from display_fcns_4 import *
from setup_images import *

import threading

################


sleep_time = 1000
global end_time
global sleep_mode #0 is not sleeping 1 is sleeping
sleep_mode = 0
############################

#import _thread


#Page buttons
Bp1 = 14
Bp2 = 15
Bp3 = 18
Bp4 = 23

#Grid buttons
Bg1 = 24
Bg2 = 25 
Bg3 = 1
Bg4 = 12 

SHTDWN_BTN = 6
ENABLE_PIN= 16 #power ON
SLEEP_PIN = 19 #shut the screens and audio

#Mode select
global client_latch
client_latch = 21
global staff_latch
staff_latch = 20
global audio_latch
audio_latch = 13
global image_latch
image_latch = 26

#global variables
global page_select
page_select = 1

global current_mode
global page_num

global staff_mode
staff_mode = 0 #default is audio mode

global image_select
image_select=0

debounce_time= 10 #milliseconds
global counter
counter =0

global path0
path0 = "/home/pi/touchtalk/images/"
#/home/pi/touchtalk/Images
################################################################################

def sleep_main():
	global sleep_mode
	global end_time
	gpio.output(SLEEP_PIN, 1)
	print(time.time())
	print(end_time)
	
	while(True):
		sleep_mode = sleep_mode_read()
		
		if (time.time() > end_time):
			if (sleep_mode == 0):
				sleep_mode = 1
				sleep_mode_write(1)
			if (sleep_mode == 1):
                            end_time = int(time.time()) + sleep_time
                            print('Turn off the screens and the audio power')
                            while(sleep_mode ==1):
                                gpio.output(SLEEP_PIN, 0)
                                sleep_mode = sleep_mode_read()
                                time.sleep(1)
		else:
			sleep_mode_write(0)
			gpio.output(SLEEP_PIN, 1)
			time.sleep(0.25)
            
def doShutdown():
    print("Waiting for >3sec button press")
    time.sleep(1)
    if (gpio.input(SHTDWN_BTN)==False):
        print ("Would shutdown the RPi Now")
        time.sleep(3)
        if(gpio.input(SHTDWN_BTN)==False):
            gpio.output(ENABLE_PIN,0)
            os.system("sudo shutdown -h now")
    else:
        print("Ignore the shutdown (<3sec)")

def determine_mode(start):
    #Mode select
    global current_mode
    #global end_time
    #end_time = int(time.time()) + sleep_time
    #time.sleep(0.1)
    if not gpio.input(client_latch) and gpio.input(staff_latch):
        current_mode = 0 #client mode
        print("Switching to Client Mode")
        page_input(page_select,start)
        image_select_write(0)
        grid_select_write(0) #reset for next image mode
        
    elif not gpio.input(staff_latch) and gpio.input(client_latch): #turn the switch to staff mode and image/audio mode
        current_mode = 1 #Staff mode
        print("Switching to Staff Mode")
        page_input(page_select,start)
        if (gpio.input(audio_latch) == 0):
        	staff_mode_audio()
        	image_select_write(0)
        	grid_select_write(0) #reset for next image mode
        elif (gpio.input(image_latch) == 0):
        	staff_mode_image()
    
        
###################################################################################################

def page_input(page_num,start):
	global counter
	global end_time
	#end_time = int(time.time()) + sleep_time
	#sleep_mode_write(0)
	#time.sleep(0.1)
	image_select = image_select_read()
	if (image_select==0):
		global page_select
		if (not gpio.input(Bp1) or start):
			print('button _page_1_ pressed')
			page_select = 1
			set_page(1)
        
		elif (not gpio.input(Bp2)):
			print('button _page_2_ pressed')
			page_select = 2
			set_page(2)

		elif (not gpio.input(Bp3)):
			print('button _page_3_ pressed')
			page_select = 3
			set_page(3)
        
		elif (not gpio.input(Bp4)):
			print('button _page_4_ pressed')
			page_select = 4
			set_page(4)
	else:
		grid_select=grid_select_read()
		
		min_image =0
		max_image = max_image_number()
		print('max nuber of images:', max_image)
		image_array = myimages_name()
		if (not gpio.input(Bp1) or start):
                    print('button _page_1_ pressed')
                    if(counter < max_image):
                        counter += 1
                        print(counter)
                        print('increment counter') 
                    elif(counter == max_image):
                        counter = min_image
                        print(counter)
			# send the counter the display the image
                    display_image_staff(grid_select,path0+image_array[counter%max_image])
        
		elif (not gpio.input(Bp2)):
                    print('button _page_2_ pressed')
                    if(counter > min_image):
                        counter -= 1
                        print(counter)
                        print('decrement counter') 
                    elif(counter == min_image):
                        counter = max_image
                        print(counter)
                    display_image_staff(grid_select,path0+image_array[counter%max_image])	#using the modulus to avoid the error of pointing to an empty location
			

		elif (not gpio.input(Bp3)):	#this is for save the image
			print('button _page_3_ pressed')
			image_save(grid_select,page_select,counter)
			image_select_write(0)
		elif (not gpio.input(Bp4)):	#this is for cancel and go back to the selection menu
			image_select_write(0) # cancel image s
			print('exit') #page_select = 4
	

################################################################################



#Staff mode
def staff_mode_audio():
	time.sleep(0.01)
	image_select_write(0)
	global staff_mode
	#global end_time
	#end_time = int(time.time()) + sleep_time
	if  not gpio.input(audio_latch) and gpio.input(image_latch):
		staff_mode=0;
		print('You are in audio setup')
		print(staff_mode)
	
	
    
def staff_mode_image():
	time.sleep(0.01)
	global staff_mode
	#global end_time
	#end_time = int(time.time()) + sleep_time
	if not gpio.input(image_latch) and gpio.input(audio_latch):
		staff_mode=1;
		print('You are in image setup')
	
    


gpio.cleanup()
gpio = GPIO.get_platform_gpio()
#Page buttons
gpio.setup(Bp1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bp2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bp4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bp3,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(ENABLE_PIN,GPIO.OUT)
gpio.setup(SLEEP_PIN,GPIO.OUT)

#Grid buttons
gpio.setup(Bg1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bg2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bg3,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bg4,GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Mode latches
gpio.setup(client_latch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(staff_latch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(image_latch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(audio_latch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

gpio.setup(SHTDWN_BTN,GPIO.IN,pull_up_down=GPIO.PUD_UP)

gpio.add_event_detect(SHTDWN_BTN,GPIO.FALLING, callback = lambda x:doShutdown(), bouncetime=3000)

gpio.add_event_detect(client_latch, GPIO.FALLING, callback = lambda x: determine_mode(0), bouncetime=300)
gpio.add_event_detect(staff_latch, GPIO.FALLING, callback = lambda x: determine_mode(0), bouncetime=300)
gpio.add_event_detect(image_latch, GPIO.FALLING, callback = lambda x: staff_mode_image(), bouncetime=300)
gpio.add_event_detect(audio_latch, GPIO.FALLING, callback = lambda x: staff_mode_audio(), bouncetime=300)


gpio.add_event_detect(Bp1, GPIO.FALLING, callback = lambda x: page_input(1,0), bouncetime=debounce_time)
gpio.add_event_detect(Bp2, GPIO.FALLING, callback = lambda x: page_input(2,0), bouncetime=debounce_time)
gpio.add_event_detect(Bp3, GPIO.FALLING, callback = lambda x: page_input(3,0), bouncetime=debounce_time)
gpio.add_event_detect(Bp4, GPIO.FALLING, callback = lambda x: page_input(4,0), bouncetime=debounce_time)
    
gpio.add_event_detect(Bg1, GPIO.FALLING, callback = lambda x:grid_input(1,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg2, GPIO.FALLING, callback = lambda x:grid_input(2,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg3, GPIO.FALLING, callback = lambda x:grid_input(3,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg4, GPIO.FALLING, callback = lambda x:grid_input(4,page_select,current_mode,staff_mode), bouncetime=debounce_time)


#Process(target=sleep_main(end_time)).start()
gpio.output(ENABLE_PIN, 1)
gpio.output(SLEEP_PIN, 1)

determine_mode(1) # grab default state

#end_time = int(time.time()) + sleep_time   #number of
#print(time.time())
#print(end_time)

#t=threading.Thread(target=sleep_main())
#t.start()

try:
    while True:
        signal.pause()
        
except KeyboardInterrupt:
    gpio.cleanup()
