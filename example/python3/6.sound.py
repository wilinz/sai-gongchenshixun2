#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：sound.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX3）的第6位拨到ON上，
#       做完实验之后，记得拨下来

# 导入树莓Pi GPIO库
import RPi.GPIO as GPIO
# 从time模块导入sleep函数
from time import sleep

# 定义声音传感器端口
makerobo_sound_pin = 18

# 暂时忽略警告
GPIO.setwarnings(False)
# 使用实际的PIN管脚编码
GPIO.setmode(GPIO.BOARD)

# 设置为输入脚,并设置为上拉为高电平（3.3V）
GPIO.setup(makerobo_sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 程序入口
if __name__ == "__main__":
    try:
        while True:
            # 检查是否检测到声音
            if(GPIO.input(makerobo_sound_pin)==GPIO.LOW):
                print('Makerobo Sound Detected!')
                sleep(0.1)
            else:
                print('Makerobo No Sound Detected!')
                sleep(0.1)
    except KeyboardInterrupt:
        # 检测到CTRL+C，清除并退出脚本
        GPIO.cleanup()