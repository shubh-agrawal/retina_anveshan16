#!/usr/bin/env python

import RPi.GPIO as GPIO

def initBuzzer(buzzerPin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzerPin, GPIO.OUT)


def correctHeading(counter,buzzerPin):
    if abs(counter < 1000):
        GPIO.output(buzzerPin, GPIO.HIGH)
    elif abs(counter >= 1000) and abs(counter < 2000):
        GPIO.output(buzzerPin, GPIO.LOW)
    else:
	counter = 0


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.OUT)
    while True:

        GPIO.output(19,GPIO.HIGH)
#	if KeyboardInterrupt:	
#	    GPIO.cleanup()
