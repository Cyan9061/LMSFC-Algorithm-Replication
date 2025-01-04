import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from genetic_alg import genetic_algorithm
from generate_space import merge_sort_with_custom_order
from create_SFC import SFC,Gettheta
from query_process import ObjectiveFunction

D = pd.read_csv('OSMdata_process_positive_very_little.csv')


def objective(theta_values):
    theta_values = merge_sort_with_custom_order(theta_values)
    #print("theta_values = ",theta_values)
    theta_half = int(len(theta_values)/2)
    theta_0 = np.array(theta_values)[:theta_half]
    theta_1 = np.array(theta_values)[theta_half:]
    theta = np.vstack([Gettheta(theta_0),Gettheta(theta_1)])
    #print(theta)
    # 调用目标函数进行评估
    curve = SFC(D,theta)
    unfitness = ObjectiveFunction(D, theta,theta_values,curve)
    #print("Objective Function value = ",unfitness)
    return -unfitness,unfitness

# 设置初始值
initial_mean = [0,0,0,0,0,0,0,0,0,0,0,0]
initial_std = [1,1,1,1,1,1,1,1,1,1,1,1]  # 包括位置扰动的标准差

best_solution, best_error, loss= genetic_algorithm(
    fitness_func=objective,
    initial_mean=initial_mean,
    initial_std=initial_std,
    population_size=50,
    num_generations=800,
    mutation_rate=0.05,
    mutation_strength=0.05
)

print("Best solution:", merge_sort_with_custom_order(best_solution))
print("Best query time:", best_error)
iterations = []
for i in range(0,len(loss)):
    iterations.append(i+1)
plt.figure(figsize=(10, 5))
plt.plot(iterations, loss, marker='o')
plt.xlabel('Iteration')
plt.ylabel('Objective Function Value')
plt.title('Genetic Optimization Process')
plt.grid(True)
plt.show()