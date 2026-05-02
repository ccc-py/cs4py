"""
Shor 因數分解演算法 - 指數級加速的量子演算法
"""

from typing import List, Tuple, Optional
import math
import random
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def gcd(a: int, b: int) -> int:
    """計算最大公因數"""
    while b:
        a, b = b, a % b
    return a


def is_prime(n: int) -> bool:
    """檢查是否為質數"""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def modular_exponentiation(base: int, exp: int, mod: int) -> int:
    """快速模冪運算"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


def continued_fraction(x: float, max_denominator: int) -> Tuple[int, int]:
    """
    將分數轉換為連分數，找尋最佳有理數近似
    
    Args:
        x: 要近似的數
        max_denominator: 最大分母
    
    Returns:
        (分子, 分母)
    """
    # 連分數展開
    a = int(math.floor(x))
    frac = x - a
    p_prev, p_curr = 0, 1
    q_prev, q_curr = 1, 0
    
    while abs(x - p_curr / q_curr) > 1.0 / (q_curr * max_denominator) and q_curr <= max_denominator:
        if frac == 0:
            break
        frac = 1.0 / frac
        a = int(math.floor(frac))
        frac = frac - a
        
        p_next = a * p_curr + p_prev
        q_next = a * q_curr + q_prev
        
        p_prev, p_curr = p_curr, p_next
        q_prev, q_curr = q_curr, q_next
        
        if q_curr > max_denominator:
            break
    
    return p_curr, q_curr


def quantum_period_finding(a: int, N: int) -> int:
    """
    量子週期尋找（簡化模擬版）
    
    Args:
        a: 與 N 互質的數
        N: 要分解的數
    
    Returns:
        函數 f(x) = a^x mod N 的週期 r
    """
    # 實際量子實作會用量子傅立葉變換
    # 這裡用古典方法模擬（僅用於教學）
    x = 1
    r = 1
    while True:
        x = (x * a) % N
        if x == 1:
            return r
        r += 1
        if r > N:  # 防止無限循環
            return r


def shor_algorithm(N: int) -> Optional[Tuple[int, int]]:
    """
    Shor 因數分解演算法
    
    Args:
        N: 要分解的合數
    
    Returns:
        因數對 (p, q) 或 None
    """
    if N % 2 == 0:
        return (2, N // 2)
    
    if is_prime(N):
        print(f"{N} 是質數，無法分解")
        return None
    
    # 重複直到找到因數
    for _ in range(100):
        # 隨機選擇 a
        a = random.randint(2, N - 2)
        # 確保 gcd(a, N) = 1
        d = gcd(a, N)
        if d > 1:
            return (d, N // d)
        
        # 量子週期尋找（模擬）
        r = quantum_period_finding(a, N)
        
        # 檢查 r 是否為偶數且 a^(r/2) ≠ -1 mod N
        if r % 2 == 0:
            x = modular_exponentiation(a, r // 2, N)
            if x != N - 1:  # x ≠ -1 mod N
                p = gcd(x - 1, N)
                q = gcd(x + 1, N)
                if p > 1 and p < N:
                    return (p, N // p)
                if q > 1 and q < N:
                    return (q, N // q)
    
    return None


def qft_circuit(state: List[complex], n: int) -> List[complex]:
    """
    量子傅立葉變換（簡化版）
    
    Args:
        state: 輸入狀態向量
        n: 量子位元數
    
    Returns:
        變換後的狀態
    """
    N = 2 ** n
    new_state = [0j] * N
    
    for k in range(N):
        for j in range(N):
            # QFT 矩陣元素
            angle = 2 * math.pi * j * k / N
            new_state[k] += state[j] * complex(math.cos(angle), math.sin(angle))
        new_state[k] /= math.sqrt(N)
    
    return new_state


if __name__ == "__main__":
    print("=== Shor 因數分解演算法示範 ===\n")
    
    # 示範 1: 分解小數
    print("1. 分解 15:")
    result = shor_algorithm(15)
    if result:
        print(f"   15 = {result[0]} × {result[1]}")
    else:
        print("   分解失敗")
    
    # 示範 2: 分解 21
    print("\n2. 分解 21:")
    result = shor_algorithm(21)
    if result:
        print(f"   21 = {result[0]} × {result[1]}")
    
    # 示範 3: 分解 35
    print("\n3. 分解 35:")
    result = shor_algorithm(35)
    if result:
        print(f"   35 = {result[0]} × {result[1]}")
    
    # 示範 4: 說明
    print("\n=== 演算法說明 ===")
    print("Shor 演算法包含兩個部分:")
    print("1. 量子部分: 使用量子傅立葉變換找尋週期")
    print("2. 古典部分: 使用輾轉相除法和連分數")
    print("\n時間複雜度: O((log N)³)，相比古典 O(e^(log N)^(1/3))")
    print("這是指數級加速！")
    
    # 示範 5: 量子傅立葉變換
    print("\n5. 量子傅立葉變換示範 (2-qubit):")
    state = [1.0, 0.0, 0.0, 0.0]  # |00⟩
    result = qft_circuit(state, 2)
    print(f"   QFT|00⟩ = {[f'{abs(x):.3f}' for x in result]}")
