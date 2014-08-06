#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time


class SafetyThread(threading.Thread):
    """一定時間命令があるかどうかチェックする"""
    def __init__(self, threshold, tick=1):
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
        self.setDaemon(True)

    def run(self):
        """スレッドの実行．

        tickごとにthresholdを超えないか確認し，超えた場合は
        登録されたコールバック関数を呼ぶ."""
        while(1):
            time.sleep(self._tick)
            now = time.time()
            if now - self._lasttime > self._threshold:
                for f in self._callbacks:
                    f()
                self.update()
                print "safety @", now

    def update(self):
        """時間の更新"""
        self._lasttime = time.time()

    def register(self, func):
        """コールバック関数の登録

        @pre コールバック関数は引数をとらない
        """
        self._callbacks.append(func)
