# info:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 101822 entries, 0 to 101821
# Data columns (total 24 columns):
#  #   Column         Non-Null Count   Dtype
# ---  ------         --------------   -----
#  0   id             101822 non-null  int64
#  1   Date           101822 non-null  object
#  2   Location       101822 non-null  object
#  3   MinTemp        100789 non-null  float64  # 最低气温
#  4   MaxTemp        100934 non-null  float64  # 最高气温
#  5   Rainfall       99578 non-null   float64  # 降雨量
#  6   Evaporation    58036 non-null   float64  # 蒸发量
#  7   Sunshine       53099 non-null   float64  # 日照时数
#  8   WindGustDir    94639 non-null   object   # 阵风风向
#  9   WindGustSpeed  94683 non-null   float64  # 阵风风速
#  10  WindDir9am     94409 non-null   object   # 上午9点的风向
#  11  WindDir3pm     98871 non-null   object   # 下午3点的风向
#  12  WindSpeed9am   100597 non-null  float64  # 上午9点的风速
#  13  WindSpeed3pm   99676 non-null   float64  # 下午3点的风速
#  14  Humidity9am    99958 non-null   float64  # 上午9点的湿度
#  15  Humidity3pm    98632 non-null   float64  # 下午3点的湿度
#  16  Pressure9am    91293 non-null   float64  # 上午9点的气压
#  17  Pressure3pm    91312 non-null   float64  # 下午3点的气压
#  18  Cloud9am       62803 non-null   float64  # 上午9点的云量
#  19  Cloud3pm       60347 non-null   float64  # 下午3点的云量
#  20  Temp9am        100577 non-null  float64  # 上午9点的温度
#  21  Temp3pm        99260 non-null   float64  # 下午3点的温度
#  22  RainToday      99578 non-null   object   # 今天是否下雨
#  23  RainTomorrow   99531 non-null   object   # 明天是否下雨

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score
from sklearnex import patch_sklearn
patch_sklearn()

dir = "guet-saI-for-2024/"
# 加载数据集
train_data = pd.read_csv(dir+'Weather_train.csv')
test_data = pd.read_csv(dir+'weather_test.csv')

# 解析日期列
train_data['Date'] = pd.to_datetime(train_data['Date'])
test_data['Date'] = pd.to_datetime(test_data['Date'])

# 提取日期相关的特征
train_data['Year'] = train_data['Date'].dt.year
train_data['Month'] = train_data['Date'].dt.month
train_data['Season'] = train_data['Month'] % 12 // 3 + 1

test_data['Year'] = test_data['Date'].dt.year
test_data['Month'] = test_data['Date'].dt.month
test_data['Season'] = test_data['Month'] % 12 // 3 + 1

# 删除 RainTomorrow 为 nan 的数据
train_data = train_data.dropna(subset=['RainToday','RainTomorrow'])

# 填充缺失值
for column in train_data.columns:
    if train_data[column].dtype == 'object':
        train_data[column] = train_data[column].fillna(train_data[column].mode()[0])
    else:
        train_data[column] = train_data[column].fillna(train_data[column].median())

for column in test_data.columns:
    if test_data[column].dtype == 'object':
        test_data[column] = test_data[column].fillna(test_data[column].mode()[0])
    else:
        test_data[column] = test_data[column].fillna(test_data[column].median())

# 编码分类变量
label_encoders = {}
for column in train_data.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    train_data[column] = label_encoders[column].fit_transform(train_data[column])

for column in test_data.select_dtypes(include=['object']).columns:
    if column in label_encoders:
        le = label_encoders[column]
        test_data[column] = test_data[column].map(lambda s: 'other' if s not in le.classes_ else s)
        le.classes_ = np.append(le.classes_, 'other')
        test_data[column] = le.transform(test_data[column])

# 分离特征和目标变量
X_train = train_data.drop(columns=['RainTomorrow', 'id', 'Date'])
y_train = train_data['RainTomorrow']

# 标准化数值特征
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# 删除测试数据中的 'id' 列
X_test = test_data.drop(columns=['id', 'Date'])
X_test = scaler.transform(X_test)

# 将训练数据拆分为训练集和验证集
X_train_split, X_val, y_train_split, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=60)

# 使用随机森林分类器和梯度提升分类器
rf_model = RandomForestClassifier(n_estimators=2000, random_state=60)
gb_model = GradientBoostingClassifier(n_estimators=2000, random_state=60)

# 使用投票分类器组合模型
voting_model = VotingClassifier(estimators=[('rf', rf_model), ('gb', gb_model)], voting='soft')

# 训练投票分类器
voting_model.fit(X_train_split, y_train_split)

# 在验证集上进行预测
y_val_pred = voting_model.predict(X_val)

# 评估模型
accuracy = accuracy_score(y_val, y_val_pred)
print(f'验证集准确率: {accuracy:.4f}')

# 在测试数据上进行预测
test_data['RainTomorrow'] = voting_model.predict(X_test)

# 准备提交文件
submission = test_data[['id', 'RainTomorrow']].copy()
submission['RainTomorrow'] = submission['RainTomorrow'].astype(int)
submission['RainTomorrow'] = submission['RainTomorrow'].map({1: 'Yes', 0: 'No'})
submission.to_csv('submission.csv', index=False)