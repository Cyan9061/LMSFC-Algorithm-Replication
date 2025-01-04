#本文件有两个测试项目，均已被注释掉，可以翻到最去选择
#测试1对比分割后查询和直接查询的效率
#测试2对比查询准确率（用假阳性率评估)
import pandas as pd
import numpy as np
df = pd.read_csv('OSMdata_process_positive_large.csv')

from query_process import QueryProcess
from generate_query import GenerateSkewedQuery, GenerateUniformQuery
from alg4_recursive_query_splitting import RecursiveQuerySplitting
def QueryProcessWithSplitting(D, query, theta, theta_values, curve):
    k_maxsplit = 4
    SplittedQuerys = RecursiveQuerySplitting(query, theta, k_maxsplit)
    scanned_point = [0] * (2**k_maxsplit)#最多分裂出2**k_maxsplit个子查询
    for i in range(len(SplittedQuerys)):
        scanned_point[i] = QueryProcess(D,SplittedQuerys[i],theta, theta_values, curve)
    return scanned_point

from create_SFC import SFC, Gettheta
x_bit_array = np.arange(0, 26, 2)
y_bit_array = np.arange(1, 27, 2)
theta_values = np.concatenate((x_bit_array,y_bit_array))
theta = (Gettheta(x_bit_array),Gettheta(y_bit_array))
curve = SFC(df,theta)

"""
#测试，对比分割后查询和直接查询的效率
import timeit
time1 = 0
time2 = 0
for i in range(90):
    query = GenerateSkewedQuery(df)
    time1 += timeit.timeit(lambda: QueryProcessWithSplitting(df,query,theta, theta_values, curve), number=1)
    time2 += timeit.timeit(lambda: QueryProcess(df,query,theta, theta_values, curve), number=1)
for i in range(10):
    query = GenerateUniformQuery(df)
    time1 += timeit.timeit(lambda: QueryProcessWithSplitting(df, query, theta, theta_values, curve), number=1)
    time2 += timeit.timeit(lambda: QueryProcess(df, query, theta, theta_values, curve), number=1)
print("time consume of QueryProcessWithSplitting:",time1/100)
print("time consume of straight QueryProcess:",time2/100)
print(f'QueryProcessWithSplitting over straight QueryProcess times:{time2/time1}')
"""



"""
#测试对比查询准确率（用假阳性率评估)
error_point1 = 0
true_point1 = 0
error_point2 = 0
true_point2 = 0
for i in range(9):
    query = GenerateSkewedQuery(df)
    result1 = QueryProcessWithSplitting(df,query,theta, theta_values, curve)
    result2 = QueryProcess(df,query,theta, theta_values, curve)
    for j in range(0,len(result1)):
        true_point1 += result1[j][0]
        error_point1 += result1[j][1]
    true_point2 += result2[0]
    error_point2 += result2[1]
for i in range(1):
    query = GenerateUniformQuery(df)
    result1 = QueryProcessWithSplitting(df, query, theta, theta_values, curve)
    result2 = QueryProcess(df, query, theta, theta_values, curve)
    for j in range(0, len(result1)):
        true_point1 += result1[j][0]
        error_point1 += result1[j][1]
    true_point2 += result2[0]
    error_point2 += result2[1]
print("true_point,error_point,rate of false positive of QueryProcessWithSplitting:\n",error_point1,true_point1,error_point1/(error_point1+true_point1))
print("true_point,error_point,rate of false positive of QueryProcess:\n",error_point2,true_point2,error_point2/(error_point2+true_point2))
"""