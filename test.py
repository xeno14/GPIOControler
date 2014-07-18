#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from GPIOControler.wheel import WheelControler
from GPIOControler.servo import ServoBlaster

w = WheelControler([7,11,13,15])
print("forward")
w.execute("forward")
time.sleep(1)
print("back")
w.execute("back")
time.sleep(1)
print("brake")
w.execute("brake")
time.sleep(1)

print "##### servo test #####"
servo = ServoBlaster(7,0.05)
print "### 10 ###"
servo.move(10)
time.sleep(1)
print "### -10 ###"
servo.move(-10)
print "### 50 ###"
servo.move(50)
time.sleep(1)
print "### -50 ###"
servo.move(-50)

GPIO.cleanup()
