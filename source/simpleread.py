import RPi.GPIO as GPIO
from datetime import *
import time

"""
Just a script for testing Rpi.GPIO, not really part of this library

"""

SWITCH = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def pressevent(time):
    print('pressed')

GPIO.add_event_detect(SWITCH, GPIO.RISING, callback = pressevent)
GPIO.setup(19, GPIO.OUT)

mytime = datetime.now()

GPIO.output(19, GPIO.LOW)
time.sleep(5)
GPIO.output(19, GPIO.HIGH)
time.sleep(5)

print(datetime.now())
