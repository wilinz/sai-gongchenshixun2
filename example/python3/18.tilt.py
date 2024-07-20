#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：tilt.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX2）的第2位拨到ON上，
#       做完实验之后，记得拨下来

import RPi.GPIO as GPIO
from time import sleep

makerobo_TiltPin =  15   #倾斜传感器Pin端口

# GPIO口定义
def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)           # 采用实际的物理管脚给GPIO口
	GPIO.setwarnings(False)            # 去除GPIO口警告
	GPIO.setup(makerobo_TiltPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # 设置makerobo_TiltPin管脚为输入模式，上拉至高电平(3.3V)
	# 中断函数，当发生倾斜时，调用makerobo_detect函数
#	GPIO.add_event_detect(makerobo_TiltPin, GPIO.BOTH, callback=makerobo_detect, bouncetime=200)

# 打印函数，显示出发生倾斜
def makerobo_Print(x):
    if x == 0:
        print('***************************************')
        print('********** "[-] Left Tilt"  ***********')
        print('***************************************')

    if x == 1:
        print('***************************************')
        print('********** "[-] Right Tilt"  **********')
        print('***************************************')

# 中断函数，发生倾斜时，响应中断函数
def makerobo_detect():
    makerobo_Print(GPIO.input(makerobo_TiltPin))       # 打印出倾斜传感器信息
    sleep(0.2)


# 循环函数
def makerobo_loop():
    while True:
        makerobo_detect()


def destroy():
	GPIO.cleanup()                     # 释放资源

# 程序入口
if __name__ == '__main__':
	makerobo_setup()           # 初始化GPIO资源
	try:
		makerobo_loop()        #  循环函数
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()