#!/usr/bin/env python

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
	print("Por favor pase su tarjeta por el lector...")
	id, text = reader.read()
	print("¡Hola!",text)
	print("ID:",id)

finally:
	GPIO.cleanup()
