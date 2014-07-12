#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPIOでコントロールするもの
"""

import RPi.GPIO as GPIO
import threading
import time

class GPIOControler(object):
    """GPIOによってコントロールされるクラスのベースクラス．
    命令はstringで渡される．命令に対するコールバックを辞書に登録しておく．
    """
    _last_order = ""        # 最後に実行した命令
    _current_order = ""     # 現在処理中の命令

    def __init__(self, pins, mode=GPIO.BOARD):
        self._order_dict = {}
        self._pins = pins[:]
        GPIO.setmode(mode)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    def execute(self, order, args={}):
        """命令(order)に従ってアクションを起こす
        
        @param order 命令(string)
        """
        self._current_order = order
        do = self._order_dict[order]

        if args:
            do[0](**args)
        else:
            do[0](**do[1])
        
        self._last_order = order

    def register(self, order, func, args={}):
        """命令に対するコールバックの登録"""
        self._order_dict[order] = (func, args)

    def set_by_bits(self, bits):
        """ビット列でオン，オフを制御する

        @param bits "1011"みたいな10でできた文字列
        """
        numloop = min(len(bits), len(self._pins))
        for i in range(numloop):
            if bits[i] is "1":
                GPIO.output(self._pins[i], True)
            else:
                GPIO.output(self._pins[i], False)
        # bitsの長さが足りなければFalseで埋める
        if len(bits) < len(self._pins):
            for i in range(len(bits),len(self._pins)):
                GPIO.output(self._pins[i], False)

    def last_order(self):
        """最後に実行した命令の取得"""
        return self._last_order

    def current_order(self):
        """現在実行中の命令の取得"""
        return self._current_order

    def dump(self):
        """GPIOのピンの状態の出力．使用するピンの状態を調べ，Trueならoを，Falseなら
        xを順次出力する．

        例： [1,0,1,0] -> oxox
        """
        for pin in self._pins:
            if GPIO.input(pin):
                print "o",
            else:
                print "x",
        print ""


class SafetyThread(threading.Thread):
    """一定時間命令があるかどうかチェックする"""
    def __init__(self,threshold,tick=1):
        """コンストラクタ

        @param threshold 時間の閾値(sec)．\
                最後の時間の更新よりthreshold秒経ったらコールバックを呼ぶ．
        @param tick スレッドのループの時間間隔(sec)
        """
        threading.Thread.__init__(self)
        self._threshold = threshold
        self._tick = tick 
        self._callbacks = []
        self.update()
        self.setDaemon(True)    #メインスレッドが死んだら私も死ぬ

    def run(self):
        """スレッドの実行．
        
        tickごとにthresholdを超えないか確認し，超えた場合は
        登録されたコールバック関数を呼ぶ."""
        while(1):
            time.sleep(self._tick)
            now = time.time()
            #print now
            if now - self._lasttime > self._threshold:
                for f in self._callbacks:   #コールバックの実行
                    f()
                self.update()
                print "safety @",now

    def update(self):
        """時間の更新"""
        self._lasttime = time.time()

    def register(self, func):
        """コールバック関数の登録．コールバック関数は引数なしにしてね．"""
        self._callbacks.append(func)
