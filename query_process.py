import bisect
from create_SFC import CalcSFCposition,CalcInverseSFC
from generate_query import GenerateUniformQuery,GenerateSkewedQuery
# 发现问题：可能在EndPoint上越界
def QueryProcess(D, query, theta, theta_values, curve):
    ((q_xL, q_xU), (q_yL, q_yU)) = query

    StartPoint = CalcSFCposition(q_xL, q_yL, theta)
    EndPoint = CalcSFCposition(q_xU, q_yU, theta)

    StartIndex = bisect.bisect_left(curve, StartPoint)  # curve中第一个不小于StartPoint的元素的序号
    EndIndex = bisect.bisect_right(curve, EndPoint)  # curve中最后一个不大于EndPoint的元素的序号+1

    # print("StartIndex,EndIndex = ",StartPoint,EndPoint)
    NumOfPoints = 0  # 正确的点
    FalsePosPoints = 0  # 假阳性点
    for i in range(StartIndex, EndIndex):
        #if(i%1000 == 1):
        #    print("查询进度：",(i - StartIndex)/(EndIndex-StartIndex)*100,"%")
        x, y = CalcInverseSFC(curve[i], theta, theta_values)
        if q_xL <= x <= q_xU and q_yL <= y <= q_yU:
            # (x, y) 在范围内或在边缘
            NumOfPoints += 1
        else:
            # (x, y) 不在范围内
            FalsePosPoints += 1
    #print("NumOfPoints:",NumOfPoints,"FalsePosPoints:",FalsePosPoints)
    return (NumOfPoints, FalsePosPoints)



import timeit

def ObjectiveFunction(D,theta,theta_values,curve):
    #90%skewedQuery
    SkewedQuery_time = timeit.timeit(lambda: QueryProcess(D, GenerateSkewedQuery(D), theta, theta_values, curve), number=45)
    #10%uniformQuery
    UniformQuery_time = timeit.timeit(lambda: QueryProcess(D, GenerateUniformQuery(D), theta, theta_values, curve), number=5)
    return SkewedQuery_time+UniformQuery_time/50


