"""
Push-Relabel 演算法：用於最大流問題

Push-Relabel 演算法由 Goldberg 和 Tarjan 於 1988 年提出，是目前最快的
最大流演算法之一。與 Ford-Fulkerson 的增廣路方法不同，Push-Relabel
使用前饋（preflow）和高度函數的概念，更有效率地處理網絡流。

時間複雜度：O(n³)（一般版本），使用 Gap heuristic 可達 O(n²√m)
空間複雜度：O(n²)

核心概念：
- Preflow：允許流入節點的流量超過流出流量（違背流守恆）
- Height function：確保流量只從高處流向低處
- Push：將多餘流量從溢位節點推送至相鄰節點
- Relabel：當節點無法推送時，提高其高度

作者：陳鍾誠
日期：2024
"""

from collections import deque
from typing import Optional


class PushRelabel:
    """Push-Relabel 最大流演算法實現"""

    def __init__(self, num_vertices: int, source: int, sink: int):
        """
        初始化網絡流演算法

        Args:
            num_vertices: 節點數量
            source: 源點索引
            sink: 匯點索引
        """
        self.n = num_vertices
        self.s = source
        self.t = sink
        self.capacity: list[list[int]] = [[0] * num_vertices for _ in range(num_vertices)]
        self.flow: list[list[int]] = [[0] * num_vertices for _ in range(num_vertices)]
        self.height: list[int] = [0] * num_vertices
        self.excess: list[int] = [0] * num_vertices
        self.count: list[int] = [0] * (2 * num_vertices)
        self.active: list[bool] = [False] * num_vertices
        self.queue: deque[int] = deque()

    def add_edge(self, u: int, v: int, cap: int) -> None:
        """
        添加一條有向邊及其容量

        Args:
            u: 起點
            v: 終點
            cap: 容量
        """
        self.capacity[u][v] += cap

    def _initialize_preflow(self) -> None:
        """初始化前饋：從源點流出所有可能流量"""
        self.height[self.s] = self.n
        for v in range(self.n):
            if self.capacity[self.s][v] > 0:
                self.flow[self.s][v] = self.capacity[self.s][v]
                self.flow[v][self.s] = -self.flow[self.s][v]
                self.excess[v] = self.capacity[self.s][v]
                if v != self.t and v != self.s:
                    self.queue.append(v)

    def _push(self, u: int, v: int) -> bool:
        """
        嘗試從 u 推送流量到 v

        Args:
            u: 源節點
            v: 目標節點

        Returns:
            是否成功推送
        """
        send = min(self.excess[u], self.capacity[u][v] - self.flow[u][v])
        if send <= 0:
            return False
        self.flow[u][v] += send
        self.flow[v][u] -= send
        self.excess[u] -= send
        self.excess[v] += send
        if not self.active[v] and v != self.s and v != self.t:
            self.active[v] = True
            self.queue.append(v)
        return True

    def _relabel(self, u: int) -> None:
        """重新標記節點 u 的高度"""
        min_height = float('inf')
        for v in range(self.n):
            if self.capacity[u][v] - self.flow[u][v] > 0:
                min_height = min(min_height, self.height[v])
        if min_height == float('inf'):
            return
        self.height[u] = min_height + 1

    def _gap_heuristic(self, height: int) -> None:
        """
        Gap 啟發式：如果某高度沒有節點，則所有高於該高度的節點
        都無法到達匯點，可以標記為無效

        Args:
            height: 間隙高度
        """
        for v in range(self.n):
            if self.height[v] > height and v != self.s and v != self.t:
                self.height[v] = max(self.height[v], self.n + 1)

    def _discharge(self, u: int) -> None:
        """
        排出節點 u 的所有 excess flow

        Args:
            u: 要排出的節點
        """
        while self.excess[u] > 0:
            if self.height[u] <= self.height[u]:
                self._relabel(u)
                self.count[self.height[u]] += 1
                if self.count[self.height[u]] == 0:
                    self._gap_heuristic(self.height[u])
            pushed = False
            for v in range(self.n):
                if self.excess[u] > 0 and self.capacity[u][v] - self.flow[u][v] > 0:
                    if self.height[u] == self.height[v] + 1:
                        self._push(u, v)
                        pushed = True
            if not pushed:
                self._relabel(u)
                self.count[self.height[u]] += 1
                if self.count[self.height[u]] == 0:
                    self._gap_heuristic(self.height[u])

    def max_flow(self) -> int:
        """
        計算最大流值

        Returns:
            最大流量
        """
        self._initialize_preflow()
        self.count[0] = self.n - 1

        while self.queue:
            u = self.queue.popleft()
            self.active[u] = False
            self._discharge(u)

        return self.excess[self.t]

    def get_flow(self, u: int, v: int) -> int:
        """取得邊 (u, v) 的流量"""
        return self.flow[u][v]

    def get_min_cut(self) -> set[int]:
        """
        取得最小割的源側節點集合

        Returns:
            在最小割源側的節點集合
        """
        visited = [False] * self.n
        visited[self.s] = True
        queue = deque([self.s])

        while queue:
            u = queue.popleft()
            for v in range(self.n):
                if not visited[v] and self.capacity[u][v] - self.flow[u][v] > 0:
                    visited[v] = True
                    queue.append(v)

        cut_nodes = {i for i in range(self.n) if visited[i]}
        return cut_nodes


def create_network(num_vertices: int) -> PushRelabel:
    """
    建立範例網絡

    Args:
        num_vertices: 節點數量

    Returns:
        PushRelabel 實例
    """
    return PushRelabel(num_vertices, source=0, sink=num_vertices - 1)


if __name__ == "__main__":
    print("=" * 60)
    print("Push-Relabel 最大流演算法範例")
    print("=" * 60)

    n = 6
    pr = PushRelabel(n, source=0, sink=5)

    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 10), (1, 3, 12),
        (2, 1, 4), (2, 4, 14),
        (3, 2, 9), (3, 5, 20),
        (4, 3, 7), (4, 5, 4)
    ]

    for u, v, cap in edges:
        pr.add_edge(u, v, cap)

    print(f"\n網絡：{n} 個節點，{len(edges)} 條邊")
    print(f"源點：0，匯點：5")
    print("\n邊的容量：")
    for u, v, cap in edges:
        print(f"  ({u} → {v}): {cap}")

    maxflow = pr.max_flow()
    print(f"\n最大流量：{maxflow}")

    cut = pr.get_min_cut()
    print(f"最小割的源側節點：{cut}")

    print("\n各邊的流量：")
    for u in range(n):
        for v in range(n):
            f = pr.get_flow(u, v)
            if f > 0:
                print(f"  ({u} → {v}): {f} / {pr.capacity[u][v]}")

    print("\n" + "=" * 60)
    print("範例 2：更簡單的網絡")
    print("=" * 60)

    pr2 = PushRelabel(4, source=0, sink=3)
    pr2.add_edge(0, 1, 10)
    pr2.add_edge(0, 2, 10)
    pr2.add_edge(1, 2, 2)
    pr2.add_edge(1, 3, 4)
    pr2.add_edge(2, 3, 8)

    print("\n網絡：4 個節點")
    print("邊：(0→1:10), (0→2:10), (1→2:2), (1→3:4), (2→3:8)")

    result = pr2.max_flow()
    print(f"\n最大流量：{result}")