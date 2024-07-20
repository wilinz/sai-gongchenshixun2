#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：blinking_led.py
#  版本：V2.0
#  author: zhulin
# 说明：LED灯显示实验
#------------------------------------------

#导入树莓Pi GPIO库
import RPi.GPIO as GPIO
#从time模块导入sleep函数
from time import sleep

# 定义 LED 引脚
makerobo_led_pin = 31

#暂时忽略警告
GPIO.setwarnings(False)
# 使用实际的PIN管脚编码
GPIO.setmode(GPIO.BOARD)
# 将LED引脚设置为输出引脚，并将初始值设置为低（关闭）
GPIO.setup(makerobo_led_pin, GPIO.OUT, initial=GPIO.LOW)

# 程序入口
if __name__ == "__main__":
    try:
        while True: # 无限循环
            GPIO.output(makerobo_led_pin, GPIO.HIGH) # 打开
            sleep(0.5) # 延时1s
            GPIO.output(makerobo_led_pin, GPIO.LOW) # 关闭
            sleep(0.5) # 延时1s
    except KeyboardInterrupt:
        # 按下 CTRL+C 键, 清除并退出脚本
        GPIO.cleanup()