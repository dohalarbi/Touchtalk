#client Mode setup
import Adafruit_GPIO as GPIO
gpio = GPIO.get_platform_gpio()
#import RPi.GPIO as GPIO
import time
import signal

from mode_operation_2 import *
from display_fcns import *

#Page buttons
Bp1 = 0 #18 10/9/17
Bp2 = 23
Bp3 = 24
Bp4 = 25

#Grid buttons
Bg1 = 12
Bg2 = 16
Bg3 = 6 #20 SPI 1 MOSI
Bg4 = 13 #21 SPI 1 CLK

#image chip_selects
global cs1, cs2, cs3, cs4
cs1 = 26
cs2 = 27
cs3 = 5
cs4 = 7

#reset pins
global rst1,rst2, rst3, rst4
rst1 = 2
rst2 = 17
rst3 = 22
rst4 = 8

#Mode select
global client_latch
client_latch = 14
global staff_latch
staff_latch = 15
global audio_latch
audio_latch = 1
global image_latch
image_latch = 18 #3

#global variables
global page_select
page_select = 1

global current_mode
global page_num

global staff_mode
staff_mode = 0 #default is to change audio

debounce_time=1000 #milliseconds
################################################################################
def determine_mode():
    #Mode select
    global current_mode
    if (gpio.input(client_latch) == 0):
        current_mode = 0 #client mode
        print("Switching to Client Mode")
        page_input(page_select)
        
    elif (gpio.input(staff_latch) == 0): #turn the switch to staff mode and image/audio mode
        current_mode = 1 #Staff mode
        print("Switching to Staff Mode")
        page_input(page_select)
        if (gpio.input(audio_latch) == 0):
        	staff_mode_audio()
        elif (gpio.input(audio_latch) == 1):
        	staff_mode_image()
        
###################################################################################################
        ##########################################
def page_input(page_num):
    global page_select
    
    if (page_num == 1):
        print('button _page_1_ pressed')
        page_select = 1
        display_image(cs1,rst1,0,"P1B1.jpg")
        time.sleep(0.5)
        display_image(cs2,rst2,0,"P1B2.jpg")
        time.sleep(0.5)
        display_image(cs3,rst3,1,"P1B3.jpg")
        time.sleep(0.5)
        display_image(cs4,rst4,1,"P1B4.jpg")
        
    elif (page_num == 2):
    	print('button _page_2_ pressed')
    	page_select = 2
    	display_image(cs1,rst1,0,"P2B1.jpg")
    	time.sleep(0.5)
    	display_image(cs2,rst2,0,"P2B2.jpg")
    	time.sleep(0.5)
    	display_image(cs3,rst3,1,"P2B3.jpg")
    	time.sleep(0.5)
    	display_image(cs4,rst4,1,"P2B4.jpg")

    elif (page_num == 3):
        print('button _page_3_ pressed')
        page_select = 3
        display_image(cs1,rst1,0,"scope_3.bmp")
        time.sleep(0.5)
        display_image(cs2,rst2,0,"scope_4.bmp")
        time.sleep(0.5)
        display_image(cs3,rst3,1,"scope_5.bmp")
        time.sleep(0.5)
        display_image(cs4,rst4,1,"scope_6.bmp")
        
    elif (page_num == 4):
        print('button _page_4_ pressed')
        page_select = 4
        display_image(cs1,rst1,0,"scope_7.bmp")
        time.sleep(0.5)
        display_image(cs2,rst2,0,"scope_8.bmp")
        time.sleep(0.5)
        display_image(cs3,rst3,1,"scope_9.bmp")
        time.sleep(0.5)
        display_image(cs4,rst4,1,"scope_24.bmp")
#####################################
#Staff mode       
def staff_mode_audio():
    print('You are in audio setup')
    
def staff_mode_image():
	print('You are in image setup')
    
	##turn the switch to staff mode and then to image mode
	#select the page you want to change the images on it
    #page_input(page_select) #uncomment this
	#select the Bg you want to change the image on it
	#page buttons become special functions (increment, decrement, save, cancel)
	#when you hit cancel=Bp4 and/or save=Bp3 the page buttons go back to their normal use (page selection)
	#select the Bg and the image will flash (display and not display)
	#from the page buttons 1 and 2 scroll down and up the images 
	#the page button 3 for save and 4 for cancel
	#index decrease when Pb1 pressed
	#index increase when Pb2 pressed

#Page buttons
gpio.setup(Bp1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bp2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bp4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bp3,GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

gpio.add_event_detect(client_latch, GPIO.BOTH, callback = lambda x: determine_mode(), bouncetime=debounce_time)
gpio.add_event_detect(staff_latch, GPIO.BOTH, callback = lambda x: determine_mode(), bouncetime=debounce_time)
gpio.add_event_detect(image_latch, GPIO.BOTH, callback = lambda x: staff_mode_image(), bouncetime=debounce_time)
gpio.add_event_detect(audio_latch, GPIO.BOTH, callback = lambda x: staff_mode_audio(), bouncetime=debounce_time)


gpio.add_event_detect(Bp1, GPIO.FALLING, callback = lambda x: page_input(1), bouncetime=debounce_time)
gpio.add_event_detect(Bp2, GPIO.FALLING, callback = lambda x: page_input(2), bouncetime=debounce_time)
gpio.add_event_detect(Bp3, GPIO.FALLING, callback = lambda x: page_input(3), bouncetime=debounce_time)
gpio.add_event_detect(Bp4, GPIO.FALLING, callback = lambda x: page_input(4), bouncetime=debounce_time)
    
gpio.add_event_detect(Bg1, GPIO.FALLING, callback = lambda x:grid_input(1,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg2, GPIO.FALLING, callback = lambda x:grid_input(2,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg3, GPIO.FALLING, callback = lambda x:grid_input(3,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg4, GPIO.FALLING, callback = lambda x:grid_input(4,page_select,current_mode,staff_mode), bouncetime=debounce_time)


determine_mode() # grab default state


try:
    while True:
        signal.pause()


except KeyboardInterrupt:
    gpio.cleanup()






