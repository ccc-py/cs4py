"""
粒子群優化演算法 (Particle Swarm Optimization, PSO)

歷史背景：
- 1995 年由 James Kennedy 和 Russell Eberhart 提出
- 靈感來自鳥群覓食和魚群游動的社會行為
- 每個粒子代表搜尋空間中的一個候選解
- 粒子根據自身經驗和群體經驗調整飛行方向和速度
- 廣泛應用於函數最佳化、神經網路訓練、排程問題

核心概念：
- 粒子：位置 x 和速度 v
- 個體最佳 (pbest)：粒子歷史最佳位置
- 群體最佳 (gbest)：整個群體歷史最佳位置
- 速度更新：v = w·v + c1·r1·(pbest-x) + c2·r2·(gbest-x)
- 位置更新：x = x + v
"""

from typing import List, Tuple, Callable, Optional
import random
import math


class Particle:
    """粒子"""

    def __init__(self, n_dims: int, bounds: Tuple[float, float]):
        low, high = bounds
        self.position = [random.uniform(low, high) for _ in range(n_dims)]
        self.velocity = [random.uniform(-1, 1) for _ in range(n_dims)]
        self.pbest_position = self.position[:]
        self.pbest_fitness = float('inf')
        self.fitness = float('inf')


def particle_swarm_optimization(
    n_dims: int,
    fitness_func: Callable[[List[float]], float],
    n_particles: int = 30,
    n_iterations: int = 100,
    bounds: Tuple[float, float] = (-5.0, 5.0),
    w: float = 0.7,       # 慣性權重
    c1: float = 1.5,      # 個體學習因子
    c2: float = 1.5,      # 群體學習因子
    seed: Optional[int] = None,
) -> Tuple[List[float], float, List[float]]:
    """
    粒子群優化演算法

    參數：
        n_dims: 問題維度
        fitness_func: 適應度函數（要最小化）
        n_particles: 粒子數量
        n_iterations: 迭代次數
        bounds: 搜尋空間邊界 (low, high)
        w: 慣性權重
        c1: 個體學習因子
        c2: 群體學習因子
        seed: 隨機種子

    返回：
        (全局最佳位置, 全局最佳適應度, 適應度歷史)
    """
    if seed is not None:
        random.seed(seed)

    low, high = bounds
    max_velocity = (high - low) * 0.2

    # 初始化粒子
    particles = [Particle(n_dims, bounds) for _ in range(n_particles)]

    # 初始評估
    gbest_position = None
    gbest_fitness = float('inf')

    for p in particles:
        p.fitness = fitness_func(p.position)
        if p.fitness < p.pbest_fitness:
            p.pbest_fitness = p.fitness
            p.pbest_position = p.position[:]

        if p.fitness < gbest_fitness:
            gbest_fitness = p.fitness
            gbest_position = p.position[:]

    history = [gbest_fitness]

    for iteration in range(n_iterations):
        for p in particles:
            # 更新速度
            for d in range(n_dims):
                r1 = random.random()
                r2 = random.random()

                cognitive = c1 * r1 * (p.pbest_position[d] - p.position[d])
                social = c2 * r2 * (gbest_position[d] - p.position[d])

                p.velocity[d] = w * p.velocity[d] + cognitive + social

                # 速度限制
                p.velocity[d] = max(-max_velocity, min(max_velocity, p.velocity[d]))

            # 更新位置
            for d in range(n_dims):
                p.position[d] += p.velocity[d]
                # 邊界限制
                p.position[d] = max(low, min(high, p.position[d]))

            # 評估
            p.fitness = fitness_func(p.position)

            # 更新個體最佳
            if p.fitness < p.pbest_fitness:
                p.pbest_fitness = p.fitness
                p.pbest_position = p.position[:]

            # 更新全局最佳
            if p.fitness < gbest_fitness:
                gbest_fitness = p.fitness
                gbest_position = p.position[:]

        history.append(gbest_fitness)

    return gbest_position, gbest_fitness, history


def demo_sphere():
    """Sphere 函數最佳化"""
    print("=== Sphere 函數最佳化 ===\n")
    print("目標：minimize f(x) = Σ x_i²")
    print("全域最佳：x = [0,0,...,0], f = 0\n")

    def fitness(x):
        return sum(xi ** 2 for xi in x)

    best_pos, best_fit, history = particle_swarm_optimization(
        n_dims=3,
        fitness_func=fitness,
        n_particles=20,
        n_iterations=50,
        bounds=(-5.0, 5.0),
        seed=42,
    )

    print(f"最佳位置：{[round(x, 4) for x in best_pos]}")
    print(f"最佳適應度：{best_fit:.6f}")


def demo_rastrigin():
    """Rastrigin 函數最佳化"""
    print("\n=== Rastrigin 函數最佳化 ===\n")
    print("目標：minimize f(x,y) = 20 + x²-10cos(2πx) + y²-10cos(2πy)")
    print("全域最佳：(0, 0), f = 0\n")

    def fitness(point):
        x, y = point
        return 20 + (x**2 - 10*math.cos(2*math.pi*x)) + \
               (y**2 - 10*math.cos(2*math.pi*y))

    best_pos, best_fit, history = particle_swarm_optimization(
        n_dims=2,
        fitness_func=fitness,
        n_particles=30,
        n_iterations=100,
        bounds=(-5.12, 5.12),
        seed=42,
    )

    print(f"最佳位置：x={best_pos[0]:.4f}, y={best_pos[1]:.4f}")
    print(f"最佳適應度：{best_fit:.4f}")


def demo_history():
    """收斂歷史"""
    print("\n=== 收斂歷史 ===\n")

    def fitness(x):
        return sum((xi - 0.5)**2 for xi in x)

    _, _, history = particle_swarm_optimization(
        n_dims=2,
        fitness_func=fitness,
        n_particles=20,
        n_iterations=50,
        bounds=(0.0, 1.0),
        seed=42,
    )

    print(f"{'迭代':>5} | {'最佳適應度':>12} | 收斂曲線")
    print("-" * 50)
    for i in range(0, len(history), 5):
        val = history[i]
        bar = "█" * int(val * 50)
        print(f"{i:>5} | {val:>12.6f} | {bar}")


def demo_parameters():
    """參數影響比較"""
    print("\n=== 參數影響比較 ===\n")

    def fitness(x):
        return x[0]**2 + x[1]**2

    configs = [
        ("w=0.3 (低慣性)", {"w": 0.3}),
        ("w=0.7 (標準)", {"w": 0.7}),
        ("w=0.9 (高慣性)", {"w": 0.9}),
    ]

    for name, params in configs:
        _, fit, _ = particle_swarm_optimization(
            n_dims=2,
            fitness_func=fitness,
            n_particles=20,
            n_iterations=30,
            bounds=(-5.0, 5.0),
            seed=42,
            **params
        )
        print(f"  {name}: f = {fit:.6f}")


if __name__ == "__main__":
    demo_sphere()
    demo_rastrigin()
    demo_history()
    demo_parameters()
