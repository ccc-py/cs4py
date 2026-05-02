"""
遺傳搜尋演算法 (Genetic Search Algorithm)

歷史背景：
- 基於 John Holland 於 1975 年提出的遺傳演算法框架
- 不同於 function optimization，遺傳搜尋專注於搜尋離散解空間
- 應用於約束滿足問題、路徑搜尋、排程等組合搜尋問題
- 結合演化計算與搜尋理論，處理大型離散搜尋空間

核心概念：
- 將搜尋問題編碼為染色體（通常為二進制或排列）
- 適應度函數評估候選解在搜尋空間中的品質
- 透過選擇、交叉、突變探索搜尋空間
- 不同於 evolution/genetic_algorithm.py 的連續最佳化，此處專注離散搜尋
"""

from typing import List, Tuple, Optional, Callable
import random


def binary_genetic_search(
    create_chromosome: Callable[[], List[int]],
    fitness_func: Callable[[List[int]], float],
    is_solution: Callable[[List[int]], bool],
    decode: Callable[[List[int]], str],
    n_bits: int,
    population_size: int = 100,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.01,
    max_generations: int = 500,
    seed: Optional[int] = None,
) -> Tuple[Optional[List[int]], float, List[float]]:
    """
    二進制編碼的遺傳搜尋

    參數：
        create_chromosome: 建立隨機染色體的函數
        fitness_func: 適應度函數（越高越好）
        is_solution: 檢查是否為合法解的函數
        decode: 解碼染色體為可讀字串的函數
        n_bits: 染色體長度
        population_size: 族群大小
        crossover_rate: 交叉率
        mutation_rate: 突變率
        max_generations: 最大世代數
        seed: 隨機種子

    返回：
        (最佳染色體, 最佳適應度, 歷史記錄)
    """
    if seed is not None:
        random.seed(seed)

    # 初始化族群
    population = [create_chromosome() for _ in range(population_size)]
    history = []
    best_chromosome = None
    best_fitness = float('-inf')

    for generation in range(max_generations):
        # 評估
        fitnesses = [fitness_func(chromo) for chromo in population]

        # 找出當代最佳
        gen_best_idx = fitnesses.index(max(fitnesses))
        gen_best_fitness = fitnesses[gen_best_idx]
        gen_best_chromo = population[gen_best_idx]

        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best_chromosome = gen_best_chromo[:]

        history.append(best_fitness)

        # 檢查是否找到解
        if is_solution(gen_best_chromo):
            return gen_best_chromo, gen_best_fitness, history

        # 排序（高適應度在前）
        individuals = list(zip(population, fitnesses))
        individuals.sort(key=lambda x: x[1], reverse=True)

        # 菁英保留（保留前 10%）
        elite_count = max(1, population_size // 10)
        new_population = [ind[0][:] for ind in individuals[:elite_count]]

        # 輪盤賭選擇
        total_fitness = sum(fitnesses)
        if total_fitness <= 0:
            probs = [1.0 / len(fitnesses)] * len(fitnesses)
        else:
            probs = [f / total_fitness for f in fitnesses]

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
            if random.random() < crossover_rate and n_bits > 1:
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

    return best_chromosome, best_fitness, history


class SubsetSumProblem:
    """
    子集和問題（搜尋應用示範）

    給定一組數字和目標值，找出一個子集使其和等於目標值。
    染色體：二進制，長度為數字個數，1 表示選取該數字。
    """

    def __init__(self, numbers: List[int], target: int):
        self.numbers = numbers
        self.target = target
        self.n = len(numbers)

    def create_chromosome(self) -> List[int]:
        """隨機選取子集"""
        return [random.randint(0, 1) for _ in range(self.n)]

    def fitness(self, chromosome: List[int]) -> float:
        """適應度：越接近目標值越好"""
        subset_sum = sum(self.numbers[i] for i in range(self.n) if chromosome[i] == 1)

        if subset_sum == self.target:
            return 1000.0  # 找到解，給予高獎勵

        return float(-abs(subset_sum - self.target))

    def decode(self, chromosome: List[int]) -> str:
        """解碼為選取的數字"""
        selected = [self.numbers[i] for i in range(self.n) if chromosome[i] == 1]
        return f"選取：{selected}，和：{sum(selected)}"

    def is_solution(self, chromosome: List[int]) -> bool:
        """檢查是否為合法解"""
        subset_sum = sum(self.numbers[i] for i in range(self.n) if chromosome[i] == 1)
        return subset_sum == self.target


def demo_subset_sum():
    """子集和問題示範"""
    print("=== 子集和問題遺傳搜尋 ===\n")
    print("目標：從數字列表中找出一個子集，使其和等於目標值\n")

    numbers = [3, 34, 4, 12, 5, 2]
    target = 9

    print(f"數字：{numbers}")
    print(f"目標：{target}\n")

    problem = SubsetSumProblem(numbers, target)

    best, fitness, history = binary_genetic_search(
        create_chromosome=problem.create_chromosome,
        fitness_func=problem.fitness,
        is_solution=problem.is_solution,
        decode=problem.decode,
        n_bits=len(numbers),
        population_size=50,
        crossover_rate=0.8,
        mutation_rate=0.05,
        max_generations=100,
        seed=42,
    )

    if best:
        print(f"結果：{problem.decode(best)}")
        if problem.is_solution(best):
            print("找到解！")
        else:
            print(f"未找到完整解，最佳適應度：{fitness}")
    print()


def demo_n_queens_simple():
    """N-皇后問題簡化示範（使用排列編碼）"""
    print("=== N-皇后問題遺傳搜尋（簡化版）===\n")
    print("目標：在 N×N 棋盤上放置 N 個皇后，使其互不攻擊\n")

    def create_nqueens_chromosome(n: int) -> List[int]:
        """建立隨機排列（每行一個皇后）"""
        chromo = list(range(n))
        random.shuffle(chromo)
        return chromo

    def nqueens_fitness(chromosome: List[int]) -> float:
        """適應度：攻擊對數越少分數越高"""
        n = len(chromosome)
        attacks = 0
        for i in range(n):
            for j in range(i + 1, n):
                if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == abs(i - j):
                    attacks += 1
        total_pairs = n * (n - 1) // 2
        return float(total_pairs - attacks)

    def nqueens_is_solution(chromosome: List[int]) -> bool:
        return nqueens_fitness(chromosome) == len(chromosome) * (len(chromosome) - 1) // 2

    def nqueens_decode(chromosome: List[int]) -> str:
        n = len(chromosome)
        lines = []
        for row in range(n):
            line = ""
            for col in range(n):
                line += "Q " if chromosome[row] == col else ". "
            lines.append(line)
        return "\n".join(lines)

    for n in [4, 8]:
        print(f"--- {n}-皇后問題 ---")

        best = None
        best_fitness = float('-inf')

        # 簡單隨機搜尋（因為 N-皇后較難用二進制 GA）
        for _ in range(10000):
            chromo = create_nqueens_chromosome(n)
            fit = nqueens_fitness(chromo)
            if fit > best_fitness:
                best_fitness = fit
                best = chromo
                if nqueens_is_solution(chromo):
                    break

        if best and nqueens_is_solution(best):
            print(f"找到解！適應度：{best_fitness}")
            print(f"棋盤：\n{nqueens_decode(best)}\n")
        else:
            print(f"未找到完整解，最佳適應度：{best_fitness}")
            print(f"目前最佳：{best}\n")


def demo_history():
    """收斂歷史展示"""
    print("=== 收斂歷史展示 ===\n")

    numbers = [1, 2, 3, 4, 5, 6, 7]
    target = 14

    problem = SubsetSumProblem(numbers, target)

    _, _, history = binary_genetic_search(
        create_chromosome=problem.create_chromosome,
        fitness_func=problem.fitness,
        is_solution=problem.is_solution,
        decode=problem.decode,
        n_bits=len(numbers),
        population_size=50,
        max_generations=50,
        seed=42,
    )

    print(f"{'世代':>5} | {'最佳適應度':>12} | 收斂曲線")
    print("-" * 45)
    for i in range(0, len(history), 5):
        val = history[i]
        bar = "█" * int(val / 200)  # 1000 是最大適應度
        print(f"{i:>5} | {val:>12.1f} | {bar}")


if __name__ == "__main__":
    demo_subset_sum()
    demo_n_queens_simple()
    demo_history()
