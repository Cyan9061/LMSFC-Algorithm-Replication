import pandas as pd
df = pd.read_csv('OSMdata_process_positive_very_little.csv')
"""
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.scatter(df['lon'], df['lat'], c='blue', s=1, alpha=0.5)  # c指定颜色，s指定点大小，alpha指定透明度
plt.title('Scatter plot of lat and lon')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()
"""
from create_SFC import SFC,Gettheta,GetPageMBR
#z_order_theta_values = [0,2,4,6,8,10,12,14,1,3,5,7,9,11,13,15]
colume_theta_values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]#,16,17,18,19,20,21,22,23,24,25]
x_bit_array = colume_theta_values[:int(len(colume_theta_values)/2)]
y_bit_array = colume_theta_values[int(len(colume_theta_values)/2):]
theta = (Gettheta(x_bit_array),Gettheta(y_bit_array))
curve = SFC(df,theta)

def ScoringFunc(P_curve,theta,theta_values):
    size = len(P_curve)
    (x_min, x_max), (y_min, y_max) = GetPageMBR(P_curve,theta,theta_values)
    vol = (x_max - x_min+1) * (y_max - y_min+1)
    #print("vol,size = ",vol,size)
    return vol/size

def dynamic_programming_paging(curve, ScoringFunc, page_size_kb, f=0.6):

    n = len(curve)
    #初始化
    OPT = [float('inf')] * (n + 1)
    page_splits = [-1] * (n + 1)

    #0个数据点成本为0
    OPT[0] = 0
    # 计算分页大小范围
    min_page_size = max(1, int(page_size_kb * f))
    max_page_size = page_size_kb
    #动态规划实现
    for i in range(1, n + 1):
        if(i%100 == 1):
            print("分页进度：",i/n*100,"%")

        #print("min_page_size,max_page_size",min_page_size,max_page_size)
        #从可能的分页大小范围中选择最优分割点
        #print("i = ", i)
        for split_point in range(max(0, i - max_page_size), i - min_page_size + 1):
            # 计算当前页面的评分
            current_page = curve[split_point:i]
            cost = OPT[split_point] + ScoringFunc(current_page, theta, colume_theta_values)
            #print("page_splits,cost = ", split_point, cost)
            if cost < OPT[i]:
                OPT[i] = cost
                page_splits[i] = split_point

    #通过回溯构建分页结果
    pages = []
    i = n
    while i > 0:
        split_point = page_splits[i]
        pages.append((split_point, i - 1))
        i = split_point

    #翻转分页结果顺序
    pages.reverse()
    return pages, OPT

"""
#测试速度
import timeit
time = timeit.timeit(lambda: dynamic_programming_paging(curve, ScoringFunc, f=0.6, page_size_kb=128), number=5)
print(time/5)"""

pages, OPT = dynamic_programming_paging(curve, ScoringFunc, page_size_kb=128, f=0.6)
# 输出分页结果
for idx, (start, end) in enumerate(pages):
    print(f"Page {idx + 1}: curve[{start}:{end}] -> {curve[start:end + 1]}")
#print(OPT)




