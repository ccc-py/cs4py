"""
馬可夫鏈蒙地卡羅 (MCMC)

使用馬可夫鏈從複雜分佈中抽樣，包含 Metropolis-Hastings 演算法
和 Gibbs 抽樣。
"""

import random
import math
from typing import Callable, List, Tuple, Any, Optional


def metropolis_hastings(
    target_log_pdf: Callable[[float], float],
    proposal_sampler: Callable[[float], float],
    initial: float,
    n_samples: int = 10000,
    burn_in: int = 1000
) -> List[float]:
    """
    Metropolis-Hastings 演算法
    
    從目標分佈 π(x) ∝ exp(log_π(x)) 抽樣，
    使用提議分佈 q(x'|x) 產生候選樣本。
    
    參數:
        target_log_pdf: 目標分佈的對數機率密度函數 log π(x)
        proposal_sampler: 提議分佈 q(x'|x)，給定當前 x 產生下一個候選
        initial: 初始值
        n_samples: 需要的樣本數（不含 burn-in）
        burn_in: 捨棄的前 burn_in 個樣本
    
    返回:
        抽樣結果列表
    """
    samples = []
    current = initial
    current_log_pdf = target_log_pdf(current)
    accepted = 0
    
    total_iterations = burn_in + n_samples
    for i in range(total_iterations):
        # 從提議分佈產生候選
        candidate = proposal_sampler(current)
        
        # 計算接受機率
        candidate_log_pdf = target_log_pdf(candidate)
        
        # log 接受比: log(π(x')q(x|x') / π(x)q(x'|x))
        # 對稱提議分佈時 q(x'|x) = q(x|x')，簡化為 log(π(x')/π(x))
        log_accept_ratio = candidate_log_pdf - current_log_pdf
        
        # 接受或拒絕
        if log_accept_ratio >= 0 or random.random() < math.exp(log_accept_ratio):
            current = candidate
            current_log_pdf = candidate_log_pdf
            if i >= burn_in:
                accepted += 1
        
        if i >= burn_in:
            samples.append(current)
    
    acceptance_rate = accepted / n_samples if n_samples > 0 else 0
    print(f"   Metropolis-Hastings 接受率: {acceptance_rate:.2%}")
    
    return samples


def metropolis_hastings_symmetric(
    target_log_pdf: Callable[[float], float],
    proposal_std: float,
    initial: float,
    n_samples: int = 10000,
    burn_in: int = 1000
) -> List[float]:
    """
    使用對稱提議分佈（常態分佈）的 Metropolis-Hastings
    
    參數:
        target_log_pdf: 目標分佈的對數機率密度
        proposal_std: 提議分佈的標準差
        initial: 初始值
        n_samples: 樣本數
        burn_in: 捨棄樣本數
    
    返回:
        抽樣結果
    """
    def proposal_sampler(x: float) -> float:
        return random.gauss(x, proposal_std)
    
    return metropolis_hastings(
        target_log_pdf, proposal_sampler, initial, n_samples, burn_in
    )


def gibbs_sampling(
    n_vars: int,
    conditional_samplers: List[Callable[[List[float]], float]],
    initial: List[float],
    n_samples: int = 10000,
    burn_in: int = 1000
) -> List[List[float]]:
    """
    Gibbs 抽樣
    
    當可以從每個變數的條件分佈抽樣時使用。
    依序更新每個變數，給定其他變數的值。
    
    參數:
        n_vars: 變數數量
        conditional_samplers: 列表，第 i 個元素是從 p(x_i | x_{-i}) 抽樣的函數
        initial: 初始值
        n_samples: 樣本數
        burn_in: 捨棄樣本數
    
    返回:
        樣本列表，每個樣本是一個 list[float]
    """
    samples = []
    current = initial.copy()
    
    total_iterations = burn_in + n_samples
    for i in range(total_iterations):
        # 依序更新每個變數
        for j in range(n_vars):
            current[j] = conditional_samplers[j](current)
        
        if i >= burn_in:
            samples.append(current.copy())
    
    return samples


def sample_normal_mixture(
    n_samples: int = 10000,
    burn_in: int = 1000
) -> List[float]:
    """
    從混合常態分佈抽樣的範例
    
    目標: 0.3 * N(-2, 0.5) + 0.7 * N(2, 0.5)
    
    參數:
        n_samples: 樣本數
        burn_in: 捨棄樣本數
    
    返回:
        抽樣結果
    """
    def target_log_pdf(x: float) -> float:
        # 混合分佈的對數密度
        p1 = 0.3 * math.exp(-0.5 * ((x + 2) ** 2) / 0.5) / math.sqrt(2 * math.pi * 0.5)
        p2 = 0.7 * math.exp(-0.5 * ((x - 2) ** 2) / 0.5) / math.sqrt(2 * math.pi * 0.5)
        return math.log(p1 + p2)
    
    return metropolis_hastings_symmetric(
        target_log_pdf, proposal_std=1.0, 
        initial=0.0, n_samples=n_samples, burn_in=burn_in
    )


def sample_bivariate_normal(
    n_samples: int = 10000,
    burn_in: int = 1000
) -> List[List[float]]:
    """
    從二元常態分佈抽樣 (使用 Gibbs 抽樣)
    
    參數:
        n_samples: 樣本數
        burn_in: 捨棄樣本數
    
    返回:
        二元樣本列表
    """
    # 目標: N(μ, Σ) 其中 μ = [0, 0], Σ = [[1, ρ], [ρ, 1]]
    rho = 0.8
    mean1, mean2 = 0.0, 0.0
    var1, var2 = 1.0, 1.0
    
    def sample_x2_given_x1(state: List[float]) -> float:
        x1 = state[0]
        # p(x2|x1) ~ N(μ2 + ρ(x1-μ1), 1-ρ²)
        cond_mean = mean2 + rho * (x1 - mean1)
        cond_std = math.sqrt((1 - rho ** 2) * var2)
        return random.gauss(cond_mean, cond_std)
    
    def sample_x1_given_x2(state: List[float]) -> float:
        x2 = state[1]
        # p(x1|x2) ~ N(μ1 + ρ(x2-μ2), 1-ρ²)
        cond_mean = mean1 + rho * (x2 - mean2)
        cond_std = math.sqrt((1 - rho ** 2) * var1)
        return random.gauss(cond_mean, cond_std)
    
    conditional_samplers = [sample_x1_given_x2, sample_x2_given_x1]
    
    return gibbs_sampling(
        2, conditional_samplers, [0.0, 0.0], n_samples, burn_in
    )


def estimate_mean(samples: List[float]) -> float:
    """估計樣本平均"""
    return sum(samples) / len(samples)


def estimate_variance(samples: List[float]) -> float:
    """估計樣本變異數"""
    n = len(samples)
    mean = estimate_mean(samples)
    return sum((x - mean) ** 2 for x in samples) / (n - 1)


if __name__ == "__main__":
    print("=== MCMC 測試 ===\n")
    
    # 測試 1: 從標準常態分佈抽樣
    print("1. Metropolis-Hastings: 標準常態分佈 N(0,1)")
    def normal_log_pdf(x: float) -> float:
        return -0.5 * x ** 2  # 忽略常數項
    
    samples = metropolis_hastings_symmetric(
        normal_log_pdf, proposal_std=1.0, 
        initial=0.0, n_samples=5000, burn_in=500
    )
    mean = estimate_mean(samples)
    var = estimate_variance(samples)
    print(f"   樣本平均: {mean:.4f} (理論: 0.0)")
    print(f"   樣本變異數: {var:.4f} (理論: 1.0)")
    
    # 測試 2: 混合常態分佈
    print(f"\n2. 混合常態分佈抽樣")
    print(f"   目標: 0.3*N(-2,0.5) + 0.7*N(2,0.5)")
    samples_mix = sample_normal_mixture(n_samples=5000, burn_in=500)
    mean_mix = estimate_mean(samples_mix)
    print(f"   樣本平均: {mean_mix:.4f} (理論: 0.3*(-2) + 0.7*2 = 0.8)")
    
    # 計算雙峰性
    below_zero = sum(1 for x in samples_mix if x < 0) / len(samples_mix)
    print(f"   負值比例: {below_zero:.2%} (理論: ~30%)")
    
    # 測試 3: Gibbs 抽樣 - 二元常態
    print(f"\n3. Gibbs 抽樣: 二元常態 (ρ=0.8)")
    samples_bv = sample_bivariate_normal(n_samples=5000, burn_in=500)
    mean_x1 = sum(s[0] for s in samples_bv) / len(samples_bv)
    mean_x2 = sum(s[1] for s in samples_bv) / len(samples_bv)
    print(f"   X1 平均: {mean_x1:.4f} (理論: 0.0)")
    print(f"   X2 平均: {mean_x2:.4f} (理論: 0.0)")
    
    # 計算樣本相關係數
    cov = sum((s[0] - mean_x1) * (s[1] - mean_x2) for s in samples_bv) / (len(samples_bv) - 1)
    var1 = sum((s[0] - mean_x1) ** 2 for s in samples_bv) / (len(samples_bv) - 1)
    var2 = sum((s[1] - mean_x2) ** 2 for s in samples_bv) / (len(samples_bv) - 1)
    corr = cov / math.sqrt(var1 * var2)
    print(f"   相關係數: {corr:.4f} (理論: 0.8)")
    
    # 測試 4: 不同提議分佈參數的影響
    print(f"\n4. 提議分佈標準差的影響")
    print(f"   {'標準差':>8} {'接受率':>10} {'平均':>10} {'變異數':>10}")
    for std in [0.1, 0.5, 1.0, 2.0, 5.0]:
        samples_test = metropolis_hastings_symmetric(
            normal_log_pdf, proposal_std=std,
            initial=0.0, n_samples=2000, burn_in=500
        )
        # 重新計算接受率
        mean_t = estimate_mean(samples_test)
        var_t = estimate_variance(samples_test)
        # 注意: metropolis_hastings_symmetric 內部會印出接受率
        print(f"   {std:>8.1f}: ", end="")
        print(f"平均={mean_t:.4f}, 變異數={var_t:.4f}")
