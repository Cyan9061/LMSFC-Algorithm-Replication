import pandas as pd
df = pd.read_csv('OSMdata_process_positive_very_little.csv')

from create_SFC import SFC,Gettheta,GetPageMBR
#z_order_theta_values = [0,2,4,6,8,10,12,14,1,3,5,7,9,11,13,15]
colume_theta_values = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
x_bit_array = colume_theta_values[:8]
y_bit_array =colume_theta_values[8:]
theta = (Gettheta(x_bit_array),Gettheta(y_bit_array))
curve = SFC(df,theta)


def heuristic_paging(curve, GetPageMBRVolume, page_size_kb, f, alpha):
    n = len(curve)
    pages = []  # 存储分页结果
    current_page = []  # 当前页面的数据点
    current_mbr_volume = None  # 当前页面的MBR体积

    i = 0
    while i < n:
        # 如果当前页面为空，加载fB/4d个数据点
        if not current_page:
            current_page = curve[i:i + int(page_size_kb * f)]
            current_mbr_volume = GetPageMBRVolume(current_page, theta, colume_theta_values)
            i += len(current_page)

        # 计算添加下一个数据点后的MBR
        if i < n:
            next_data_point = curve[i]
        else:
            next_data_point = None
        if next_data_point:
            potential_page = current_page + [next_data_point]
            potential_mbr_volume = GetPageMBRVolume(potential_page, theta, colume_theta_values)

            # 判断是否违反 MBR 增长速率的限制
            if len(current_page) < page_size_kb and potential_mbr_volume < alpha * current_mbr_volume:
                # 如果不违反条件，添加数据点到当前页面
                current_page.append(next_data_point)
                current_mbr_volume = potential_mbr_volume
                i += 1
            else:
                # 否则，将当前页面保存并重新初始化一个新current_page
                pages.append(current_page)
                current_page = []

    # 保存最后一个页面
    if current_page:
        pages.append(current_page)

    return pages

def GetPageMBRVolume(P_curve, theta, theta_values):
    (x_min, x_max), (y_min, y_max) = GetPageMBR(P_curve, theta, theta_values)
    return (x_max - x_min + 1) * (y_max - y_min + 1)

pages = heuristic_paging(curve, GetPageMBRVolume, page_size_kb=128, f=0.6, alpha=1.2)

for idx, page in enumerate(pages):
    print(f"Page {idx + 1}: len:{len(page)},{page}")
