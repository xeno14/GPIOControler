#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, os
import subprocess
import threading

def initialize(pins=[], pwm=-1):
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

#childexception
    if pwm > 0:
        for i in range(len(pins)):
            cmd = "echo %d=%d > /dev/servoblaster" % (i, pwm)
            os.system(cmd)

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
        @param interval=0 [sec]
        角度を１度動かすときの時間間隔．0以下なら一気に動かす． 
        """
        self._no = no
        self._interval = interval
        self._pwm0 = pwm0
        self._pwm1 = pwm1
        self._angle0 = angle0
        self._angle1 = angle1

        self._angle = 0        #現在の角度(最初０でいいんかなぁ・・・）
        self._threads = []     #稼働しているスレッドを入れとくリスト 

    def _move_by_angle(self, angle):
        """角度を指定して動かす
        """
        # ↓↓pwmと角度の関係が線型だと思ってる式（ただの１次関数）
        pwm = (angle - self._angle0)\
                * (self._pwm1 - self._pwm0)/(self._angle1 - self._angle0)\
                + self._pwm0
        cmd = "echo %d=%d > /dev/servoblaster" % (self._no, pwm)
        os.system(cmd)
        #print "[%d] %s" % (angle, cmd)
        self._angle = angle

    def move(self, angle):
        """角度を指定して動かす
        
        @param angle [degree]
        @pre angle0 <= angle <= angle1
        """
        # 既に動いているスレッドの破棄
        for t in self._threads:
            t.abort()

        # 角度が動ける範囲に入るようにする
        if angle < min(self._angle0, self._angle1):
            angle = min(self._angle0, self._angle1)
        if angle > max(self._angle0, self._angle1):
            angle = max(self._angle0, self._angle1)

        start = self._angle     #deperture angle
        stop = angle            #destination angle
        step = 1 if start < stop else -1
        if self._interval > 0:
            # 非同期処理で動かす．
            self._threads.append(\
                    _ServoThread(self, start, stop, step))
        else:
            self._move_by_angle(stop + step)

    def set_interval(self, interval=0):
        """インターバルの設定"""
        self._interval = interval

class _ServoThread():
    """サーボ用のスレッド

    abortメソッドを用意してループ中に破棄できるようにする．気分的にはServoBlasterの
    内部クラスにしたい．

    http://stackoverflow.com/questions/14976430/python-threads-thread-is-not-informed-to-stop
    """
    def __init__(self, servo, start, stop, step):
        self.stop_event = threading.Event()
        self.servo = servo
        self.start = start
        self.stop = stop
        self.step = step
        self.thread = threading.Thread(target = self.moving)
        self.thread.start()

    def moving(self):
        angle = self.start
        while not self.stop_event.isSet() and angle != self.stop + self.step:
            self.servo._move_by_angle(angle)
            time.sleep(self.servo._interval)
            angle += self.step
        
    def abort(self):
        # Request thread to stop.
        self.stop_event.set()
        # Wait for thread to exit.
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
