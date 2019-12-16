import RPi.GPIO as GPIO
import time
import sys
import subprocess
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

while True:
	input_state = GPIO.input(3)
	if input_state == False:
		print 'Boton pulsado'
		time.sleep(0.3)
		os.system('lxterminal -e /usr/bin/python /home/pi/richard-app/Read.py')
		sys.exit()

