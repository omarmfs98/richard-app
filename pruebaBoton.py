import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

reading = True

print "[MODO LECTURA]"
subprocess.Popen(['python', 'Read.py'])

while True:
	input_state = GPIO.input(24)
	if input_state == False:
		reading = not reading
	if reading:
		subprocess.Popen(['python', 'Read.py'])
	else:
		subprocess.Popen(['python', 'RegisterCard.py'])
