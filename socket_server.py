#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import threading
import time
import datetime
import RPi.GPIO as GPIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from GPIOControler.GPIOControler import SafetyThread
from WheelControler import WheelControler

# index.htmlを開く
f = open("./html/index.html");
content = f.read()
f.close()

wheel = WheelControler([7,11,13,15]) #車輪の制御プログラム
th = SafetyThread(10)                #安全装置(10秒)    

def app(env, start_response):
    """WebSocketのサーバ"""
    if env["PATH_INFO"] == '/echo':
        ws = env["wsgi.websocket"]
        while True:
            src = ws.receive()
            if src is None:
                break
            try:
                wheel.execute(src)
                th.update()
                ws.send(src + "...done")
            except:
                ws.send(src + "...failed")
    else:
        start_response("200 OK", [
                ("Content-Type", "text/html"),
                ("Content-Length", str(len(content)))
                ])  
        return iter([content])

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("usage: %s servername port" % sys.argv[0])
        sys.exit(1)
    ipadress = sys.argv[1]
    port = int(sys.argv[2])

    th.register(wheel.stop) #安全装置のコールバックの登録
    th.start()              #安全装置スレッドの開始

    try:
        server = pywsgi.WSGIServer((ipadress, port), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print "detect KeyboardInterrupt. cleanup and exit."
        GPIO.cleanup()
        sys.exit(1)
