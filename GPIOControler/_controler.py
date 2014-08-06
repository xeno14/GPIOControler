#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPIOでコントロールするもの
"""

import RPi.GPIO as GPIO


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
        if order in self._order_dict:
            do = self._order_dict[order]
            self._current_order = order
            if args:
                do[0](**args)
            else:
                do[0](**do[1])
            self._last_order = order
        else:
            raise NotImplementedError

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
            for i in range(len(bits), len(self._pins)):
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
