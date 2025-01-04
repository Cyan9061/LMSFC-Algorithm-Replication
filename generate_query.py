def GetMBR(D):
    x_L = D['lon'].min()
    y_L = D['lat'].min()
    x_U = D['lon'].max()
    y_U = D['lat'].max()
    return (x_L,y_L),(x_U,y_U)
import random
query_range = 0.01/2

def GenerateUniformQuery(D):
    (x_L,y_L),(x_U,y_U) = GetMBR(D)
    lon_width = x_U - x_L
    lat_width = y_U - y_L
    x = int(random.uniform(x_L, x_U))
    y = int(random.uniform(y_L, y_U))
    #调整是在一定范围内随机选取查询框大小，还是固定查询框大小
    x_width = lon_width * query_range#int(random.uniform(0, lon_width * query_range))#
    y_width = lat_width * query_range#int(random.uniform(0, lat_width * query_range))#
    #print(x_U-x_L,y_U-y_L)
    #print(x,y)
    q_xL = max(x - x_width,x_L)
    q_xU = min(x + x_width,x_U)
    q_yL = max(y - y_width,y_L)
    q_yU = min(y + y_width,y_U)
    UniformQuery = ((int(q_xL),int(q_xU)),(int(q_yL),int(q_yU)))
    return UniformQuery
#print(GenerateUniformQuery(df))

def GenerateSkewedQuery(D):
    (x_L,y_L),(x_U,y_U) = GetMBR(D)
    lon_width = x_U - x_L
    lat_width = y_U - y_L
    random_row = D.sample(n=1)
    x = random_row['lon'].values[0]
    y = random_row['lat'].values[0]
    x_width = lon_width * query_range#int(random.uniform(0, lon_width * query_range))#
    y_width = lat_width * query_range#int(random.uniform(0, lat_width * query_range))#
    #print('x,y = ',x,y)
    q_xL = max(x - x_width,x_L)
    q_xU = min(x + x_width,x_U)
    q_yL = max(y - y_width,y_L)
    q_yU = min(y + y_width,y_U)
    SkewedQuery = ((int(q_xL),int(q_xU)),(int(q_yL),int(q_yU)))
    return SkewedQuery

