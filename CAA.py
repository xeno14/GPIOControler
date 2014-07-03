#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from GPIOcontrol import GPIOcontrol
import RPi.GPIO as GPIO

class WheelControl(GPIOcontrol):
    """
    車輪の制御を行うクラス
    """

    def __init__(self, pins, mode=GPIO.BOARD):
        """
        初期化

        @param pins 制御ピン．左から，1010で前進，0101で後退するように設定する．
        """
        super(WheelControl,self).__init__(pins, mode)

        self.register("forward", self.setByBits, {"bits":"1010"})
        self.register("back",    self.setByBits, {"bits":"0101"})
        self.register("brake",   self.setByBits, {"bits":"1111"})
        self.register("stop",    self.setByBits, {"bits":"0000"})
        self.register("cw",      self.setByBits, {"bits":"0110"})
        self.register("ccw",     self.setByBits, {"bits":"1001"})

        self._lasttime = time.time()
        self._lastorder = ""

    def execute(self, order):
        now = time.time()
        
        # 異なる制御をするときは間で一回止める
        if order != self._lastorder:
            super(WheelControl,self).execute("stop")

        super(WheelControl,self).execute(order)
        self._lasttime = now
        self._lastorder = order


