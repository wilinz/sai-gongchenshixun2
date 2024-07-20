#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：dh11.py
#  版本：V2.0
#  author: zhulin
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX4）的第1位拨到ON上，
#       做完实验之后，记得拨下来
# 说明：在做这个项目的时候，要把指拨开关（BUTTON:UX4）的第3位拨到ON上，
#       做完实验之后，记得拨下来

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import csv
import datetime
# 初始化工作

import csv
import Adafruit_DHT
import time
import datetime
import RPi.GPIO as GPIO

makerobo_pin = 17  # DHT11 温湿度传感器管脚定义




#def write1(a,b,c):
 #   with open('data.csv', 'wb') as file:
  #      writer = csv.writer(file)
   #     writer.writerow([a,b,c])
        # Use writerows() not writerow()
    #file.close()



# GPIO口定义
def makerobo_setup():
	ADC.setup(0x48)      # 设置PCF8591模块地址
	global sensor
	sensor = Adafruit_DHT.DHT11
            # 延时1s

# 循环函数
def loop():
    makerobo_status = 1 # 状态值
    with open('data3_3.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["temperature", 'humidity','Photoresistor Value', 'time'])
        for i in range(36000):
            humidity,temperature = Adafruit_DHT.read_retry(sensor, makerobo_pin)
            now=datetime.datetime.now()
            photoresistor_value=ADC.read(1)
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}% photoresistor_value={2:0.1f}%'.format(temperature, humidity,photoresistor_value))
                writer.writerow([temperature,humidity,photoresistor_value,now])
                print('Yi Xie Ru')
            else:
                print('error! Failed to get reading. Try again!')
            time.sleep(1)
        print('done')


def destroy():
	GPIO.cleanup()                     # 释放资源

# 程序入口
if __name__ == '__main__':

	makerobo_setup()
	try:
		loop()
	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
		destroy()