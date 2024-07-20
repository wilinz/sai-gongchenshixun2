#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：vibration.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX2）的第1位拨到ON上，
#       做完实验之后，记得拨下来

# 导入树莓Pi GPIO库
import RPi.GPIO as GPIO
# 从time模块导入sleep函数
from time import sleep

# 定义振动传感器管脚
makerobo_vibration_pin = 13

# 暂时忽略警告
GPIO.setwarnings(False)
# 将board模式设置为GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# 设置振动管脚为输出模式,并将初始值设置为LOW（关闭）
GPIO.setup(makerobo_vibration_pin, GPIO.OUT,initial=GPIO.LOW)

# 程序入口
if __name__ == "__main__":
    try:
        # 打开振动传感器
        GPIO.output(makerobo_vibration_pin, GPIO.HIGH)
        # 等待2S时间
        sleep(2)
        # 关闭震动传感器
        GPIO.output(makerobo_vibration_pin, GPIO.LOW)

    except KeyboardInterrupt:
        GPIO.cleanup() # 清空GPIO