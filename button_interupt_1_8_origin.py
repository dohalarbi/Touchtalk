#client Mode setup
import Adafruit_GPIO as GPIO
gpio = GPIO.get_platform_gpio()
#import RPi.GPIO as GPIO
import time
import signal

from mode_operation_2 import *
from display_fcns import *

#Page buttons
Bp1 = 18
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

#global variables
global page_select
page_select = 1

global current_mode

global staff_mode
staff_mode = 0 #default is to change audio

debounce_time=400 #milliseconds
################################################################################
def determine_mode():
    #Mode select
    global current_mode
    if (gpio.input(client_latch) == 0):
        current_mode = 0 #client mode
        print("Switching to Client Mode")
        
    elif (gpio.input(staff_latch) == 0):
        current_mode = 1 #Staff mode
        print("Switching to Staff Mode")

###################################################################################################
        ##########################################
def page_input(page_num,current_mode):
    global page_select
    
    if   (page_num == 1):
        print('button _page_1_ pressed')
        page_select = 1
        if (current_mode == 0):
            display_image(cs1,rst1,0,"P1B1.jpg")
            time.sleep(0.5)
            display_image(cs2,rst2,0,"P1B2.jpg")
            time.sleep(0.5)
            display_image(cs3,rst3,1,"P1B3.jpg")
            time.sleep(0.5)
            display_image(cs4,rst4,1,"P1B4.jpg")
        
    elif (page_num == 2):
        if (current_mode == 0):
            display_image(cs1,rst1,0,"P2B1.jpg")
            time.sleep(0.5)
            display_image(cs2,rst2,0,"P2B2.jpg")
            time.sleep(0.5)
            display_image(cs3,rst3,1,"P2B3.jpg")
            time.sleep(0.5)
            display_image(cs4,rst4,1,"P2B4.jpg")
        print('button _page_2_ pressed')
        page_select = 2
        
    elif (page_num == 3):
        print('button _page_3_ pressed')
        page_select = 3
        
    elif (page_num == 4):
        print('button _page_4_ pressed')
        page_select = 4
#####################################
        
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


gpio.add_event_detect(client_latch, GPIO.BOTH, callback = lambda x: determine_mode(), bouncetime=debounce_time)
gpio.add_event_detect(staff_latch, GPIO.BOTH, callback = lambda x: determine_mode(), bouncetime=debounce_time)

gpio.add_event_detect(Bp1, GPIO.FALLING, callback = lambda x: page_input(1,current_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bp2, GPIO.FALLING, callback = lambda x: page_input(2,current_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bp3, GPIO.FALLING, callback = lambda x: page_input(3,current_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bp4, GPIO.FALLING, callback = lambda x: page_input(4,current_mode), bouncetime=debounce_time)
    
gpio.add_event_detect(Bg1, GPIO.FALLING, callback = lambda x:grid_input(1,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg2, GPIO.FALLING, callback = lambda x:grid_input(2,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg3, GPIO.FALLING, callback = lambda x:grid_input(3,page_select,current_mode,staff_mode), bouncetime=debounce_time)
gpio.add_event_detect(Bg4, GPIO.FALLING, callback = lambda x:grid_input(4,page_select,current_mode,staff_mode), bouncetime=debounce_time)


determine_mode() # grab default state
page_input(page_select,current_mode)

try:
    while True:
        signal.pause()


except KeyboardInterrupt:
    gpio.cleanup()






