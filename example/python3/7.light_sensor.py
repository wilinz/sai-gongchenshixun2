#!/usr/bin/python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：light_sensor.py
#  版本：V2.0
#  author: zhulin
#  说明：IIC总线，地址为0x5c

import RPi.GPIO as GPIO
import smbus
import time

# 默认设备I2C地址
DEVICE     = 0x5c # 默认设备I2C地址

POWER_DOWN = 0x00 # 关闭电源
POWER_ON   = 0x01 # 打开电源
RESET      = 0x07 # 复位数据寄存器值

# 以4lx分辨率开始测量。 时间通常为16ms。
CONTINUOUS_LOW_RES_MODE = 0x13
# 以1lx分辨率开始测量。 时间通常为120毫秒
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# 以0.5lx分辨率开始测量。 时间通常为120毫秒
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# 以1lx分辨率开始测量。 时间通常为120毫秒
# 测量后，设备自动设置为掉电。
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# 以0.5lx分辨率开始测量。 时间通常为120毫秒
# 测量后，设备自动设置为掉电。
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# 以1lx分辨率开始测量。 时间通常为120毫秒
# 测量后，设备自动设置为掉电。
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
#bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
 # 为IIC总线找到正确的设备
if(GPIO.RPI_REVISION == 1):
    bus = smbus.SMBus(0)
else:
    bus = smbus.SMBus(1)

# 转换成数字
def convertToNumber(data):
    # 简单的函数来转换2个字节的数据
    # 转换为十进制数。 可选参数“十进制”
    # 将四舍五入到指定的小数位数。
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

# 从I2C接口读取数据
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

# 定义主函数
def main():
  # 无限循环函数
  while True:
    lightLevel=readLight() # 读取亮度值
    print("BH1750 Light Level : " + format(lightLevel,'.2f') + " lx") # 打印出亮度值
    time.sleep(0.5) # 延时0.5s

# 程序入口
if __name__=="__main__":
    try:
        main()  # 调用主函数
    except KeyboardInterrupt: # 按下 CTRL+C 键, 清除并退出脚本
        GPIO.cleanup() # 清空GPIO