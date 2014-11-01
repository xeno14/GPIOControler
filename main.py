#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import RPi.GPIO as GPIO
import registry
import socket_client
import time

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print >> sys.stderr, 'Require 2 parameters: server_address and index.'
        sys.exit(1)

    server_address = sys.argv[1]
    index = sys.argv[2]


    registry.register(server_address, index)
    socket_client.init_safety()

    while True:
        try:
            ws = socket_client.get_websocket(server_address, index)
            ws.run_forever()
            # 再接続の試行までのインターバル
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            break

    registry.delete(server_address, index)
