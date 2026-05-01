"""
Dijkstra 最短路徑算法

歷史背景：
- 1956 年由 Edsger W. Dijkstra 發明
- 解決單源最短路徑問題
- 適用於權重非負的圖
- 時間複雜度：O((V + E) log V) 使用堆積
"""

import heapq
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict


class Graph:
    """帶權重的圖"""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)

    def add_edge(self, u: int, v: int, weight: int) -> None:
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def dijkstra(self, start: int) -> Tuple[Dict[int, float], Dict[int, int]]:
        """
        Dijkstra 最短路徑算法

        參數：
            start: 起點

        返回：
            (distances, predecessors)
            - distances: 每個頂點到 start 的最短距離
            - predecessors: 最短路徑樹（每個節點的前驅）

        時間複雜度：O((V + E) log V)
        """
        distances: Dict[int, float] = {start: 0.0}
        predecessors: Dict[int, int] = {}
        visited: Set[int] = set()
        heap = [(0.0, start)]

        while heap:
            current_dist, u = heapq.heappop(heap)

            if u in visited:
                continue

            visited.add(u)

            for v, weight in self.adj[u]:
                if v in visited:
                    continue

                new_dist = current_dist + weight

                if v not in distances or new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    heapq.heappush(heap, (new_dist, v))

        return distances, predecessors

    def dijkstra_with_path(self, start: int, end: int) -> Optional[List[int]]:
        """使用 Dijkstra 找最短路徑"""
        distances, predecessors = self.dijkstra(start)

        if end not in distances:
            return None

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors.get(current)

        path.reverse()
        return path

    def dijkstra_all_pairs(self) -> Dict[int, Dict[int, float]]:
        """計算所有頂點對的最短距離"""
        all_distances = {}

        for vertex in self.adj:
            distances, _ = self.dijkstra(vertex)
            all_distances[vertex] = distances

        return all_distances

    def bellman_ford(self, start: int) -> Tuple[Dict[int, float], Dict[int, int]]:
        """
        Bellman-Ford 算法

        可處理負權重邊，並檢測負環
        時間複雜度：O(V * E)
        """
        distances: Dict[int, float] = {start: 0.0}
        predecessors: Dict[int, int] = {}
        vertices = list(self.adj.keys())

        for _ in range(len(vertices) - 1):
            for u in vertices:
                for v, weight in self.adj[u]:
                    if u in distances:
                        new_dist = distances[u] + weight
                        if v not in distances or new_dist < distances[v]:
                            distances[v] = new_dist
                            predecessors[v] = u

        for u in vertices:
            for v, weight in self.adj[u]:
                if u in distances and distances[u] + weight < distances[v]:
                    raise ValueError("負環 detected")

        return distances, predecessors

    def floyd_warshall(self) -> Dict[int, Dict[int, float]]:
        """
        Floyd-Warshall 算法

        計算所有頂點對的最短路徑
        時間複雜度：O(V³)
        """
        vertices = list(self.adj.keys())
        dist = defaultdict(lambda: defaultdict(lambda: float('inf')))

        for v in vertices:
            dist[v][v] = 0.0

        for u in vertices:
            for v, weight in self.adj[u]:
                dist[u][v] = weight

        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dict(dist)


def demo_dijkstra():
    """Dijkstra 算法演示"""
    print("=== Dijkstra 最短路徑演示 ===\n")

    g = Graph()
    edges = [
        (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5),
        (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    print("圖結構（權重圖）：")
    print("       4")
    print("   0 -------- 1")
    print("   | \\      / |")
    print("  2|  2\  /5  |")
    print("   |   \/    |")
    print("   2-------- 3")
    print("    \    8 /")
    print("     \   / 2")
    print("      \ /")
    print("       4")
    print("       |")
    print("       6")
    print("       |")
    print("       5")
    print()

    distances, predecessors = g.dijkstra(0)
    print(f"從 0 出發的最短距離：{distances}")
    print(f"前驅節點：{predecessors}")

    print("\n最短路徑：")
    for target in range(6):
        path = g.dijkstra_with_path(0, target)
        print(f"  0 → {target}：{path}（距離 {distances.get(target, '∞')}）")


def demo_bellman_ford():
    """Bellman-Ford 算法演示"""
    print("\n=== Bellman-Ford 算法演示 ===\n")

    g = Graph()
    edges = [
        (0, 1, 4), (0, 2, 2), (1, 2, -3), (1, 3, 5),
        (2, 3, 8), (3, 4, 2),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    distances, predecessors = g.bellman_ford(0)
    print(f"從 0 出發的最短距離：{dict(distances)}")
    print(f"前驅節點：{predecessors}")

    print("\n最短路徑：")
    for target in range(5):
        if target in distances:
            path = []
            current = target
            while current is not None:
                path.append(current)
                current = predecessors.get(current)
            path.reverse()
            print(f"  0 → {target}：{path}（距離 {distances[target]}）")


def demo_floyd_warshall():
    """Floyd-Warshall 算法演示"""
    print("\n=== Floyd-Warshall 算法演示 ===\n")

    g = Graph()
    edges = [
        (0, 1, 5), (1, 2, 3), (2, 3, 1),
        (3, 0, 2), (0, 2, 4),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    all_distances = g.floyd_warshall()
    print("所有頂點對的最短距離：")
    for u in sorted(all_distances.keys()):
        for v in sorted(all_distances[u].keys()):
            d = all_distances[u][v]
            if d < float('inf'):
                print(f"  {u} → {v}：{d}")


if __name__ == "__main__":
    demo_dijkstra()
    demo_bellman_ford()
    demo_floyd_warshall()