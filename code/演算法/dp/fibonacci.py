"""
費波那契數列計算
包含多種計算方法：遞迴、記憶化、迭代、矩陣快速冪、閉合公式
"""

from typing import Dict, Tuple
import math


def fibonacci_recursive(n: int) -> int:
    """
    純遞迴計算費波那契數（效率極低，僅供教學展示）
    
    Args:
        n: 第 n 個費波那契數（從 0 開始）
        
    Returns:
        第 n 個費波那契數
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_memo(n: int, memo: Dict[int, int] = None) -> int:
    """
    記憶化遞迴（自頂向下動態規劃）
    
    Args:
        n: 第 n 個費波那契數
        memo: 記憶化字典
        
    Returns:
        第 n 個費波那契數
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_iterative(n: int) -> int:
    """
    迭代計算（自底向上動態規劃）
    
    Args:
        n: 第 n 個費波那契數
        
    Returns:
        第 n 個費波那契數
    """
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    
    return curr


def fibonacci_matrix(n: int) -> int:
    """
    矩陣快速冪計算（O(log n) 時間複雜度）
    利用 [[1, 1], [1, 0]]^n 的快速冪運算
    
    Args:
        n: 第 n 個費波那契數
        
    Returns:
        第 n 個費波那契數
    """
    if n <= 1:
        return n
    
    def matrix_mult(a: Tuple, b: Tuple) -> Tuple:
        """2x2 矩陣乘法"""
        return (
            a[0] * b[0] + a[1] * b[2],
            a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2],
            a[2] * b[1] + a[3] * b[3],
        )
    
    def matrix_pow(mat: Tuple, power: int) -> Tuple:
        """矩陣快速冪"""
        result = (1, 0, 0, 1)  # 單位矩陣
        base = mat
        
        while power > 0:
            if power & 1:
                result = matrix_mult(result, base)
            base = matrix_mult(base, base)
            power >>= 1
        
        return result
    
    # 轉移矩陣 [[1, 1], [1, 0]]
    mat = (1, 1, 1, 0)
    result = matrix_pow(mat, n)
    
    return result[1]  # 返回矩陣的 [0][1] 元素


def fibonacci_binet(n: int) -> int:
    """
    比內公式（Binet's Formula）計算費波那契數
    F(n) = (φ^n - ψ^n) / √5
    其中 φ = (1+√5)/2, ψ = (1-√5)/2
    
    Args:
        n: 第 n 個費波那契數
        
    Returns:
        第 n 個費波那契數（浮點數運算可能有誤差）
    """
    if n <= 1:
        return n
    
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2
    
    # 使用四捨五入避免浮點誤差
    result = (phi ** n - psi ** n) / math.sqrt(5)
    return round(result)


def fibonacci_generator():
    """
    費波那契數生成器（無限序列）
    
    Yields:
        依序產生費波那契數
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


if __name__ == "__main__":
    n = 10
    print(f"=== 計算第 {n} 個費波那契數 ===")
    print(f"純遞迴: {fibonacci_recursive(n)}")
    print(f"記憶化: {fibonacci_memo(n)}")
    print(f"迭代: {fibonacci_iterative(n)}")
    print(f"矩陣快速冪: {fibonacci_matrix(n)}")
    print(f"比內公式: {fibonacci_binet(n)}")
    
    print("\n=== 前 15 個費波那契數（生成器）===")
    fib_gen = fibonacci_generator()
    for i in range(15):
        print(f"F({i}) = {next(fib_gen)}")
    
    print("\n=== 較大數值比較 ===")
    n = 30
    import time
    
    start = time.time()
    result1 = fibonacci_iterative(n)
    t1 = time.time() - start
    
    start = time.time()
    result2 = fibonacci_matrix(n)
    t2 = time.time() - start
    
    start = time.time()
    result3 = fibonacci_memo(n)
    t3 = time.time() - start
    
    print(f"n = {n}")
    print(f"迭代: {result1}, 時間: {t1:.6f}s")
    print(f"矩陣快速冪: {result2}, 時間: {t2:.6f}s")
    print(f"記憶化: {result3}, 時間: {t3:.6f}s")
