"""
背包問題 FPTAS (Knapsack FPTAS)

歷史背景：
- 0/1 背包問題是 Karp 1972 年列出的 21 個 NP-完全問題之一
- 動態規劃可在偽多項式時間 O(nW) 解決
- FPTAS (Fully Polynomial Time Approximation Scheme) 於 1970 年代提出
- Ibarra-Kim 和 Lawler 分別提出 FPTAS

應用場景：
- 資源分配（預算限制下最大化價值）
- 投資組合選擇
- 貨物裝載
- 廣告預算分配
"""

from typing import List, Tuple, Optional
import math


class KnapsackFPTAS:
    """背包問題 FPTAS"""

    def __init__(self, weights: List[int], values: List[float], capacity: int):
        """
        初始化背包問題

        Args:
            weights: 每個物品的重量
            values: 每個物品的價值
            capacity: 背包容量
        """
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.n = len(weights)

    def dp_exact(self) -> Tuple[float, List[int]]:
        """
        精確動態規劃（偽多項式時間 O(n*W)）

        Returns:
            (最大總價值, 選中的物品索引列表)
        """
        n = self.n
        W = self.capacity

        # dp[i][w] = 前 i 個物品，重量恰好 w 時的最大價值
        dp = [[-float('inf')] * (W + 1) for _ in range(n + 1)]
        dp[0][0] = 0

        # 記錄選擇
        choice = [[False] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(W + 1):
                # 不選第 i 個物品
                if dp[i-1][w] > dp[i][w]:
                    dp[i][w] = dp[i-1][w]
                    choice[i][w] = False

                # 選第 i 個物品（若重量允許）
                if w >= self.weights[i-1]:
                    val = dp[i-1][w - self.weights[i-1]] + self.values[i-1]
                    if val > dp[i][w]:
                        dp[i][w] = val
                        choice[i][w] = True

        # 找最大價值
        max_val = max(dp[n])
        max_w = dp[n].index(max_val)

        # 回溯找選中的物品
        items = []
        w = max_w
        for i in range(n, 0, -1):
            if choice[i][w]:
                items.append(i - 1)
                w -= self.weights[i-1]
        items.reverse()

        return max_val, items

    def fptas(self, epsilon: float) -> Tuple[float, List[int]]:
        """
        FPTAS for 背包問題

        原理：
        1. 計算縮放因子 k = (epsilon * max_value) / n
        2. 將所有價值縮放為整數：v'_i = floor(v_i / k)
        3. 對縮放後的價值跑動態規劃（值域縮小）
        4. 返回對應原價值的結果

        近似保證：(1 - epsilon) * OPT
        時間複雜度：O(n^2 / epsilon)

        Args:
            epsilon: 近似參數（0 < epsilon < 1）

        Returns:
            (總價值, 選中的物品索引列表)
        """
        if epsilon <= 0 or epsilon >= 1:
            raise ValueError("epsilon 必須在 (0, 1) 之間")

        max_val = max(self.values)
        n = self.n

        # 計算縮放因子
        k = (epsilon * max_val) / n

        # 縮放價值為整數
        scaled_values = [int(v / k) for v in self.values]

        max_scaled = max(scaled_values)
        dp = [[-float('inf')] * (max_scaled + 1) for _ in range(n + 1)]
        dp[0][0] = 0

        for i in range(1, n + 1):
            for v in range(max_scaled + 1):
                # 不選
                dp[i][v] = dp[i-1][v]

                # 選（若價值允許）
                prev_v = v - scaled_values[i-1]
                if prev_v >= 0 and dp[i-1][prev_v] + self.weights[i-1] <= self.capacity:
                    if dp[i-1][prev_v] + self.weights[i-1] > dp[i][v]:
                        dp[i][v] = dp[i-1][prev_v] + self.weights[i-1]

        # 找最大價值對應的選擇
        best_v = -1
        best_weight = float('inf')
        for v in range(max_scaled + 1):
            if dp[n][v] >= 0 and v > best_v:
                # 計算實際重量
                items = self._reconstruct_items(dp, scaled_values, n, v)
                actual_weight = sum(self.weights[i] for i in items)
                if actual_weight <= self.capacity:
                    best_v = v
                    best_weight = actual_weight

        if best_v == -1:
            return 0.0, []

        items = self._reconstruct_items(dp, scaled_values, n, best_v)
        total_value = sum(self.values[i] for i in items)

        return total_value, items

    def _reconstruct_items(self, dp: List[List[float]], scaled_values: List[int],
                            n: int, target_v: int) -> List[int]:
        """回溯找選中的物品"""
        items = []
        v = target_v
        for i in range(n, 0, -1):
            if v >= scaled_values[i-1]:
                # 檢查是否選了
                if dp[i-1][v - scaled_values[i-1]] + self.weights[i-1] == dp[i][v]:
                    items.append(i - 1)
                    v -= scaled_values[i-1]
        items.reverse()
        return items


def build_sample_knapsack() -> KnapsackFPTAS:
    """建立示例背包問題"""
    weights = [2, 3, 4, 5]
    values = [3.0, 4.0, 5.0, 6.0]
    capacity = 8
    return KnapsackFPTAS(weights, values, capacity)


if __name__ == "__main__":
    print("=== 背包問題 FPTAS (Knapsack FPTAS) 測試 ===\n")

    # 測試 1：示例問題
    print("1. 示例背包問題：")
    weights = [2, 3, 4, 5]
    values = [3.0, 4.0, 5.0, 6.0]
    capacity = 8
    print(f"  物品重量：{weights}")
    print(f"  物品價值：{values}")
    print(f"  背包容量：{capacity}")
    ks1 = KnapsackFPTAS(weights, values, capacity)

    val_exact, items_exact = ks1.dp_exact()
    print(f"\n  精確解（DP）：")
    print(f"    選中物品：{items_exact}")
    print(f"    總價值：{val_exact}")
    print(f"    總重量：{sum(weights[i] for i in items_exact)}")

    val_approx, items_approx = ks1.fptas(0.2)
    print(f"\n  FPTAS (epsilon=0.2)：")
    print(f"    選中物品：{items_approx}")
    print(f"    總價值：{val_approx}")
    print(f"    總重量：{sum(weights[i] for i in items_approx)}")
    print()

    # 測試 2：較大問題
    print("2. 較大背包問題：")
    weights2 = [1, 2, 3, 4, 5, 6, 7, 8]
    values2 = [1.0, 5.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0]
    capacity2 = 20
    ks2 = KnapsackFPTAS(weights2, values2, capacity2)

    val_exact, items_exact = ks2.dp_exact()
    print(f"  精確解：價值={val_exact}, 物品={items_exact}")

    for eps in [0.1, 0.3, 0.5]:
        val_approx, items_approx = ks2.fptas(eps)
        ratio = val_approx / val_exact if val_exact > 0 else 0
        print(f"  FPTAS (epsilon={eps})：價值={val_approx}, 物品={items_approx}, 比率={ratio:.3f}")
    print()

    # 測試 3：空背包
    print("3. 容量為 0：")
    ks3 = KnapsackFPTAS([1, 2, 3], [1.0, 2.0, 3.0], 0)
    val, items = ks3.fptas(0.5)
    print(f"  結果：價值={val}, 物品={items}")
    print()

    # 測試 4：所有物品都放得下
    print("4. 所有物品都放得下：")
    ks4 = KnapsackFPTAS([1, 2], [10.0, 20.0], 100)
    val, items = ks4.fptas(0.1)
    print(f"  結果：價值={val}, 物品={items}")
    print()
    print("測試完成！")
