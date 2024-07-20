#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：buzzer.py
#  版本：V2.0
#  author: zhulin
# 说明：有源蜂鸣器

# 导入树莓Pi GPIO库
import RPi.GPIO as GPIO
# 从time模块导入sleep函数
from time import sleep
# 暂时忽略警告
GPIO.setwarnings(False)
# 使用实际的PIN管脚编码
GPIO.setmode(GPIO.BOARD) 
# 设置蜂鸣器-引脚12作为输出
makerobo_buzzer=12

# 将蜂鸣器引脚设置为输出引脚，并将初始值设置为LOW（关闭）
GPIO.setup(makerobo_buzzer, GPIO.OUT, initial=GPIO.LOW) 

# 程序入口
if __name__ == "__main__":
    try:
        while True:
            GPIO.output(makerobo_buzzer,GPIO.HIGH)
            print ("Beep")
            sleep(0.5) # 延时0.5s
            GPIO.output(makerobo_buzzer,GPIO.LOW)
            print ("No Beep")
            sleep(0.5)
    except KeyboardInterrupt:
        # 按下 CTRL+C 键, 清除并退出脚本
        GPIO.cleanup()    
