#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：13.tnt_detector.py
#  版本：V2.0
#  author: zhulin
# 说明：TNT 炸弹检测器，检测到炸弹后驱动
# 蜂鸣器鸣叫
#------------------------------------------
import RPi.GPIO as GPIO
import time
from mcpi.minecraft import Minecraft

# 建立一个Minecraft对象
CreatePi_mc = Minecraft.create() 

CreatePi_buzzer_pin = 12 # 定义蜂鸣器管脚PIN12

GPIO.setmode(GPIO.BOARD) # 设置GPIO口模式为BOARD模式
GPIO.setup(CreatePi_buzzer_pin, GPIO.OUT) # 设置蜂鸣器为输出模式

# 程序入口
if __name__ == "__main__":
    try:
        #无限循环下列代码
        while True:
            # 获取当前角色的坐标位置
            x, y, z = CreatePi_mc.player.getPos()
            # 逐一对比每块是否为TNT
            for i in range(15):
                if CreatePi_mc.getBlock(x, y - i, z) == 46:
                    GPIO.output(CreatePi_buzzer_pin, True) # 打开蜂鸣器
                    time.sleep(0.5) # 延时0.5s
                    GPIO.output(CreatePi_buzzer_pin, False) # 关闭蜂鸣器
                    time.sleep(0.5) # 延时0.5s
    except KeyboardInterrupt:
        # 按下 CTRL+C 键, 清除并退出脚本
        GPIO.cleanup()