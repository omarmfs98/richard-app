#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import subprocess
import requests
import json
import datetime
import time
import sys

continue_reading = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

# Capture SIGINT for cleanup when the script is aborted

def end_read(signal, frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT

signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522

MIFAREReader = MFRC522.MFRC522()

# Welcome message

print 'Por favor pase la tarjeta por el lector'

# This loop keeps checking for chips. If one is near it will get the UID and authenticate

while continue_reading:
    input_state = GPIO.input(3)
    if input_state == False:
        time.sleep(0.3)
        subprocess.Popen(['python', 'RegisterCard.py'])
        sys.exit()
	# Scan for cards
	(status, TagType) = \
	      MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	# If a card is found
	if status == MIFAREReader.MI_OK:
		print 'Card detected'
		# Get the UID of the card

		(status, uid) = MIFAREReader.MFRC522_Anticoll()

		# If we have the UID, continue

		if status == MIFAREReader.MI_OK:

			# Print UID

		        print 'Card read UID: %s,%s,%s,%s' % (uid[0], uid[1], uid[2],
		                uid[3])

		        # This is the default key for authentication

		        key = [
		            0xFF,
		            0xFF,
		            0xFF,
		            0xFF,
		            0xFF,
		            0xFF,
		            ]

		        # Select the scanned tag

		        MIFAREReader.MFRC522_SelectTag(uid)

		        # Authenticate

		        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A,
		                8, key, uid)

		        # Check if authenticated

		        if status == MIFAREReader.MI_OK:
		            MIFAREReader.MFRC522_Read(8)
		            MIFAREReader.MFRC522_StopCrypto1()
		            dataEmployee = {'query': str(uid[0]) + str(uid[1]) \
		                            + str(uid[2]) + str(uid[3])}
		            res = requests.post(url='https://ratboy.me/api/findQR',
		                                data=dataEmployee,
		                                headers={'X-Requested-With': 'XMLHttpRequest'
		                            })
		            js = json.loads(res.text)

		            if js['success']:
		                if js['data']['code'] == 1:
		                    print 'Bienvenido(a): ' + js['data']['user']['first_name']
		                    print "Registrando..."

		                    subprocess.call('/home/pi/richard-app/takePhoto.sh', shell=True)
		                    file = open('/home/pi/Pictures/employee.jpg', 'rb')
		                    files = {'photo_employee': file}
		                    data = { 'employee_id': js['data']['id'] }
		                    res = requests.post(url='https://ratboy.me/api/employee_incomes',
		                                        data=data,
		                                        files=files,
		                                        headers={'X-Requested-With': 'XMLHttpRequest'
		                                    })
		                    js_income = json.loads(res.text)
		                    print 'REGISTRO EXITOSO'
		                    print 'Hora de entrada: ' + js_income['data']['created_at']
		                if js['data']['code'] == 2:
		                    print 'Hola ' + js['data']['user']['first_name']
		                    print "Actualizando fecha de salida..."

		                    subprocess.call('/home/pi/richard-app/takePhoto.sh', shell=True)
		                    file = open('/home/pi/Pictures/employee.jpg', 'rb')
		                    files = {'photo_employee_exit': file}
		                    data = { 'employee_id': js['data']['id'] }
		                    res = requests.post(url='https://ratboy.me/api/employee_incomes/' + str(js['data']['employee_income_id']),
		                                        data=data,
		                                        files=files,
		                                        headers={'X-Requested-With': 'XMLHttpRequest'
		                                    })
		                    js_income = json.loads(res.text)
		                    print 'Hora de salida: ' + js_income['data']['created_at']
		                    print 'Nos vemos mañana!'
		                if js['data']['code'] == 3:
		                    print js['message']
		            else:
		                print "[ALERTA]: " + js['message']
		            print '\n' + '\n' + 'Por favor pase la tarjeta por el lector'
		        else:
		            print 'Authentication error'
		            print '\n' + '\n' + 'Por favor pase la tarjeta por el lector'
