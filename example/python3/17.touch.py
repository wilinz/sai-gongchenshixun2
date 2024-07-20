#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：touch.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX3）的第1位拨到ON上，
#       做完实验之后，记得拨下来

import RPi.GPIO as GPIO

makerobo_TouchPin = 11   # 触摸传感器管脚PIN


makerobo_tmp = 0    #是否有触摸判断

# GPIO口定义
def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)       # 采用实际的物理管脚给GPIO口
	GPIO.setwarnings(False)        # 忽略GPIO操作注意警告
    # 设置makerobo_TouchPin管脚为输入模式，上拉至低电平(0V)
	GPIO.setup(makerobo_TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(makerobo_TouchPin,GPIO.OUT)
    # 打印函数，显示出是否有触摸
def makerobo_Print(x):
	global makerobo_tmp
	if x != makerobo_tmp:
		if x == 1:    #  发生触摸
			print ('*************************')
			print ('* Makerobo Have a touch *')
			print ('*************************')
		if x == 0:    # 没有发生触摸
			print ('*****************************')
			print ('* Makerobo No touch occurred*')
			print ('*****************************')

		makerobo_tmp = x  # 触摸状态值保存和下次做比较，避免重复打印

# 循环函数
def makerobo_loop():
	while True:  # 无限循环
		makerobo_Print(GPIO.input(makerobo_TouchPin))  # 调用打印函数，显示出是否有触摸

# 资源释放函数
def destroy():
	GPIO.cleanup()                     # 释放资源

# 程序入口
if __name__ == '__main__':
	makerobo_setup()  # GPIO口定义
	try:
		makerobo_loop() # 循环函数
	except KeyboardInterrupt:   # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy() # 资源释放函数