#可视化数据点
import pandas as pd
import numpy as np
df = pd.read_csv('OSMdata_process_positive_very_little.csv')

import matplotlib.pyplot as plt
#可视化数据
"""plt.figure(figsize=(10, 6))
plt.scatter(df['lon'], df['lat'], c='blue', s=1, alpha=0.5)  # c指定颜色，s指定点大小，alpha指定透明度
plt.title('Scatter plot of lat and lon')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

plt.show()"""

#from generate_query import GenerateUniformQuery,GenerateSkewedQuery
#测试query
"""
print(GenerateUniformQuery(df))
((q_xL,q_xU),(q_yL,q_yU)) = GenerateSkewedQuery(df)
print((q_xL,q_xU),(q_yL,q_yU))
print((q_xU + q_xL)/2,(q_yL+q_yU)/2)
x = int((q_xU + q_xL)/2)
y = int((q_yL+q_yU)/2)
print(x,y)
#检验随机抽取的点是否位于df中
exists = ((df['lon'] == x) & (df['lat'] == y)).any()
if exists:
    print(f"元组({x}, {y}) 存在于df中。")
"""

from create_SFC import SFC,Gettheta
#测试创建一个SFC
"""
z_curve = SFC(df,theta)
#2476403
print(len(z_curve))
print(z_curve[:5])
print(z_curve[555:])
"""

from query_process import ObjectiveFunction
#测试运行目标函数
"""
z_order_theta_values = [0,  2,  4,  6,  8, 10,  1,  3,  5,  7,  9, 11]
x_bit_array = z_order_theta_values[:6]
y_bit_array =z_order_theta_values[6:]
theta = (Gettheta(x_bit_array),Gettheta(y_bit_array))
z_curve = SFC(df,theta)
#z_curve下的查询速率
Querytime = ObjectiveFunction(df,theta,z_order_theta_values,z_curve)
print('AverageQuerytime = ',Querytime)
"""

from skopt import Optimizer
from skopt.space import Real
from generate_space import merge_sort_with_custom_order
import pickle
import os
# 设定搜索空间
theta_0_space = [
    Real(0, 1, name=f'theta_0_{i}') for i in range(6)
]
theta_1_space = [
    Real(0, 1, name=f'theta_1_{i}') for i in range(6)
]
space = theta_0_space + theta_1_space

D = df

def objective(theta_values):
    theta_values = merge_sort_with_custom_order(theta_values)
    print("theta_values = ",theta_values)
    theta_half = int(len(theta_values)/2)
    theta_0 = np.array(theta_values)[:theta_half]
    theta_1 = np.array(theta_values)[theta_half:]
    theta = np.vstack([Gettheta(theta_0),Gettheta(theta_1)])
    #print(theta)
    # 调用目标函数进行评估
    curve = SFC(D,theta)
    return ObjectiveFunction(D, theta,theta_values,curve)


# 初始化优化器
def create_optimizer():
    return Optimizer(dimensions=space, base_estimator='RF', acq_func="EI", random_state=2, n_initial_points=20)

# 保存优化器状态
def save_optimizer_state(optimizer, filename, iteration):
    with open(filename, 'wb') as f:
        pickle.dump((optimizer, iteration), f)

# 加载优化器状态
def load_optimizer_state(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# 文件名
optimizer_file = 'optimizer_state_sort_EI.pkl'

# 检查是否已有保存的状态
if os.path.exists(optimizer_file):
    try:
        optimizer, start_iteration = load_optimizer_state(optimizer_file)
        start_iteration = start_iteration  # 考虑已经插入的初始点
        print(f"Loaded optimizer state from file. Resuming from iteration {start_iteration + 1}.")
    except (FileNotFoundError, EOFError):
        optimizer = create_optimizer()
        print("Created a new optimizer.")
        start_iteration = 0
else:
    optimizer = create_optimizer()
    print("Created a new optimizer.")
    start_iteration = 0


iterations = []
values = []

def record_results(iteration, value):
    iterations.append(iteration)
    values.append(value)
    print(f"Iteration {iteration}: Objective Function Value = {value}")

# 优化过程
num_iterations = 100  # 设置优化迭代次数
for i in range(start_iteration, start_iteration + num_iterations):
    next_point = optimizer.ask()
    #print("next_point",next_point)
    f_val = objective(next_point)
    # 记录并输出结果
    record_results(i + 1, f_val)
    # 将结果告知优化器
    optimizer.tell(next_point, f_val)
    # 保存优化器状态，每100次保存一次
    if (i + 1) % 100 == 0:
        save_optimizer_state(optimizer, optimizer_file, i + 1)

# 输出优化结果
best_theta = optimizer.Xi[np.argmin(optimizer.yi)]
best_theta_values = merge_sort_with_custom_order(best_theta)
print(f'best theta found: {best_theta_values}')
print(f'Objective function value: {min(optimizer.yi)}')

# 绘制优化过程图
plt.figure(figsize=(10, 5))
plt.plot(iterations, values, marker='o')
plt.xlabel('Iteration')
plt.ylabel('Objective Function Value')
plt.title('Optimization Process')
plt.grid(True)
plt.show()

