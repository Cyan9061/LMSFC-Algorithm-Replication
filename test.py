import pandas as pd
import numpy as np
df = pd.read_csv('OSMdata_process_positive_large.csv')

from query_process import QueryProcess
from generate_query import GenerateSkewedQuery, GenerateUniformQuery
from alg4_recursive_query_splitting import RecursiveQuerySplitting
def QueryProcessWithSplitting(D, query, theta, theta_values, curve):
    k_maxsplit = 5
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
