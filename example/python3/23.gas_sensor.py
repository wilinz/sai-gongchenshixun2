#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：gas_sensor.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX2）的第7位拨到ON上，
#       做完实验之后，记得拨下来
import RPi.GPIO as GPIO
import time
import math

makerobo_DO = 37                    # 烟雾传感器数字IO口
makerobo_Buzz = 12                  # 蜂鸣器数字IO口
GPIO.setmode(GPIO.BOARD)            # 管脚映射，采用BOARD编码
# 暂时忽略警告
GPIO.setwarnings(False)

# 初始化工作
def makerobo_setup():
	GPIO.setup	(makerobo_DO,GPIO.IN)    # 烟雾传感器数字IO口,设置为输入模式
	# 设置蜂鸣器为低电平，初始状态关闭蜂鸣器鸣叫
	GPIO.setup(makerobo_Buzz,GPIO.OUT,initial=GPIO.LOW) # 蜂鸣器数字IO口,设置为输出模式

# 打印信息，打印出是否检测到烟雾信息
def makerobo_Print(x):
	if x == 1:     # 安全
		print ('')
		print ('   ******************')
		print ('   * Makerobo Safe~ *')
		print ('   ******************')
		print ('')
	if x == 0:    # 检测到烟雾
		print ('')
		print ('   ************************')
		print ('   * Makerobo Danger Gas! *')
		print ('   ************************')
		print ('')

# 循环函数
def makerobo_loop():
	makerobo_status = 1   # 定义状态值变量
	makerobo_count = 0    # 定义计数器变量值
	while True:    # 无限循环		
		makerobo_tmp = GPIO.input(makerobo_DO)  # 读取GAS烟雾传感器数字IO口值
		if makerobo_tmp != makerobo_status:     # 判断状态发生改变
			makerobo_Print(makerobo_tmp)        # 打印函数，打印出烟雾传感器信息
			makerobo_status = makerobo_tmp      # 把当前状态值设置为比较状态值，避免重复打印；
		if makerobo_status == 0:                # 当检测到烟雾
			makerobo_count += 1                 # 计数器值累计
			# 高低电平交替变化，让蜂鸣器发声
			if makerobo_count % 2 == 0:         # 进行求余处理，一半为1，一半为0
				GPIO.output(makerobo_Buzz, 0)
			else:
				GPIO.output(makerobo_Buzz, 1)
		else:
			GPIO.output(makerobo_Buzz, 0)       # 设置蜂鸣器为高电平，初始状态关闭蜂鸣器鸣叫
			makerobo_count = 0                  # 计数器赋0
				
		time.sleep(0.2)                         # 延时200ms

# 资源释放函数
def destroy():
	GPIO.output(makerobo_Buzz, 0)   # 设置蜂鸣器为高电平，初始状态关闭蜂鸣器鸣叫
	GPIO.cleanup()         # 释放资源

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup()   # 初始化函数
		makerobo_loop()    # 循环函数
	except KeyboardInterrupt: # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()  #资源释放