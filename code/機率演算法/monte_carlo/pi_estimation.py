"""
π 估計 (Pi Estimation)

使用蒙地卡羅方法估計圓周率 π 的數值。
包含擲飛鏢法 (Dart Throwing) 和布豐投針法 (Buffon's Needle)。
"""

import random
import math
from typing import Tuple, List


def estimate_pi_dart_throwing(n_darts: int = 10000) -> float:
    """
    使用擲飛鏢法估計 π
    
    在單位正方形 [0,1]×[0,1] 內隨機投擲飛鏢，
    計算落在四分之一圓內的比例。
    
    參數:
        n_darts: 投擲次數
    
    返回:
        π 的估計值
    """
    inside = 0
    for _ in range(n_darts):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x * x + y * y <= 1:
            inside += 1
    return 4.0 * inside / n_darts


def estimate_pi_dart_throwing_with_history(
    n_darts: int = 10000,
    record_interval: int = 1000
) -> Tuple[float, List[Tuple[int, float]]]:
    """
    擲飛鏢法估計 π，並記錄收斂過程
    
    參數:
        n_darts: 總投擲次數
        record_interval: 記錄間隔
    
    返回:
        (最終估計值, [(迭代次數, 當前估計值), ...])
    """
    inside = 0
    history = []
    for i in range(1, n_darts + 1):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x * x + y * y <= 1:
            inside += 1
        if i % record_interval == 0:
            history.append((i, 4.0 * inside / i))
    return 4.0 * inside / n_darts, history


def buffon_needle(
    n_needles: int = 10000,
    needle_length: float = 1.0,
    line_spacing: float = 2.0
) -> float:
    """
    布豐投針法估計 π
    
    在平面上畫平行線，間距為 d，隨機投擲長度為 l 的針，
    針與線相交的機率為 2l/(πd)，藉此估計 π。
    
    參數:
        n_needles: 投擲針數
        needle_length: 針的長度 l
        line_spacing: 平行線間距 d
    
    返回:
        π 的估計值
    """
    hits = 0
    for _ in range(n_needles):
        # 針中心到最近直線的距離
        y = random.uniform(0, line_spacing / 2)
        # 針與平行線的夾角
        theta = random.uniform(0, math.pi / 2)
        # 針在垂直方向的投影一半
        projection = (needle_length / 2) * math.sin(theta)
        if y <= projection:
            hits += 1
    
    if hits == 0:
        return float('inf')
    return 2.0 * needle_length * n_needles / (line_spacing * hits)


def estimate_pi_with_convergence(n_runs: int = 5, n_darts: int = 10000) -> List[float]:
    """
    多次執行取平均，觀察收斂性
    
    參數:
        n_runs: 執行次數
        n_darts: 每次投擲次數
    
    返回:
        每次的估計值列表
    """
    return [estimate_pi_dart_throwing(n_darts) for _ in range(n_runs)]


def calculate_error(pi_estimate: float) -> float:
    """
    計算與真實 π 的誤差
    
    參數:
        pi_estimate: π 的估計值
    
    返回:
        絕對誤差
    """
    return abs(pi_estimate - math.pi)


if __name__ == "__main__":
    print("=== π 估計測試 ===\n")
    
    # 測試 1: 擲飛鏢法
    print("1. 擲飛鏢法 (Dart Throwing)")
    for n in [1000, 5000, 10000, 50000, 100000]:
        pi_est = estimate_pi_dart_throwing(n)
        error = calculate_error(pi_est)
        print(f"   n={n:>6d}: π ≈ {pi_est:.6f}, 誤差 = {error:.6f}")
    
    # 測試 2: 布豐投針法
    print(f"\n2. 布豐投針法 (Buffon's Needle)")
    for n in [1000, 5000, 10000, 50000]:
        pi_est = buffon_needle(n, needle_length=1.0, line_spacing=2.0)
        error = calculate_error(pi_est)
        print(f"   n={n:>6d}: π ≈ {pi_est:.6f}, 誤差 = {error:.6f}")
    
    # 測試 3: 收斂過程
    print(f"\n3. 收斂過程 (n=10000, 每 1000 次記錄)")
    final_pi, history = estimate_pi_dart_throwing_with_history(10000, 1000)
    for i, (n, est) in enumerate(history):
        print(f"   n={n:>5d}: π ≈ {est:.6f}")
    print(f"   最終估計: π ≈ {final_pi:.6f}")
    
    # 測試 4: 多次執行統計
    print(f"\n4. 多次執行統計 (執行 10 次，每次 10000 次投擲)")
    estimates = estimate_pi_with_convergence(10, 10000)
    mean_est = sum(estimates) / len(estimates)
    variance = sum((x - mean_est) ** 2 for x in estimates) / (len(estimates) - 1)
    print(f"   平均估計: {mean_est:.6f}")
    print(f"   標準差:   {math.sqrt(variance):.6f}")
    print(f"   真實 π:   {math.pi:.6f}")
