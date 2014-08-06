#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
from _controler import GPIOControler
import RPi.GPIO as GPIO


class WheelControler(GPIOControler):
    """車輪の制御を行うクラス"""

    def __init__(self, pins, mode=GPIO.BOARD):
        """初期化

        @param pins 制御ピン．左から，1010で前進，0101で後退するように設定する．"""
        super(WheelControler, self).__init__(pins, mode)

        self.register("forward", self.forward)
        self.register("back",    self.back)
        self.register("brake",   self.brake)
        self.register("stop",    self.stop)
        self.register("cw",      self.cw)
        self.register("ccw",     self.ccw)
        self.register("left",    self.left)
        self.register("right",   self.right)

    def execute(self, order):

        # 異なる制御をするときは間で一回止める
        if order != self.last_order():
            super(WheelControler, self).execute("stop")
        super(WheelControler, self).execute(order)

    def forward(self):
        """前進，左輪，右輪ともに前進，"""
        self.set_by_bits("1010")

    def back(self):
        """後退．左輪，右輪ともに後退．"""
        self.set_by_bits("0101")

    def brake(self):
        """ブレーキ，"""
        self.set_by_bits("1111")

    def stop(self):
        """停止，ピンを全てLOWにする．"""
        self.set_by_bits("0000")

    def cw(self):
        """時計回り旋回，左輪前進，右輪後退．"""
        self.set_by_bits("1001")

    def ccw(self):
        """反時計回り旋回，左輪後退，右輪前進．"""
        self.set_by_bits("0110")

    def left(self):
        """左に曲がる．左の車輪の頻度を半分にする．"""
        self.blink("1010", "0010")

    def right(self):
        """右に曲がる．右の車輪の頻度を半分にする．"""
        self.blink("1010", "1000")

    def blink(self, on_bits, off_bits="0000", interval=0.1):
        """ピンの状態をinterval秒ごとにon，offの状態にする

        @param on_bits オンのときの状態
        @param off_bits オフのときの状態 ["0000"]
        @param interval 切り替えの間隔 [0.1]
        """
        blinkorder = self.current_order()

        def _blink():
            while True:
                # 命令が変わっていた場合はループを抜ける
                if self.current_order() != blinkorder:
                    break
                self.set_by_bits(on_bits)
                time.sleep(interval)
                if self.current_order() != blinkorder:
                    break
                self.set_by_bits(off_bits)
                time.sleep(interval)
        t = threading.Thread(target=_blink)
        t.setDaemon(True)
        t.start()
