import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)

GPIO.setup(5, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        if (GPIO.input(5)==1):
		os.system('speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav')
        else:
            print("No audio is playing at this time")

except KeyboardInterrupt:
    GPIO.cleanup()

##Wasn't working on Rpi3 since it would always play the test sound.  Also should just replace with a new jpeg