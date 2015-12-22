# Copyright (C) 2015 Pierre-Henri Joubert
# Contact: pierrehenrijoubert@gmail.com

import time
import RPi.GPIO as GPIO


#
# API for LEDs and Buttons!
#

def set_led(pin, value):
	if value:
		GPIO.output(pin, GPIO.LOW)
	else:
		GPIO.output(pin, GPIO.HIGH)

def read_button(pin):
	return GPIO.input(pin)


#
# Animations
#

def anim_walk(ledpins, delay):
	for i in range(len(ledpins)):
		set_led(ledpins, False)
		set_led(ledpins[i], True)
		time.sleep(delay)
	set_led(ledpins, False)
	time.sleep(delay)

def blink_loop(ledpins, buttonpins):
	b1 = read_button(buttonpins[0])
	b2 = read_button(buttonpins[1])
	if b1:
		anim_walk(ledpins, 0.1)
	if b2:
		reversed_list = ledpins[::-1]
		anim_walk(reversed_list, 0.1)

def pwm_loop():
	p = GPIO.PWM(18, 50)
	p.start(0)
	while True:
		for dc in range(0, 101, 5):
			p.ChangeDutyCycle(dc)
			time.sleep(0.1)
		for dc in range(100, -1, -5):
			p.ChangeDutyCycle(dc)
			time.sleep(0.1)

#
# main loop!
#

def loop(ledpins, buttonpins):
	blink_loop(ledpins, buttonpins)
#
# configuration code below: 
#

def setup(ledpins, buttonpins):
	print "***"
	print "*** SETTING UP..."
	print "***"	
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	for pin in ledpins:
		print "  setting led pin", pin, "to output"
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
	for pin in buttonpins:
		print "  setting button pin", pin, "to output"
		GPIO.setup(pin, GPIO.IN) 
	print "***"
	print "*** SETUP DONE"
	print "***"

def exit(ledpins, buttonpins):
	print ""
	print "***"
	print "*** SHUTTING DOWN..."
	print "***"
	GPIO.cleanup()
	print "***"
	print "*** SHUTDOWN DONE"
	print "***"
		

def main():
	ledpins = [25, 24, 23, 18]
	buttonpins = [7, 8]
	
	setup(ledpins, buttonpins)

	try:
		while True:
			loop(ledpins, buttonpins)
	except KeyboardInterrupt:
		exit(ledpins, buttonpins)
	

main()

