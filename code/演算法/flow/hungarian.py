"""
Hungarian 演算法（Kuhn-Munkres 演算法）：指派問題的最優解

指派問題是組合優化中的經典問題：將 n 個任務分配給 n 個工作者，
使得總成本最小（或總收益最大）。

匈牙利演算法由 Harold Kuhn (1955) 提出，基於 Hungarian method
（由匈牙利數學家 Dénes Kőnig 和 Jenő Egérvár 奠定理論基礎）。
後來 Munkres (1957) 將其推廣至非方形矩陣和最大化的情形。

時間複雜度：O(n³)
空間複雜度：O(n²)

核心概念：
- 對偶變數（potential）：行對偶和列對偶
- 覆蓋線（covering lines）：最少直線覆蓋所有零元素
- 標記法（labeling）：尋找增廣路徑

作者：陳鍾誠
日期：2024
"""

from typing import Optional


class HungarianAlgorithm:
    """匈牙利演算法實現（最小化版本）"""

    def __init__(self, cost_matrix: list[list[float]]):
        """
        初始化演算法

        Args:
            cost_matrix: 成本矩陣，cost_matrix[i][j] 表示將任務 i 分配給工作者 j 的成本
        """
        self.original = cost_matrix
        self.n = len(cost_matrix)
        self.m = len(cost_matrix[0]) if cost_matrix else 0
        self.maximize = False
        self.cost: list[list[float]] = [row[:] for row in cost_matrix]
        self.u: list[float] = [0.0] * (self.n + 1)
        self.v: list[float] = [0.0] * (self.m + 1)
        self.p: list[int] = [0] * (self.m + 1)
        self.way: list[int] = [0] * (self.m + 1)

    def solve(self) -> tuple[float, list[int]]:
        """
        求解指派問題

        Returns:
            (最小總成本, 指派陣列)，其中 assignment[i] = j 表示任務 i 分配給工作者 j
        """
        self._hungarian()
        assignment = [-1] * self.n
        for j in range(1, self.m + 1):
            if self.p[j] != 0:
                assignment[self.p[j] - 1] = j - 1
        min_cost = -self.u[0]
        for i in range(1, self.n + 1):
            min_cost += self.cost[i - 1][self.p[i] - 1] if self.p[i] != 0 else 0
        return self._get_total_cost(), assignment

    def _get_total_cost(self) -> float:
        """計算總成本"""
        total = 0.0
        for i in range(self.n):
            for j in range(self.m):
                if self.p[j + 1] == i + 1:
                    total += self.original[i][j]
        return total

    def _hungarian(self) -> None:
        """匈牙利演算法的核心實現"""
        n, m = self.n, self.m
        u = self.u
        v = self.v
        p = self.p
        way = self.way

        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            minv = [float('inf')] * (m + 1)
            used = [False] * (m + 1)
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = float('inf')
                j1 = 0
                for j in range(1, m + 1):
                    if not used[j]:
                        cur = self.cost[i0 - 1][j - 1] - u[i0] - v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j
                for j in range(m + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break


class HungarianMaximize:
    """匈牙利演算法實現（最大化版本）"""

    def __init__(self, profit_matrix: list[list[float]]):
        """
        初始化演算法（最大化版本）

        Args:
            profit_matrix: 利潤矩陣，profit_matrix[i][j] 表示將任務 i 分配給工作者 j 的收益
        """
        self.n = len(profit_matrix)
        self.m = len(profit_matrix[0]) if profit_matrix else 0
        max_val = max(max(row) for row in profit_matrix) if profit_matrix else 0
        self.cost = [
            [max_val - profit_matrix[i][j] for j in range(self.m)]
            for i in range(self.n)
        ]
        self.original = profit_matrix
        self.u: list[float] = [0.0] * (self.n + 1)
        self.v: list[float] = [0.0] * (self.m + 1)
        self.p: list[int] = [0] * (self.m + 1)
        self.way: list[int] = [0] * (self.m + 1)

    def solve(self) -> tuple[float, list[int]]:
        """
        求解指派問題（最大化）

        Returns:
            (最大總收益, 指派陣列)
        """
        n, m = self.n, self.m
        u, v, p, way = self.u, self.v, self.p, self.way
        cost = self.cost

        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            minv = [float('inf')] * (m + 1)
            used = [False] * (m + 1)
            while True:
                used[j0] = True
                i0 = p[j0]
                delta = float('inf')
                j1 = 0
                for j in range(1, m + 1):
                    if not used[j]:
                        cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j
                for j in range(m + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break
            while True:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1
                if j0 == 0:
                    break

        assignment = [-1] * n
        for j in range(1, m + 1):
            if p[j] != 0:
                assignment[p[j] - 1] = j - 1

        total_profit = sum(
            self.original[i][assignment[i]]
            for i in range(n)
            if assignment[i] != -1
        )
        return total_profit, assignment


def hungarian(cost_matrix: list[list[float]]) -> tuple[float, list[int]]:
    """
    求解指派問題（最小化版本）的便捷函數

    Args:
        cost_matrix: 成本矩陣

    Returns:
        (最小總成本, 指派陣列)
    """
    solver = HungarianAlgorithm(cost_matrix)
    return solver.solve()


def hungarian_maximize(profit_matrix: list[list[float]]) -> tuple[float, list[int]]:
    """
    求解指派問題（最大化版本）的便捷函數

    Args:
        profit_matrix: 利潤矩陣

    Returns:
        (最大總收益, 指派陣列)
    """
    solver = HungarianMaximize(profit_matrix)
    return solver.solve()


if __name__ == "__main__":
    print("=" * 60)
    print("Hungarian 演算法（Kuhn-Munkres）範例")
    print("=" * 60)

    print("\n範例 1：任務指派（最小化成本）")
    print("-" * 40)

    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]

    print("成本矩陣：")
    for i, row in enumerate(cost_matrix):
        print(f"  任務 {i}: {row}")

    min_cost, assignment = hungarian(cost_matrix)
    print(f"\n最小總成本：{min_cost}")
    print("指派方案：")
    for i, j in enumerate(assignment):
        print(f"  任務 {i} → 工作站 {j}（成本：{cost_matrix[i][j]}）")

    print("\n" + "=" * 60)
    print("範例 2：員工分配（最大化收益）")
    print("-" * 40)

    profit_matrix = [
        [3, 8, 2, 9],
        [7, 2, 5, 1],
        [8, 4, 6, 3],
        [5, 7, 3, 6]
    ]

    print("收益矩陣：")
    for i, row in enumerate(profit_matrix):
        print(f"  員工 {i}: {row}")

    max_profit, assignment2 = hungarian_maximize(profit_matrix)
    print(f"\n最大總收益：{max_profit}")
    print("指派方案：")
    for i, j in enumerate(assignment2):
        print(f"  員工 {i} → 任務 {j}（收益：{profit_matrix[i][j]}）")

    print("\n" + "=" * 60)
    print("範例 3：非方形矩陣")
    print("-" * 40)

    cost_matrix2 = [
        [3, 8, 4],
        [6, 1, 5],
        [2, 9, 6]
    ]

    print("成本矩陣（3x3）：")
    for i, row in enumerate(cost_matrix2):
        print(f"  機器 {i}: {row}")

    min_cost2, assignment3 = hungarian(cost_matrix2)
    print(f"\n最小總成本：{min_cost2}")
    print("指派方案：")
    for i, j in enumerate(assignment3):
        if j != -1:
            print(f"  機器 {i} → 任務 {j}（成本：{cost_matrix2[i][j]}）")