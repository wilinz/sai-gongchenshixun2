#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：motion.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX3）的第5位拨到ON上，
#       做完实验之后，记得拨下来

# 导入树莓Pi GPIO库
import RPi.GPIO as GPIO
# 从time模块导入sleep函数
from time import sleep

# 定义 motion 传感器的管脚
makerobo_motion_pin = 16
# 暂时忽略警告
GPIO.setwarnings(False)
# 使用实际的PIN管脚编码
GPIO.setmode(GPIO.BOARD) 
# 设置管脚模式为输入模式,设置为上拉模式（+3.3V）
GPIO.setup(makerobo_motion_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# 程序入口
if __name__ == "__main__":
      try:
            while True:
                  if(GPIO.input(makerobo_motion_pin) == 0):
                        print("Makerobo Nothing moves ...")  # 没有检测到移动的物体；
                  elif(GPIO.input(makerobo_motion_pin) == 1):
                        print("Makerobo Motion detected!")  # 有检测到移动的物体；
                  sleep(0.1)
      except KeyboardInterrupt:
            # 检测到CTRL+C，清除并退出脚本
            GPIO.cleanup()