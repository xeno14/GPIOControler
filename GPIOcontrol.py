#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GPIOでコントロールするもの
"""

import RPi.GPIO as GPIO


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
