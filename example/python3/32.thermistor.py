#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：thermistor.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX4）的第4位拨到ON上,
#       “如果不拨上去还会出现报错”，
#       做完实验之后，记得拨下来
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

# 初始化设置
def makerobo_setup():
	ADC.setup(0x48)  # 设置PCF8591模块地址

# 打印出温度传感器的提示信息
def makerobo_Print(x):
	if x == 1:  # 正合适
		print('')
		print('***********')
		print('* Better~ *')
		print('***********')
		print('')
	if x == 0:    # 太热
		print('')
		print('************')
		print('* Too Hot! *')
		print('************')
		print('')
		
# 循环函数
def makerobo_loop():
	makerobo_status = 1   # 状态值
	makerobo_tmp = 1      # 当前值
	while True:
		makerobo_analogVal = ADC.read(2)  # 读取AIN2上的模拟值
		makerobo_Vr = 5 * float(makerobo_analogVal) / 255
		makerobo_Rt = 10000 * makerobo_Vr / (5 - makerobo_Vr)
		makerobo_temp = 1/(((math.log(makerobo_Rt / 10000)) / 3950) + (1 / (273.15+25)))
		makerobo_temp = makerobo_temp - 273.15
		print('temperature = ', makerobo_temp, 'C')
		
		if makerobo_temp > 33:
			makerobo_tmp = 0
		elif makerobo_temp < 31:
			makerobo_tmp = 1

		if makerobo_tmp != makerobo_status: # 判断状态值发生改变
			makerobo_Print(makerobo_tmp)    # 打印出温度传感器的提示信息
			makerobo_status = makerobo_tmp  # 把当前状态值设置为比较状态值，避免重复打印；

		time.sleep(0.2)        # 延时 200ms

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() #初始化程序
		makerobo_loop()  #循环函数
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		pass	