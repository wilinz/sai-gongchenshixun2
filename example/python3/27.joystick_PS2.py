#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：joystick_PS2.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX4）的第5,6,7位拨到ON上，
#       做完实验之后，记得拨下来
#------------------------------------------------------
#		这个程序依赖于PCF8591 ADC芯片。
#------------------------------------------------------
import PCF8591 as ADC
import time

# 初始化
def makerobo_setup():
	ADC.setup(0x48)					# 设置 PCF8591 芯片的IIC地址
	global makerobo_state

# 方向判断函数
def makerobo_direction():	# 得到操纵杆结果
	state = ['home', 'up', 'down', 'left', 'right', 'pressed']  # 方向状态信息
	i = 0

	if ADC.read(0) <= 5:
		i = 3		# 左方向
	if ADC.read(0) >= 250:
		i = 4		# 右方向
	if ADC.read(1) >= 250:
		i = 1		# 上方向
	if ADC.read(1) <= 5:
		i = 2		# 下方向
	if ADC.read(2) == 0:
		i = 5		# 按钮按下

    # home位置
	if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15	and ADC.read(1) - 125 < 15 and ADC.read(1) - 125 > -15 and ADC.read(2) == 255:
		i = 0 #在中间
	return state[i] # 返回状态

# 循环函数
def makerobo_loop():
	makerobo_status = ''       # 状态值赋空值
	while True:
		makerobo_tmp = makerobo_direction()  # 调用方向判断函数
		if makerobo_tmp != None and makerobo_tmp != makerobo_status: # 判断状态是否发生改变
			print(makerobo_tmp)
			makerobo_status = makerobo_tmp  # 把当前状态赋给状态值，以防止同一状态多次打印

# 异常处理函数
def destroy():
	pass

if __name__ == '__main__':		# 程序从main开始
	makerobo_setup()  # 初始化
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt:  	# 当按下Ctrl+C时，将执行子程序destroy()。
		destroy()  # 调用释放函数