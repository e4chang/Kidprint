#!/usr/bin/env python

'''
   KP_Serial.py
   We are interested in communicating with the ProMicro Module from Sparkfun
   which will have name given by udev (May add more in the future if need to)
       'usb-SparkFun_SparkFun_Pro_Micro_if00'
           Baud Rate: 9600 Bit/s
           Setup: '8N1'

   This will control a Varioptic Wet Lens Driver via I2C
        Driver Address: 0xEE for write
                        0xEF for read

   Function one:
       0. Initialize Serial Control with the Board
       1. Initialize lens
       2. Check Lens Connection(CheckFails and Fail)
       3. Sense Lens Temperature
       4. Enter into Sleep Mode
       5. Enter into Shut Down Mode
       6. Enter into Active Mode
       7. Driver Configuration(To be made)
       8. Send Focus Point 0x000 - 0x3FF
       9. Read Focus Point 0x000 - 0x3FF
'''

import serial

__author__= "Yunting Zhao"
__email__="yuz060@eng.ucsd.edu"

INIT = 0x10
SEND = 0x11
READ = 0x12

bn = "/dev/serial/by-id/usb-SparkFun_SparkFun_Pro_Micro-if00"
baudrate = 9600

def PMint():
    pm = serial.Serial(bn, timeout = 1)
    return pm

def lenint(pm):
    pm.write(chr(INIT))
    print(pm)
    return

# LensValue = 0-1023
def lenset(pm, lensValue):
    # We have 10 bits for each value, need two bytes to transmit
    pm.write(chr(SEND)) # Signal the Controller to send value to lens driver
    print lensValue
    pm.write(chr((lensValue >> 2) & 0xff)) # Ensure a 8 bit value
    pm.write(chr(lensValue & 0b11))     # Only take last two bits
    return
