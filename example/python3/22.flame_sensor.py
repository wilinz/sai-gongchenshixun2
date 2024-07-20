#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：flame_sensor.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX1）的第5位拨到ON上，
#       做完实验之后，记得拨下来
import RPi.GPIO as GPIO
import time
import math

makerobo_DO = 33  # 火焰传感器数字IO口
# 将board模式设置为GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# 初始化工作
def makerobo_setup():
	GPIO.setup(makerobo_DO, GPIO.IN) # 设置火焰传感器数字IO口为输入模式

# 打印信息，打印出火焰传感器的状态值
def makerobo_Print(x):
	if x == 1:      # 安全
		print ('')
		print ('   *******************')
		print ('   *  Makerobo Safe~ *')
		print ('   *******************')
		print ('')
	if x == 0:     # 有火焰
		print ('')
		print ('   ******************')
		print ('   * Makerobo Fire! *')
		print ('   ******************')
		print ('')

# 循环函数
def makerobo_loop():
	makerobo_status = 1      # 状态值
	# 无限循环
	while True:
		# 读取火焰传感器数字IO口
		makerobo_tmp = GPIO.input(makerobo_DO)
		if makerobo_tmp != makerobo_status:     # 判断状态发生改变
			makerobo_Print(makerobo_tmp)        # 打印出火焰传感器的提示信息
			makerobo_status = makerobo_tmp               # 当前状态值作为下次状态值进行比较，避免重复打印
		
		time.sleep(0.2)                         # 延时200ms

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() # 初始化
		makerobo_loop()  # 循环函数
	except KeyboardInterrupt:
		pass	