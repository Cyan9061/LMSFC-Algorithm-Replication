import pandas as pd
df = pd.read_csv('OSMdata_process_positive_very_little.csv')

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

def dynamic_programming_paging(curve, scoringFunc, f, page_size_kb):

    n = len(curve)
    OPT = [float('inf')] * (n + 1)
    OPT[0] = 0
    page_splits = [-1] * (n + 1)

    i = int(f * page_size_kb)
    OPT[i] = scoringFunc(curve[0:i], theta, colume_theta_values)
    while i <= n:
        if (i % 100 == 1):
            print("分页进度：", i / n * 100, "%")
        min_cost = float('inf')
        optimal_s = -1
        for s in range(int(f * page_size_kb), page_size_kb + 1):
            if i - s >= 0:
                cost = OPT[i - s] + scoringFunc(curve[i - s:i], theta, colume_theta_values)
                if cost < min_cost:
                    min_cost = cost
                    optimal_s = s
        OPT[i] = min_cost
        page_splits[i] = optimal_s
        i += 1
    # 通过回溯构建分页结果
    pages = []
    i = n
    while i > 0:
        s = page_splits[i]
        pages.append((i - s, i - 1))
        i -= s

    pages.reverse()
    return pages, OPT

# 示例：假设 z_curve 列表和 scoringFunc 函数
# z_curve = [1, 3, 7, 9, 12, 18, 25, 30, 35, 42, 50, 60, 70, 80, 90,10000]  # 示例的 z-address 列表

# scoringFunc 函数示例，计算 P_curve 范围的评分
# def scoringFunc(P_curve):
#     return max(P_curve) - min(P_curve)

# 运行动态规划分页算法
"""
#测试速度
import timeit
time = timeit.timeit(lambda: dynamic_programming_paging(curve, ScoringFunc, f=0.6, page_size_kb=128), number=5)
print(time/5)"""

pages, OPT = dynamic_programming_paging(curve, ScoringFunc, f=0.6, page_size_kb=128)
# 输出分页结果
for idx, (start, end) in enumerate(pages):
    print(f"Page {idx + 1}: curve[{start}:{end}] -> {curve[start:end+1]}")
