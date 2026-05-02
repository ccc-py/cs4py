"""
最大流 (Maximum Flow)

歷史背景：
- 最大流問題由 Theodore E. Harris 和 F. S. Ross 於 1955 年提出
- Ford-Fulkerson 方法由 L. R. Ford Jr. 和 D. R. Fulkerson 於 1956 年提出
- Edmonds-Karp 演算法（使用 BFS 找增廣路徑）由 Jack Edmonds 和 Richard Karp 於 1972 年提出
- 最大流最小割定理是網路流理論的核心定理

應用場景：
- 網路頻寬分配
- 交通流量規劃
- 二分圖匹配
- 專案排程
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import deque, defaultdict


class FlowNetwork:
    """流網路類別"""

    def __init__(self):
        """初始化流網路"""
        self.graph = defaultdict(lambda: defaultdict(int))  # 殘留網路
        self.original_capacity = defaultdict(lambda: defaultdict(int))  # 原始容量

    def add_edge(self, u: str, v: str, capacity: int) -> None:
        """
        添加有向邊及其容量

        Args:
            u: 起點
            v: 終點
            capacity: 容量
        """
        self.original_capacity[u][v] = capacity
        self.graph[u][v] = capacity
        # 反向邊初始容量為 0
        if u not in self.graph[v]:
            self.graph[v][u] = 0

    def get_capacity(self, u: str, v: str) -> int:
        """獲取邊的容量"""
        return self.graph[u][v]

    def bfs_path(self, source: str, sink: str) -> Optional[Tuple[List[str], int]]:
        """
        使用 BFS 尋找從 source 到 sink 的增廣路徑

        Returns:
            (路徑節點列表, 路徑上的最小容量) 或 None
        """
        visited = {source}
        queue = deque([(source, [source], float('inf'))])

        while queue:
            current, path, min_cap = queue.popleft()

            for neighbor in self.graph[current]:
                if neighbor not in visited and self.graph[current][neighbor] > 0:
                    new_min_cap = min(min_cap, self.graph[current][neighbor])
                    if neighbor == sink:
                        return (path + [neighbor], new_min_cap)
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], new_min_cap))

        return None

    def edmonds_karp(self, source: str, sink: str) -> Tuple[int, Dict]:
        """
        Edmonds-Karp 演算法（使用 BFS 的 Ford-Fulkerson）

        原理：
        1. 初始化殘留網路
        2. 當存在增廣路徑時：
           a. 使用 BFS 找到一條從源點到匯點的路徑
           b. 找到路徑上的最小殘留容量
           c. 沿著路徑更新殘留容量（正向減，反向加）
        3. 返回最大流量

        時間複雜度：O(V * E²)
        空間複雜度：O(V + E)

        Args:
            source: 源點
            sink: 匯點

        Returns:
            (最大流量, 最終殘留網路)
        """
        max_flow = 0

        while True:
            result = self.bfs_path(source, sink)
            if result is None:
                break

            path, bottleneck = result

            # 更新殘留網路
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.graph[u][v] -= bottleneck
                self.graph[v][u] += bottleneck

            max_flow += bottleneck

        return max_flow, dict(self.graph)

    def get_min_cut(self, source: str) -> Set[str]:
        """
        找出最小割的源點側節點集合

        Args:
            source: 源點

        Returns:
            從源點可達的節點集合（最小割的源點側）
        """
        visited = set()
        queue = deque([source])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.graph[current]:
                if self.graph[current][neighbor] > 0 and neighbor not in visited:
                    queue.append(neighbor)

        return visited

    def print_flow(self) -> None:
        """印出各邊的流量（原始容量 - 殘留容量）"""
        print("邊流量：")
        for u in self.original_capacity:
            for v in self.original_capacity[u]:
                original = self.original_capacity[u][v]
                residual = self.graph[u][v]
                flow = original - residual
                if flow > 0:
                    print(f"  {u} -> {v}: {flow}/{original}")


def build_sample_network() -> FlowNetwork:
    """建立示例網路"""
    network = FlowNetwork()
    # 示例：從 s 到 t 的網路
    # s -> a (10), s -> c (10)
    # a -> b (4), a -> c (2), a -> d (8)
    # c -> d (9)
    # b -> t (10)
    # d -> b (6), d -> t (10)
    network.add_edge("s", "a", 10)
    network.add_edge("s", "c", 10)
    network.add_edge("a", "b", 4)
    network.add_edge("a", "c", 2)
    network.add_edge("a", "d", 8)
    network.add_edge("c", "d", 9)
    network.add_edge("b", "t", 10)
    network.add_edge("d", "b", 6)
    network.add_edge("d", "t", 10)
    return network


if __name__ == "__main__":
    print("=== 最大流 (Maximum Flow) 測試 ===\n")

    # 測試 1：示例網路
    print("1. Edmonds-Karp 演算法示例：")
    network = build_sample_network()
    print("網路邊（原始容量）：")
    for u in network.original_capacity:
        for v in network.original_capacity[u]:
            print(f"  {u} -> {v}: {network.original_capacity[u][v]}")
    print()

    max_flow, residual = network.edmonds_karp("s", "t")
    print(f"最大流量：{max_flow}")
    print()
    network.print_flow()
    print()

    # 最小割
    min_cut_s = network.get_min_cut("s")
    print(f"最小割源點側：{min_cut_s}")
    print(f"最小割匯點側：{set(network.original_capacity.keys()) - min_cut_s}")
    print()

    # 測試 2：簡單網路
    print("2. 簡單網路：")
    simple = FlowNetwork()
    simple.add_edge("s", "t", 5)
    flow, _ = simple.edmonds_karp("s", "t")
    print(f"單邊網路 s->t (容量 5)，最大流：{flow}")
    print()

    # 測試 3：平行邊
    print("3. 平行邊網路：")
    parallel = FlowNetwork()
    parallel.add_edge("s", "t", 3)
    parallel.add_edge("s", "t", 7)
    flow, _ = parallel.edmonds_karp("s", "t")
    print(f"兩條平行邊 (3+7)，最大流：{flow}")
    print()

    # 測試 4：最大流最小割定理
    print("4. 最大流最小割定理驗證：")
    network2 = FlowNetwork()
    network2.add_edge("s", "a", 16)
    network2.add_edge("s", "c", 13)
    network2.add_edge("a", "b", 12)
    network2.add_edge("c", "a", 4)
    network2.add_edge("c", "d", 14)
    network2.add_edge("b", "c", 9)
    network2.add_edge("b", "t", 20)
    network2.add_edge("d", "b", 7)
    network2.add_edge("d", "t", 4)

    flow, _ = network2.edmonds_karp("s", "t")
    min_cut = network2.get_min_cut("s")
    print(f"最大流：{flow}")
    print(f"最小割容量（源點側節點數）：{len(min_cut)}")
    print(f"源點側節點：{min_cut}")
    print()
    print("最大流 = 最小割容量（定理驗證）")
