import Adafruit_DHT
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    sensor = Adafruit_DHT.DHT11  # 传感器类型，可以改为DHT22或其他传感器
    pin = 17  # 连接到树莓派的GPIO引脚号

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        data = {
            'temperature': temperature,
            'humidity': humidity
        }
        return jsonify(data)
    else:
        return '无法获取传感器数据'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)