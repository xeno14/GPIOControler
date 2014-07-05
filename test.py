import RPi.GPIO as GPIO
import time
from CAA import WheelControl
from GPIOcontrol import SafetyThread
from GPIOcontrol import GPIOcontrol

w = WheelControl([7,11,13,15])

safety = SafetyThread(3,1)
def safe():
    w.execute("brake")
safety.register(safe)
safety.start()

# w.execute("back")



time.sleep(3)

# w.execute("ccw")

time.sleep(3)
GPIOcontrol.cleanup()
