# 自定义数据处理2：预测是否可以进行户外运动

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
data = pd.read_csv('merged_sensor_data.csv')

# 提取时间部分并转换为datetime格式
data['time'] = pd.to_datetime(data['timestamp']).dt.time

# 定义一个函数来判断是否适合户外运动
def is_outdoor_friendly(time):
    if pd.to_datetime('12:00:00').time() <= time <= pd.to_datetime('18:00:00').time():
        return False
    else:
        return True

# 应用函数并添加新列
data['is_outdoor_friendly'] = data['time'].apply(is_outdoor_friendly)

# 删除时间列和原始时间戳列
data = data.drop(columns=['timestamp', 'time', 'bmp_altitude'])

# 查看类分布
class_distribution = data['is_outdoor_friendly'].value_counts()
print("Class Distribution:")
print(class_distribution)

# 定义特征和标签
X = data.drop(columns=['is_outdoor_friendly'])
y = data['is_outdoor_friendly']

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True ,random_state=42)

# 定义并训练模型
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# 预测
y_pred = clf.predict(X_test)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# 查看特征重要性
feature_importances = pd.DataFrame(clf.feature_importances_, index=X.columns, columns=['importance']).sort_values('importance', ascending=False)
print("Feature Importances:")
print(feature_importances)

# 分类报告
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 交叉验证
cross_val_scores = cross_val_score(clf, X, y, cv=5)
print(f'Cross-Validation Scores: {cross_val_scores}')
print(f'Mean Cross-Validation Score: {cross_val_scores.mean()}')

# 显示预测结果
predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print("Predictions:")
print(predictions.head())
