"""
蒙地卡羅積分（Monte Carlo Integration）

利用隨機抽樣來估計積分值。對於高維積分，蒙地卡羅方法的
收斂速度與維度無關，這是它相較於確定性方法的最大優勢。
"""

from typing import Callable, Tuple
import random
import math


def monte_carlo_1d(
    f: Callable[[float], float],
    a: float,
    b: float,
    N: int = 10000
) -> Tuple[float, float]:
    """
    使用蒙地卡羅方法計算一維積分 ∫_a^b f(x) dx

    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        N: 抽樣點數

    回傳:
        (integral, error_estimate): 積分估計值和標準誤差
    """
    total = 0.0
    total_sq = 0.0

    for _ in range(N):
        x = random.uniform(a, b)
        fx = f(x)
        total += fx
        total_sq += fx * fx

    mean = total / N
    integral = (b - a) * mean

    # 估計方差和標準誤差
    variance = total_sq / N - mean * mean
    std_error = (b - a) * math.sqrt(variance / N)

    return integral, std_error


def monte_carlo_nd(
    f: Callable[[list], float],
    bounds: list,
    N: int = 10000
) -> Tuple[float, float]:
    """
    使用蒙地卡羅方法計算高維積分

    參數:
        f: 被積函數，接受長度為 d 的列表，回傳 float
        bounds: 每個維度的 [下限, 上限]，形式為 [[a1, b1], [a2, b2], ...]
        N: 抽樣點數

    回傳:
        (integral, error_estimate)
    """
    d = len(bounds)
    volume = 1.0
    for a, b in bounds:
        volume *= (b - a)

    total = 0.0
    total_sq = 0.0

    for _ in range(N):
        x = [random.uniform(a, b) for a, b in bounds]
        fx = f(x)
        total += fx
        total_sq += fx * fx

    mean = total / N
    integral = volume * mean

    variance = total_sq / N - mean * mean
    std_error = volume * math.sqrt(variance / N)

    return integral, std_error


def estimate_pi(N: int = 100000) -> Tuple[float, float]:
    """
    使用蒙地卡羅方法估計 π

    方法：在單位正方形 [0,1]×[0,1] 中均勻抽樣，
    計算落在四分之一圓內的點的比例。

    參數:
        N: 抽樣點數

    回傳:
        (pi_estimate, error_estimate)
    """
    count_inside = 0
    for _ in range(N):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            count_inside += 1

    pi_estimate = 4.0 * count_inside / N
    # 二項分佈的標準差
    p = count_inside / N
    std_error = 4.0 * math.sqrt(p * (1 - p) / N)

    return pi_estimate, std_error


def demo_1d() -> None:
    """一維積分範例"""
    import math
    f = lambda x: math.exp(x)
    a, b = 0.0, 1.0
    exact = math.exp(1) - 1

    N = 10000
    result, error = monte_carlo_1d(f, a, b, N)
    print(f"∫₀¹ e^x dx (N={N}):")
    print(f"  蒙地卡羅估計: {result}")
    print(f"  精確值: {exact}")
    print(f"  誤差: {abs(result - exact)}")
    print(f"  標準誤差: {error}")


def demo_2d() -> None:
    """二維積分範例"""
    # ∫∫_{[0,1]×[0,1]} (x + y) dx dy = 1
    f = lambda xy: xy[0] + xy[1]
    bounds = [[0.0, 1.0], [0.0, 1.0]]

    N = 50000
    result, error = monte_carlo_nd(f, bounds, N)
    exact = 1.0
    print(f"\n∫∫ (x+y) dx dy over [0,1]² (N={N}):")
    print(f"  蒙地卡羅估計: {result}")
    print(f"  精確值: {exact}")
    print(f"  誤差: {abs(result - exact)}")
    print(f"  標準誤差: {error}")


def demo_pi() -> None:
    """估計 π"""
    N = 100000
    pi_est, error = estimate_pi(N)
    print(f"\nπ 的蒙地卡羅估計 (N={N}):")
    print(f"  估計值: {pi_est}")
    print(f"  精確值: {math.pi}")
    print(f"  誤差: {abs(pi_est - math.pi)}")
    print(f"  標準誤差: {error}")


def compare_methods() -> None:
    """比較蒙地卡羅法與確定性方法的精度"""
    import math
    f = lambda x: math.exp(x)
    a, b = 0.0, 1.0
    exact = math.exp(1) - 1

    print("\n比較不同積分方法的精度 (∫₀¹ e^x dx):")
    print(f"  精確值: {exact}")

    # 嘗試使用梯形法則
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from integration.trapezoidal import trapezoidal
        t_result = trapezoidal(f, a, b, n=1000)
        print(f"\n  梯形法則 (n=1000):")
        print(f"    誤差: {abs(t_result - exact):.2e}")
    except ImportError:
        print(f"\n  梯形法則: (比較已跳過)")

    # 嘗試使用 Simpson 法則
    try:
        from integration.simpson import simpson
        s_result = simpson(f, a, b, n=100)
        print(f"  Simpson 法則 (n=100):")
        print(f"    誤差: {abs(s_result - exact):.2e}")
    except ImportError:
        print(f"  Simpson 法則: (比較已跳過)")

    # 蒙地卡羅
    mc_result, mc_error = monte_carlo_1d(f, a, b, N=10000)
    print(f"  蒙地卡羅 (N=10000):")
    print(f"    誤差: {abs(mc_result - exact):.2e}")
    print(f"    標準誤差: {mc_error:.2e}")


if __name__ == "__main__":
    print("=== 蒙地卡羅積分 ===\n")
    demo_1d()
    demo_2d()
    demo_pi()
    compare_methods()
