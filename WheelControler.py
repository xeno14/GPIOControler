# -*- coding: utf-8 -*-

import time
import threading
from GPIOControler.GPIOControler import GPIOControler
import RPi.GPIO as GPIO

class WheelControler(GPIOControler):
    """
    車輪の制御を行うクラス
    """

    def __init__(self, pins, mode=GPIO.BOARD):
        """
        初期化

        @param pins 制御ピン．左から，1010で前進，0101で後退するように設定する．
        """
        super(WheelControler,self).__init__(pins, mode)

        self.register("forward", self.forward)
        self.register("back",    self.back)
        self.register("brake",   self.brake)
        self.register("stop",    self.stop)
        self.register("cw",      self.cw)
        self.register("ccw",     self.ccw)
        self.register("left",    self.left)
        self.register("right",   self.right)

    def execute(self, order):
        now = time.time()
        
        # 異なる制御をするときは間で一回止める
        if order != self.last_order():
            super(WheelControler,self).execute("stop")
        super(WheelControler,self).execute(order)

    def forward(self):
        self.set_by_bits("1010")

    def back(self):
        self.set_by_bits("0101")

    def brake(self):
        self.set_by_bits("1111")

    def stop(self):
        self.set_by_bits("0000")

    def cw(self):
        """
        時計回り旋回
        """
        self.set_by_bits("1001")
    
    def ccw(self):
        """
        反時計回り旋回
        """
        self.set_by_bits("0110")
    
    def left(self):
        """
        左に曲がる．左の車輪の頻度を半分にする．
        """
        self.blink("1010","0010")   #左の車輪だけ状態が変わる

    def right(self):
        """
        右に曲がる．右の車輪の頻度を半分にする．
        """
        self.blink("1010","1000")   #右の車輪だけ状態が変わる
    
    def blink(self,on_bits,off_bits="0000",interval=0.1):
        """
        ピンの状態をinterval秒ごとにon，offの状態にする

        @param on_bits オンのときの状態
        @param off_bits オフのときの状態 ["0000"]
        @param interval 切り替えの間隔 [0.1]
        """
        def _blink():
            while self.current_order() == "left" \
                    or self.current_order() == "right":
                self.set_by_bits(on_bits)
                time.sleep(interval)
                self.set_by_bits(off_bits)
                time.sleep(interval)
            # TODO ここで処理しないとoff_bitsになったままになることがある
            self.execute("stop")
        t = threading.Thread(target = _blink)
        t.setDaemon(True)
        t.start()
