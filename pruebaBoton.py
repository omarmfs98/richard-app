import RPi.GPIO as GPIO
import time
import sys
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

reading = True

while True:
	input_state = GPIO.input(24)
	if input_state == False:
		reading = not reading
	if reading:
		process1 = subprocess.Popen(['python', 'Read.py'])
	else:
		process1 = subprocess.Popen(['python', 'RegisterCard.py'])
