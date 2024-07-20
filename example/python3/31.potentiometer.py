#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：potentiometer.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX4）的第2位拨到ON上，
#       做完实验之后，记得拨下来

import PCF8591 as ADC
import time

# 模块地址设置
def makerobo_setup():
	ADC.setup(0x48)  # 设置PCF8591模块地址

# 无限循环
def makerobo_loop():
	makerobo_status = 1 # 给状态变量赋1值
	while True:   # 无限循环
		print ('Potentiometer Value:', ADC.read(0)) # 获取AIN0上的值，读取电位器模拟量值；
		makerobo_Value = ADC.read(0)   # 打印出该值   
		makerobo_outvalue = map(makerobo_Value,0,255,120,255) # 通过map函数按比例缩放到一个具体的范围
		ADC.write(makerobo_outvalue)  # 控制AOUT输出电平控制LED灯
		time.sleep(0.2)               # 延时200ms
# 释放资源
def destroy():
	ADC.write(0) # 给AOUT 赋值 0，关闭LED显示

# 范围区域变换函数
def map(x, in_min, in_max, out_min, out_max):
        '''从一个范围区域转换到另一个范围区域'''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() # 初始化函数
		makerobo_loop()  # 无限循环
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy() # 释放资源
