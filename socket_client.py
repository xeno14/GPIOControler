#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""socket_client 

サーバーとWebSocketを使って通信を行い，送られてきた命令に従ってGPIOの制御をする．
"""

import sys
import RPi.GPIO as GPIO
from GPIOControler.GPIOControler import SafetyThread
from GPIOControler.WheelControler import Wheel
import websocket
import time

wh = Wheel([7,11,13,15])
th = SafetyThread(10)

def on_message(ws, msg):
    """受信時のコールバック関数

    受け取った命令に従って動作をする．動作が成功したかどうかを返事する．
    返事は先頭に'>'をつけ，そのメッセージを自分が受信したときには何もしないようにする．
    """
    if msg.startswith(">") is False:
        try:
            print msg
            wh.execute(msg)
            th.update()
            ws.send(">" + msg + " success")
        except:
            ws.send(">" + msg + " fail")

def on_error(ws, error):
    """エラー時のコールバック
    """
    print error

def on_close(ws):
    """接続が閉じた時のコールバック
    """
    print "### closed ###"

def on_open(ws):
    """接続開始時のコールバック
    """
    print "### open ###"

if __name__ == "__main__":
    server_adress = "localhost:5000"
    if len(sys.argv) == 2:
        server_adress = sys.argv[1]

    # 安全装置の稼働
    th.register(wh.stop)
    th.start()

    websocket.enableTrace(True)

    while True:
        try:
            ws = websocket.WebSocketApp("ws://" + server_adress + "/echo",
                                      on_message = on_message,
                                      on_error = on_error,
                                      on_close = on_close)
            ws.on_open = on_open
            ws.run_forever()
            time.sleep(1)       #再接続の試行までのインターバル
        except KeyboardInterrupt:
            GPIO.cleanup()
            break
