"""
Simon 演算法 - 指數級加速的前驅演算法
"""

from typing import List, Tuple, Optional
import math
import random


def simon_oracle_function(s: str) -> callable:
    """
    建立 Simon 問題的 Oracle 函數
    
    Args:
        s: 隱藏的週期字串 (n bits)，如果 s=0...0 則函數是一對一的
    
    Returns:
        Oracle 函數 f: {0,1}^n -> {0,1}^n
    """
    n = len(s)
    s_int = int(s, 2)
    
    # 建立一個隨機但確定的二對一映射
    # 對於每個 x，f(x) = f(x ⊕ s)
    # 使用上半部分的值作為輸出
    
    def f(x: int) -> int:
        """
        Simon 的 Oracle: f(x) = f(x ⊕ s)
        返回一個 n-bit 的哈希值
        """
        if s_int == 0:
            # 一對一函數
            return x
        
        x_xor_s = x ^ s_int
        # 返回較小的那個，確保 f(x) = f(x⊕s)
        return min(x, x_xor_s)
    
    return f


def find_linear_equations_simon(n: int, f: callable, s_int: int) -> List[int]:
    """
    模擬量子 Simon 演算法，生成線性方程 y·s = 0
    
    Args:
        n: 位元數
        f: Oracle 函數
        s_int: 隱藏的 s (整數)
    
    Returns:
        y 值列表，每個滿足 y·s = 0 (mod 2)
    """
    equations = []
    
    # 模擬量子過程:
    # 1. 初始化 |0⟩⊗n |0⟩⊗n
    # 2. Hadamard 到第一組
    # 3. 查詢 Oracle
    # 4. 測量第二組，坍縮到某個 f(x)
    # 5. 對第一組應用 Hadamard
    # 6. 測量第一組，得到 y 滿足 y·s = 0
    
    # 簡化: 直接生成隨機 y 滿足 y·s = 0
    # 在實際量子版本中，這會自然發生
    
    attempts = 0
    while len(equations) < n and attempts < 10 * n:
        attempts += 1
        # 生成隨機 x
        x = random.randint(0, (1 << n) - 1)
        
        # 經過 Oracle 和測量後，狀態為 (|x⟩ + |x⊕s⟩)/√2
        # 應用 H⊗n 後測量，得到 y 滿足 y·s = 0
        
        # 模擬測量: 選一個隨機非零 y 滿足 y·s = 0
        # 實際上，任何 y 在 s 的正交補空間中都會以非零機率出現
        
        # 生成一個隨機 y
        y = random.randint(1, (1 << n) - 1)
        
        # 計算 y·s (點積 mod 2)
        dot_product = 0
        for i in range(n):
            y_bit = (y >> i) & 1
            s_bit = (s_int >> i) & 1
            dot_product ^= (y_bit & s_bit)
        
        # 在量子版本中，只有當 y·s = 0 時才會有非零機率
        # 這裡我們只保留滿足條件的 y
        if dot_product == 0:
            if y not in equations:
                equations.append(y)
    
    return equations


def solve_linear_equations(equations: List[int], n: int) -> Optional[str]:
    """
    解線性方程組 over GF(2): y·s = 0
    
    Args:
        equations: y 值列表，每個滿足 y·s = 0
        n: 位元數
    
    Returns:
        s 字串或 None
    """
    if len(equations) < n - 1:
        return None
    
    # 建立矩陣 (equations 是行向量)
    # 我們需要找到非零 s 使得所有 y·s = 0
    
    # 使用高斯消去法找零空間
    # 建立矩陣 A (equations 作為行)
    A = []
    for y in equations:
        row = [(y >> i) & 1 for i in range(n)]
        A.append(row)
    
    # 轉置並找零空間
    # A 是 m x n 矩陣，找 s 使得 A·s = 0
    
    # 簡化: 使用線性代數 over GF(2)
    # 執行高斯消去法
    
    m = len(A)
    rank = 0
    pivot_cols = []
    
    for col in range(n):
        # 找到 pivot
        pivot_row = None
        for row in range(rank, m):
            if A[row][col] == 1:
                pivot_row = row
                break
        
        if pivot_row is None:
            continue
        
        # 交換行
        A[rank], A[pivot_row] = A[pivot_row], A[rank]
        pivot_cols.append(col)
        
        # 消去其他行
        for row in range(m):
            if row != rank and A[row][col] == 1:
                for c in range(n):
                    A[row][c] ^= A[rank][c]
        
        rank += 1
        if rank >= n - 1:
            break
    
    # 找自由變數
    all_cols = set(range(n))
    free_cols = all_cols - set(pivot_cols)
    
    if not free_cols:
        return None
    
    # 設定一個自由變數為 1，解出其他
    free_col = min(free_cols)
    
    s_bits = [0] * n
    s_bits[free_col] = 1
    
    # 對於每個 pivot，解出對應的 s 值
    for i, col in enumerate(pivot_cols):
        # A[i]·s = 0
        # s[col] = sum of other bits
        val = 0
        for j in range(n):
            if j != col and A[i][j] == 1:
                val ^= s_bits[j]
        s_bits[col] = val
    
    s_str = ''.join(str(b) for b in reversed(s_bits))
    
    # 驗證
    s_int = int(s_str, 2)
    if s_int == 0:
        return None
    
    # 檢查所有方程
    for y in equations:
        dot = 0
        for i in range(n):
            y_bit = (y >> i) & 1
            s_bit = (s_int >> i) & 1
            dot ^= (y_bit & s_bit)
        if dot != 0:
            return None
    
    return s_str


def simon_algorithm(n: int, f: callable, s: str) -> Optional[str]:
    """
    Simon 演算法：找出隱藏的週期 s
    
    Args:
        n: 輸入位元數
        f: Oracle 函數 f: {0,1}^n -> {0,1}^n
        s: 真實的 s (用於模擬生成方程)
    
    Returns:
        隱藏的週期 s，或 None
    """
    s_int = int(s, 2)
    
    # 生成線性方程
    equations = find_linear_equations_simon(n, f, s_int)
    
    # 解線性方程
    result = solve_linear_equations(equations, n)
    
    return result


if __name__ == "__main__":
    print("=== Simon 演算法示範 ===\n")
    
    # 示範 1: s = "110" (3 bits)
    print("1. 隱藏週期 s = '110' (3 bits):")
    s = "110"
    n = len(s)
    f = simon_oracle_function(s)
    result = simon_algorithm(n, f, s)
    print(f"   隱藏週期: {s}")
    print(f"   演算法結果: {result}")
    print(f"   成功: {result == s}")
    
    # 示範 2: s = "1011" (4 bits)
    print("\n2. 隱藏週期 s = '1011' (4 bits):")
    s = "1011"
    n = len(s)
    f = simon_oracle_function(s)
    result = simon_algorithm(n, f, s)
    print(f"   隱藏週期: {s}")
    print(f"   演算法結果: {result}")
    print(f"   成功: {result == s}")
    
    # 示範 3: s = "10" (2 bits)
    print("\n3. 隱藏週期 s = '10' (2 bits):")
    s = "10"
    n = len(s)
    f = simon_oracle_function(s)
    result = simon_algorithm(n, f, s)
    print(f"   隱藏週期: {s}")
    print(f"   演算法結果: {result}")
    print(f"   成功: {result == s}")
    
    # 示範 4: 說明
    print("\n=== Simon 演算法說明 ===")
    print("問題: 找出 s 使得 f(x) = f(y) iff y = x ⊕ s")
    print()
    print("古典演算法:")
    print("  - 需要 ~2^(n/2) 次查詢 (生日悖論)")
    print("  - 指數時間!")
    print()
    print("Simon 量子演算法:")
    print("  - 需要 O(n) 次查詢")
    print("  - 指數級加速!")
    print()
    print("這是 Shor 演算法的靈感來源")
