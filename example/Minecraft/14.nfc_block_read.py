#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：14.nfc_block_read.py
#  版本：V2.0
#  author: zhulin
# 说明：RFID读取Minecraft 游戏的块ID号
#------------------------------------------

import binascii
import socket
import time
import signal
import sys
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import mcpi.minecraft as minecraft
import minecraft_blocks


RFID_run = True             # 运行标志位
CreatePi_rdr = SimpleMFRC522()  # 实例化一个RC522对象

# 捕获读取异常，并及时停止系统
def end_read(signal,frame):
    global RFID_run
    print("\nCtrl+C captured, ending read.")
    RFID_run = False
    GPIO.cleanup() # 释放GPIO资源

# 异步系统事件
signal.signal(signal.SIGINT, end_read)

print("read RFID Starting")  # 开始读卡


# 定义延时函数参数，以减少读取的频率
Minecraft_MAX_UPDATE_SEC = 0.5

# 创建块函数
# 在运行Minecraft游戏，可以指定ID号，子类型可选，
# 如果没有子类型默认为None.
def Minecraft_create_block(mc, block_id, subtype=None):
    # 获取角色的位置和姿态位置
    ptx, pty, ptz = mc.player.getTilePos()
    px, py, pz = mc.player.getPos()
    # 在角色的当前位置上创建块
    if subtype is None:
        mc.setBlock(ptx, pty, ptz, block_id)
    else:
        mc.setBlock(ptx, pty, ptz, block_id, subtype)
    # 把角色的位置往上移动一个空间，以留出块的生成模块
    mc.player.setPos(px, py+1, pz)


# 在没有运行Minecraft游戏之前，我们先读取卡数据并进行解析
mc = None

print('Detecting the existence of RFID card')
print('')
print('Wait for the RFID card to be placed in the card reading area...')

while RFID_run:
    id, RFID_data = CreatePi_rdr.read() #读取卡
    # 读取到卡，打印出读取到的卡的ID号
    print("[-] Card read UID: "+str(id))
    print(RFID_data)  # 打印读取到卡的数据信息
    # 打印出读卡失败信息
    if RFID_data is None:
        print('Card reading failed!')
        continue

    # 通过检查标题'MCPI'关键字来识别是否为生成块数据……
    if not 'MCPI' in RFID_data:  # 打印出提示信息，表明读取的数据格式不正确
        print('The read card data format is incorrect!')
        continue

    # 解析出数据中，卡的类型和子类型     
    date_len=0
    for i in range(1,len(RFID_data)):
        if not str(RFID_data[i]) == ' ':
            date_len=date_len+1
    print(date_len)
    if date_len == 7:
        block_id_L = int(RFID_data[4])
        block_id_H = int(RFID_data[5])
        block_id = block_id_L*10+block_id_H
        has_subtype = int(RFID_data[6])
        subtype_id =  int(RFID_data[7])
    if date_len == 6:
        block_id = int(RFID_data[4])
        has_subtype = int(RFID_data[5])
        subtype_id =  int(RFID_data[6])        
    # 找到块名
    for block in minecraft_blocks.BLOCKS:
        if block[1] == block_id:
            block_name = block[0]
            break
    print('RFID Found block!')
    print('Type: {0}'.format(block_name))

    if has_subtype:
        subtype_name = minecraft_blocks.SUBTYPES[block_name][subtype_id]
        print('Subtype: {0}'.format(subtype_name))

    # 在Minecraft游戏中创建块模块
    # 检查是否运行了Minecraft游戏
    try:
        if mc is None:
            mc = minecraft.Minecraft.create()
        Minecraft_create_block(mc,block_id, subtype_id if has_subtype else None)
        time.sleep(Minecraft_MAX_UPDATE_SEC)
    except socket.error:
        # 通讯错误，没有运行Minecraft游戏
        print('Minecraft game is not running, please run minecraft game first and try again!')
        time.sleep(1)
        continue
