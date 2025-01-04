import numpy as np
def CalcBinary(x):
    # 将整数转换为二进制字符串，去掉 '0b' 前缀
    binary_str = bin(x)[2:]
    # 将二进制字符串中的每个字符转换为整数
    x_binary_array = np.array([int(bit) for bit in binary_str], dtype=np.int8)
    return x_binary_array
"""x_binary_array = CalcBinary(63)
print(x_binary_array)
len(x_binary_array)"""


def Gettheta(bit_array):
    x_len = len(bit_array)
    theta1 = np.full(x_len, 2,dtype = np.int64)**bit_array
    return theta1
"""#以z-order为例
#x_bit_array = np.arange(0, 11, 2)  # 从 0 开始，每次增加 2，直到 14个
#y_bit_array = np.arange(1, 12, 2)  # 从 1 开始，每次增加 2，直到 14个
z2_order = np.array([0,  2,  4,  6,  8, 10,  1,  3,  5,  7,  9, 11])
x_bit_array = z2_order[:6]
y_bit_array =z2_order[6:]
theta = (Gettheta(x_bit_array),Gettheta(y_bit_array))
print(theta)
print(len(y_bit_array))"""


def CalcSFCposition(x, y, theta):
    x_binary_array = CalcBinary(x)[::-1]
    y_binary_array = CalcBinary(y)[::-1]
    x_binary_array = x_binary_array.astype(np.int64)
    y_binary_array = y_binary_array.astype(np.int64)

    #print("x,y,x_binary_array,y_binary_array",x,y,x_binary_array,y_binary_array)
    theta_x = theta[0][:len(x_binary_array)]
    theta_y = theta[1][:len(y_binary_array)]
    theta_x = theta_x.astype(np.int64)
    theta_y = theta_y.astype(np.int64)
    #print("theta_x,theta_y",theta_x,theta_y)
    x_1 = np.sum(np.multiply(x_binary_array, theta_x))
    y_1 = np.sum(np.multiply(y_binary_array, theta_y))
    SFCposition = x_1 + y_1
    return SFCposition


#print(CalcSFCposition(31, 8, theta))


def CalcInverseSFC(SFCposition, theta, theta_values):
    SFC_binary_array = CalcBinary(SFCposition)[::-1]  # 得到的数组eg[1,0]中1代表2^0位0代表2^1位
    while (len(SFC_binary_array) < len(theta_values)):
        SFC_binary_array = np.append(SFC_binary_array, 0)
    #print('SFC_binary_array1',SFC_binary_array)

    bit_num = int(len(theta_values) / 2)
    x_bit_array = theta_values[:bit_num]
    y_bit_array = theta_values[bit_num:]

    x_bit = np.array([], dtype=int)
    y_bit = np.array([], dtype=int)

    max_i = len(SFC_binary_array) / 2

    #print('x_bit_array,y_bit_array',x_bit_array,y_bit_array)

    for i in range(0, int(max_i)):
        x_bit = np.append(x_bit, SFC_binary_array[int(x_bit_array[i])])
        y_bit = np.append(y_bit, SFC_binary_array[int(y_bit_array[i])])

    x_bit = x_bit[::-1]
    y_bit = y_bit[::-1]
    #print("x_bit,y_bit",x_bit,y_bit)
    # 将 x_bit 转换为二进制字符串
    x_binary_str = ''.join(map(str, x_bit))
    # 将二进制字符串转换为十进制数字
    x_decimal = int(x_binary_str, 2)

    y_binary_str = ''.join(map(str, y_bit))
    y_decimal = int(y_binary_str, 2)
    return x_decimal, y_decimal


"""# print(CalcSFCposition(7195,3607,theta))#此处发现问题
theta_values = np.concatenate((x_bit_array, y_bit_array))
x1, y1 = CalcInverseSFC(469, theta, theta_values)
print("x1,y1 = ", x1, y1)
# x2,y2 = CalcInverseSFC(15762277,theta,theta_values)
# print("x2,y2 = ",x2,y2)"""


def SFC(D,theta):
    curve = []
    i_max = len(D)
    for i in range(0,i_max):
        x = D['lon'].iloc[i]
        y = D['lat'].iloc[i]
        curve.append(CalcSFCposition(x,y,theta))
        #if((i%10000 == 1)or(i == i_max-1)):
        #    print(f'SFC构建进度：{(i+1)/i_max*100}%')
    curve.sort()
    return curve

def GetPageMBR(P_curve, theta, theta_values):
    x_min, y_min = CalcInverseSFC(P_curve[0], theta, theta_values)
    x_max, y_max = x_min, y_min
    lenth = len(P_curve)
    for i in range(1,lenth):
        #if(i%10000 == 1):
        #    print("计算MBR进度:",i/lenth*100,"%")
        x,y = CalcInverseSFC(P_curve[i], theta, theta_values)
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    #print((x_min, x_max), (y_min, y_max))
    return(x_min, x_max), (y_min, y_max)
