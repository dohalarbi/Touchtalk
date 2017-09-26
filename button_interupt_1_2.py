import Adafruit_GPIO as GPIO
#import RPi.GPIO as GPIO
import time

gpio = GPIO.get_platform_gpio()
#GPIO.setmode(GPIO.BCM)



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

#global variables
global page_select
page_select = 2


grid_select = 0

def function1(channel):
	print('button _page_1_ pressed')
	global page_select
	page_select = 1
	print(page_select)
	return page_select

def function2(channel):
	print('button _page_2_ pressed')
	global page_select
	page_select = 2
	print(page_select)

def function3(channel):
	print('button _page_3_ pressed')
	global page_select
	page_select = 3
	print(page_select)

def function4(channel):
	print('button _page_4_ pressed')
	global page_select
	page_select = 4
	print(page_select)

#grid button selection
def function5(channel):
	print('button _grid_1_ pressed') #play sound 1
	grid_select = 1
	print(grid_select)

def function6(channel):
	print('button _grid_2_ pressed')#play sound 2
	grid_select = 2
	print(grid_select)

def function7(channel):
 	print('button _grid_3_ pressed')#play sound 3
	grid_select = 3
	print(grid_select)

def function8(channel):
    print('button _grid_4_ pressed')#play sound 4
    grid_select = 4
    print(grid_select)
    


#Page buttons
gpio.setup(Bp1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.add_event_detect(Bp1, GPIO.FALLING, callback=function1)

gpio.setup(Bp2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.add_event_detect(Bp2, GPIO.FALLING, callback=function2)

gpio.setup(Bp3,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.add_event_detect(Bp3, GPIO.FALLING, callback=function3)

gpio.setup(Bp4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.add_event_detect(Bp4, GPIO.FALLING, callback=function4)

#Grid buttons
gpio.setup(Bg1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bg2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bg3,GPIO.IN, pull_up_down=GPIO.PUD_UP)
gpio.setup(Bg4,GPIO.IN, pull_up_down=GPIO.PUD_UP)




def grid_input(grid_select,page_select): 
    if (page_select == 1):
        #Load the pictures for page 1
        if grid_select == 1:
            #play sound 1
            print('You are in page_1 picture_1')
            grid_select = 0
        if grid_select == 2:
            #play sound 2
            print('You are in page_1 picture_2')
            grid_select = 0
        if grid_select == 3:
            #play sound 3
            print('You are in page_1 picture_3')
            grid_select = 0
        if grid_select == 4:
            #play sound 4
            print('You are in page_1 picture_4')
            grid_select = 0
    elif (page_select == 2):
        #Load the pictures for page 1
        if grid_select == 1:
            #play sound 1
            print('You are in page_2 picture_1')
            grid_select = 0
        if grid_select == 2:
            #play sound 2
            print('You are in page_2 picture_2')
            grid_select = 0
        if grid_select == 3:
            #play sound 3
            print('You are in page_2 picture_3')
            grid_select = 0
        if grid_select == 4:
            #play sound 4
            print('You are in page_2 picture_4')
            grid_select = 0
    elif (page_select == 3):
        #Load the pictures for page 1
        if grid_select == 1:
            #play sound 1
            print('You are in page_3 picture_1')
            grid_select = 0
        if grid_select == 2:
            #play sound 2
            print('You are in page_3 picture_2')
            grid_select = 0
        if grid_select == 3:
            #play sound 3
            print('You are in page_3 picture_3')
            grid_select = 0
        if grid_select == 4:
            #play sound 4
            print('You are in page_3 picture_4')
            grid_select = 0
    elif (page_select == 4):
        #Load the pictures for page 1
        if grid_select == 1:
            #play sound 1
            print('You are in page_4 picture_1')
            grid_select = 0
        if grid_select == 2:
            #play sound 2
            print('You are in page_4 picture_2')
            grid_select = 0
        if grid_select == 3:
            #play sound 3

            print('You are in page_4 picture_3')
            grid_select = 0
        if grid_select == 4:
            #play sound 4
            print('You are in page_4 picture_4')
            grid_select = 0

#Grid buttons

gpio.add_event_detect(Bg1, GPIO.FALLING, callback = lambda x:grid_input(1,page_select))


gpio.add_event_detect(Bg2, GPIO.FALLING, callback = lambda x:grid_input(2,page_select))


gpio.add_event_detect(Bg3, GPIO.FALLING, callback = lambda x:grid_input(3,page_select))


gpio.add_event_detect(Bg4, GPIO.FALLING, callback = lambda x:grid_input(4,page_select))


i=0
while True:
	i=i+1
