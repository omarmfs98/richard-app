import RPi.GPIO as GPIO
import time 
import sys
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
	input_state = GPIO.input(24)
	if input_state == False:
		print 'Boton pulsado'
		time.sleep(0.3)
		process1 = subprocess.Popen(['python', 'Read.py'])
		sys.exit()
