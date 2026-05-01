"""
背包問題（NP-Hard） (Knapsack Problem)

背包問題是組合最佳化的經典 NP-Hard 問題。

問題描述（0-1 背包）：
給定 n 個物品，每個物品有重量 w[i] 和價值 v[i]，
以及背包容量 W。
選擇物品的子集，使得總重量不超過 W，且總價值最大。

歷史背景：
- 1950 年代：背包問題在資源分配中被研究
- 1972 年：Karp 證明了背包問題是 NP-Hard 的
- 應用：資源分配、投資組合、密碼學（背包密碼）

參考：Karp, R. M. (1972). Reducibility among combinatorial problems.
"""

from typing import List, Tuple


def brute_force_knapsack(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    暴力求解背包問題（列舉所有子集）

    時間複雜度：O(2^n)，僅適用於小 n

    Args:
        weights: 重量列表
        values: 價值列表
        capacity: 背包容量

    Returns:
        (最大價值, 選中的物品索引列表)
    """
    n = len(weights)
    max_value = 0
    best_items = []

    # 列舉所有子集 (1 到 2^n - 1)
    for mask in range(1, 1 << n):
        total_weight = 0
        total_value = 0
        items = []

        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
                items.append(i)

        if total_weight <= capacity and total_value > max_value:
            max_value = total_value
            best_items = items.copy()

    return max_value, best_items


def dp_knapsack(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    動態規劃求解背包問題

    時間複雜度：O(nW)，偽多項式時間（Pseudo-polynomial）

    Args:
        weights: 重量列表
        values: 價值列表
        capacity: 背包容量

    Returns:
        (最大價值, 選中的物品索引列表)
    """
    n = len(weights)
    # dp[i][w] = 前 i 個物品，容量 w 時的最大價值
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # 不選第 i 個物品
            dp[i][w] = dp[i - 1][w]
            # 選第 i 個物品（如果重量允許）
            if weights[i - 1] <= w:
                val = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                if val > dp[i][w]:
                    dp[i][w] = val

    # 回溯找出選中的物品
    items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append(i - 1)
            w -= weights[i - 1]
    items.reverse()

    return dp[n][capacity], items


def create_example_knapsack() -> Tuple[List[int], List[int], int, List[str]]:
    """
    建立一個背包問題範例

    物品：
    0: 重量 2, 價值 3
    1: 重量 3, 價值 4
    2: 重量 4, 價值 5
    3: 重量 5, 價值 6
    容量: 8
    """
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    names = ['物品A', '物品B', '物品C', '物品D']
    return weights, values, capacity, names


def demonstrate_pseudo_polynomial():
    """
    演示偽多項式時間

    動態規劃的 O(nW) 不是真正的多項式時間，
    因為 W 的位元數是 log(W)，所以時間是 O(n * 2^log(W))。
    """
    print("=== 偽多項式時間討論 ===")
    print()
    print("動態規劃時間複雜度：O(n × W)")
    print()
    print("如果 W 用二進位表示需要 b 位：W = 2^b")
    print("則時間 = O(n × 2^b)")
    print()
    print("這不是真正的多項式時間（輸入大小是 n + b）")
    print("因此背包問題仍然是 NP-Hard 的")
    print()
    print("但是，對於『小』容量，動態規劃很實用！")


if __name__ == "__main__":
    print("=== 背包問題（NP-Hard）測試 ===")
    print()

    # 建立範例
    weights, values, capacity, names = create_example_knapsack()
    print(f"背包容量: {capacity}")
    print("物品:")
    for i, (w, v, n) in enumerate(zip(weights, values, names)):
        print(f"  {n}: 重量 {w}, 價值 {v}")
    print()

    # 暴力求解
    print("暴力求解（適用於小 n）：")
    max_val, items = brute_force_knapsack(weights, values, capacity)
    print(f"  最大價值: {max_val}")
    print(f"  選中物品: {[names[i] for i in items]}")
    print(f"  總重量: {sum(weights[i] for i in items)}")
    print()

    # 動態規劃
    print("動態規劃求解：")
    max_val, items = dp_knapsack(weights, values, capacity)
    print(f"  最大價值: {max_val}")
    print(f"  選中物品: {[names[i] for i in items]}")
    print(f"  總重量: {sum(weights[i] for i in items)}")
    print()

    # 討論
    demonstrate_pseudo_polynomial()
