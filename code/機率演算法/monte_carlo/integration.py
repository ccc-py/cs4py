"""
蒙地卡羅積分 (Monte Carlo Integration)

使用隨機抽樣來估計定積分的數值方法。
相比傳統數值積分方法，在高維度問題上具有優勢。
"""

import random
from typing import Callable, Tuple, List


def monte_carlo_integration(
    f: Callable[[float], float],
    a: float,
    b: float,
    n_samples: int = 10000
) -> float:
    """
    使用蒙地卡羅方法估計定積分 ∫_a^b f(x) dx
    
    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n_samples: 抽樣數量
    
    返回:
        積分的估計值
    """
    total = 0.0
    for _ in range(n_samples):
        x = random.uniform(a, b)
        total += f(x)
    return (b - a) * total / n_samples


def monte_carlo_integration_2d(
    f: Callable[[float, float], float],
    x_range: Tuple[float, float],
    y_range: Tuple[float, float],
    n_samples: int = 10000
) -> float:
    """
    二維蒙地卡羅積分 ∫∫ f(x,y) dx dy
    
    參數:
        f: 二元函數
        x_range: x 的積分範圍 (x_min, x_max)
        y_range: y 的積分範圍 (y_min, y_max)
        n_samples: 抽樣數量
    
    返回:
        積分的估計值
    """
    x_min, x_max = x_range
    y_min, y_max = y_range
    total = 0.0
    for _ in range(n_samples):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        total += f(x, y)
    area = (x_max - x_min) * (y_max - y_min)
    return area * total / n_samples


def stratified_sampling(
    f: Callable[[float], float],
    a: float,
    b: float,
    n_samples: int = 10000,
    n_strata: int = 10
) -> float:
    """
    分層抽樣 (Stratified Sampling) - 減少變異數
    
    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n_samples: 總抽樣數量
        n_strata: 分層數量
    
    返回:
        積分的估計值
    """
    stratum_size = (b - a) / n_strata
    samples_per_stratum = n_samples // n_strata
    total = 0.0
    
    for i in range(n_strata):
        stratum_start = a + i * stratum_size
        stratum_end = stratum_start + stratum_size
        stratum_sum = 0.0
        for _ in range(samples_per_stratum):
            x = random.uniform(stratum_start, stratum_end)
            stratum_sum += f(x)
        total += stratum_size * stratum_sum / samples_per_stratum
    
    return total


def importance_sampling(
    f: Callable[[float], float],
    g: Callable[[float], float],
    g_sampler: Callable[[], float],
    a: float,
    b: float,
    n_samples: int = 10000
) -> float:
    """
    重要性抽樣 (Importance Sampling) - 對低機率區域加權
    
    參數:
        f: 被積函數 f(x)
        g: 提議分佈的密度函數 g(x)，滿足 ∫_a^b g(x) dx = 1
        g_sampler: 從 g(x) 抽樣的函數
        a: 積分下限
        b: 積分上限
        n_samples: 抽樣數量
    
    返回:
        積分的估計值
    """
    total = 0.0
    for _ in range(n_samples):
        x = g_sampler()
        if a <= x <= b:
            total += f(x) / g(x)
    return total / n_samples


def trapezoidal_rule(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 1000
) -> float:
    """
    梯形法則 (Trapezoidal Rule) - 傳統數值積分方法
    
    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n: 區間數量
    
    返回:
        積分的估計值
    """
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return h * total


def estimate_variance(
    estimates: List[float]
) -> float:
    """
    估計多次蒙地卡羅積分的變異數
    
    參數:
        estimates: 多次估計的結果列表
    
    返回:
        變異數估計值
    """
    n = len(estimates)
    mean = sum(estimates) / n
    return sum((x - mean) ** 2 for x in estimates) / (n - 1)


if __name__ == "__main__":
    # 測試函數: f(x) = x^2，在 [0, 1] 的積分為 1/3
    def f(x: float) -> float:
        return x ** 2
    
    # 測試函數: sin(x)，在 [0, π] 的積分為 2
    import math
    
    def g(x: float) -> float:
        return math.sin(x)
    
    print("=== 蒙地卡羅積分測試 ===\n")
    
    # 測試 1: f(x) = x^2 在 [0, 1]
    print("1. ∫_0^1 x^2 dx = 1/3 ≈ 0.3333")
    print(f"   蒙地卡羅 (n=10000):    {monte_carlo_integration(f, 0, 1, 10000):.6f}")
    print(f"   分層抽樣 (n=10000):     {stratified_sampling(f, 0, 1, 10000, 10):.6f}")
    print(f"   梯形法則 (n=1000):      {trapezoidal_rule(f, 0, 1, 1000):.6f}")
    
    # 測試 2: sin(x) 在 [0, π]
    print(f"\n2. ∫_0^π sin(x) dx = 2")
    print(f"   蒙地卡羅 (n=10000):    {monte_carlo_integration(g, 0, math.pi, 10000):.6f}")
    print(f"   梯形法則 (n=1000):      {trapezoidal_rule(g, 0, math.pi, 1000):.6f}")
    
    # 測試 3: 變異數比較
    print(f"\n3. 變異數比較 (f(x)=x^2, [0,1], 各執行 100 次)")
    mc_estimates = [monte_carlo_integration(f, 0, 1, 1000) for _ in range(100)]
    strat_estimates = [stratified_sampling(f, 0, 1, 1000, 10) for _ in range(100)]
    print(f"   蒙地卡羅變異數:   {estimate_variance(mc_estimates):.8f}")
    print(f"   分層抽樣變異數:   {estimate_variance(strat_estimates):.8f}")
    
    # 測試 4: 二維積分 ∫∫ x*y dx dy, x∈[0,1], y∈[0,1] = 1/4
    def h(x: float, y: float) -> float:
        return x * y
    
    print(f"\n4. ∫_0^1∫_0^1 x*y dx dy = 1/4 = 0.25")
    result = monte_carlo_integration_2d(h, (0, 1), (0, 1), 20000)
    print(f"   二維蒙地卡羅 (n=20000): {result:.6f}")
