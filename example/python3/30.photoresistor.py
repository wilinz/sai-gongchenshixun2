#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：photoresistor.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX4）的第3位拨到ON上，
#       做完实验之后，记得拨下来

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import csv
import datetime
# 初始化工作
def makerobo_setup():
	ADC.setup(0x48)      # 设置PCF8591模块地址

def makerobo_loop():
    makerobo_status = 1 # 状态值
    with open('data1_2_1.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Photoresistor Value', 'time'])
        for i in range(3600):
            now=datetime.datetime.now()
            print ('Photoresistor Value: ', ADC.read(1)) # 读取AIN1的值，获取光敏模拟量值	
            writer.writerow([ADC.read(1),now])
            time.sleep(1)                              # 延时200ms

# 程序入口
if __name__ == '__main__':
	try:
		makerobo_setup() # 地址设置
		makerobo_loop()  # 调用无限循环
	except KeyboardInterrupt:
		pass		