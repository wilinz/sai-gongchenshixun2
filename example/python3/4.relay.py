#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：relay.py
#  版本：V2.0
#  author: zhulin
#  说明：直接运行即可，可以在继电器上接一些控制设备

# 导入树莓Pi GPIO库
import RPi.GPIO as GPIO
# 从time模块导入sleep函数
from time import sleep

# 定义继电器管脚
makerobo_relay_pin = 40

# 暂时忽略警告
GPIO.setwarnings(False)
# 设置GPIO模式作为 GPIO.BOARD
GPIO.setmode(GPIO.BOARD)
# 将蜂继电器引脚作为输出引脚，并将初始值设置为HIGH（关闭）
GPIO.setup(makerobo_relay_pin, GPIO.OUT,initial=GPIO.HIGH)

# 程序入口
if __name__ == "__main__":
    try:
        while True:
            # 打开继电器
            GPIO.output(makerobo_relay_pin, GPIO.LOW)
            # 等待0.5S时间
            sleep(0.5)
            # 关闭继电器
            GPIO.output(makerobo_relay_pin, GPIO.HIGH)
            # 等待0.5S时间
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup() # 清空GPIO


