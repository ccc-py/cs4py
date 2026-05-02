"""
資訊理論 - 通道容量計算

實作通道容量計算、香農第二定理、離散無記憶通道容量。
"""

from typing import List, Tuple
import math


def channel_capacity_bsc(p_error: float) -> float:
    """
    計算二元對稱通道 (BSC) 的容量
    
    BSC: 傳輸正確機率 1-p，錯誤機率 p
    容量 C = 1 - H₂(p) = 1 + p*log₂(p) + (1-p)*log₂(1-p)
    
    Args:
        p_error: 錯誤機率 p (0 ≤ p ≤ 1)
        
    Returns:
        通道容量（位元/符號）
    """
    if p_error == 0 or p_error == 1:
        return 1.0
    h = -p_error * math.log2(p_error) - (1 - p_error) * math.log2(1 - p_error)
    return 1.0 - h


def channel_capacity_bec(p_erase: float) -> float:
    """
    計算二元擦除通道 (BEC) 的容量
    
    BEC: 擦除機率 p，正確機率 1-p
    容量 C = 1 - p
    
    Args:
        p_erase: 擦除機率 p (0 ≤ p ≤ 1)
        
    Returns:
        通道容量（位元/符號）
    """
    return 1.0 - p_erase


def dmc_capacity(transition_matrix: List[List[float]]) -> float:
    """
    計算離散無記憶通道 (DMC) 的容量
    
    使用 Blahut-Arimoto 演算法近似計算。
    對於給定的轉移機率矩陣 W(y|x)，容量為：
    C = max_{p(x)} I(X;Y)
    
    Args:
        transition_matrix: 轉移機率矩陣 W[y][x] = P(Y=y|X=x)
                          shape: [n_outputs, n_inputs]
        
    Returns:
        通道容量（位元/符號）
    """
    n_inputs = len(transition_matrix[0])
    n_outputs = len(transition_matrix)
    
    # 初始化均勻輸入分佈
    p_x = [1.0 / n_inputs] * n_inputs
    
    # Blahut-Arimoto 迭代
    for _ in range(100):
        # 計算聯合分佈 p(x,y) = p(x) * W(y|x)
        p_xy = [[p_x[x] * transition_matrix[y][x] 
                 for x in range(n_inputs)] 
                for y in range(n_outputs)]
        
        # 計算邊際 p(y)
        p_y = [sum(p_xy[y][x] for x in range(n_inputs)) 
               for y in range(n_outputs)]
        
        # 更新輸入分佈（資訊瓶頸步驟）
        new_p_x = [0.0] * n_inputs
        for x in range(n_inputs):
            s = 0.0
            for y in range(n_outputs):
                if p_xy[y][x] > 0 and p_y[y] > 0:
                    s += transition_matrix[y][x] * math.log2(p_xy[y][x] / p_y[y])
            new_p_x[x] = math.exp(s)
        
        # 正規化
        total = sum(new_p_x)
        new_p_x = [p / total for p in new_p_x]
        p_x = new_p_x
    
    # 計算最終互資訊
    p_xy = [[p_x[x] * transition_matrix[y][x] 
             for x in range(n_inputs)] 
            for y in range(n_outputs)]
    p_y = [sum(p_xy[y][x] for x in range(n_inputs)) 
           for y in range(n_outputs)]
    
    mi = 0.0
    for x in range(n_inputs):
        for y in range(n_outputs):
            if p_xy[y][x] > 0 and p_x[x] > 0 and p_y[y] > 0:
                mi += p_xy[y][x] * math.log2(p_xy[y][x] / (p_x[x] * p_y[y]))
    return mi


def shannon_second_theorem_demo(p_error: float) -> None:
    """
    示範香農第二定理：當傳輸速率 R < C 時，存在編碼使錯誤機率趨近 0
    
    Args:
        p_error: BSC 錯誤機率
    """
    c = channel_capacity_bsc(p_error)
    print(f"BSC 錯誤機率 p = {p_error}")
    print(f"通道容量 C = {c:.4f} bits/symbol")
    print(f"當 R < {c:.4f} 時，可實現可靠通訊")
    print(f"當 R > {c:.4f} 時，錯誤機率有下界")


if __name__ == "__main__":
    # 示範：BSC 容量
    print("=== BSC 通道容量 ===")
    for p in [0.0, 0.1, 0.5, 0.9, 1.0]:
        c = channel_capacity_bsc(p)
        print(f"p={p:.1f}, C={c:.4f} bits/symbol")
    
    # 示範：BEC 容量
    print("\n=== BEC 通道容量 ===")
    for p in [0.0, 0.1, 0.5, 0.9]:
        c = channel_capacity_bec(p)
        print(f"p={p:.1f}, C={c:.4f} bits/symbol")
    
    # 示範：DMC 容量
    print("\n=== DMC 通道容量 ===")
    # 二元非對稱通道
    w = [[0.9, 0.2],  # Y=0 給定 X=0,1
         [0.1, 0.8]]  # Y=1 給定 X=0,1
    c = dmc_capacity(w)
    print(f"非對稱二元通道容量: {c:.4f} bits/symbol")
    
    # 香農第二定理
    print("\n=== 香農第二定理示範 ===")
    shannon_second_theorem_demo(0.1)
