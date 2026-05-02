"""
資訊理論 - 率失真理論 (Rate-Distortion Theory)

實作率失真函數計算與 Blahut-Arimoto 演算法。
"""

from typing import List, Tuple
import math


def binary_symmetric_distortion(x: int, y: int) -> float:
    """
    二元對稱失真度量：Hamming 距離
    
    Args:
        x: 輸入符號 (0 或 1)
        y: 輸出符號 (0 或 1)
        
    Returns:
        失真值 (0 如果相同，1 如果不同)
    """
    return 0.0 if x == y else 1.0


def rate_distortion_function(p: float, d_max: float, n_iter: int = 100) -> List[Tuple[float, float]]:
    """
    計算二元對稱源的率失真函數 R(D)
    
    對於 Bernoulli(p) 源，失真度量為 Hamming 距離：
    R(D) = H₂(p) - H₂(D)  for 0 ≤ D ≤ min(p, 1-p)
    R(D) = 0              for D ≥ min(p, 1-p)
    
    Args:
        p: 源分佈 P(X=1) = p
        d_max: 最大失真
        n_iter: 迭代次數（預留給 Blahut-Arimoto）
        
    Returns:
        [(D, R(D))] 列表
    """
    d_min = 0.0
    d_bound = min(p, 1 - p)
    
    h_p = _binary_entropy(p)
    results = []
    
    for i in range(100):
        d = d_max * i / 99
        if d >= d_bound:
            r = 0.0
        else:
            h_d = _binary_entropy(d)
            r = h_p - h_d
        results.append((d, r))
    
    return results


def _binary_entropy(p: float) -> float:
    """二元熵 H₂(p) = -p*log2(p) - (1-p)*log2(1-p)"""
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def blahut_arimoto_rd(px: List[float], d_func, beta: float, n_iter: int = 100) -> Tuple[List[List[float]], float]:
    """
    Blahut-Arimoto 演算法求解率失真問題
    
    Args:
        px: 源分佈 P(X=x)
        d_func: 失真函數 d(x,y)
        beta: Lagrange 乘數（控制失真）
        n_iter: 迭代次數
        
    Returns:
        (轉移機率 Q(Y|X), 率失真值)
    """
    n_x = len(px)
    n_y = n_x  # 簡化：假設相同字母表
    
    # 初始化均勻轉移機率
    qyx = [[1.0 / n_y for _ in range(n_x)] for _ in range(n_y)]
    
    for _ in range(n_iter):
        # 計算輔助量
        # c(x,y) = exp(-beta * d(x,y))
        c = [[math.exp(-beta * d_func(i, j)) for j in range(n_x)] 
             for i in range(n_y)]
        
        # 更新 Q(Y|X)
        # q(y|x) = c(y,x) / Σ_y' c(y',x)
        for j in range(n_x):
            total = sum(c[i][j] for i in range(n_y))
            for i in range(n_y):
                qyx[i][j] = c[i][j] / total if total > 0 else 1.0 / n_y
    
    # 計算率失真值
    # R(D) = Σ p(x) Σ q(y|x) log2(q(y|x) / q(y))
    # 其中 q(y) = Σ p(x) q(y|x)
    qy = [sum(px[j] * qyx[i][j] for j in range(n_x)) for i in range(n_y)]
    
    rd = 0.0
    for i in range(n_y):
        for j in range(n_x):
            if px[j] > 0 and qyx[i][j] > 0 and qy[i] > 0:
                rd += px[j] * qyx[i][j] * math.log2(qyx[i][j] / qy[i])
    
    return qyx, rd


def lossy_compression_demo() -> None:
    """展示有損壓縮的理論極限"""
    print("=== 率失真理論示範 ===")
    print("二元對稱源，失真 = Hamming 距離")
    
    p = 0.5  # 均勻 Bernoulli 源
    h_p = _binary_entropy(p)
    print(f"\n源熵 H(X) = H₂({p}) = {h_p:.4f} bits")
    
    print(f"\n{'失真 D':<12} {'速率 R(D)':<12} {'壓縮比'}")
    print("-" * 40)
    
    rd_pairs = rate_distortion_function(p, min(p, 1-p), 10)
    for d, r in rd_pairs[::10]:  # 取樣
        ratio = h_p / r if r > 0 else float('inf')
        print(f"{d:<12.4f} {r:<12.4f} {ratio:<.2f}:1")
    
    print("\n當 D = 0 時，R(D) = H(X)（無損壓縮）")
    print("當 D 增加，R(D) 減少（允許失真可提昇壓縮率）")


if __name__ == "__main__":
    lossy_compression_demo()
    
    # 示範 Blahut-Arimoto
    print("\n=== Blahut-Arimoto 演算法示範 ===")
    px = [0.5, 0.5]
    qyx, rd = blahut_arimoto_rd(px, binary_symmetric_distortion, beta=1.0)
    print(f"轉移機率矩陣:")
    for i in range(len(qyx)):
        print(f"  {qyx[i]}")
    print(f"率失真值: {rd:.4f} bits")
