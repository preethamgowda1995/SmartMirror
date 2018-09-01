import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.IN)
import time
while True:
	time.sleep(4)
	if GPIO.input(20)==1:
		value=1
	else:
		value=0
	with open("ldrdata.txt","w") as f:
			f.write(str(value))
	print(value)