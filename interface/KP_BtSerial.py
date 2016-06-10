#
# KP_BtSerial.py
# Testing script for communicating with Bluetooth module. 
#

import platform
import serial
import time

WINDOWS_PORT = "COM15"		# Bluetooth port for Windows
LINUX_PORT = "/dev/rfcomm0"	# Bluetooth port for Linux
BAUDRATE = 9600				# bits/sec rate

test = ["this", "is", "an", "example", "string"]

# Windows connection
if platform.system() == "Windows":
	ser = serial.Serial(port=WINDOWS_PORT,
							   baudrate=BAUDRATE,
							   timeout = 0)
	time.sleep(1)
# Linux/Mac connection
else:
	ser = serial.Serial(LINUX_PORT, BAUDRATE)

def test_input(ser, test):
	print "Test beginning!"
	initial = int(round(time.time()*1000))
	for word in test:
		ser.write(word)
	after = int(round(time.time()*1000))
	print "Finished sending!"
	print "%d milliseconds" % (after-initial)

	initial = int(round(time.time()*1000))
	input = "".join(test)
	result = ""
	while result != input:
		next = ser.readline()
		if next != "":
			print next
			result = result+next
	after = int(round(time.time()*1000))
	print "%d milliseconds" % (after-initial)

# continually get input from terminal and pass it into the Pro Micro
def manual_input(ser):
	print "Type string to input or 'quit' to exit:"
	input = raw_input("> ")
	if input == "quit":
		return
	else:
		initial = int(round(time.time()*1000))
		ser.write(input)
		result = ""
		while input != result:
			next = ser.readline()
			if next != "":
				print next
				result = result+next
		after = int(round(time.time()*1000))
		print "%d milliseconds" % (after-initial)

test_input(ser, test)
