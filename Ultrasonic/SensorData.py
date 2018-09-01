import RPi.GPIO as GPIO
import time
import pyautogui

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED=21
TRIG = 23
ECHO = 24
treshold=150
print("Distance Measurement in Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)



while True:

	GPIO.output(TRIG,False)

	print("Waiting For Sensor To Settle")

	time.sleep(2)

	GPIO.output(TRIG,True)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)


	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
	
	while GPIO.input(ECHO)==1:
		pulse_end = time.time()
	
	pulse_duration = pulse_end - pulse_start 

	distance = pulse_duration * 17150

	distance = round(distance,2)

	if distance >= treshold:
		GPIO.output(LED,GPIO.LOW)
	else:
		GPIO.output(LED,GPIO.HIGH)

	print("Distance: ",distance," cm")
	with open("Values.txt","w") as f:
		time.sleep(1)
		f.write(str(int(distance)))
	
	

GPIO.cleanup()
GPIO.output(LED,GPIO.LOW)
