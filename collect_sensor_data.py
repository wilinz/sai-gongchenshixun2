#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import csv
import datetime
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import os
import math

# DHT11 温湿度传感器管脚定义
DHT_PIN = 17
INTERVAL = 10  # 采集间隔，单位：秒

# 初始化各个传感器
def setup():
    ADC.setup(0x48)  # 设置PCF8591模块地址
    global bmp_sensor, dht_sensor, ds18b20_device
    bmp_sensor = BMP085.BMP085()  # 气压传感器
    dht_sensor = Adafruit_DHT.DHT11  # 温湿度传感器
    ds18b20_device = setup_ds18b20()  # DS18B20温度传感器

# 设置DS18B20温度传感器
def setup_ds18b20():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            return i

# 读取DS18B20温度值
def read_ds18b20():
    location = f'/sys/bus/w1/devices/{ds18b20_device}/w1_slave'
    with open(location) as tfile:
        text = tfile.read()
    temperature_data = text.split("\n")[1].split(" ")[9]
    temperature = float(temperature_data[2:]) / 1000
    return round(temperature, 2)

# 读取热敏电阻温度值
def read_thermistor():
    analog_val = ADC.read(2)
    vr = 5 * float(analog_val) / 255
    rt = 10000 * vr / (5 - vr)
    temperature = 1 / ((math.log(rt / 10000) / 3950) + (1 / (273.15 + 25))) - 273.15
    return round(temperature, 2)

# 读取数据并保存到CSV文件
def loop():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    directory = './output-data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f'{directory}/sensor_data_{timestamp}.csv'
    print(f"Write to {os.path.abspath(filename)}")

    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['timestamp', 'photoresistor', 'bmp_temp', 'bmp_pressure', 'bmp_altitude', 'dht_temp', 'dht_humidity',
             'ds18b20_temp', 'thermistor_temp'])

        rows_per_day = int(86400 / INTERVAL)
        estimated_size_per_row = 100  # 估计每行100字节
        estimated_file_size_kb = rows_per_day * estimated_size_per_row / 1024  # 以KB为单位
        estimated_file_size_mb = estimated_file_size_kb / 1024  # 以MB为单位

        print(f"Interval: {INTERVAL} seconds")
        print(f"Rows per day: {rows_per_day}")
        print(f"Estimated file size per day: {estimated_file_size_kb:.2f} KB ({estimated_file_size_mb:.2f} MB)")

        while True:
            start_time = time.time()  # 记录循环开始时间

            now = datetime.datetime.now()
            photoresistor = ADC.read(1)
            bmp_temp = round(bmp_sensor.read_temperature(), 2)
            bmp_pressure = bmp_sensor.read_pressure()
            bmp_altitude = round(bmp_sensor.read_altitude(), 2)
            dht_humidity, dht_temp = Adafruit_DHT.read_retry(dht_sensor, DHT_PIN)
            if dht_humidity is not None and dht_temp is not None:
                dht_humidity = round(dht_humidity, 2)
                dht_temp = round(dht_temp, 2)
            ds18b20_temp = read_ds18b20()
            thermistor_temp = read_thermistor()

            writer.writerow(
                [now, photoresistor, bmp_temp, bmp_pressure, bmp_altitude, dht_temp, dht_humidity, ds18b20_temp,
                 thermistor_temp])
            file.flush()  # 刷新文件缓冲区
            print(
                f'[{now}] Photoresistor: {photoresistor}, BMP Temp: {bmp_temp}, BMP Pressure: {bmp_pressure}, BMP Altitude: {bmp_altitude}, DHT Temp: {dht_temp}, DHT Humidity: {dht_humidity}, DS18B20 Temp: {ds18b20_temp}, Thermistor Temp: {thermistor_temp}')

            print(
                f'[{now}] 光敏电阻: {photoresistor}, BMP 温度: {bmp_temp}, BMP 气压: {bmp_pressure}, BMP 海拔: {bmp_altitude}, DHT 温度: {dht_temp}, DHT 湿度: {dht_humidity}, DS18B20 温度: {ds18b20_temp}, 热敏电阻 温度: {thermistor_temp}')

            end_time = time.time()  # 记录循环结束时间
            elapsed_time = end_time - start_time  # 计算本次循环的执行时间

            sleep_time = max(0, INTERVAL - elapsed_time)  # 确保休眠时间不为负数
            time.sleep(sleep_time)

# 释放资源
def destroy():
    GPIO.cleanup()

# 程序入口
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
