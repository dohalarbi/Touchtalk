# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from PIL import Image


import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import os

gpio = GPIO.get_platform_gpio()
gpio.setup(27, GPIO.OUT)
gpio.output(27, GPIO.HIGH)

gpio.setup(2, GPIO.OUT)
gpio.output(2, GPIO.HIGH)

# Raspberry Pi configuration.
DC = 4 
RST1 = 17
RST2 = 22
SPI_PORT = 0
SPI_DEVICE = 0


# BeagleBone Black configuration.
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Create TFT LCD display class.
disp1 = TFT.ILI9341(DC, rst=RST1, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp2 = TFT.ILI9341(DC, rst=RST2, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

okay_path="/home/pi/touchtalk/Images/I_am_okay_RS.jpg"
sick_path="/home/pi/touchtalk/Images/I_dont_feel_well_RS.jpg"
###################################
#UPDATE Screen 1 to display dog.jpg
###################################
# Initialize display.
gpio.output(27, GPIO.LOW)
disp1.begin()
gpio.output(27, GPIO.HIGH)

# Load an image.
print('Loading image...')
image = Image.open(okay_path)

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(180)#.resize(240, 320)

# Draw the image on the display hardware.
print('Drawing image')
gpio.output(27, GPIO.LOW)
disp1.display(image)
gpio.output(27, GPIO.HIGH)

###################################
#UPDATE Screen 2 to display cat.jpg
###################################

# Initialize display.
gpio.output(2, GPIO.LOW)
disp2.begin()
gpio.output(2, GPIO.HIGH)

# Load an image.
print('Loading image...')
image = Image.open(sick_path)

# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(180)#.resize((240, 320))

# Draw the image on the display hardware.
print('Drawing image')
gpio.output(2, GPIO.LOW)
disp2.display(image)
gpio.output(2, GPIO.HIGH)

os.system('sleep 5') #pauses program for 5 seconds
####################################
#SWAP SCREEN IMAGES#
####################################
image = Image.open(sick_path)
image = image.rotate(180)#.resize((240, 320))
gpio.output(27, GPIO.LOW)
disp1.display(image)
gpio.output(27, GPIO.HIGH)

image = Image.open(okay_path)
image = image.rotate(180)#.resize((240, 320))
gpio.output(2, GPIO.LOW)
disp2.display(image)
gpio.output(2, GPIO.HIGH)