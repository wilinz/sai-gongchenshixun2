# 舒适度分析代码

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('merged_sensor_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 定义时段
time_intervals = [
    ('2024-07-21 18:00:00', '2024-07-22 02:00:00'),
    ('2024-07-22 02:00:00', '2024-07-22 10:00:00'),
    ('2024-07-22 10:00:00', '2024-07-22 18:00:00')
]

# 定义舒适区间
comfort_temp_range = (28.5, 32.5)
comfort_humidity_range = (40, 70)


# 计算每小时的舒适性
def calculate_comfort_rate(data):
    comfort_hours = 0
    total_hours = len(data['timestamp'].dt.hour.unique())  # 计算总的小时数

    hourly_data = data.groupby(data['timestamp'].dt.hour)  # 按小时分组数据
    hourly_comfort = {}
    for hour, group in hourly_data:
        # 计算温度在舒适范围内的比例
        temp_in_range = group['thermistor_temp'].between(comfort_temp_range[0], comfort_temp_range[1]).mean()
        # 计算湿度在舒适范围内的比例
        humidity_in_range = group['dht_humidity'].between(comfort_humidity_range[0], comfort_humidity_range[1]).mean()

        # 判断是否在该小时内温度和湿度都在舒适范围内
        is_comfortable = temp_in_range > 0.5 and humidity_in_range > 0.5
        hourly_comfort[hour] = is_comfortable

        if is_comfortable:
            comfort_hours += 1  # 如果该小时内温度和湿度都在舒适范围内，则舒适小时数加1

    # 计算舒适率
    comfort_rate = (comfort_hours / total_hours) * 100
    return comfort_rate, hourly_comfort  # 返回舒适率和每小时的舒适状态



# 绘制每分钟温湿度变化
fig, axs = plt.subplots(6, 1, figsize=(12, 24))

comfort_rates = []
hourly_comforts = []
for i, (start, end) in enumerate(time_intervals):
    period_data = df[(df['timestamp'] >= start) & (df['timestamp'] < end)]

    axs[2 * i].plot(period_data['timestamp'], period_data['thermistor_temp'], label='Temperature (°C)', color='orange')
    axs[2 * i].set_title(f'Period {i + 1} Temperature: {start} to {end}')
    axs[2 * i].set_xlabel('Timestamp')
    axs[2 * i].set_ylabel('Temperature (°C)')
    axs[2 * i].legend()

    axs[2 * i + 1].plot(period_data['timestamp'], period_data['dht_humidity'], label='Humidity (%)', color='blue')
    axs[2 * i + 1].set_title(f'Period {i + 1} Humidity: {start} to {end}')
    axs[2 * i + 1].set_xlabel('Timestamp')
    axs[2 * i + 1].set_ylabel('Humidity (%)')
    axs[2 * i + 1].legend()

    comfort_rate, hourly_comfort = calculate_comfort_rate(period_data)
    comfort_rates.append(comfort_rate)
    hourly_comforts.append(hourly_comfort)

plt.tight_layout()
plt.show()

# 计算每日舒适率
df['date'] = df['timestamp'].dt.date
daily_comfort_rates = df.groupby('date').apply(lambda x: calculate_comfort_rate(x)[0])

# 输出结果
print("每个时段的舒适率：", comfort_rates)
print("每个时段每小时的舒适性：", hourly_comforts)
print("每日的舒适率：", daily_comfort_rates)
