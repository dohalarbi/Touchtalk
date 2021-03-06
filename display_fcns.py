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
gpio = GPIO.get_platform_gpio()
import Adafruit_GPIO.SPI as SPI
import os
    
def display_image(cs,reset,port_num, image_name):

    gpio.setup(cs, GPIO.OUT) #cs: 27,2, , 
    gpio.output(cs, GPIO.HIGH)

    # Raspberry Pi configuration.
    DC = 4 
    RST = reset #rst: 17,22, ,
    SPI_PORT = port_num
    SPI_DEVICE = 0

    # Create TFT LCD display class.
    disp1 = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=640))

    image_path="/home/pi/touchtalk/Images/" + image_name
    
    # Initialize display.

    gpio.output(cs, GPIO.LOW)
    disp1.begin()
    gpio.output(cs, GPIO.HIGH)

    # Load an image.
    print('Loading image...')
    image = Image.open(image_path)

    # Resize the image and rotate it so it's 240x320 pixels.
    image = image.rotate(180).resize((240, 320))

    # Draw the image on the display hardware.
    print('Drawing image')
    gpio.output(cs, GPIO.LOW)
    disp1.display(image)
    gpio.output(cs, GPIO.HIGH)
