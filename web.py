#!/usr/bin/python3
import csv
import json
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import datetime
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import os
import math
import smbus
from flask import Flask, Response, request, jsonify, render_template, send_file

# Flask app
app = Flask(__name__)

# DHT11 温湿度传感器管脚定义
DHT_PIN = 17

# 默认设备I2C地址
BH1750_DEVICE = 0x5c  # BH1750光传感器默认设备I2C地址

# 设置BH1750光传感器测量模式
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# 用于保存传感器数据的列表
sensor_data_list = []

# 初始化各个传感器
def setup():
    ADC.setup(0x48)  # 设置PCF8591模块地址
    global bmp_sensor, dht_sensor, ds18b20_device, bus
    bmp_sensor = BMP085.BMP085()  # 气压传感器
    dht_sensor = Adafruit_DHT.DHT11  # 温湿度传感器
    ds18b20_device = setup_ds18b20()  # DS18B20温度传感器

    # 初始化I2C总线
    if (GPIO.RPI_REVISION == 1):
        bus = smbus.SMBus(0)
    else:
        bus = smbus.SMBus(1)


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


# 转换BH1750数据
def convertToNumber(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return result


# 读取BH1750光传感器数据
def read_bh1750(addr=BH1750_DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)


# 读取所有传感器数据
def read_sensors():
    photoresistor = ADC.read(1)
    bmp_temp = round(bmp_sensor.read_temperature(), 4)
    bmp_pressure = bmp_sensor.read_pressure()
    bmp_altitude = round(bmp_sensor.read_altitude(), 4)
    dht_humidity, dht_temp = Adafruit_DHT.read_retry(dht_sensor, DHT_PIN)
    if dht_humidity is not None and dht_temp is not None:
        dht_humidity = round(dht_humidity, 4)
        dht_temp = round(dht_temp, 4)
    ds18b20_temp = read_ds18b20()
    thermistor_temp = read_thermistor()
    bh1750_light = round(read_bh1750(), 4)

    data = {
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'photoresistor': photoresistor,
        'bmp_temp': bmp_temp,
        'bmp_pressure': bmp_pressure,
        'bmp_altitude': bmp_altitude,
        'dht_temp': dht_temp,
        'dht_humidity': dht_humidity,
        'ds18b20_temp': ds18b20_temp,
        'thermistor_temp': thermistor_temp,
        'bh1750_light': bh1750_light
    }
    sensor_data_list.append(data)
    return data


# http://192.168.137.69:5000/sensor_data?interval=1
# SSE endpoint
@app.route('/sensor_data')
def sensor_data():
    def generate(interval):
        while True:
            start_time = time.time()
            data = read_sensors()
            yield f"data: {json.dumps(data)}\n\n"
            elapsed_time = time.time() - start_time
            sleep_time = max(0, interval - elapsed_time)
            time.sleep(sleep_time)

    interval = request.args.get('interval', default=1, type=int)
    return Response(generate(interval), mimetype='text/event-stream')


# 导出传感器数据为CSV
@app.route('/export')
def export():
    keys = sensor_data_list[0].keys()
    with open('/tmp/sensor_data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(sensor_data_list)
    return send_file('/tmp/sensor_data.csv', as_attachment=True)


# Web UI
@app.route('/')
def index():
    return render_template('index.html')


# Main entry point
if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5000)
