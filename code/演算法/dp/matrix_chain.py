"""
矩陣鏈乘積最佳化 (Matrix Chain Multiplication)
使用動態規劃找出最優的括號化方式，使標量乘法次數最少
"""

from typing import List, Tuple


def matrix_chain_order(dims: List[int]) -> Tuple[int, List[List[int]]]:
    """
    計算矩陣鏈乘積的最佳括號化方式
    
    Args:
        dims: 矩陣維度陣列，若有 n 個矩陣，則 dims 長度為 n+1
              dims[i-1] × dims[i] 為第 i 個矩陣的維度
              
    Returns:
        (最少乘法次數, 分割點表 s)
    """
    n = len(dims) - 1  # 矩陣個數
    
    # m[i][j] 表示計算矩陣 A[i..j] 所需的最少乘法次數
    m = [[0] * (n + 1) for _ in range(n + 1)]
    # s[i][j] 記錄分割點，用於重建括號化方式
    s = [[0] * (n + 1) for _ in range(n + 1)]
    
    # l 是鏈的長度
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            
            # 嘗試所有分割點
            for k in range(i, j):
                # 計算 p[i-1] * p[k] * p[j]
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    
    return m[1][n], s


def get_optimal_parens(s: List[List[int]], i: int, j: int) -> str:
    """
    遞迴重建最優括號化方式
    
    Args:
        s: 分割點表
        i: 起始索引
        j: 結束索引
        
    Returns:
        括號化字串表示
    """
    if i == j:
        return f"A{i}"
    else:
        k = s[i][j]
        left = get_optimal_parens(s, i, k)
        right = get_optimal_parens(s, k + 1, j)
        return f"({left}{right})"


def matrix_chain_multiply(matrices: List, s: List[List[int]], i: int, j: int):
    """
    根據最優括號化方式實際計算矩陣乘積
    
    Args:
        matrices: 矩陣列表
        s: 分割點表
        i: 起始索引
        j: 結束索引
        
    Returns:
        乘積結果矩陣
    """
    if i == j:
        return matrices[i - 1]
    
    k = s[i][j]
    left = matrix_chain_multiply(matrices, s, i, k)
    right = matrix_chain_multiply(matrices, s, k + 1, j)
    
    # 執行矩陣乘法
    return matrix_multiply(left, right)


def matrix_multiply(a, b):
    """簡單的矩陣乘法實作（假設維度相容）"""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result


def print_optimal_order(dims: List[int]) -> None:
    """
    印出矩陣鏈的最佳乘積順序
    
    Args:
        dims: 矩陣維度陣列
    """
    min_cost, s = matrix_chain_order(dims)
    n = len(dims) - 1
    
    print(f"矩陣維度: {dims}")
    print(f"矩陣個數: {n}")
    print(f"最少乘法次數: {min_cost}")
    print(f"最佳括號化: {get_optimal_parens(s, 1, n)}")


if __name__ == "__main__":
    # 測試案例 1：經典例子
    print("=== 測試案例 1 ===")
    # 四個矩陣：A1(30×35), A2(35×15), A3(15×5), A4(5×10)
    dims = [30, 35, 15, 5, 10]
    print_optimal_order(dims)
    
    # 測試案例 2
    print("\n=== 測試案例 2 ===")
    # 三個矩陣：A1(10×20), A2(20×30), A3(30×40)
    dims = [10, 20, 30, 40]
    print_optimal_order(dims)
    
    # 測試案例 3：更多矩陣
    print("\n=== 測試案例 3 ===")
    dims = [5, 10, 3, 12, 5, 50, 6]
    print_optimal_order(dims)
    
    # 實際計算驗證
    print("\n=== 實際計算驗證 ===")
    import random
    random.seed(42)
    
    # 建立測試矩陣
    dims = [2, 3, 4, 2]
    matrices = []
    for i in range(len(dims) - 1):
        mat = [[random.randint(1, 5) for _ in range(dims[i + 1])] 
               for _ in range(dims[i])]
        matrices.append(mat)
    
    _, s = matrix_chain_order(dims)
    result = matrix_chain_multiply(matrices, s, 1, len(dims) - 1)
    
    print(f"矩陣維度: {dims}")
    print(f"最佳順序: {get_optimal_parens(s, 1, len(dims) - 1)}")
    print(f"結果矩陣維度: {len(result)} × {len(result[0])}")
