"""
最小成本最大流 (Minimum Cost Maximum Flow)

歷史背景：
- 最小成本流問題是網路流理論的重要擴展
- 由 George Dantzig 於 1951 年提出線性規劃公式
- 連續最短路徑演算法（Successive Shortest Path）由 Busacker 和 Gowen 於 1961 年提出
- 可用於運輸問題、供應鏈優化等場景

應用場景：
- 運輸問題（最小化運輸成本）
- 網路路由（最小化延遲）
- 資源分配
- 電路設計
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, deque


class MinCostFlowNetwork:
    """最小成本流網路類別"""

    def __init__(self):
        """初始化網路"""
        self.graph: Dict[str, List['Edge']] = defaultdict(list)
        self.original_edges: List[Tuple[str, str, int, int]] = []

    def add_edge(self, u: str, v: str, capacity: int, cost: int) -> None:
        """
        添加有向邊及其容量和成本

        Args:
            u: 起點
            v: 終點
            capacity: 容量
            cost: 單位流量成本
        """
        self.original_edges.append((u, v, capacity, cost))
        # 正向邊
        forward = Edge(u, v, capacity, cost)
        # 反向邊（初始容量 0，成本為負）
        backward = Edge(v, u, 0, -cost)
        forward.reverse = backward
        backward.reverse = forward
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def bellman_ford(self, source: str, sink: str) -> Optional[Tuple[List[str], List['Edge'], int]]:
        """
        使用 Bellman-Ford 找從 source 到 sink 的最短路徑（以成本為權重）
        僅考慮殘留容量 > 0 的邊

        Returns:
            (路徑節點列表, 路徑邊列表, 路徑總成本) 或 None
        """
        dist: Dict[str, float] = defaultdict(lambda: float('inf'))
        dist[source] = 0
        prev_node: Dict[str, Optional[str]] = {source: None}
        prev_edge: Dict[str, Optional['Edge']] = {source: None}

        # 需要所有節點列表
        nodes = set(self.graph.keys())

        # 鬆弛 V-1 次
        for _ in range(len(nodes) - 1):
            updated = False
            for u in nodes:
                if dist[u] == float('inf'):
                    continue
                for edge in self.graph[u]:
                    if edge.capacity > 0 and dist[u] + edge.cost < dist[edge.v]:
                        dist[edge.v] = dist[u] + edge.cost
                        prev_node[edge.v] = u
                        prev_edge[edge.v] = edge
                        updated = True
            if not updated:
                break

        if dist[sink] == float('inf'):
            return None

        # 重建路徑
        path_nodes = []
        path_edges = []
        curr = sink
        while curr != source:
            edge = prev_edge[curr]
            path_edges.append(edge)
            path_nodes.append(curr)
            curr = prev_node[curr]
        path_nodes.append(source)
        path_nodes.reverse()
        path_edges.reverse()

        return path_nodes, path_edges, dist[sink]

    def min_cost_max_flow(self, source: str, sink: str) -> Tuple[int, int, Dict]:
        """
        連續最短路徑演算法求最小成本最大流

        原理：
        1. 初始化總流量 = 0，總成本 = 0
        2. 當存在從源點到匯點的路徑（以成本為權重的最短路徑）：
           a. 使用 Bellman-Ford 找最短路徑
           b. 找出路徑上的瓶頸容量（最小殘留容量）
           c. 沿路徑增廣流量，更新殘留網路
           d. 更新總流量和總成本
        3. 返回（總流量, 總成本, 最終殘留網路）

        時間複雜度：O(V * E * F)，F 為最大流量
        空間複雜度：O(V + E)

        Args:
            source: 源點
            sink: 匯點

        Returns:
            (最大流量, 最小總成本, 各邊流量字典)
        """
        total_flow = 0
        total_cost = 0
        edge_flow: Dict[Tuple[str, str], int] = defaultdict(int)

        while True:
            result = self.bellman_ford(source, sink)
            if result is None:
                break

            path_nodes, path_edges, path_cost = result

            # 找瓶頸容量
            bottleneck = min(edge.capacity for edge in path_edges)

            # 增廣流量
            for edge in path_edges:
                edge.capacity -= bottleneck
                edge.reverse.capacity += bottleneck

                # 記錄正向邊的流量
                if edge.cost >= 0:  # 正向邊
                    edge_flow[(edge.u, edge.v)] += bottleneck
                else:  # 反向邊（表示取消流量）
                    edge_flow[(edge.v, edge.u)] -= bottleneck

            total_flow += bottleneck
            total_cost += bottleneck * path_cost

        return total_flow, total_cost, dict(edge_flow)

    def print_result(self, source: str, sink: str) -> None:
        """印出計算結果"""
        flow, cost, edge_flow = self.min_cost_max_flow(source, sink)
        print(f"最小成本最大流：")
        print(f"  最大流量：{flow}")
        print(f"  最小總成本：{cost}")
        print(f"  各邊流量：")
        for (u, v), f in edge_flow.items():
            if f > 0:
                print(f"    {u} -> {v}: {f}")


class Edge:
    """邊類別"""

    def __init__(self, u: str, v: str, capacity: int, cost: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.cost = cost
        self.reverse: Optional['Edge'] = None

    def __repr__(self):
        return f"Edge({self.u}->{self.v}, cap={self.capacity}, cost={self.cost})"


def build_sample_network() -> MinCostFlowNetwork:
    """建立示例網路"""
    network = MinCostFlowNetwork()
    # 示例：運輸網路
    # s -> a (容量 4, 成本 2)
    # s -> b (容量 2, 成本 5)
    # a -> t (容量 3, 成本 3)
    # b -> t (容量 3, 成本 2)
    # a -> b (容量 1, 成本 1)  # 允許轉運
    network.add_edge("s", "a", 4, 2)
    network.add_edge("s", "b", 2, 5)
    network.add_edge("a", "t", 3, 3)
    network.add_edge("b", "t", 3, 2)
    network.add_edge("a", "b", 1, 1)
    return network


if __name__ == "__main__":
    print("=== 最小成本最大流 (Minimum Cost Maximum Flow) 測試 ===\n")

    # 測試 1：示例網路
    print("1. 運輸網路示例：")
    network = build_sample_network()
    print("網路邊（容量, 成本）：")
    for u, v, cap, cost in network.original_edges:
        print(f"  {u} -> {v}: 容量 {cap}, 成本 {cost}")
    print()

    flow, cost, edge_flow = network.min_cost_max_flow("s", "t")
    print(f"最大流量：{flow}")
    print(f"最小總成本：{cost}")
    print("各邊流量：")
    for (u, v), f in edge_flow.items():
        if f > 0:
            print(f"  {u} -> {v}: {f}")
    print()

    # 測試 2：簡單網路
    print("2. 簡單網路：")
    simple = MinCostFlowNetwork()
    simple.add_edge("s", "t", 5, 10)
    flow, cost, _ = simple.min_cost_max_flow("s", "t")
    print(f"單邊 s->t (容量 5, 成本 10)，最大流：{flow}，總成本：{cost}")
    print()

    # 測試 3：多路徑選擇
    print("3. 多路徑成本比較：")
    multi = MinCostFlowNetwork()
    multi.add_edge("s", "a", 3, 1)
    multi.add_edge("s", "b", 3, 4)
    multi.add_edge("a", "t", 3, 1)
    multi.add_edge("b", "t", 3, 1)
    multi.add_edge("a", "b", 2, 1)
    flow, cost, _ = multi.min_cost_max_flow("s", "t")
    print(f"網路有低成本路徑，最大流：{flow}，總成本：{cost}")
    print()

    # 測試 4：零流量情況
    print("4. 無可行流：")
    empty = MinCostFlowNetwork()
    empty.add_edge("a", "b", 0, 5)
    flow, cost, _ = empty.min_cost_max_flow("a", "b")
    print(f"容量為 0 的邊，最大流：{flow}，總成本：{cost}")
    print()
    print("測試完成！")
