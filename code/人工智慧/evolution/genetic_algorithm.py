"""
遺傳演算法 (Genetic Algorithm)

歷史背景：
- 1975 年由 John Holland 在《Adaptation in Natural and Artificial Systems》中提出
- 靈感來自達爾文進化論：適者生存
- 1989 年 David Goldberg 的《Genetic Algorithms》奠定了實務應用基礎
- 廣泛應用於最佳化、排程、機器學習、自動設計等領域

核心概念：
- 編碼：將解表示為染色體（通常為二進制或實數序列）
- 適應度函數：評估解的好壞
- 選擇：輪盤賭、競賽選擇等方式挑選優良個體
- 交叉：交換父母染色體片段產生後代
- 突變：隨機改變基因以維持多樣性
"""

from typing import List, Tuple, Callable, Optional
import random
import math


class Individual:
    """個體：代表一個候選解"""

    def __init__(self, genes: List[float], fitness: float = 0.0):
        self.genes = genes
        self.fitness = fitness

    def __repr__(self):
        return f"Individual(fitness={self.fitness:.4f}, genes={[round(g, 3) for g in self.genes[:5]]}...)"


def create_random_individual(n_genes: int, gene_range: Tuple[float, float] = (0.0, 1.0)) -> Individual:
    """隨機產生個體"""
    low, high = gene_range
    genes = [random.uniform(low, high) for _ in range(n_genes)]
    return Individual(genes)


def tournament_selection(
    population: List[Individual],
    tournament_size: int = 3,
) -> Individual:
    """競賽選擇：隨機選 k 個個體，取適應度最高的"""
    competitors = random.sample(population, min(tournament_size, len(population)))
    return max(competitors, key=lambda ind: ind.fitness)


def roulette_selection(population: List[Individual]) -> Individual:
    """輪盤賭選擇：適應度越高被選中機率越大"""
    total_fitness = sum(ind.fitness for ind in population)
    if total_fitness == 0:
        return random.choice(population)

    r = random.uniform(0, total_fitness)
    cumulative = 0.0
    for ind in population:
        cumulative += ind.fitness
        if cumulative >= r:
            return ind
    return population[-1]


def crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """
    算術交叉：線性組合父母基因
    child1 = α·parent1 + (1-α)·parent2
    child2 = (1-α)·parent1 + α·parent2
    """
    alpha = random.uniform(0.2, 0.8)

    child1_genes = [
        alpha * g1 + (1 - alpha) * g2
        for g1, g2 in zip(parent1.genes, parent2.genes)
    ]
    child2_genes = [
        (1 - alpha) * g1 + alpha * g2
        for g1, g2 in zip(parent1.genes, parent2.genes)
    ]

    return Individual(child1_genes), Individual(child2_genes)


def mutate(
    individual: Individual,
    mutation_rate: float = 0.1,
    mutation_strength: float = 0.2,
    gene_range: Tuple[float, float] = (0.0, 1.0),
) -> None:
    """高斯突變：以機率對每個基因添加高斯雜訊"""
    low, high = gene_range
    for i in range(len(individual.genes)):
        if random.random() < mutation_rate:
            new_gene = individual.genes[i] + random.gauss(0, mutation_strength)
            individual.genes[i] = max(low, min(high, new_gene))


def genetic_algorithm(
    n_genes: int,
    fitness_func: Callable[[List[float]], float],
    population_size: int = 50,
    n_generations: int = 100,
    mutation_rate: float = 0.1,
    mutation_strength: float = 0.2,
    crossover_rate: float = 0.8,
    gene_range: Tuple[float, float] = (0.0, 1.0),
    elite_ratio: float = 0.1,
    seed: Optional[int] = None,
) -> Tuple[Individual, List[float]]:
    """
    遺傳演算法主流程

    參數：
        n_genes: 每個個體的基因數量
        fitness_func: 適應度函數（越大越好）
        population_size: 族群大小
        n_generations: 最大代數
        mutation_rate: 突變率
        mutation_strength: 突變強度
        crossover_rate: 交叉率
        gene_range: 基因值範圍
        elite_ratio: 菁英保留比例
        seed: 隨機種子

    返回：
        (最佳個體, 每代最佳適應度歷史)
    """
    if seed is not None:
        random.seed(seed)

    # 初始化族群
    population = [
        create_random_individual(n_genes, gene_range)
        for _ in range(population_size)
    ]
    for ind in population:
        ind.fitness = fitness_func(ind.genes)

    elite_count = max(1, int(population_size * elite_ratio))
    history = []

    for generation in range(n_generations):
        # 評估適應度
        for ind in population:
            ind.fitness = fitness_func(ind.genes)

        # 排序並記錄最佳
        population.sort(key=lambda ind: ind.fitness, reverse=True)
        best = population[0]
        history.append(best.fitness)

        # 保留菁英
        new_population = population[:elite_count]

        # 產生新一代
        while len(new_population) < population_size:
            # 選擇父母
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            # 交叉
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = Individual(parent1.genes[:]), Individual(parent2.genes[:])

            # 突變
            mutate(child1, mutation_rate, mutation_strength, gene_range)
            mutate(child2, mutation_rate, mutation_strength, gene_range)

            # 重新評估
            child1.fitness = fitness_func(child1.genes)
            child2.fitness = fitness_func(child2.genes)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    # 最終評估
    for ind in population:
        ind.fitness = fitness_func(ind.genes)
    population.sort(key=lambda ind: ind.fitness, reverse=True)

    return population[0], history


def binary_to_real(binary: List[int], low: float, high: float) -> float:
    """將二進制基因轉換為實數值"""
    value = int("".join(map(str, binary)), 2)
    max_value = 2 ** len(binary) - 1
    return low + (high - low) * value / max_value


def genetic_algorithm_binary(
    n_bits: int,
    fitness_func: Callable[[List[int]], float],
    population_size: int = 50,
    n_generations: int = 100,
    mutation_rate: float = 0.01,
    crossover_rate: float = 0.8,
    elite_ratio: float = 0.1,
    seed: Optional[int] = None,
) -> Tuple[List[int], float, List[float]]:
    """
    二進制編碼的遺傳演算法

    返回：
        (最佳染色體, 最佳適應度, 歷史)
    """
    if seed is not None:
        random.seed(seed)

    def create_binary():
        return [random.randint(0, 1) for _ in range(n_bits)]

    population = [create_binary() for _ in range(population_size)]

    elite_count = max(1, int(population_size * elite_ratio))
    history = []

    for generation in range(n_generations):
        # 評估
        fitnesses = [fitness_func(chromo) for chromo in population]

        # 記錄最佳
        best_idx = fitnesses.index(max(fitnesses))
        best_fitness = fitnesses[best_idx]
        history.append(best_fitness)

        # 帶適應度的個體列表
        individuals = list(zip(population, fitnesses))
        individuals.sort(key=lambda x: x[1], reverse=True)

        # 菁英保留
        new_population = [ind[0][:] for ind in individuals[:elite_count]]

        # 輪盤賭選擇
        total_fitness = sum(fitnesses)
        if total_fitness > 0:
            probs = [f / total_fitness for f in fitnesses]
        else:
            probs = [1.0 / len(fitnesses)] * len(fitnesses)

        def select():
            r = random.random()
            cumulative = 0.0
            for i, p in enumerate(probs):
                cumulative += p
                if cumulative >= r:
                    return population[i][:]
            return population[-1][:]

        # 產生新一代
        while len(new_population) < population_size:
            p1 = select()
            p2 = select()

            # 單點交叉
            if random.random() < crossover_rate:
                point = random.randint(1, n_bits - 1)
                child = p1[:point] + p2[point:]
            else:
                child = p1[:]

            # 位元突變
            for i in range(n_bits):
                if random.random() < mutation_rate:
                    child[i] = 1 - child[i]

            new_population.append(child)

        population = new_population

    # 最終評估
    fitnesses = [fitness_func(chromo) for chromo in population]
    best_idx = fitnesses.index(max(fitnesses))

    return population[best_idx], fitnesses[best_idx], history


def demo_sphere():
    """Sphere 函數最佳化：f(x) = Σ x_i²"""
    print("=== Sphere 函數最佳化 ===\n")
    print("目標：minimize f(x) = Σ x_i²")
    print("全域最佳：x = [0,0,...,0], f = 0\n")

    def fitness(genes):
        # GA 最大化，取負值
        return -sum(x ** 2 for x in genes)

    best, history = genetic_algorithm(
        n_genes=5,
        fitness_func=fitness,
        population_size=50,
        n_generations=100,
        gene_range=(-5.0, 5.0),
        mutation_rate=0.1,
        mutation_strength=0.3,
        seed=42,
    )

    actual_fitness = -best.fitness
    print(f"最佳解：{[round(g, 4) for g in best.genes]}")
    print(f"f(x) = {actual_fitness:.6f}")
    print(f"誤差：{abs(actual_fitness):.6f}")


def demo_rastrigin():
    """Rastrigin 函數最佳化"""
    print("\n=== Rastrigin 函數最佳化 ===\n")

    def fitness(genes):
        x, y = genes
        val = 20 + (x ** 2 - 10 * math.cos(2 * math.pi * x)) + \
              (y ** 2 - 10 * math.cos(2 * math.pi * y))
        return -val  # GA 最大化

    best, history = genetic_algorithm(
        n_genes=2,
        fitness_func=fitness,
        population_size=50,
        n_generations=100,
        gene_range=(-5.12, 5.12),
        mutation_rate=0.15,
        mutation_strength=0.5,
        seed=42,
    )

    actual_fitness = -best.fitness
    print(f"最佳解：x={best.genes[0]:.4f}, y={best.genes[1]:.4f}")
    print(f"f(x,y) = {actual_fitness:.4f}")


def demo_history():
    """收斂歷史展示"""
    print("\n=== 收斂歷史 ===\n")

    def fitness(genes):
        return -(genes[0] - 0.7) ** 2 - (genes[1] - 0.3) ** 2

    _, history = genetic_algorithm(
        n_genes=2,
        fitness_func=fitness,
        population_size=30,
        n_generations=50,
        gene_range=(0.0, 1.0),
        seed=42,
    )

    # 轉換為正值顯示
    history = [-h for h in history]

    print(f"{'代數':>5} | {'最佳適應度':>12} | 收斂曲線")
    print("-" * 50)
    for i in range(0, len(history), 5):
        val = history[i]
        bar = "█" * int(val * 30)
        print(f"{i:>5} | {val:>12.4f} | {bar}")


def demo_binary():
    """二進制編碼 GA：最大化 1 的數量"""
    print("\n=== 二進制編碼 GA（最大化 1 的數量） ===\n")

    def fitness(chromo):
        return sum(chromo)

    n_bits = 20
    best, best_fit, history = genetic_algorithm_binary(
        n_bits=n_bits,
        fitness_func=fitness,
        population_size=30,
        n_generations=50,
        mutation_rate=0.02,
        seed=42,
    )

    print(f"最佳染色體：{''.join(map(str, best))}")
    print(f"1 的數量：{best_fit}/{n_bits}")


if __name__ == "__main__":
    demo_sphere()
    demo_rastrigin()
    demo_history()
    demo_binary()
