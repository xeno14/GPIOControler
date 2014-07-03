#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
こぴぺ元
http://d.hatena.ne.jp/hekyou/20120712/p1
"""


import sys
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from CAA import WheelControl

f = open("./index.html");
content = f.read()
f.close()

wheel = WheelControl([7,11,13,15])

def app(environ, start_response):
    if environ["PATH_INFO"] == '/echo':
        ws = environ["wsgi.websocket"]
        while True:
            src = ws.receive()
            if src is None:
                break
            try:
                wheel.execute(src)
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
    server = pywsgi.WSGIServer(('192.168.24.121', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    GPIO.cleanup()
