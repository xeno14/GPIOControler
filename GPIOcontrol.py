#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GPIOでコントロールするもの
"""

import RPi.GPIO as GPIO
import threading
import time


class GPIOcontrol(object):
    """
    GPIOによってコントロールされるクラスのベースクラス．
    命令はstringで渡される．命令に対するコールバックを辞書に登録しておく．
    """

    def __init__(self, pins, mode=GPIO.BOARD):
        self._order_dict = {}
        self.pins = pins[:]
        GPIO.setmode(mode)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    def execute(self, order, args={}):
        """
        命令(order)に従ってアクションを起こす
        
        @param order 命令(string)
        """
        do = self._order_dict[order]

        if args:
            do[0](**args)
        else:
            do[0](**do[1])

    def register(self, order, func, args={}):
        """
        命令に対するコールバックの登録
        """
        self._order_dict[order] = (func, args)

    def setByBits(self, bits):
        """
        ビット列でオン，オフを制御する

        @param bits "1011"みたいな10でできた文字列
        """
        numloop = min(len(bits), len(self.pins))
        for i in range(numloop):
            if bits[i] is "1":
                GPIO.output(self.pins[i], True)
            else:
                GPIO.output(self.pins[i], False)
        # bitsの長さが足りなければFalseで埋める
        if len(bits) < len(self.pins):
            for i in range(len(bits),len(self.pins)):
                GPIO.output(self.pins[i], False)

class SafetyThread(threading.Thread):
    """
    一定時間命令があるかどうかチェックする
    TODO コールバック関数を登録するようにする
    """
    def __init__(self,threshold,tick=1):
        """
        コンストラクタ

        @param threshold
        時間の閾値(sec)．最後の時間の更新よりthreshold秒経ったらコールバックを呼ぶ．
        @param tick スレッドのループの時間間隔
        """
        threading.Thread.__init__(self)
        self._threshold = threshold
        self._tick = tick 
        self._callbacks = []
        self.update()
        self.setDaemon(True)    #メインスレッドが死んだら私も死ぬ

    def run(self):
        """スレッドの実行．tickごとにthresholdを超えないか確認し，超えた場合は
        登録されたコールバック関数を呼ぶ.
        """
        while(1):
            time.sleep(self._tick)
            now = time.time()
            print now
            if now - self._lasttime > self._threshold:
                for f in self._callbacks:   #コールバックの実行
                    f()
                self.update()
                print "safety @",now

    def update(self):
        """時間の更新
        """
        self._lasttime = time.time()

    def register(self, func):
        """コールバック関数の登録．コールバック関数は引数なしにしてね．"""
        self._callbacks.append(func)
