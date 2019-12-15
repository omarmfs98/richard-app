#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import subprocess
import requests
import json
import datetime

continue_reading = True


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
            dataEmployee = {'serial': str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])}
            res = requests.post(url='https://ratboy.me/api/rfidCodes',
                                data=dataEmployee,
                                headers={'X-Requested-With': 'XMLHttpRequest'
                            })
            js = json.loads(res.text)

            print "[ALERTA]: " + js['message']
            print '\n' + '\n' + 'Por favor pase la tarjeta por el lector'
        else:
            print 'Authentication error'
            print '\n' + '\n' + 'Por favor pase la tarjeta por el lector'