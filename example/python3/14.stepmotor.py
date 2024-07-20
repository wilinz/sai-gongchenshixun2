#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：stepmotor.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX2）的第3,4,5,6位拨到ON上，
#       做完实验之后，记得拨下来

import RPi.GPIO as GPIO
from time import sleep

makerobo_motorPin = (29,31,33,35)     # 步进电机管脚PIN
makerobo_rolePerMinute =15            # 每分钟转数
makerobo_stepsPerRevolution = 2048    # 每转一圈的步数
makerobo_stepSpeed = (60/makerobo_rolePerMinute)/makerobo_stepsPerRevolution  # 每一步所用的时间

# 初始化设置
def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)  # 将GPIO模式设置为BOARD编号
    GPIO.setwarnings(False) # 忽略警告
    for i in makerobo_motorPin:
        GPIO.setup(i, GPIO.OUT) # 设置步进电机的所有管脚为输出模式

# 步进电机旋转
def makerobo_rotary(clb_direction):
    if(clb_direction == 'c'):
        for j in range(4):
            for i in range(4):
                GPIO.output(makerobo_motorPin[i],0x99>>j & (0x08>>i))
            sleep(makerobo_stepSpeed)

    elif(clb_direction == 'a'):
        for j in range(4):
            for i in range(4):
                GPIO.output(makerobo_motorPin[i],0x99<<j & (0x80>>i))
            sleep(makerobo_stepSpeed)

# 循环函数
def makerobo_loop():
    while True:
        clb_direction = input('Makerobo select motor direction a=anticlockwise, c=clockwise: ')
        if(clb_direction == 'c'):
            print('Makerobo motor running clockwise\n')       # 顺时针旋转
            break
        elif(clb_direction == 'a'):
            print('Makerobo motor running anti-clockwise\n')  # 逆时针旋转
            break
        else:
            print('Makerobo input error, please try again!') # 输入错误，再次输入
    while True:
        makerobo_rotary(clb_direction)       # 让步进电机旋转

# 释放资源
def destroy():
    for i in makerobo_motorPin:
        GPIO.output(i, GPIO.LOW) # 设置步进电机的所有管脚为输出模式
    #GPIO.cleanup() # 释放资源

# 程序入口
if __name__ == '__main__':
    makerobo_setup()   # 初始化设置函数
    try:
        makerobo_loop()  # 循环函数
    except KeyboardInterrupt:   # 当按下Ctrl+C时，将执行destroy()子程序。
        destroy()  # 资源释放