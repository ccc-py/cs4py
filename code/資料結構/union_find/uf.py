"""並查集（Union-Find）實作，又稱不相交集合（Disjoint Set）。

歷史背景：
並查集由Bernard A. Galler和Michael J. Fischer在1964年提出，用於維護一組不相交集合的資料結構，支援兩個核心操作：查找（find）和合併（union）。它是Kruskal最小生成樹演算法的核心組件。

核心概念：
- 路徑壓縮（Path Compression）：查找時將節點直接掛到根節點下，壓平樹結構
- 按秩合併（Union by Rank）：將高度較小的樹合併到高度較大的樹，避免樹過深
- 按大小合併（Union by Size）：將大小較小的樹合併到大小較大的樹
"""

from typing import Dict, Any, List, Tuple


class UnionFind:
    """並查集實作（支援路徑壓縮和按秩合併）。"""
    def __init__(self, elements: List[Any] = None) -> None:
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
        if elements:
            for elem in elements:
                self.make_set(elem)

    def make_set(self, x: Any) -> None:
        """建立新集合，x為唯一元素。"""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x: Any) -> Any:
        """查找x所在集合的根節點（含路徑壓縮）。"""
        if x not in self.parent:
            self.make_set(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> None:
        """合併x和y所在的集合（按秩合併）。"""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

    def connected(self, x: Any, y: Any) -> bool:
        """檢查x和y是否在同一集合中。"""
        return self.find(x) == self.find(y)

    def count_components(self) -> int:
        """返回當前連通分量數量。"""
        roots = set()
        for elem in self.parent:
            roots.add(self.find(elem))
        return len(roots)

    def get_components(self) -> List[List[Any]]:
        """返回所有連通分量。"""
        components: Dict[Any, List[Any]] = {}
        for elem in self.parent:
            root = self.find(elem)
            if root not in components:
                components[root] = []
            components[root].append(elem)
        return list(components.values())


def kruskal_mst(edges: List[Tuple[Any, Any, int]], vertices: List[Any]) -> List[Tuple[Any, Any, int]]:
    """使用Kruskal演算法求最小生成樹。"""
    edges_sorted = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(vertices)
    mst = []
    for u, v, weight in edges_sorted:
        if not uf.connected(u, v):
            uf.union(u, v)
            mst.append((u, v, weight))
    return mst


if __name__ == "__main__":
    print("=== 並查集測試 ===")
    uf = UnionFind([0, 1, 2, 3, 4, 5])
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    print(f"0和2是否連通: {uf.connected(0, 2)}")
    print(f"0和3是否連通: {uf.connected(0, 3)}")
    print(f"連通分量數: {uf.count_components()}")
    print(f"所有分量: {uf.get_components()}")

    print("\n=== Kruskal最小生成樹測試 ===")
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        ('A', 'B', 1), ('A', 'C', 3), ('B', 'C', 2),
        ('B', 'D', 4), ('C', 'D', 5), ('C', 'E', 6), ('D', 'E', 7)
    ]
    mst = kruskal_mst(edges, vertices)
    print(f"MST邊: {mst}")
    print(f"MST總權重: {sum(w for _, _, w in mst)}")
