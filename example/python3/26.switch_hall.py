#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：switch_hall.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX1）的第6位拨到ON上，
#       做完实验之后，记得拨下来
import RPi.GPIO as GPIO

makerobo_HallPin = 35  # 模拟霍尔传感器管脚定义

# GPIO口定义
def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)       # 按物理管脚给GPIO编号
	GPIO.setup(makerobo_HallPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # 设置BtnPin模式为输入，上拉至高电平(3.3V)
	# 中断函数，当检测到磁性物体，调用makerobo_detect函数
	GPIO.add_event_detect(makerobo_HallPin, GPIO.BOTH, callback=makerobo_detect, bouncetime=200)

# 打印函数，显示出是否检测到磁性物质
def  makerobo_Print(x):
	if x == 0:
		print('*****************************************')
		print('*makerobo Detected magnetic materials   *')
		print('*****************************************')

# 中断函数，检测到磁性物质，响应中断函数
def makerobo_detect(chn):
	makerobo_Print(GPIO.input(makerobo_HallPin))

# 循环函数
def loop():
	while True:
		pass

def destroy():
	GPIO.cleanup()                     # 释放所有IO口资源

if __name__ == '__main__':     # 程序开始位置
	makerobo_setup()  # GPIO 初始化
	try:
		loop()
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行子程序destroy()。
		destroy()