import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 加载数据集
# train_data = pd.read_csv('/kaggle/input/guet-saI-for-2024/Weather_train.csv')
# test_data = pd.read_csv('/kaggle/input/guet-saI-for-2024/weather_test.csv')
# sample_submission = pd.read_csv('/kaggle/input/guet-saI-for-2024/sample_submission.csv')

dir = "guet-saI-for-2024/"
train_data = pd.read_csv(dir+'Weather_train.csv')
test_data = pd.read_csv(dir+'weather_test.csv')

# 显示训练数据的前几行
print(train_data.head())

# 数据集的基本信息
print(train_data.info())

# 描述性统计
print(train_data.describe())

# 检查缺失值
missing_values = train_data.isnull().sum()
print(missing_values[missing_values > 0])

# 用中位数填充数值列的缺失值，用众数填充分类列的缺失值
for column in train_data.columns:
    if train_data[column].dtype == 'object':
        train_data[column] = train_data[column].fillna(train_data[column].mode()[0])
    else:
        train_data[column] = train_data[column].fillna(train_data[column].median())

# 编码分类变量
label_encoders = {}
for column in train_data.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    train_data[column] = label_encoders[column].fit_transform(train_data[column])

# 分离特征和目标变量，删除 'id' 列
X_train = train_data.drop(columns=['RainTomorrow', 'id'])
y_train = train_data['RainTomorrow']

# 同样预处理测试数据
for column in test_data.columns:
    if test_data[column].dtype == 'object':
        test_data[column] = test_data[column].fillna(test_data[column].mode()[0])
    else:
        test_data[column] = test_data[column].fillna(test_data[column].median())

# 确保处理测试集中未见过的标签
for column in test_data.select_dtypes(include=['object']).columns:
    if column in label_encoders:
        le = label_encoders[column]
        test_data[column] = test_data[column].map(lambda s: 'other' if s not in le.classes_ else s)
        le.classes_ = np.append(le.classes_, 'other')
        test_data[column] = le.transform(test_data[column])

# 删除测试数据中的 'id' 列
X_test = test_data.drop(columns=['id'])

# 将训练数据拆分为训练集和验证集
X_train_split, X_val, y_train_split, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# 训练逻辑回归模型
model = LogisticRegression(max_iter=2000)
model.fit(X_train_split, y_train_split)

# 在验证集上进行预测
y_val_pred = model.predict(X_val)

# 评估模型
accuracy = accuracy_score(y_val, y_val_pred)
print(f'验证集准确率: {accuracy:.2f}')

# 在测试数据上进行预测
test_data['RainTomorrow'] = model.predict(X_test)

# 准备提交文件
submission = test_data[['id', 'RainTomorrow']].copy()
submission.loc[:, 'RainTomorrow'] = submission['RainTomorrow'].astype(int)  # 确保预测结果为整数类型
submission['RainTomorrow'] = submission['RainTomorrow'].astype(str).map({'1': 'Yes', '0': 'No'})
submission.to_csv('submission.csv', index=False)
