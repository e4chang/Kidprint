#
# KP_BtSerial.py
# This script attempts to 
#

import platform
import serial
import time

WINDOWS_PORT = "COM15"		# Bluetooth port for Windows
LINUX_PORT = "/dev/rfcomm0"	# Bluetooth port for Linux
BAUDRATE = 9600				# bits/sec rate

# Windows connection
if platform.system() == "Windows":
	ser = serial.Serial(port=WINDOWS_PORT, baudrate=BAUDRATE, timeout=5)
	time.sleep(2)
# Linux/Mac connection
else:
	ser = serial.Serial(LINUX_PORT, BAUDRATE)

# continually get input and pass it into the Pro Micro
while True:
	print "Type string to input or 'quit' to exit:"
	input = raw_input("> ")
	if input == "quit":
		break
	else:
		ser.write(input)
		time.sleep(2)
		print ser.read(ser.in_waiting)
