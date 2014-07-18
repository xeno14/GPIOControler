#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

class ServoBlaster(object):
    """ServoBlasterのラッパー

    \TODO 番号の指定をP1のピン番号とで切り替えられるように
    \TODO 相対的な位置の変更(+,-で値を指定)
    """

    def __init__(self, no, pwmmin=90, pwmmax=210, angle0=60, angle1=-60):
        """コンストラクタ
        
        @param no サーボの番号（servoblasterのREADME参照）
        @param pwmmin, pwmmax [ms*10] パルスの範囲 
        @param angle0, angle1 [degree] パルスを動かした時に動く角度の範囲
        """
        self._no = no
        self._pwmmin = pwmmin
        self._pwmmax = pwmmax
        self._angle0 = angle0
        self._angle1 = angle1
        self._pwm= 0    #現在の値

    def execute(self, angle):
        if angle < min(self._angle0, self._angle1):
            angle = min(self._angle0, self._angle1)
        if angle > max(self._angle0, self._angle1):
            angle = max(self._angle0, self._angle1)
        pwm = (angle - self._angle0)\
                * (self._pwmmax - self._pwmmin)/(self._angle1 - self._angle0)\
                + self._pwmmin
        cmd = "echo %d=%d > /dev/servoblaster" % (self._no, pwm)
        print cmd   #delete after test
        subprocess.call(cmd, shell=True)
        self._pwm = pwm

    def pwm(self):
        return self._pwm
