#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：14.nfc_block_writer.py
#  版本：V2.0
#  author: zhulin
# 说明：RFID写入Minecraft 游戏的块ID号
#------------------------------------------

import signal
import time
import minecraft_blocks as mcpi_data
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import sys


try:
    input = raw_input
except NameError:
    pass


RFID_run = True  # 运行标志位
CreatePi_rdr = SimpleMFRC522()  # 实例化一个RC522对象

# 捕获读取异常，并及时停止系统
def end_read(signal,frame):
    global RFID_run
    print("\nCtrl+C captured, ending read.")
    RFID_run = False
    GPIO.cleanup()  # 释放GPIO资源

# 异步系统事件
signal.signal(signal.SIGINT, end_read)

print("Write RFID Starting")

# 第一步，等待RFID标签卡放在读卡区域。
print('Write the Minecraft block to the RFID tag card')
print('')
print('==================== STEP 1 =========================')
print('Please place the RFID card to be written on the RFID card reading area...')

while RFID_run:
    id, text = CreatePi_rdr.read()    # 读取RFID标签卡的UID号
    print("[-] RFID Card read UID: "+str(id)) # 打印出RFID标签卡的UID号
    # 显示出提示信息
    print('===================================================================================') 
    print('WARNING: Do not immediately remove the RFID tag card until the reading is complete!')
    print('===================================================================================')
    print('')
    print('==================== STEP 2 =========================') # 第二步选择块类型写入到RFID标签中
    print('Now select a Minecraft game block type write card.')
    block_choice = None
    while block_choice is None:
        print('') # 输入L查Minecraft块ID号，或者直接输入块ID号的编号即可。
        print('Enter L for the Minecraft block ID, or enter the block ID directly.')
        print('') # 输入L查询或者直接的块ID号
        choice = input('Enter choice (L or block #): ')
        print('')
        # 如果输入的是l进行查询
        if choice.lower() == 'l':
            # 打印出块的ID号和名称
            print('Number\tBlock name')
            print('------\t----------')
            for i, b in enumerate(mcpi_data.BLOCKS): # 循环查询打印出块名称和ID号
                block_name, block_id = b
                print('{0:>6}\t{1}'.format(i, block_name))
        else:
            # 如果输入的是直接的块ID号
            try:
                block_choice = int(choice)
            except ValueError:
                # 如果输入的不是数字，而是其他字符弹出错误信息进行说明
                print('Error!Please enter the specific number or L query.')
                continue
                # 检测输入的数字是在块的ID号之内
            if not (0 <= block_choice < len(mcpi_data.BLOCKS)):
                print('Error! Block number must be within 0 to {0}.'.format(len(mcpi_data.BLOCKS)-1))
                continue
    # 块ID号已被选中，请查找其他名称和ID号
    block_name, block_id = mcpi_data.BLOCKS[block_choice]
    print('You chose the block type: {0}'.format(block_name))
    print('')

    # 获取块类型的子类型（如果有子类型的话）
    subtype_choice = None
    if block_name in mcpi_data.SUBTYPES:
        print('Now set the subtype of the block type.') # 输入块类型的子类型
        print('')
        print('Number\tSubtype')
        print('------\t-------')
        # 打印此块的所有子类型。
        block_subtypes = mcpi_data.SUBTYPES[block_name]
        for subtype_id, subtype_name in block_subtypes.items():
            print('{0:>6}\t{1}'.format(subtype_id, subtype_name))
        # 从输入直接获取子类型
        while subtype_choice is None:
            print('')
            try:
                subtype_choice = int(input('Enter subtype number: ')) # 请输入子类型的数字
            except ValueError:
                # 输入的不是数字，而是其他无法识别的字符，请再试一次！
                print('Error!Not a number but something else please try again!.')
                continue
            if subtype_id not in block_subtypes:
                print('Error! Subtype number must be one shown above!')
                continue
    if subtype_choice is not None:
        print('You also chose the subtype: {0}'.format(block_subtypes[subtype_choice]))
        print('')

    # 确认写入块的类型.
    print('==================== STEP 3 =========================')
    print('Confirm you are ready to write to the card:')  # 确认写入到卡的块类型
    print('Block: {0}'.format(block_name))                # 并进行打印
    if subtype_choice is not None:                        # 打印出子类型
        print('Subtype: {0}'.format(block_subtypes[subtype_choice]))
    print('')
    choice = input('Confirm card write (Y or N)? ')       # 确认是否写入
    if choice.lower() != 'y' and choice.lower() != 'yes': # 如果输入的不是y或者yes，则说明放弃写入
        print('Abort write!')                             # 放弃写入
        sys.exit(0)                                       # 退出系统
    # 写卡进行中……
    print('Card writing in progress...Please do not remove the card.')

        # 接下来构建要写入卡的数据。
        # 格式如下:
        # - 0-3字节是一个带有ASCII值'MCPI'的头
        # - 第4字节是块ID字节
        # - 如果块没有子类型，第5字节为0;如果块有子类型，第1字节为1
        # - 字节6是子类型Byte(可选，仅当字节5是1时)

    Block_data = bytearray(16)
    Block_data[0:4] = b'MCPI'  # 格式头 'MCPI'
    Block_data[4]   = block_id & 0xFF

    if subtype_choice is not None:
        Block_data[5] = 1
        Block_data[6] = subtype_choice & 0xFF

    # 写入RDIF卡中……
    CreatePi_rdr.write("MCPI"+str(Block_data[4])+str(Block_data[5])+str(Block_data[6]))

    id, Block_data = CreatePi_rdr.read()  #打印出回显信息进行确定写入成功
    # 发现一个卡片，现在尝试读取第4块以检测块类型。
    print("[-] RFID Card read UID: "+str(id)) #打印出RFID卡的UID号
    print(Block_data) #打印出数据
    print('You can now remove the card from the RC522 read card area..') # 提示写入成功，可以移除卡片
    RFID_run = False