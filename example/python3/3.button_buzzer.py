#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：button_buzzer.py
#  版本：V2.0
#  author: zhulin
# 说明：按下(key3:37)按键，触发蜂鸣器，
# 也可以使用其他按键：key1:22,key2:33,key4:35

# 导入树莓Pi GPIO库
import RPi.GPIO as GPIO
# 从time模块导入sleep函数
from time import sleep

# 配置按钮和蜂鸣器引脚
makerobo_button_pin = 37 # 按键
makerobo_buzzer_pin = 12 # 蜂鸣器

# 暂时忽略警告
GPIO.setwarnings(False)
# 使用实际的PIN管脚编码
GPIO.setmode(GPIO.BOARD)

# 设置按钮引脚按键管脚为输入和蜂鸣器引脚作为输出
GPIO.setup(makerobo_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 将蜂鸣器引脚设置为输出引脚，并将初始值设置为LOW（关闭）
GPIO.setup(makerobo_buzzer_pin, GPIO.OUT,initial=GPIO.LOW)

# 程序入口
if __name__ == "__main__":
    try:
        while True:
            # 检查按键是否按下
            if(GPIO.input(makerobo_button_pin) ==0):
                sleep(0.1) # 延时10ms
                if(GPIO.input(makerobo_button_pin) ==0):
                    # 打开蜂鸣器
                    GPIO.output(makerobo_buzzer_pin, GPIO.HIGH)
            else:
                # 没有按键按下, 关闭蜂鸣器
                GPIO.output(makerobo_buzzer_pin, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup() # 清空GPIO