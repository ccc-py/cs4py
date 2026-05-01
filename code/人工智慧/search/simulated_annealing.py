"""
模擬退火演算法 (Simulated Annealing)

歷史背景：
- 1953 年 Nicholas Metropolis 提出 Metropolis 演算法
- 1983 年 Kirkpatrick, Gelatt, Vecchi 將其應用於最佳化問題
- 靈感來自金屬退火過程：加熱後緩慢冷卻使原子排列到最低能量狀態
- 是第一個能有效跳脫局部最佳解的隨機搜尋演算法
- 影響了後續的演化算法和隨機搜尋方法

核心概念：
- 接受惡化解的概率：P = exp(-ΔE / T)，其中 T 為溫度
- 高溫時接受惡化機率大（探索），低溫時機率小（開發）
- 溫度依退火計畫逐漸下降
- 理論上以足夠慢的速度冷卻保證收斂到全域最佳解
"""

from typing import Callable, List, Tuple, Optional
import math
import random


def simulated_annealing(
    current_solution: List[float],
    cost_func: Callable[[List[float]], float],
    neighbor_func: Callable[[List[float]], List[float]],
    initial_temp: float = 1000.0,
    cooling_rate: float = 0.995,
    min_temp: float = 1e-6,
    max_iterations: int = 10000,
    seed: Optional[int] = None,
) -> Tuple[List[float], float, List[float]]:
    """
    模擬退火演算法

    參數：
        current_solution: 初始解
        cost_func: 成本函數（要最小化）
        neighbor_func: 鄰居生成函數
        initial_temp: 初始溫度
        cooling_rate: 冷卻速率（每次乘以這個值）
        min_temp: 最小溫度（停止條件）
        max_iterations: 最大迭代次數
        seed: 隨機種子

    返回：
        (最佳解, 最佳成本, 成本歷史記錄)
    """
    if seed is not None:
        random.seed(seed)

    temp = initial_temp
    current_cost = cost_func(current_solution)

    best_solution = current_solution[:]
    best_cost = current_cost
    history = [current_cost]

    for i in range(max_iterations):
        # 生成鄰居解
        neighbor = neighbor_func(current_solution[:])
        neighbor_cost = cost_func(neighbor)

        # 計算成本變化
        delta = neighbor_cost - current_cost

        # 接受惡化解的概率（Metropolis 準則）
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_solution = neighbor
            current_cost = neighbor_cost

            # 更新全域最佳
            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost

        # 冷卻
        temp *= cooling_rate
        history.append(best_cost)

        # 終止條件
        if temp < min_temp:
            break

    return best_solution, best_cost, history


def acceptance_probability(delta: float, temperature: float) -> float:
    """計算接受惡化解的概率"""
    if delta < 0:
        return 1.0
    return math.exp(-delta / temperature)


def random_neighbor_1d(x: List[float], step_size: float = 0.5) -> List[float]:
    """1D 鄰居生成：在當前解附近隨機擾動"""
    return [xi + random.uniform(-step_size, step_size) for xi in x]


def random_neighbor_2d_opt(x: List[float], step_size: float = 0.3) -> List[float]:
    """2D 鄰居生成（逐漸縮小步長）"""
    return [
        xi + random.gauss(0, step_size) for xi in x
    ]


def demo_1d():
    """1D 函數最佳化：f(x) = x² - 4x + 5（最小值在 x=2，f=1）"""
    print("=== 1D 函數最佳化 ===\n")
    print("目標函數：f(x) = x² - 4x + 5（最小值 x=2, f=1）\n")

    def cost(x):
        return x[0] ** 2 - 4 * x[0] + 5

    initial = [random.uniform(-10, 10)]
    print(f"初始解：x = {initial[0]:.4f}, f(x) = {cost(initial):.4f}")

    best_sol, best_cost, _ = simulated_annealing(
        current_solution=initial,
        cost_func=cost,
        neighbor_func=lambda x: random_neighbor_1d(x, step_size=1.0),
        initial_temp=100.0,
        cooling_rate=0.99,
        max_iterations=5000,
        seed=42,
    )

    print(f"最佳解：x = {best_sol[0]:.4f}, f(x) = {best_cost:.4f}")
    print(f"誤差：{abs(best_cost - 1.0):.6f}")


def demo_2d():
    """2D 函數最佳化：Rastrigin 函數"""
    print("\n=== 2D 函數最佳化（Rastrigin） ===\n")
    print("目標函數：f(x,y) = 20 + x² - 10cos(2πx) + y² - 10cos(2πy)")
    print("全域最小值：(0, 0), f = 0\n")

    def rastrigin(point):
        x, y = point
        return 20 + (x ** 2 - 10 * math.cos(2 * math.pi * x)) + \
               (y ** 2 - 10 * math.cos(2 * math.pi * y))

    initial = [random.uniform(-5, 5), random.uniform(-5, 5)]
    print(f"初始解：{initial}, f = {rastrigin(initial):.4f}")

    best_sol, best_cost, history = simulated_annealing(
        current_solution=initial,
        cost_func=rastrigin,
        neighbor_func=lambda x: random_neighbor_2d_opt(x, step_size=0.5),
        initial_temp=500.0,
        cooling_rate=0.995,
        max_iterations=20000,
        seed=42,
    )

    print(f"最佳解：x={best_sol[0]:.4f}, y={best_sol[1]:.4f}")
    print(f"f(x,y) = {best_cost:.4f}")
    print(f"誤差：{best_cost:.6f}")


def demo_temperature_effect():
    """溫度對接受概率的影響"""
    print("\n=== 溫度效應 ===\n")

    print(f"{'成本差 ΔE':>10} | {'T=1000':>10} | {'T=100':>10} | {'T=10':>10} | {'T=1':>10}")
    print("-" * 60)

    for delta in [0.1, 1, 5, 10, 50, 100]:
        probs = []
        for t in [1000, 100, 10, 1]:
            probs.append(acceptance_probability(delta, t))

        print(f"{delta:>10} | {probs[0]:>10.4f} | {probs[1]:>10.4f} | "
              f"{probs[2]:>10.4f} | {probs[3]:>10.4f}")


def demo_history():
    """收斂歷史展示"""
    print("\n=== 收斂歷史 ===\n")

    def cost(x):
        return (x[0] - 3) ** 2 + (x[1] + 2) ** 2 + 5  # 最小值 5 在 (3, -2)

    initial = [0.0, 0.0]

    _, _, history = simulated_annealing(
        current_solution=initial,
        cost_func=cost,
        neighbor_func=lambda x: random_neighbor_2d_opt(x, step_size=1.0),
        initial_temp=500.0,
        cooling_rate=0.98,
        max_iterations=2000,
        seed=42,
    )

    print("收斂過程（每隔 200 次迭代）：")
    for i in range(0, len(history), 200):
        bar = "█" * int((history[i] - 5) / 10) if history[i] > 5 else ""
        print(f"  迭代 {i:>5}: cost = {history[i]:.2f} {bar}")


if __name__ == "__main__":
    demo_1d()
    demo_2d()
    demo_temperature_effect()
    demo_history()
