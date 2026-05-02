"""
最小生成樹 (Minimum Spanning Tree) 演算法：Prim's 與 Kruskal's

歷史背景：
- Prim's 演算法由 Vojtěch Jarník 於 1930 年提出，後由 Robert Prim 於 1957 年重新發現
- Kruskal's 演算法由 Joseph Kruskal 於 1956 年提出
- 兩者都是貪婪演算法，用於在加權無向圖中找出最小生成樹
- 應用：網路設計、電路佈局、聚類分析等
"""

from typing import List, Tuple, Dict, Set, Optional, Any
import heapq


class UnionFind:
    """並查集 (Union-Find) 資料結構，用於 Kruskal 演算法"""

    def __init__(self, vertices: List[Any]):
        """初始化並查集"""
        self.parent: Dict[Any, Any] = {v: v for v in vertices}
        self.rank: Dict[Any, int] = {v: 0 for v in vertices}

    def find(self, x: Any) -> Any:
        """
        查找元素所屬的集合（帶路徑壓縮）

        時間複雜度：近似 O(1)（經路徑壓縮後）
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路徑壓縮
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """
        合併兩個集合

        Returns:
            若合併成功返回 True，若已在同一集合返回 False
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # 已在同一集合，會形成環

        # 按秩合併
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


def prim_mst(
    vertices: List[Any],
    edges: List[Tuple[Any, Any, float]]
) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """
    Prim's 最小生成樹演算法（使用優先佇列）

    原理：
    1. 從任意頂點開始，將其加入 MST
    2. 每次選擇連接 MST 與非 MST 頂點的最小權重邊
    3. 重複直到所有頂點都在 MST 中

    時間複雜度：O(E log V)（使用二元堆）
    空間複雜度：O(V)

    Args:
        vertices: 頂點列表
        edges: 邊列表，每條邊為 (u, v, weight) 元組

    Returns:
        (MST 邊列表, 總權重)
    """
    if not vertices:
        return [], 0.0

    # 建立鄰接表
    adj: Dict[Any, List[Tuple[Any, float]]] = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))  # 無向圖

    # 初始化
    start = vertices[0]
    visited: Set[Any] = {start}
    mst_edges: List[Tuple[Any, Any, float]] = []
    total_weight = 0.0

    # 使用最小堆儲存 (權重, 起點, 終點)
    heap: List[Tuple[float, Any, Any]] = []
    for neighbor, w in adj[start]:
        heapq.heappush(heap, (w, start, neighbor))

    # 主迴圈
    while heap and len(visited) < len(vertices):
        w, u, v = heapq.heappop(heap)

        # 跳過已訪問的邊
        if v in visited:
            continue

        # 加入 MST
        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w

        # 將新頂點的鄰邊加入堆
        for neighbor, weight in adj[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))

    return mst_edges, total_weight


def kruskal_mst(
    vertices: List[Any],
    edges: List[Tuple[Any, Any, float]]
) -> Tuple[List[Tuple[Any, Any, float]], float]:
    """
    Kruskal's 最小生成樹演算法（使用並查集）

    原理：
    1. 將所有邊按權重從小到大排序
    2. 依序選取邊，若該邊不會形成環則加入 MST
    3. 使用並查集 (Union-Find) 檢測環

    時間複雜度：O(E log E)（排序佔主要）
    空間複雜度：O(V)

    Args:
        vertices: 頂點列表
        edges: 邊列表，每條邊為 (u, v, weight) 元組

    Returns:
        (MST 邊列表, 總權重)
    """
    # 初始化並查集
    uf = UnionFind(vertices)

    # 將邊按權重排序
    sorted_edges = sorted(edges, key=lambda e: e[2])

    mst_edges: List[Tuple[Any, Any, float]] = []
    total_weight = 0.0

    for u, v, w in sorted_edges:
        # 若加入這條邊不會形成環
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w

            # 若已選取 V-1 條邊，MST 完成
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges, total_weight


if __name__ == "__main__":
    print("=== Prim's 最小生成樹演算法測試 ===\n")

    # 測試圖
    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 4),
        ('B', 'C', 2),
        ('B', 'D', 5),
        ('C', 'D', 5),
        ('C', 'E', 3),
        ('D', 'E', 2),
        ('D', 'F', 3),
        ('E', 'F', 1),
    ]

    mst_edges, total = prim_mst(vertices, edges)
    print("Prim's MST 邊：")
    for u, v, w in mst_edges:
        print(f"  {u} -- {v} : {w}")
    print(f"總權重：{total}")

    print("\n=== Kruskal's 最小生成樹演算法測試 ===\n")

    mst_edges2, total2 = kruskal_mst(vertices, edges)
    print("Kruskal's MST 邊：")
    for u, v, w in mst_edges2:
        print(f"  {u} -- {v} : {w}")
    print(f"總權重：{total2}")

    print("\n=== 視覺化 MST ===\n")

    def print_mst(edges: List[Tuple[Any, Any, float]]) -> None:
        """簡單的 MST 視覺化"""
        adj: Dict[Any, List[Any]] = {v: [] for v in vertices}
        for u, v, w in edges:
            adj[u].append(v)
            adj[v].append(u)

        print("MST 結構：")
        for v in vertices:
            if adj[v]:
                print(f"  {v} -- {adj[v]}")

    print("Prim's MST:")
    print_mst(mst_edges)
    print()
    print("Kruskal's MST:")
    print_mst(mst_edges2)

    print("\n=== 比較結果 ===\n")
    print(f"Prim's 總權重: {total}")
    print(f"Kruskal's 總權重: {total2}")
    print(f"兩者結果相同: {abs(total - total2) < 1e-9}")
