"""
背包問題 - 動態規劃實作
包含 0/1 背包問題與無界背包問題
"""

from typing import List, Tuple


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    0/1 背包問題 - 使用二維 DP 表求解
    
    Args:
        weights: 每個物品的重量列表
        values: 每個物品的價值列表
        capacity: 背包容量
        
    Returns:
        (最大價值, 被選中物品的索引列表)
    """
    n = len(weights)
    # dp[i][w] 表示前 i 個物品在容量 w 下的最大價值
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # 建立 DP 表
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                # 選擇或不選擇第 i 個物品
                dp[i][w] = max(
                    dp[i - 1][w],  # 不選
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]  # 選
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    # 回溯找出被選中的物品
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        # 如果 dp[i][w] != dp[i-1][w]，表示選了第 i 個物品
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    
    selected.reverse()
    return dp[n][capacity], selected


def knapsack_01_optimized(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    0/1 背包問題 - 空間優化版本（一維陣列）
    
    Args:
        weights: 每個物品的的重量列表
        values: 每個物品的價值列表
        capacity: 背包容量
        
    Returns:
        (最大價值, 被選中物品的索引列表)
    """
    n = len(weights)
    # 一維 DP 陣列
    dp = [0] * (capacity + 1)
    # 記錄選擇的輔助陣列
    choice = [[False] * (capacity + 1) for _ in range(n)]
    
    for i in range(n):
        # 必須從後往前遍歷，避免重複選取
        for w in range(capacity, weights[i] - 1, -1):
            if dp[w - weights[i]] + values[i] > dp[w]:
                dp[w] = dp[w - weights[i]] + values[i]
                choice[i][w] = True
    
    # 回溯找出被選中的物品
    selected = []
    w = capacity
    for i in range(n - 1, -1, -1):
        if choice[i][w]:
            selected.append(i)
            w -= weights[i]
    
    selected.reverse()
    return dp[capacity], selected


def knapsack_unbounded(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    無界背包問題 - 每個物品可以選取無限次
    
    Args:
        weights: 每個物品的重量列表
        values: 每個物品的價值列表
        capacity: 背包容量
        
    Returns:
        (最大價值, 被選中物品的索引列表（可重複）)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    # 記錄每個容量下最後選取的物品
    last_item = [-1] * (capacity + 1)
    
    for w in range(1, capacity + 1):
        for i in range(n):
            if weights[i] <= w:
                if dp[w - weights[i]] + values[i] > dp[w]:
                    dp[w] = dp[w - weights[i]] + values[i]
                    last_item[w] = i
    
    # 回溯找出所有選取的物品
    selected = []
    w = capacity
    while w > 0 and last_item[w] != -1:
        i = last_item[w]
        selected.append(i)
        w -= weights[i]
    
    selected.reverse()
    return dp[capacity], selected


if __name__ == "__main__":
    # 範例：三個物品，重量分別為 2, 3, 4，價值分別為 3, 4, 5，背包容量為 5
    weights = [2, 3, 4]
    values = [3, 4, 5]
    capacity = 5
    
    print("=== 0/1 背包問題（二維 DP）===")
    max_value, items = knapsack_01(weights, values, capacity)
    print(f"背包容量: {capacity}")
    print(f"最大價值: {max_value}")
    print(f"選取物品索引: {items}")
    print(f"選取物品重量: {[weights[i] for i in items]}")
    print(f"選取物品價值: {[values[i] for i in items]}")
    
    print("\n=== 0/1 背包問題（空間優化）===")
    max_value, items = knapsack_01_optimized(weights, values, capacity)
    print(f"最大價值: {max_value}")
    print(f"選取物品索引: {items}")
    
    print("\n=== 無界背包問題 ===")
    max_value, items = knapsack_unbounded(weights, values, capacity)
    print(f"最大價值: {max_value}")
    print(f"選取物品索引: {items}")
    
    # 另一個測試案例
    print("\n=== 另一個測試案例 ===")
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    max_value, items = knapsack_01(weights, values, capacity)
    print(f"重量: {weights}, 價值: {values}, 容量: {capacity}")
    print(f"最大價值: {max_value}, 選取物品: {items}")
    
    max_value, items = knapsack_unbounded(weights, values, capacity)
    print(f"無界背包 - 最大價值: {max_value}, 選取物品: {items}")
