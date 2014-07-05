#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
こぴぺ元
http://d.hatena.ne.jp/hekyou/20120712/p1
"""


import sys
import threading
import time
import datetime
import RPi.GPIO as GPIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from CAA import WheelControl
from GPIOcontrol import SafetyThread

# index.htmlを開く
f = open("./index.html");
content = f.read()
f.close()

wheel = WheelControl([7,11,13,15])  #車輪の制御プログラム
th = SafetyThread(10)               #安全装置(10秒)    

def app(environ, start_response):
    if environ["PATH_INFO"] == '/echo':
        ws = environ["wsgi.websocket"]
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

    if len(sys.argv) != 2:
        print("usage: %s ipadress" % sys.argv[0])
        sys.exit(1)
    ipadress = sys.argv[1]

    th.register(wheel.stop)
    th.start()  #安全装置スレッドの開始

    server = pywsgi.WSGIServer((ipadress, 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    GPIO.cleanup()
