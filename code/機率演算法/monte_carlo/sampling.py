"""
蒙地卡羅抽樣方法 (Sampling Methods)

包含重要性抽樣 (Importance Sampling) 和拒絕抽樣 (Rejection Sampling)
等減少蒙地卡羅變異數的技術。
"""

import random
import math
from typing import Callable, Tuple, Optional


def uniform_sampler(a: float, b: float) -> Callable[[], float]:
    """
    建立均勻分佈抽樣器
    
    參數:
        a: 下限
        b: 上限
    
    返回:
        抽樣函數
    """
    return lambda: random.uniform(a, b)


def rejection_sampling(
    target_pdf: Callable[[float], float],
    proposal_sampler: Callable[[], float],
    proposal_pdf: Callable[[float], float],
    M: float,
    n_samples: int = 1000
) -> list[float]:
    """
    拒絕抽樣 (Rejection Sampling)
    
    從目標分佈 p(x) 抽樣，使用提議分佈 q(x) 滿足 p(x) ≤ M·q(x)。
    
    參數:
        target_pdf: 目標機率密度函數 p(x)
        proposal_sampler: 從提議分佈抽樣的函數
        proposal_pdf: 提議分佈的機率密度函數 q(x)
        M: 常數，滿足 p(x) ≤ M·q(x) 對所有 x
        n_samples: 需要的樣本數
    
    返回:
        抽樣結果列表
    """
    samples = []
    while len(samples) < n_samples:
        x = proposal_sampler()
        u = random.uniform(0, 1)
        # 接受機率: p(x) / (M * q(x))
        accept_prob = target_pdf(x) / (M * proposal_pdf(x))
        if u <= accept_prob:
            samples.append(x)
    return samples


def importance_sampling_estimate(
    integrand: Callable[[float], float],
    target_pdf: Callable[[float], float],
    proposal_sampler: Callable[[], float],
    proposal_pdf: Callable[[float], float],
    n_samples: int = 10000
) -> float:
    """
    重要性抽樣估計
    
    估計 ∫ f(x)p(x) dx，其中 p(x) 是目標分佈，
    但從提議分佈 q(x) 抽樣。
    
    參數:
        integrand: 被積函數 f(x)
        target_pdf: 目標分佈 p(x)
        proposal_sampler: 從提議分佈抽樣
        proposal_pdf: 提議分佈 q(x)
        n_samples: 抽樣數量
    
    返回:
        積分估計值
    """
    total = 0.0
    for _ in range(n_samples):
        x = proposal_sampler()
        weight = target_pdf(x) / proposal_pdf(x)  # 重要性權重
        total += integrand(x) * weight
    return total / n_samples


def latin_hypercube_sampling(
    n_samples: int,
    n_dimensions: int,
    bounds: Optional[list[Tuple[float, float]]] = None
) -> list[list[float]]:
    """
    拉丁超立方抽樣 (Latin Hypercube Sampling)
    
    確保在每個維度的每個區間內恰好有一個樣本。
    
    參數:
        n_samples: 樣本數
        n_dimensions: 維度數
        bounds: 每個維度的範圍 [(min, max), ...]，預設 [0,1]
    
    返回:
        樣本列表，每個樣本是一個 list[float]
    """
    if bounds is None:
        bounds = [(0.0, 1.0)] * n_dimensions
    
    samples = []
    # 為每個維度建立排列
    permutations = [random.sample(range(n_samples), n_samples) 
                    for _ in range(n_dimensions)]
    
    for i in range(n_samples):
        sample = []
        for d in range(n_dimensions):
            # 在區間內隨機位置
            bin_idx = permutations[d][i]
            lower, upper = bounds[d]
            x = (bin_idx + random.random()) / n_samples
            x = lower + x * (upper - lower)
            sample.append(x)
        samples.append(sample)
    
    return samples


def control_variates(
    f: Callable[[float], float],
    g: Callable[[float], float],
    g_integral: float,
    a: float,
    b: float,
    n_samples: int = 10000
) -> float:
    """
    控制變量法 (Control Variates)
    
    使用已知積分的輔助函數 g(x) 來減少估計變異數。
    
    參數:
        f: 目標函數
        g: 控制函數（已知其積分值）
        g_integral: ∫_a^b g(x) dx 的已知值
        a: 積分下限
        b: 積分上限
        n_samples: 抽樣數量
    
    返回:
        積分估計值
    """
    # 估計最佳係數 c
    # 簡化版本：使用樣本共變異數
    f_samples = []
    g_samples = []
    
    for _ in range(n_samples):
        x = random.uniform(a, b)
        f_samples.append(f(x))
        g_samples.append(g(x))
    
    # 計算樣本共變異數和 g 的變異數
    mean_f = sum(f_samples) / n_samples
    mean_g = sum(g_samples) / n_samples
    
    cov_fg = sum((f_samples[i] - mean_f) * (g_samples[i] - mean_g) 
                 for i in range(n_samples)) / (n_samples - 1)
    var_g = sum((g_i - mean_g) ** 2 for g_i in g_samples) / (n_samples - 1)
    
    # 最佳係數
    c = cov_fg / var_g if var_g > 0 else 0
    
    # 控制變量估計
    f_estimate = (b - a) * sum(f_samples) / n_samples
    g_estimate = (b - a) * sum(g_samples) / n_samples
    
    return f_estimate - c * (g_estimate - g_integral)


if __name__ == "__main__":
    print("=== 蒙地卡羅抽樣方法測試 ===\n")
    
    # 測試 1: 拒絕抽樣 - 從 Beta(2,2) 分佈抽樣
    print("1. 拒絕抽樣 - Beta(2,2) 分佈")
    def beta_pdf(x: float) -> float:
        if 0 <= x <= 1:
            return 6 * x * (1 - x)  # Beta(2,2) 的 PDF (未正規化)
        return 0.0
    
    uniform_samp = uniform_sampler(0, 1)
    def uniform_pdf(x: float) -> float:
        return 1.0 if 0 <= x <= 1 else 0.0
    
    samples = rejection_sampling(beta_pdf, uniform_samp, uniform_pdf, M=1.5, n_samples=1000)
    mean = sum(samples) / len(samples)
    print(f"   樣本數: {len(samples)}, 平均: {mean:.4f} (理論值: 0.5)")
    
    # 測試 2: 重要性抽樣
    print(f"\n2. 重要性抽樣 - 估計 ∫_0^1 e^x dx = e - 1 ≈ {math.e - 1:.4f}")
    
    def exp_integrand(x: float) -> float:
        return math.exp(x)
    
    def uniform_pdf2(x: float) -> float:
        return 1.0
    
    result = importance_sampling_estimate(
        exp_integrand, uniform_pdf2, 
        uniform_sampler(0, 1), uniform_pdf2,
        n_samples=10000
    )
    print(f"   估計值: {result:.6f}")
    
    # 測試 3: 拉丁超立方抽樣
    print(f"\n3. 拉丁超立方抽樣 (2D, 10 個樣本)")
    lhs_samples = latin_hypercube_sampling(10, 2)
    print(f"   樣本數: {len(lhs_samples)}")
    for i, s in enumerate(lhs_samples[:5]):
        print(f"   樣本 {i+1}: {s}")
    
    # 測試 4: 控制變量法
    print(f"\n4. 控制變量法")
    def f(x: float) -> float:
        return x ** 2 + 0.1 * x
    
    def g(x: float) -> float:
        return x  # 已知 ∫_0^1 x dx = 0.5
    
    result_cv = control_variates(f, g, 0.5, 0, 1, 10000)
    # 真實值: ∫_0^1 (x^2 + 0.1x) dx = 1/3 + 0.05 = 0.3833...
    print(f"   控制變量估計: {result_cv:.6f}")
    print(f"   真實值: {1/3 + 0.05:.6f}")
