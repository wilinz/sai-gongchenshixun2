#!/usr/bin/python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：distance.py
#  版本：V2.0
#  author: zhulin
#  说明：超声波传感器模块项目，直接运行即可。
import RPi.GPIO as GPIO
import time

makerobo_TRIG = 36  # 超声波模块Tring控制管脚
makerobo_ECHO = 32  # 超声波模块Echo控制管脚

# 超声波模块初始化工作
def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)      # 采用实际的物理管脚给GPIO口
	GPIO.setwarnings(False)       # 忽略GPIO操作注意警告
	GPIO.setup(makerobo_TRIG, GPIO.OUT) # Tring设置为输出模式
	GPIO.setup(makerobo_ECHO, GPIO.IN)  # Echo设置为输入模式

# 超声波计算距离函数
def ur_disMeasure():

	GPIO.output(makerobo_TRIG, 0)  # 开始起始
	time.sleep(0.000002)           # 延时2us

	GPIO.output(makerobo_TRIG, 1)  # 超声波启动信号，延时10us
	time.sleep(0.00001)            # 发出超声波脉冲
	GPIO.output(makerobo_TRIG, 0)           # 设置为低电平

	
	while GPIO.input(makerobo_ECHO) == 0: # 等待回传信号
		us_a = 0
	us_time1 = time.time()                # 获取当前时间
	while GPIO.input(makerobo_ECHO) == 1: # 回传信号截止信息
		us_a = 1
	us_time2 = time.time()                # 获取当前时间

	us_during = us_time2 - us_time1          # 转换微秒级的时间

	# 声速在空气中的传播速度为340m/s, 超声波要经历一个发送信号和一个回波信息，
	# 计算公式如下所示：
	return us_during * 340 / 2 * 100        # 求出距离

# 循环函数
def makerobo_loop():
	while True:
		us_dis = ur_disMeasure()   # 获取超声波计算距离
		print (us_dis, 'cm')       # 打印超声波距离值
		print ('')
		time.sleep(0.3)            # 延时300ms 

# 资源释放函数
def destroy():
	GPIO.cleanup() # 释放资源

# 程序入口
if __name__ == "__main__":
	makerobo_setup() # 调用初始化函数
	try:
		makerobo_loop() # 调用循环函数
	except KeyboardInterrupt: # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy() # 释放资源
