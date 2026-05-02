"""
最小平均權重環（Minimum Mean Cycle）：Karp 的動態規劃演算法

給定一個有向圖，找到平均權重（總權重/邊數）最小的環。

Karp 在 1968 年發表了這個經典的 O(nm) 演算法，利用動態規劃
找到圖中所有節點對之間的最短路徑，並從中推導出最小平均環。

應用場景：
- 網絡優化中的成本控制
- 馬爾可夫鏈的分析
- 博弈論中的策略選擇
- 電路設計中的時序分析

時間複雜度：O(nm)
空間複雜度：O(n²)

作者：陳鍾誠
日期：2024
"""

from typing import Optional


class DiGraph:
    """有向圖結構"""

    def __init__(self, num_vertices: int):
        """
        初始化有向圖

        Args:
            num_vertices: 節點數量
        """
        self.n = num_vertices
        self.edges: list[tuple[int, int, float]] = []
        self.adj: list[list[tuple[int, float]]] = [[] for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """
        添加有向邊

        Args:
            u: 起點
            v: 終點
            weight: 邊的權重
        """
        self.edges.append((u, v, weight))
        self.adj[u].append((v, weight))

    def get_adj(self, u: int) -> list[tuple[int, float]]:
        """取得節點 u 的所有出邊"""
        return self.adj[u]


class MinimumMeanCycle:
    """最小平均權重環求解器（Karp 演算法）"""

    def __init__(self, graph: DiGraph):
        """
        初始化求解器

        Args:
            graph: 有向圖
        """
        self.graph = graph
        self.n = graph.n
        self.dist: list[list[list[float]]] = []

    def _compute_shortest_paths(self) -> list[list[list[float]]]:
        """
        計算所有節點對之間的最短路徑（按邊數分層）

        Returns:
            dist[k][u][v]: 從 u 到 v 恰好經過 k 條邊的最短路徑
        """
        n = self.n
        edges = self.graph.edges

        dist = [[[float('inf')] * n for _ in range(n)] for _ in range(n + 1)]

        for u in range(n):
            dist[0][u][u] = 0.0

        for k in range(1, n + 1):
            for u in range(n):
                for v in range(n):
                    dist[k][u][v] = dist[k - 1][u][v]

            for u, v, w in edges:
                if dist[k - 1][u][v] + w < dist[k][u][v]:
                    dist[k][u][v] = dist[k - 1][u][v] + w

        return dist

    def find_min_mean_cycle(self) -> tuple[float, list[int]]:
        """
        找到最小平均權重環（Karp 演算法）

        Karp 的關鍵觀察：
        對於任何從 v 回到 v 的環 C，假設長度為 k，則
        dist[k][v][v] 是該環的最小可能總權重。

        環的平均權重 = (dist[k][v][v] - dist[k-1][v][v]) / k
        （由最短路徑的最優子結構性可得）

        Returns:
            (最小平均權重, 環的節點序列)
            如果圖中沒有環，返回 (float('inf'), [])
        """
        n = self.n
        dist = self._compute_shortest_paths()

        best_mean = float('inf')
        best_cycle: list[int] = []
        best_end = -1
        best_k = -1

        for v in range(n):
            for k in range(1, n + 1):
                if dist[k][v][v] < float('inf'):
                    cycle_weight = dist[k][v][v]
                    mean = cycle_weight / k
                    if mean < best_mean:
                        best_mean = mean
                        best_end = v
                        best_k = k

        if best_end >= 0:
            best_cycle = self._reconstruct_cycle(dist, best_end, best_k)

        return best_mean, best_cycle

    def _reconstruct_cycle(
        self,
        dist: list[list[list[float]]],
        end: int,
        k: int
    ) -> list[int]:
        """
        重構從某節點回到自身的環

        Args:
            dist: 最短路徑距離表
            end: 環的終點（也是起點）
            k: 環的長度

        Returns:
            環的節點序列
        """
        n = self.n
        cycle = [end]
        current = end

        for step in range(k - 1, -1, -1):
            found = False
            for u, v, w in self.graph.edges:
                if v == current and step > 0:
                    if dist[step][end][u] + w == dist[step + 1][end][v]:
                        current = u
                        cycle.append(u)
                        found = True
                        break
            if not found and step > 0:
                for prev in range(n):
                    if dist[step][end][prev] < float('inf'):
                        for u, v, w in self.graph.edges:
                            if v == current and dist[step][end][u] + w == dist[step + 1][end][v]:
                                current = u
                                cycle.append(u)
                                found = True
                                break
                    if found:
                        break

        cycle.reverse()
        return cycle

    def get_mean(self, cycle: list[int]) -> float:
        """
        計算環的平均權重

        Args:
            cycle: 環的節點序列

        Returns:
            平均權重
        """
        if len(cycle) < 2:
            return float('inf')

        total_weight = 0.0
        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            found = False
            for adj_v, w in self.graph.adj[u]:
                if adj_v == v:
                    total_weight += w
                    found = True
                    break
            if not found:
                return float('inf')
        return total_weight / len(cycle)


def build_sample_graph() -> DiGraph:
    """
    建立範例圖

    Returns:
        測試用的有向圖
    """
    g = DiGraph(4)
    g.add_edge(0, 1, 1.0)
    g.add_edge(1, 2, 2.0)
    g.add_edge(2, 0, 3.0)
    g.add_edge(2, 3, 1.0)
    g.add_edge(3, 1, 4.0)
    return g


def build_sample_graph2() -> DiGraph:
    """
    建立另一個範例圖

    Returns:
        測試用的有向圖
    """
    g = DiGraph(5)
    g.add_edge(0, 1, 2.0)
    g.add_edge(1, 0, 2.0)
    g.add_edge(1, 2, 1.0)
    g.add_edge(2, 3, 1.0)
    g.add_edge(3, 1, 4.0)
    g.add_edge(3, 4, 2.0)
    g.add_edge(4, 2, 3.0)
    return g


if __name__ == "__main__":
    print("=" * 60)
    print("最小平均權重環（Karp 演算法）範例")
    print("=" * 60)

    print("\n範例 1：基本圖")
    print("-" * 40)

    g1 = build_sample_graph()
    print("圖結構：4 個節點")
    print("邊：")
    for u, v, w in g1.edges:
        print(f"  ({u} → {v}): 權重 {w}")

    solver1 = MinimumMeanCycle(g1)
    mean1, cycle1 = solver1.find_min_mean_cycle()
    print(f"\n找到的最小平均權重環：{cycle1}")
    print(f"最小平均權重：{mean1:.4f}")

    if cycle1:
        verify_mean1 = solver1.get_mean(cycle1)
        print(f"驗證平均權重：{verify_mean1:.4f}")

    print("\n" + "=" * 60)
    print("範例 2：複雜圖")
    print("-" * 40)

    g2 = build_sample_graph2()
    print("圖結構：5 個節點")
    print("邊：")
    for u, v, w in g2.edges:
        print(f"  ({u} → {v}): 權重 {w}")

    print("\n可能的環：")
    print("  0 → 1 → 0：平均權重 (2+2)/2 = 2.0")
    print("  1 → 2 → 3 → 1：平均權重 (1+1+4)/3 ≈ 2.0")
    print("  2 → 3 → 4 → 2：平均權重 (1+2+3)/3 ≈ 2.0")
    print("  1 → 2 → 3 → 4 → 2：平均權重 (1+1+2+3)/4 = 1.75")

    solver2 = MinimumMeanCycle(g2)
    mean2, cycle2 = solver2.find_min_mean_cycle()
    print(f"\n找到的最小平均權重環：{cycle2}")
    print(f"最小平均權重：{mean2:.4f}")

    if cycle2:
        verify_mean2 = solver2.get_mean(cycle2)
        print(f"驗證平均權重：{verify_mean2:.4f}")

    print("\n" + "=" * 60)
    print("範例 3：簡單環")
    print("-" * 40)

    g3 = DiGraph(3)
    g3.add_edge(0, 1, 4.0)
    g3.add_edge(1, 2, 2.0)
    g3.add_edge(2, 0, 6.0)

    print("圖結構：3 個節點")
    print("邊：(0→1:4), (1→2:2), (2→0:6)")
    print("唯一環：0 → 1 → 2 → 0，平均權重 = (4+2+6)/3 = 4.0")

    solver3 = MinimumMeanCycle(g3)
    mean3, cycle3 = solver3.find_min_mean_cycle()
    print(f"\n找到的最小平均權重環：{cycle3}")
    print(f"最小平均權重：{mean3:.4f}")