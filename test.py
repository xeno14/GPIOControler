#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from GPIOControler.wheel import WheelControler
from GPIOControler.servo import ServoBlaster

w = WheelControler([7,11,13,15])
servo = ServoBlaster(0)

servo.execute(10)
time.sleep(1)
servo.execute(-10)
time.sleep(1)
servo.execute(50)
time.sleep(1)
servo.execute(-50)
