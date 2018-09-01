from time import sleep
import re
import serial
ser = serial.Serial("/dev/ttyACM0",9600)
while True:
	try:
		sleep(0.5)
		value = ser.readline()
		contents = (value.decode('utf-8'))
		result = contents.split()[0]
		print(result)
		if int(result)<40:
			contents = "Place finger properly"
		with open("hearrate.txt","w") as f:
			f.write(contents)
	except Exception:
		continue
