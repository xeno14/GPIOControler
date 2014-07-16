#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import RPi.GPIO as GPIO
from GPIOControler.GPIOControler import SafetyThread
from WheelControler import WheelControler
import websocket
import thread
import time

wh = WheelControler([7,11,13,15])
th = SafetyThread(10)

def on_message(ws, msg):
    """受信時のコールバック関数

    ここで制御を行う
    """
    #自分からの発信には>をつけて無限ループにならないようにした
    if msg.startswith(">") is False:
        try:
            print msg
            wh.execute(msg)
            th.update()
            ws.send(">" + msg + " done")
        except:
            ws.send(">" + msg + " failed")

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"
    GPIO.cleanup()

def on_open(ws):
    print "### open ###"
    #asynchronous message
    def run():
        ws.send(">Hello from client")
    th.register(run)
    th.register(wh.stop)
    th.start()

if __name__ == "__main__":

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/echo",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
