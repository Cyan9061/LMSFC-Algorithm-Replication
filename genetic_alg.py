import numpy as np
import random


def genetic_algorithm(fitness_func, initial_mean, initial_std, population_size=1000, num_generations=1000,
                      mutation_rate=0.01, mutation_strength=1, selection_func=None):
    # 初始化种群
    length = len(initial_mean)  # 变量长度
    population = np.random.uniform(0, 1, (population_size, length))  # 生成标准正态分布
    #print("population：",population)
    # 应用标准差和均值
    for i in range(population_size):
        population[i, :length] *= initial_std[:length]  # 应用标准差
        population[i, :length] += initial_mean  # 加上均值

    best_solution = None
    best_error = float('inf')  # 初始设为正无穷
    loss = []
    for generation in range(num_generations):
        # 计算适应度和误差
        scores_and_errors = np.array([fitness_func(ind) for ind in population])
        scores = scores_and_errors[:, 0]  # 适应度
        errors = scores_and_errors[:, 1]  # 误差
        #print("population[0]",population[0])
        # 找到当前最优个体
        best_idx = np.argmax(scores)
        loss.append(errors[best_idx])
        print("num_generations =",generation,"Objective Function value =",errors[best_idx])
        if errors[best_idx] < best_error:
            best_solution = population[best_idx]
            best_error = errors[best_idx]

        # 选择阶段
        if selection_func is None:
            # 计算概率前检查最大值与适应度的差值
            max_score = np.max(scores)
            if np.isfinite(max_score):  # 确保最大值是有限数
                probabilities = np.where(scores > 0, np.exp(scores - max_score), 0)
                total_prob = np.sum(probabilities)

                # 检查总概率是否为零或无效
                if total_prob > 0:
                    probabilities /= total_prob  # 归一化
                else:
                    probabilities = np.ones(population_size) / population_size  # 使用均匀分布

                selected_indices = np.random.choice(population_size, size=population_size, p=probabilities)
            else:
                # 如果所有分数为负无穷大或出现错误，使用均匀分布
                selected_indices = np.random.choice(population_size, size=population_size)

            selected_population = population[selected_indices]
        else:
            selected_population = selection_func(population, scores)

        # 生成新种群
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[(i + 1) % population_size]
            child1 = mutate(crossover(parent1, parent2), mutation_rate, mutation_strength)
            child2 = mutate(crossover(parent2, parent1), mutation_rate, mutation_strength)
            new_population.extend([child1, child2])
        population = np.array(new_population)

    return best_solution, best_error, loss


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)  # 保证交叉点在有效范围内
    return np.concatenate([parent1[:point], parent2[point:]])


def mutate(individual, mutation_rate, mutation_strength):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] += np.random.normal(0, mutation_strength)  # 应用小幅度的正态分布扰动
            #print("mutate individual:",individual[i])
    return individual
