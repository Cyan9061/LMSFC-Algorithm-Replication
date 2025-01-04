#可视化数据点
from create_SFC import SFC, Gettheta, CalcSFCposition, CalcBinary
def get_v(query, delta):
    # 解包 query
    (x_min, x_max), (y_min, y_max) = query

    # 根据 delta 选择 x 或 y 维度
    if delta == 0:
        q_L = x_min
        q_U = x_max
    elif delta == 1:
        q_L = y_min
        q_U = y_max

    # 计算 q_L 和 q_U 的 XOR
    xor_value = q_L ^ q_U

    # 找到 MSB（最重要不同位）的索引
    xor_value_bin_array = CalcBinary(xor_value)
    l = len(xor_value_bin_array) - 1
    if l == 0 and xor_value_bin_array[0] == 0:
        # CalcBinary返回的numpy数组为xor_values的二进制表示，如CalcBinary(3) = [1,1]，len = 2。考虑如CalcBinary(1)或0时len均为1，于是做出此调整
        l -= 1
    if l < 0:
        return -1
    # 计算并返回 v
    v = (q_U >> l) << l
    return v

def CalcBenefit(query,delta,v,theta):
    (x_min, x_max), (y_min, y_max) = query
    q_L = (x_min,y_min)
    q_U = (x_max,y_max)
    if delta == 0:
        U = (v-1,y_max)
        L = (v,y_min)
    elif delta ==1:
        U = (x_max,v-1)
        L = (x_min,v)
    f_L = CalcSFCposition(*L,theta)
    f_U = CalcSFCposition(*U,theta)
    #print(f'L{L},U{U},f_L{f_L},f_U{f_U}')
    #print(f'f_L- f_U = {f_L- f_U}')
    return  f_L- f_U



""""检验：
#假设查询窗口为 ((4, 11), (4, 11))
query = ((4, 18), (4, 9))

# 选择 x 维度（delta = 0）
v_x = get_v(query, 0)
print(f"分割点 v_x: {v_x}")

# 选择 y 维度（delta = 1）
v_y = get_v(query, 1)
print(f"分割点 v_y: {v_y}")

CalcBenefit(query,1,9,theta)#发现一种对称性：当v = v_x+1时和v_x-1时，f(L) - f(U)的值相同
"""

def RecursiveQuerySplitting(query, theta, k_maxsplit):
    q_splits = []

    def split(query, k):
        # 如果达到最大分割次数或无法进一步分割，则终止
        if k == 0 or is_no_gap_to_split(query):
            q_splits.append(query)
            return

        max_benefit = float('-inf')
        best_v = None
        best_delta = None

        for delta in range(2):  # delta = 0:x纬度，1：y
            v = get_v(query, delta)
            if v == -1:
                continue
            benefit = CalcBenefit(query, delta, v, theta)

            # 如果当前benefit更大，则更新最分割点
            if benefit > max_benefit:
                max_benefit = benefit
                best_v = v
                best_delta = delta

        if best_delta == 0:  # 分割x
            query1 = ((query[0][0], best_v - 1), query[1])
            query2 = ((best_v, query[0][1]), query[1])
        elif best_delta == 1:  # 分割y
            query1 = (query[0], (query[1][0], best_v - 1))
            query2 = (query[0], (best_v, query[1][1]))

        # 递归地分割子查询窗口
        split(query1, k - 1)
        split(query2, k - 1)

    # 开始递归分割
    split(query, k_maxsplit)

    return q_splits


def is_no_gap_to_split(query):
    return (query[0][0] == query[0][1]) and (query[1][0] == query[1][1])

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv('OSMdata_process_positive_very_little.csv')
    z_order_theta_values = [0, 2, 4, 6, 7, 10, 12, 14, 1, 3, 5, 8, 9, 11, 13, 15]
    x_bit_array = z_order_theta_values[:8]
    y_bit_array = z_order_theta_values[8:]
    theta = (Gettheta(x_bit_array), Gettheta(y_bit_array))
    curve = SFC(df, theta)
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
    query = ((4, 11), (4, 11))
    k_maxsplit = 3
    resulting_splits = RecursiveQuerySplitting(query, theta, k_maxsplit)

    for i in range(0,len(resulting_splits)):
        print(f"Split {i+1}: {resulting_splits[i]}")




