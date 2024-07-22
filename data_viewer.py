# 数据可视化代码

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('merged_sensor_data.csv', parse_dates=['timestamp'])

# 设置图表的尺寸
plt.figure(figsize=(12, 10))

# 绘制每个传感器数据的趋势图
plt.subplot(3, 3, 1)
plt.plot(data['timestamp'], data['photoresistor'], label='Photoresistor', color='blue')
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.title('Photoresistor')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 2)
plt.plot(data['timestamp'], data['bmp_temp'], label='BMP Temperature', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('BMP Temperature')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 3)
plt.plot(data['timestamp'], data['bmp_pressure'], label='BMP Pressure', color='red')
plt.xlabel('Timestamp')
plt.ylabel('Pressure (Pa)')
plt.title('BMP Pressure')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 4)
plt.plot(data['timestamp'], data['bmp_altitude'], label='BMP Altitude', color='purple')
plt.xlabel('Timestamp')
plt.ylabel('Altitude (m)')
plt.title('BMP Altitude')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 5)
plt.plot(data['timestamp'], data['dht_temp'], label='DHT Temperature', color='orange')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('DHT Temperature')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 6)
plt.plot(data['timestamp'], data['dht_humidity'], label='DHT Humidity', color='cyan')
plt.xlabel('Timestamp')
plt.ylabel('Humidity (%)')
plt.title('DHT Humidity')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 7)
plt.plot(data['timestamp'], data['ds18b20_temp'], label='DS18B20 Temperature', color='brown')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('DS18B20 Temperature')
plt.legend()
plt.xticks(rotation=45)

plt.subplot(3, 3, 8)
plt.plot(data['timestamp'], data['thermistor_temp'], label='Thermistor Temperature', color='pink')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('Thermistor Temperature')
plt.legend()
plt.xticks(rotation=45)

# 调整子图间的间距
plt.tight_layout()

# 显示图表
plt.show()
