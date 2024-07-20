#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：reed_switch.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX1）的第8位拨到ON上，
#       做完实验之后，记得拨下来
import time
import RPi.GPIO as GPIO

# 设置干簧管传感器IO口
makerobo_Reed_pin = 22

# GPIO口定义
def makerobo_setup():
    # 设置GPIO模式到GPIO
    GPIO.setmode(GPIO.BOARD)
    # 关闭GPIO警告提示
    GPIO.setwarnings(False)
    # 设置puin作为输入
    GPIO.setup(makerobo_Reed_pin, GPIO.IN)

# 程序入口
if __name__ == '__main__':
    try:
        makerobo_setup() # 初始化GPIO
        while True:
            # 没有磁铁靠近，输出高电平
            if GPIO.input(makerobo_Reed_pin):
                print("No Detected Magnetic Material!")
            else:#有磁铁靠近，输出低电平
                print("Detected Magnetic Material!")
                GPIO.setup(makerobo_Reed_pin,GPIO.OUT)
                GPIO.output(makerobo_Reed_pin,GPIO.HIGH)
                GPIO.setup(makerobo_Reed_pin, GPIO.IN)
            time.sleep(1)
    except KeyboardInterrupt:
        # 检测到CTRL+C，清除并退出脚本
        GPIO.cleanup()