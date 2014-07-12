#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from GPIOControler.GPIOControler import GPIOControler
from WheelControler import WheelControler

w = WheelControler([7,11,13,15])

if __name__ == '__main__':
    w.execute("turn_left")
    time.sleep(4)

    print "back"
    w.execute("back")

    time.sleep(3)

    GPIO.cleanup()
