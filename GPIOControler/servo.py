#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, os
import subprocess

def initialize(pins=[]):
    """servodの初期化

    既にプロセスがあったら殺して，指定したピンの設定でservodのプロセスを立ち上げる
    @param pins --p1pins=で指定するピン（GPIOピンの番号）
    @pre 管理者権限で実行されていること
    """
    args = ""
    if len(pins) > 0:
        args = " --p1pins=" + ",".join([str(i) for i in pins])
    subprocess.call("killall servod", shell=True)
    subprocess.call("servod" + args, shell=True)

class ServoBlaster(object):
    """ServoBlasterのラッパー

    @TODO 番号の指定をP1のピン番号とで切り替えられるように
    """

    def __init__(self, no=0, interval=0, pwm0=90, pwm1=210, angle0=60, angle1=-60):
        """コンストラクタ

        ServoBlasterで用いるサーボの番号，時間間隔（スピードに相当），デューティ比
        と角度の関係を決める．デューティ比，角度のデフォルト値はGWSMICRO/STD/F用．

        @param no サーボの番号（servoblasterのREADME参照）
        @param pwm0, pwm1 [ms*10] 
        @param angle0, angle1 [degree] パルスを動かした時に動く角度の範囲
        @param interval=0 [ms]
        角度を１度動かすときの時間間隔．0以下なら一気に動かす． 
        """
        self._no = no
        self._pwm0 = pwm0
        self._pwm1 = pwm1
        self._angle0 = angle0
        self._angle1 = angle1
        self._angle = 0         #現在の角度
        self._internal = interval

    def _move_by_angle(self, angle):
        """角度を指定して動かす
        """
        # ↓↓pwmと角度の関係が線型だと思ってる式（ただの１次関数）
        pwm = (angle - self._angle0)\
                * (self._pwm1 - self._pwm0)/(self._angle1 - self._angle0)\
                + self._pwm0
        cmd = "echo %d=%d > /dev/servoblaster" % (self._no, pwm)
        os.system(cmd)
        # print "[%d] %s" % (angle, cmd)
        self._angle = angle

    def move(self, angle):
        """角度を指定して動かす
        
        @param angle [degree]
        @pre angle0 <= angle <= angle1
        """
        # 角度が動ける範囲に入るようにする
        if angle < min(self._angle0, self._angle1):
            angle = min(self._angle0, self._angle1)
        if angle > max(self._angle0, self._angle1):
            angle = max(self._angle0, self._angle1)

        start = self._angle     #deperture angle
        stop = angle            #destination angle
        step = 1 if start < stop else -1
        stop += step            #終端が含まれるようにする
        if self._internal > 0:
            # 1 [degree]ずつinterval [ms]ごとに実行する
            for angle in range(start, stop, step):
                self._move_by_angle(angle)
                time.sleep(self._internal)
        else:
            self._move_by_angle(dst)
