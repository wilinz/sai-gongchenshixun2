#!/usr/bin/python3
# －－－－湖南创乐博智能科技有限公司－－－－
# 文件名：ircontrol.py
# 版本：V2.0
# autgor:zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX1）的第1,2,3位拨到ON
# 上，做完实验之后，记得拨下来。

import pylirc
import time
import RPi.GPIO as GPIO

Rpin = 13
Gpin = 15
Bpin = 29
blocking = 0;

Lv = [0, 20, 90] # Light Level
color = [0, 0, 0]

def setColor(color):
#	global p_R, p_G, p_B
	p_R.ChangeDutyCycle(100 - color[0])     # Change duty cycle
	p_G.ChangeDutyCycle(100 - color[1])
	p_B.ChangeDutyCycle(100 - color[2])

def setup():
	global p_R, p_G, p_B
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Rpin, GPIO.OUT)
	GPIO.setup(Gpin, GPIO.OUT)
	GPIO.setup(Bpin, GPIO.OUT)
	
	p_R = GPIO.PWM(Rpin, 2000) # Set Frequece to 2KHz
	p_G = GPIO.PWM(Gpin, 2000)
	p_B = GPIO.PWM(Bpin, 2000)
	
	p_R.start(100)
	p_G.start(100)
	p_B.start(100)
	pylirc.init("pylirc","/etc/lirc/conf",blocking)


def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def RGB(config):
	global color
	if config == 'KEY_CHANNELDOWN':
		color[0] = Lv[0]
		print ('Red OFF')

	if config == 'KEY_CHANNEL':
		color[0] = Lv[1]
		print ('Light Red')

	if config == 'KEY_CHANNELUP':
		color[0] = Lv[2]
		print ('Red')

	if config == 'KEY_PREVIOUS':
		color[1] = Lv[0]
		print ('Green OFF')

	if config == 'KEY_NEXT':
		color[1] = Lv[1]
		print ('Light Green')

	if config == 'KEY_PLAYPAUSE':
		color[1] = Lv[2]
		print ('Green')

	if config == 'KEY_VOLUMEDOWN':
		color[2] = Lv[0]
		print ('Blue OFF')

	if config == 'KEY_VOLUMEUP':
		color[2] = Lv[1]
		print ('Light Blue')

	if config == 'KEY_EQUAL':
		color[2] = Lv[2]
		print ('BLUE')

def loop():
	while True:
		s = pylirc.nextcode(1)
		
		while(s):
			for (code) in s:
				print ("Command: ", code["config"]) #For debug: Uncomment this
#				line to see the return value of buttons
				RGB(code["config"])
				setColor(color)
			if(not blocking):
				s = pylirc.nextcode()
			else:
				s = []

def destroy():
	p_R.stop()
	p_G.stop()
	p_B.stop()
	GPIO.output(Rpin, GPIO.HIGH)    # Turn off all leds
	GPIO.output(Gpin, GPIO.HIGH)
	GPIO.output(Bpin, GPIO.HIGH)
	GPIO.cleanup()
	pylirc.exit()

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()