# 自定义数据处理1：WebUi 实时监测传感器

#!/usr/bin/python3
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
from flask import Flask, Response, request, jsonify, render_template_string

# Flask app
app = Flask(__name__)

# DHT11 温湿度传感器管脚定义
DHT_PIN = 17

# 默认设备I2C地址
BH1750_DEVICE = 0x5c  # BH1750光传感器默认设备I2C地址

# 设置BH1750光传感器测量模式
ONE_TIME_HIGH_RES_MODE_1 = 0x20


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

    return {
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


# Web UI
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sensor Data</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { width: 80%; margin: 0 auto; padding: 20px; }
            h1 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
            th { background-color: #f4f4f4; }
            .interval-input { margin-top: 20px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>实时传感器数据</h1>
            <div class="interval-input">
                <label for="interval">刷新间隔（秒）：</label>
                <input type="number" id="interval" value="1" min="1">
                <button onclick="updateInterval()">更新间隔</button>
            </div>
            <table id="sensorData">
                <tr>
                    <th>传感器</th>
                    <th>数据</th>
                </tr>
                <tr><td>光敏电阻</td><td id="photoresistor">--</td></tr>
                <tr><td>BMP 温度 (°C)</td><td id="bmp_temp">--</td></tr>
                <tr><td>BMP 气压 (Pa)</td><td id="bmp_pressure">--</td></tr>
                <tr><td>BMP 海拔 (m)</td><td id="bmp_altitude">--</td></tr>
                <tr><td>DHT 温度 (°C)</td><td id="dht_temp">--</td></tr>
                <tr><td>DHT 湿度 (%)</td><td id="dht_humidity">--</td></tr>
                <tr><td>DS18B20 温度 (°C)</td><td id="ds18b20_temp">--</td></tr>
                <tr><td>热敏电阻 温度 (°C)</td><td id="thermistor_temp">--</td></tr>
                <tr><td>BH1750 光强 (lx)</td><td id="bh1750_light">--</td></tr>
            </table>
        </div>
        <script>
            var interval = document.getElementById('interval').value;
            var source = new EventSource('/sensor_data?interval=' + interval);

            source.addEventListener('message', function(e) {
                var data = JSON.parse(e.data);
                document.getElementById('photoresistor').innerText = data.photoresistor + ' units';
                document.getElementById('bmp_temp').innerText = data.bmp_temp + ' °C';
                document.getElementById('bmp_pressure').innerText = data.bmp_pressure + ' Pa';
                document.getElementById('bmp_altitude').innerText = data.bmp_altitude + ' m';
                document.getElementById('dht_temp').innerText = data.dht_temp + ' °C';
                document.getElementById('dht_humidity').innerText = data.dht_humidity + ' %';
                document.getElementById('ds18b20_temp').innerText = data.ds18b20_temp + ' °C';
                document.getElementById('thermistor_temp').innerText = data.thermistor_temp + ' °C';
                document.getElementById('bh1750_light').innerText = data.bh1750_light + ' lx';
            }, false);

            function updateInterval() {
                interval = document.getElementById('interval').value;
                source.close();
                source = new EventSource('/sensor_data?interval=' + interval);
                source.addEventListener('message', function(e) {
                    var data = JSON.parse(e.data);
                    document.getElementById('photoresistor').innerText = data.photoresistor + ' units';
                    document.getElementById('bmp_temp').innerText = data.bmp_temp + ' °C';
                    document.getElementById('bmp_pressure').innerText = data.bmp_pressure + ' Pa';
                    document.getElementById('bmp_altitude').innerText = data.bmp_altitude + ' m';
                    document.getElementById('dht_temp').innerText = data.dht_temp + ' °C';
                    document.getElementById('dht_humidity').innerText = data.dht_humidity + ' %';
                    document.getElementById('ds18b20_temp').innerText = data.ds18b20_temp + ' °C';
                    document.getElementById('thermistor_temp').innerText = data.thermistor_temp + ' °C';
                    document.getElementById('bh1750_light').innerText = data.bh1750_light + ' lx';
                }, false);
            }
        </script>
    </body>
    </html>
    ''')


# Main entry point
if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5000)
