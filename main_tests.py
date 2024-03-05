#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2018 Erriez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

##
# This is a Python getting started example to control a single R421A08 relay board with a
# USB - RS485 dongle.
#
# Python 2.7 and Python 3.6 are supported.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import datetime
from operator import truediv
import time
import sys

# Add system path to find relay_ Python packages
sys.path.append('.')
sys.path.append('..')

import relay_modbus
import relay_boards

# Required: Configure serial port, for example:
#   On Windows: 'COMx'
#   On Linux:   '/dev/ttyUSB0'
SERIAL_PORT = '/dev/tty.usbserial-14340'


def check(retval):
    if not retval:
        sys.exit(1)


if __name__ == '__main__':


    print('Getting started R421A08 relay board\n')

    # Create MODBUS object
    _modbus = relay_modbus.Modbus(serial_port=SERIAL_PORT, baud_rate=19200, verbose=False)

    # Open serial port
    try:
        _modbus.open()
    except relay_modbus.SerialOpenException as err:
        print(err)
        print("FALLHA ABRIR")
        sys.exit(1)


    # Create relay board object
    board = relay_boards.R421A08(_modbus, address=1, num_relays=16)


    #print(board.setBaudrate(19200))
    print(board.getBaudrate())
    #exit()

    #board.on(1)
    #print(board._read_relay_status(1))
    last_state = {}
    while True:
        inputs = board._read_all_holding()
        print(datetime.datetime.now(), inputs)
        for i, state in inputs.items():
            if i not in last_state:
                last_state.setdefault(i, None)

            if last_state[i]!=state:
                print("Status de IN{} mudou para {}".format(i, state))
                board.setState(i, state)
                last_state[i] = state

    exit()
    #board.on(8)
    #board.on(16)
    #board.on(11)
    print(board._read_all_coil())
    #board._read_holding_range(0, 10,16)
    exit()
    #print(board._read_all_holding())
    for i in range(0,20):
        try:
            print("==>", i)
            print(board._read_holding_range(i, 10,16))
        except Exception as e:
            print(e)

    #print(board.get_status(1))

    #print(board.toggle(1)) # inverte o status.

    #exit()

    print('Status all relays:')

    #check(board.print_status_all())
    #print([v for k,v in board.get_status_all().items()])
    time.sleep(1)
    exit()
    
    for _ in range(4):
        for i in range(1,17):
            print('Turn relay {} on'.format(i))
            check(board.on(i))
            #time.sleep(0.001)
            exit()

        for i in range(1,17):
            print('Turn relay {} off'.format(i))
            check(board.off(i))
            #time.sleep(0.001)

    if False:
        print('Turn relay 1 off')
        check(board.off(1))
        time.sleep(1)

        print('Toggle relay 8')
        check(board.toggle(8))
        time.sleep(1)

        print('Latch relays 6 on, all other relays off')
        check(board.latch(6))
        time.sleep(1)

        print('Turn relay 4 on for 5 seconds, all other relays off')
        check(board.delay(4, delay=5))
        time.sleep(6)

        print('Turn relays 3, 7 and 8 on')
        check(board.toggle_multi([3, 7, 8]))
        time.sleep(1)

        print('Turn all relays on')
        check(board.on_all())
        time.sleep(1)

        print('Turn all relays off')
        check(board.off_all())
        time.sleep(1)
