#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：rotary_encoder.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX3）的第2,3,4位拨到ON上，
#       做完实验之后，记得拨下来
import RPi.GPIO as GPIO
import time

makerobo_RoAPin = 13    # 旋转编码器CLK管脚
makerobo_RoBPin = 15    # 旋转编码器DT管脚
makerobo_BtnPin = 29    # 旋转编码器SW管脚

makerobo_globalCounter = 0  # 计数器值

makerobo_flag = 0                # 是否发生旋转标志位
makerobo_Last_RoB_Status = 0     # DT 状态
makerobo_Current_RoB_Status = 0  # CLK 状态

# 初始化工作
def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)       # 采用实际的物理管脚给GPIO口
	GPIO.setwarnings(False)        # 忽略GPIO操作注意警告
	GPIO.setup(makerobo_RoAPin, GPIO.IN)    # 旋转编码器CLK管脚,设置为输入模式
	GPIO.setup(makerobo_RoBPin, GPIO.IN)    # 旋转编码器DT管脚,设置为输入模式
	GPIO.setup(makerobo_BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 设置makerobo_BtnPin管脚为输入模式，上拉至高电平(3.3V)
    # 初始化中断函数，当SW管脚为0，使能中断
	GPIO.add_event_detect(makerobo_BtnPin, GPIO.FALLING, callback=makerobo_btnISR)
	
# 旋转编码方向位判断函数
def makerobo_rotaryDeal():
	global makerobo_flag                   # 是否发生旋转标志位
	global makerobo_Last_RoB_Status
	global makerobo_Current_RoB_Status
	global makerobo_globalCounter         # 计数器值

	makerobo_Last_RoB_Status = GPIO.input(makerobo_RoBPin)

	while(not GPIO.input(makerobo_RoAPin)):       # 判断CLK管脚的电平变化来区分方向
		makerobo_Current_RoB_Status = GPIO.input(makerobo_RoBPin)
		makerobo_flag = 1    # 发生旋转标记
	if makerobo_flag == 1:   # 标记位为1 发生了旋转
		makerobo_flag = 0    # 复位标记位
		if (makerobo_Last_RoB_Status == 0) and (makerobo_Current_RoB_Status == 1):
			makerobo_globalCounter = makerobo_globalCounter + 1   # 逆时针方向，正
		if (makerobo_Last_RoB_Status == 1) and (makerobo_Current_RoB_Status == 0):
			makerobo_globalCounter = makerobo_globalCounter - 1   # 顺时针方向，负

# 中断函数，当SW管脚为0，使能中断
def makerobo_btnISR(chn):
	global makerobo_globalCounter
	makerobo_globalCounter = 0 # 给计数器赋0
	#print ('makerobo_globalCounter = %d' % makerobo_globalCounter)

# 循环函数
def makerobo_loop():
	global makerobo_globalCounter  
	makerobo_tmp = 0	# 当前状态判断

	while True:
		makerobo_rotaryDeal()      # 旋转编码方向位判断函数
		if makerobo_tmp != makerobo_globalCounter: # 判断状态值发生改变
			print ('makerobo_globalCounter = %d' % makerobo_globalCounter) # 打印出状态信息
			makerobo_tmp = makerobo_globalCounter    #  把当前状态赋值到下一个状态，避免重复打印

# 释放资源
def destroy():
	GPIO.cleanup()             # 释放资源

# 程序入口
if __name__ == '__main__':    
	makerobo_setup()    # 调用初始化工作
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()

