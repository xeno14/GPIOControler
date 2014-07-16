#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from gevent import pywsgi, sleep
from geventwebsocket.handler import WebSocketHandler

# index.htmlを開く
f = open("./html/index.html");
content = f.read()
f.close()

ws_list = set()
def chat_handle(environ, start_response):
    global cnt
    ws = environ['wsgi.websocket']
    ws_list.add(ws)
    print 'enter!', len(ws_list)
    while 1:
        msg = ws.receive()
        if msg is None:
            break
        remove = set()
        for s in ws_list:
            try:
                s.send(msg)
            except Exception:
                remove.add(s)
        for s in remove:
            ws_list.remove(s)
    print 'exit!', len(ws_list)

def app(environ, start_response):
    """WebSocketのサーバ"""
    path = environ["PATH_INFO"]
    if path == '/echo':
        return chat_handle(environ, start_response)
    elif path == '/chatroom':   #deprecated
        start_response("200 OK", [("Content-Type", "text/html")])  
        return open('./html/chat_sample.html').read()
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

    try:
        server = pywsgi.WSGIServer((ipadress, port), app, \
                handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print "detect KeyboardInterrupt. cleanup and exit."
        sys.exit(1)
