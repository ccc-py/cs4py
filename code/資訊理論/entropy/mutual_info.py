"""
資訊理論 - 互資訊與相關度量

實作互資訊、KL 散度、交叉熵等資訊度量。
"""

from typing import List
import math


def mutual_information(joint_dist: List[List[float]]) -> float:
    """
    計算互資訊 I(X;Y) = ΣΣ p(x,y) * log2(p(x,y) / (p(x)*p(y)))
    
    Args:
        joint_dist: 聯合機率分佈的二維列表
        
    Returns:
        互資訊值
    """
    n = len(joint_dist)
    m = len(joint_dist[0])
    
    # 計算邊際分佈
    p_x = [sum(joint_dist[i]) for i in range(n)]
    p_y = [sum(joint_dist[i][j] for i in range(n)) for j in range(m)]
    
    mi = 0.0
    for i in range(n):
        for j in range(m):
            p_xy = joint_dist[i][j]
            if p_xy > 0 and p_x[i] > 0 and p_y[j] > 0:
                mi += p_xy * math.log2(p_xy / (p_x[i] * p_y[j]))
    return mi


def kl_divergence(p: List[float], q: List[float]) -> float:
    """
    計算 KL 散度（相對熵） D_KL(P||Q) = Σ p(x) * log2(p(x)/q(x))
    
    Args:
        p: 真實分佈
        q: 近似分佈
        
    Returns:
        KL 散度值（非對稱）
    """
    return sum(p[i] * math.log2(p[i] / q[i]) 
               for i in range(len(p)) if p[i] > 0 and q[i] > 0)


def cross_entropy(p: List[float], q: List[float]) -> float:
    """
    計算交叉熵 H(P,Q) = -Σ p(x) * log2(q(x))
    
    Args:
        p: 真實分佈
        q: 預測分佈
        
    Returns:
        交叉熵值
    """
    return -sum(p[i] * math.log2(q[i]) 
                for i in range(len(p)) if p[i] > 0 and q[i] > 0)


def joint_mutual_information(joint_dist: List[List[float]]) -> Tuple[float, float, float]:
    """
    計算聯合分佈的各種資訊度量
    
    Args:
        joint_dist: 聯合機率分佈
        
    Returns:
        (互資訊, KL散度(P||Q), 交叉熵)
    """
    n = len(joint_dist)
    m = len(joint_dist[0])
    
    # 邊際分佈
    p_x = [sum(joint_dist[i]) for i in range(n)]
    p_y = [sum(joint_dist[i][j] for i in range(n)) for j in range(m)]
    
    # 假設獨立分佈 Q(x,y) = P(x)*P(y)
    mi = mutual_information(joint_dist)
    
    # KL(P||Q) where Q is product of marginals
    kl = 0.0
    for i in range(n):
        for j in range(m):
            p_xy = joint_dist[i][j]
            q_xy = p_x[i] * p_y[j]
            if p_xy > 0 and q_xy > 0:
                kl += p_xy * math.log2(p_xy / q_xy)
    
    # 交叉熵 H(P,Q)
    ce = 0.0
    for i in range(n):
        for j in range(m):
            p_xy = joint_dist[i][j]
            q_xy = p_x[i] * p_y[j]
            if p_xy > 0 and q_xy > 0:
                ce += -p_xy * math.log2(q_xy)
    
    return mi, kl, ce


if __name__ == "__main__":
    # 示範：互資訊
    print("=== 互資訊示範 ===")
    # 獨立變數
    independent = [[0.25, 0.25], [0.25, 0.25]]
    print(f"獨立變數互資訊: {mutual_information(independent):.4f} bits")
    
    # 相關變數
    correlated = [[0.5, 0.0], [0.0, 0.5]]
    print(f"完全相關互資訊: {mutual_information(correlated):.4f} bits")
    
    # 示範：KL 散度與交叉熵
    print("\n=== KL 散度與交叉熵示範 ===")
    p = [0.5, 0.5]
    q_close = [0.5, 0.5]
    q_far = [0.8, 0.2]
    print(f"KL(P||Q) 相同分佈: {kl_divergence(p, q_close):.4f}")
    print(f"KL(P||Q) 不同分佈: {kl_divergence(p, q_far):.4f}")
    print(f"交叉熵 H(P,Q): {cross_entropy(p, q_far):.4f} bits")
    
    # 示範：聯合分佈分析
    print("\n=== 聯合分佈資訊度量 ===")
    mi, kl, ce = joint_mutual_information(correlated)
    print(f"互資訊: {mi:.4f}, KL散度: {kl:.4f}, 交叉熵: {ce:.4f}")
