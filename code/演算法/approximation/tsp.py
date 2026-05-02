"""
旅行推銷員問題近似演算法 (TSP Approximation)

歷史背景：
- TSP 是 Karp 1972 年列出的 21 個 NP-完全問題之一
- 2-近似演算法（基於 MST）由 Rosenkrantz 等人於 1977 年提出
- Christofides 於 1976 年提出 1.5-近似演算法（度量 TSP）
- TSP 在物流、PCB 鑽孔等領域有廣泛應用

應用場景：
- 物流路徑規劃
- 電路板鑽孔
- 垃圾收集路線
- 基因定序（DNA sequencing）
"""

from typing import List, Tuple, Dict, Optional
import math
import random


class TSPApproximation:
    """TSP 近似演算法類別"""

    def __init__(self, n: int):
        """
        初始化

        Args:
            n: 城市數（編號 0 到 n-1）
        """
        self.n = n
        self.dist: List[List[float]] = [[0.0] * n for _ in range(n)]

    def set_distance(self, i: int, j: int, d: float) -> None:
        """設置城市 i 和 j 之間的距離"""
        self.dist[i][j] = d
        self.dist[j][i] = d

    def mst_2approx(self) -> Tuple[List[int], float]:
        """
        基於 MST 的 2-近似演算法（適用於度量 TSP）

        原理：
        1. 計算最小生成樹（MST）
        2. 對 MST 進行 DFS 遍歷，得到訪問序列
        3. 去除重複訪問的城市（捷徑法，shortcut）
        4. 返回哈密頓迴圈

        近似比：2（對於度量 TSP）
        時間複雜度：O(V^2)

        Returns:
            (路徑（城市列表）, 總距離)
        """
        # 1. 計算 MST（使用 Prim 演算法）
        mst_edges = self._prim_mst()

        # 2. 建立 MST 的鄰接表
        adj = [[] for _ in range(self.n)]
        for u, v in mst_edges:
            adj[u].append(v)
            adj[v].append(u)

        # 3. DFS 遍歷 MST
        visited = [False] * self.n
        tour = []
        self._dfs(0, adj, visited, tour)

        # 4. 返回到起點
        tour.append(0)

        # 5. 計算總距離
        total_dist = self._calc_tour_distance(tour)

        return tour, total_dist

    def _prim_mst(self) -> List[Tuple[int, int]]:
        """使用 Prim 演算法計算 MST"""
        in_mst = [False] * self.n
        key = [float('inf')] * self.n
        parent = [-1] * self.n

        key[0] = 0

        for _ in range(self.n):
            # 找最小 key 的節點
            u = self._min_key(key, in_mst)
            in_mst[u] = True

            # 更新鄰居
            for v in range(self.n):
                if self.dist[u][v] > 0 and not in_mst[v] and self.dist[u][v] < key[v]:
                    key[v] = self.dist[u][v]
                    parent[v] = u

        # 收集 MST 邊
        edges = []
        for v in range(1, self.n):
            if parent[v] != -1:
                edges.append((parent[v], v))
        return edges

    def _min_key(self, key: List[float], in_mst: List[bool]) -> int:
        """找最小 key 且不在 MST 中的節點"""
        min_val = float('inf')
        min_idx = -1
        for v in range(self.n):
            if not in_mst[v] and key[v] < min_val:
                min_val = key[v]
                min_idx = v
        return min_idx

    def _dfs(self, u: int, adj: List[List[int]], visited: List[bool], tour: List[int]) -> None:
        """DFS 遍歷圖"""
        visited[u] = True
        tour.append(u)
        for v in adj[u]:
            if not visited[v]:
                self._dfs(v, adj, visited, tour)

    def _calc_tour_distance(self, tour: List[int]) -> float:
        """計算路徑總距離"""
        total = 0.0
        for i in range(len(tour) - 1):
            total += self.dist[tour[i]][tour[i + 1]]
        return total

    def nearest_neighbor(self, start: int = 0) -> Tuple[List[int], float]:
        """
        最近鄰居啟發式

        原理：
        1. 從起點開始
        2. 每次選擇最近的未訪問城市
        3. 返回起點

        注意：無近似比保證，但實務上通常不錯
        時間複雜度：O(V^2)

        Args:
            start: 起始城市

        Returns:
            (路徑, 總距離)
        """
        visited = [False] * self.n
        tour = [start]
        visited[start] = True
        total_dist = 0.0

        current = start
        for _ in range(self.n - 1):
            # 找最近的未訪問城市
            nearest = -1
            min_dist = float('inf')
            for v in range(self.n):
                if not visited[v] and self.dist[current][v] < min_dist:
                    min_dist = self.dist[current][v]
                    nearest = v

            if nearest == -1:
                break

            tour.append(nearest)
            visited[nearest] = True
            total_dist += min_dist
            current = nearest

        # 返回起點
        total_dist += self.dist[current][start]
        tour.append(start)

        return tour, total_dist


def build_sample_tsp() -> TSPApproximation:
    """建立示例 TSP 問題（4 個城市）"""
    tsp = TSPApproximation(4)
    # 設置距離（度量性質：對稱、三角不等式）
    tsp.set_distance(0, 1, 10)
    tsp.set_distance(0, 2, 15)
    tsp.set_distance(0, 3, 20)
    tsp.set_distance(1, 2, 35)
    tsp.set_distance(1, 3, 25)
    tsp.set_distance(2, 3, 30)
    return tsp


if __name__ == "__main__":
    print("=== TSP 近似演算法 (TSP Approximation) 測試 ===\n")

    # 測試 1：4 城市示例
    print("1. 4 城市示例：")
    tsp1 = build_sample_tsp()
    print(f"  城市數：4")
    print(f"  距離矩陣：")
    for i in range(4):
        print(f"    {[tsp1.dist[i][j] for j in range(4)]}")

    tour, dist = tsp1.mst_2approx()
    print(f"\n  MST 2-近似：")
    print(f"    路徑：{tour}")
    print(f"    總距離：{dist}")

    tour2, dist2 = tsp1.nearest_neighbor()
    print(f"\n  最近鄰居：")
    print(f"    路徑：{tour2}")
    print(f"    總距離：{dist2}")
    print()

    # 測試 2：5 城市（隨機生成）
    print("2. 5 城市（隨機座標）：")
    random.seed(42)
    n = 5
    coords = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]
    tsp2 = TSPApproximation(n)
    for i in range(n):
        for j in range(i + 1, n):
            d = math.sqrt((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)
            tsp2.set_distance(i, j, d)

    tour, dist = tsp2.mst_2approx()
    print(f"  座標：{coords}")
    print(f"  MST 2-近似總距離：{dist:.2f}")
    print(f"  路徑：{tour}")
    print()

    # 測試 3：3 城市（三角形）
    print("3. 3 城市（等邊三角形）：")
    tsp3 = TSPApproximation(3)
    tsp3.set_distance(0, 1, 10)
    tsp3.set_distance(1, 2, 10)
    tsp3.set_distance(0, 2, 10)

    tour, dist = tsp3.mst_2approx()
    print(f"  MST 2-近似：路徑={tour}, 距離={dist}")
    tour2, dist2 = tsp3.nearest_neighbor()
    print(f"  最近鄰居：路徑={tour2}, 距離={dist2}")
    print()

    # 測試 4：單城市
    print("4. 單城市：")
    tsp4 = TSPApproximation(1)
    tour, dist = tsp4.mst_2approx()
    print(f"  MST 2-近似：路徑={tour}, 距離={dist}")
    print()
    print("測試完成！")
