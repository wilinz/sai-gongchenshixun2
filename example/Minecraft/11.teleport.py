#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：11.teleport.py
#  版本：V2.0
#  author: zhulin
# 说明：红外避障传感器非接触传送玩家
#------------------------------------------
import RPi.GPIO as GPIO
from mcpi.minecraft import Minecraft
import time

# 建立一个Minecraft对象
CreatePi_mc = Minecraft.create()

# 红外避障传感器模块管脚定义
CreatePi_ObstaclePin = 11
# gpio模式设置为Gpio BOARD模式
GPIO.setmode(GPIO.BOARD)
# set as INPUT
# 将GPIO引脚设置为输入，同时设置为上拉
GPIO.setup(CreatePi_ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 程序入口
if __name__ == "__main__":
    try:
        while True:
            if GPIO.input(CreatePi_ObstaclePin) == 0: # 等待避障传感器检测到手
                CreatePi_mc.player.setPos(0, 0, 0) # 传送角色到起始位置
                print("Minecraft Teleported successfully!") # 打印提示信息
                time.sleep(0.5) # 暂停0.5s
    except KeyboardInterrupt:# 按下 CTRL+C 键, 清除并退出脚本
        GPIO.cleanup()
