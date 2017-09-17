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

gpio = GPIO.get_platform_gpio()
gpio.setup(14, GPIO.OUT) ##pin 14 == screen 1
gpio.output(14, GPIO.HIGH) #default bus state

gpio.setup(15, GPIO.OUT) ##pin 15 == screen 2
gpio.output(15, GPIO.HIGH) # default bus state

# Raspberry Pi configuration.
DC = 24 
RST_1 = 25 
RST_2 = 12 
SPI_PORT = 0
SPI_DEVICE = 0

# BeagleBone Black configuration.
# DC = 'P9_14'
# RST = 'P9_12'
# SPI_PORT = 0
# SPI_DEVICE = 0

# Create TFT LCD display class.
disp1 = TFT.ILI9341(DC, rst=RST_1, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp2 = TFT.ILI9341(DC, rst=RST_2, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
gpio.output(14, GPIO.LOW)
disp1.begin()
gpio.output(14, GPIO.HIGH)

# Load an image.
print('Loading image...')
image1 = Image.open('cat.jpg')


# Resize the image and rotate it so it's 240x320 pixels.
image1 = image1.rotate(90).resize((240, 320))


# Draw the image on the display hardware.
print('Drawing image 1')
gpio.output(14, GPIO.LOW)
disp1.display(image1)
gpio.output(14, GPIO.HIGH)

############################################
# Initialize display 2.

gpio.output(15, GPIO.LOW)
disp2.begin()
gpio.output(15, GPIO.HIGH)

# Load an image.
print('Loading image 2...')
image2 = Image.open('dog.jpg')
image2 = image2.rotate(90).resize((240, 320))

print('Drawing image 2')
gpio.output(15, GPIO.LOW)
disp2.display(image2)
gpio.output(15, GPIO.HIGH)

