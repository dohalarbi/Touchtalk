#client Mode setup
import Adafruit_GPIO as GPIO
gpio = GPIO.get_platform_gpio()
#import RPi.GPIO as GPIO
import time
import signal

from mode_operation import grid_input

#Page buttons
Bp1 = 18
Bp2 = 23
Bp3 = 24
Bp4 = 25

#Grid buttons
Bg1 = 12
Bg2 = 16
Bg3 = 20
Bg4 = 21

#Mode select
client_latch = 14
staff_latch = 15

#global variables
global page_select
page_select = 2

global current_mode

global staff_mode
staff_mode = 0 #default is to change audio

debounce_time=400 #milliseconds

def determine_mode():
    global current_mode
    if (gpio.input(client_latch) == 0):
        current_mode = 0 #client mode
        print("Switching to Client Mode")
        
    elif (gpio.input(staff_latch) == 0):
        current_mode = 1 #Staff mode
        print("Switching to Staff Mode")

def page1(channel):
	print('button _page_1_ pressed')
	global page_select
	page_select = 1
	print(page_select)
	return page_select

def page2(channel):
	print('button _page_2_ pressed')
	global page_select
	page_select = 2
	print(page_select)

def page3(channel):
	print('button _page_3_ pressed')
	global page_select
	page_select = 3
	print(page_select)

def page4(channel):
	print('button _page_4_ pressed')
	global page_select
	page_select = 4
	print(page_select)
        
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

gpio.add_event_detect(Bp1, GPIO.FALLING, callback=page1, bouncetime=debounce_time)
gpio.add_event_detect(Bp2, GPIO.FALLING, callback=page2, bouncetime=debounce_time)
gpio.add_event_detect(Bp3, GPIO.FALLING, callback=page3, bouncetime=debounce_time)
gpio.add_event_detect(Bp4, GPIO.FALLING, callback=page4, bouncetime=debounce_time)
    
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





