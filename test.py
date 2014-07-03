import RPi.GPIO as GPIO
import time
from CAA import WheelControl
from GPIOcontrol import GPIOcontrol

w = WheelControl([7,11,13,15])

w.execute("back")


time.sleep(3)

w.execute("ccw")

time.sleep(3)
GPIOcontrol.cleanup()
