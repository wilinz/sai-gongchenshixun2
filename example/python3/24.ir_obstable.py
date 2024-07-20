#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：ir_obstable.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX3）的第8位拨到ON上，
#       做完实验之后，记得拨下来

import RPi.GPIO as GPIO
import time

makerobo_TrackPin = 11 # 循迹传感器PIN管脚

#  初始化设置函数
def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)       # 采用实际的物理管脚给GPIO口
	GPIO.setwarnings(False)           # 忽略警告
	 # 设置makerobo_TrackPin管脚为输入模式，上拉至高电平(3.3V)
	GPIO.setup(makerobo_TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 循环函数
def makerobo_loop():
	while True:
		if GPIO.input(makerobo_TrackPin) == GPIO.LOW:  # 检测到白色线
			print ('Makerobo White line is detected')
		else:
			print ('...Makerobo Black line is detected') # 检测到黑色线
		
		time.sleep(0.2) # 延时200ms

# 释放资源
def destroy():
	GPIO.cleanup()                     # 释放资源

# 程序入口
if __name__ == '__main__':    
	makerobo_setup()       # 调用初始化程序
	try:
		makerobo_loop()    # 调用循环函数
	except KeyboardInterrupt:  #  当按下Ctrl+C时，将执行destroy()子程序。
		destroy()

