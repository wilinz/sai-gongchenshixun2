#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：12.house.py
#  版本：V2.0
#  author: zhulin
#  说明：建筑房子案例
#------------------------------------------
from mcpi.minecraft import Minecraft
import time

# 建立一个Minecraft对象
CreatePi_mc = Minecraft.create() 

# 程序入口
if __name__ == "__main__":
    try:
        # 获取当前角色的位置
        x, y, z = CreatePi_mc.player.getPos()
        # 建筑方块整体
        CreatePi_mc.setBlocks(x + 2, y - 1, z + 2, x + 7, y + 3, z + 8, 5) 
        # 去掉窗户孔
        CreatePi_mc.setBlocks(x + 3, y, z + 3, x + 6, y + 2, z + 7, 0) 
        # 给们开孔
        CreatePi_mc.setBlocks(x + 2, y, z + 5, x + 2, y + 1, z + 5, 0) 
        # 创建窗户1
        CreatePi_mc.setBlocks(x + 4, y + 1, z + 8, x + 5, y + 1, z + 8, 102) 
        # 创建窗户2
        CreatePi_mc.setBlocks(x + 4, y + 1, z + 2, x + 5, y + 1, z + 2, 102) 
        # 创建窗户2
        CreatePi_mc.setBlocks(x + 7, y + 1, z + 4, x + 7, y + 1, z + 6, 102)
    except KeyboardInterrupt: # 按下 CTRL+C 键, 清除并退出脚本
        pass