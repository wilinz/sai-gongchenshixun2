import os
import pandas as pd

# 定义要合并的CSV文件所在的目录
input_directory = 'output-data'
output_file = 'merged_sensor_data.csv'

# 获取目录中所有的CSV文件
csv_files = [f for f in os.listdir(input_directory) if f.endswith('.csv')]

# 初始化一个空的数据框
merged_df = pd.DataFrame()

# 剔除极端数据的函数
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# 遍历所有的CSV文件，并将它们合并到一个数据框中
for csv_file in csv_files:
    file_path = os.path.join(input_directory, csv_file)
    df = pd.read_csv(file_path)
    # 剔除每个传感器数据的极端值
    df = remove_outliers(df, 'photoresistor')
    df = remove_outliers(df, 'bmp_temp')
    df = remove_outliers(df, 'bmp_pressure')
    df = remove_outliers(df, 'bmp_altitude')
    df = remove_outliers(df, 'dht_temp')
    df = remove_outliers(df, 'dht_humidity')
    df = remove_outliers(df, 'ds18b20_temp')
    df = remove_outliers(df, 'thermistor_temp')
    merged_df = pd.concat([merged_df, df])

# 将合并后的数据框写入到一个新的CSV文件中
merged_df.to_csv(output_file, index=False)

print(f'合并后的文件已保存到 {output_file}')
