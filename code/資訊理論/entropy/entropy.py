"""
資訊理論 - 熵計算模組

實作香農熵、聯合熵、條件熵等資訊度量。
"""

from typing import List, Dict, Tuple
import math


def shannon_entropy(prob_dist: List[float]) -> float:
    """
    計算香農熵 H(X) = -Σ p(x) * log2(p(x))
    
    Args:
        prob_dist: 機率分佈列表，元素和應為 1
        
    Returns:
        熵值（位元）
    """
    return -sum(p * math.log2(p) for p in prob_dist if p > 0)


def joint_entropy(joint_dist: List[List[float]]) -> float:
    """
    計算聯合熵 H(X,Y) = -ΣΣ p(x,y) * log2(p(x,y))
    
    Args:
        joint_dist: 聯合機率分佈的二維列表
        
    Returns:
        聯合熵值
    """
    return -sum(p * math.log2(p) for row in joint_dist for p in row if p > 0)


def marginal_distributions(joint_dist: List[List[float]]) -> Tuple[List[float], List[float]]:
    """
    從聯合分佈計算邊際分佈
    
    Args:
        joint_dist: 聯合機率分佈的二維列表
        
    Returns:
        (邊際分佈 X, 邊際分佈 Y)
    """
    p_x = [sum(row) for row in joint_dist]
    p_y = [sum(joint_dist[i][j] for i in range(len(joint_dist))) 
            for j in range(len(joint_dist[0]))]
    return p_x, p_y


def conditional_entropy(joint_dist: List[List[float]], given: str = 'Y') -> float:
    """
    計算條件熵 H(X|Y) 或 H(Y|X)
    
    Args:
        joint_dist: 聯合機率分佈
        given: 給定哪個變數 ('Y' 表示 H(X|Y)，'X' 表示 H(Y|X))
        
    Returns:
        條件熵值
    """
    n = len(joint_dist)
    m = len(joint_dist[0])
    
    if given == 'Y':
        # H(X|Y) = Σ p(y) * H(X|y)
        p_y = [sum(joint_dist[i][j] for i in range(n)) for j in range(m)]
        h_xy = 0
        for j in range(m):
            if p_y[j] > 0:
                cond_probs = [joint_dist[i][j] / p_y[j] for i in range(n)]
                h_xy += p_y[j] * shannon_entropy(cond_probs)
        return h_xy
    else:
        # H(Y|X) = Σ p(x) * H(Y|x)
        p_x = [sum(joint_dist[i]) for i in range(n)]
        h_yx = 0
        for i in range(n):
            if p_x[i] > 0:
                cond_probs = [joint_dist[i][j] / p_x[i] for j in range(m)]
                h_yx += p_x[i] * shannon_entropy(cond_probs)
        return h_yx


def entropy_discrete(dist: Dict[str, float]) -> float:
    """
    計算離散分佈的熵（使用符號標籤）
    
    Args:
        dist: 符號到機率的映射字典
        
    Returns:
        熵值
    """
    return -sum(p * math.log2(p) for p in dist.values() if p > 0)


if __name__ == "__main__":
    # 示範：公平硬幣
    print("=== 香農熵示範 ===")
    fair_coin = [0.5, 0.5]
    biased_coin = [0.8, 0.2]
    print(f"公平硬幣熵: {shannon_entropy(fair_coin):.4f} bits")
    print(f"偏倚硬幣熵: {shannon_entropy(biased_coin):.4f} bits")
    
    # 示範：聯合熵與條件熵
    print("\n=== 聯合與條件熵示範 ===")
    # 聯合分佈 p(X,Y)
    joint = [
        [0.25, 0.25],  # X=0: Y=0, Y=1
        [0.25, 0.25],  # X=1: Y=0, Y=1
    ]
    print(f"聯合熵 H(X,Y): {joint_entropy(joint):.4f} bits")
    print(f"條件熵 H(X|Y): {conditional_entropy(joint, 'Y'):.4f} bits")
    print(f"條件熵 H(Y|X): {conditional_entropy(joint, 'X'):.4f} bits")
    
    # 示範：離散分佈
    print("\n=== 離散分佈熵示範 ===")
    weather = {'晴天': 0.5, '雨天': 0.3, '陰天': 0.2}
    print(f"天氣分佈熵: {entropy_discrete(weather):.4f} bits")
