"""
圖的遍歷：廣度優先搜索 (BFS) 和深度優先搜索 (DFS)

歷史背景：
- BFS 由 E. F. Codd 的學生於 1959 年提出
- DFS 的概念源於早期迷宮搜索算法
- 圖論基礎算法，應用於最短路徑、連通分量、拓撲排序等
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import deque


class Graph:
    """圖的表示"""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[int, List[int]] = {}

    def add_vertex(self, v: int) -> None:
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u: int, v: int) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start: int) -> List[int]:
        """
        廣度優先搜索

        時間複雜度：O(V + E)
        空間複雜度：O(V)

        BFS 使用佇列，確保按層級遍歷
        """
        if start not in self.adj:
            return []

        visited: Set[int] = set()
        queue = deque([start])
        result = []

        while queue:
            vertex = queue.popleft()
            if vertex in visited:
                continue

            visited.add(vertex)
            result.append(vertex)

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)

        return result

    def bfs_with_levels(self, start: int) -> Dict[int, int]:
        """BFS 並記錄每個節點的層級"""
        if start not in self.adj:
            return {}

        visited: Set[int] = set()
        queue = deque([(start, 0)])
        levels: Dict[int, int] = {}

        while queue:
            vertex, level = queue.popleft()
            if vertex in visited:
                continue

            visited.add(vertex)
            levels[vertex] = level

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))

        return levels

    def bfs_shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        """BFS 找最短路徑"""
        if start not in self.adj or end not in self.adj:
            return None

        if start == end:
            return [start]

        visited: Set[int] = set()
        queue = deque([(start, [start])])

        while queue:
            vertex, path = queue.popleft()
            if vertex in visited:
                continue

            visited.add(vertex)

            for neighbor in self.adj[vertex]:
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None

    def dfs_recursive(self, start: int) -> List[int]:
        """
        深度優先搜索（遞迴版本）

        時間複雜度：O(V + E)
        空間複雜度：O(V)
        """
        visited: Set[int] = set()
        result = []

        def dfs(v: int) -> None:
            visited.add(v)
            result.append(v)

            for neighbor in self.adj[v]:
                if neighbor not in visited:
                    dfs(neighbor)

        if start in self.adj:
            dfs(start)

        return result

    def dfs_iterative(self, start: int) -> List[int]:
        """
        深度優先搜索（迭代版本，使用堆疊）

        時間複雜度：O(V + E)
        空間複雜度：O(V)
        """
        if start not in self.adj:
            return []

        visited: Set[int] = set()
        stack = [start]
        result = []

        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue

            visited.add(vertex)
            result.append(vertex)

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)

        return result

    def dfs_stack_with_order(self, start: int) -> Tuple[List[int], List[int]]:
        """
        DFS 記錄訪問順序和完成順序

        類似於 Tarjan's algorithm 的前處理
        """
        if start not in self.adj:
            return [], []

        visited: Set[int] = set()
        visited_order = []
        finished_order = []
        stack = [(start, False)]

        while stack:
            vertex, is_processed = stack.pop()

            if is_processed:
                finished_order.append(vertex)
                continue

            if vertex in visited:
                continue

            visited.add(vertex)
            visited_order.append(vertex)
            stack.append((vertex, True))

            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    stack.append((neighbor, False))

        return visited_order, finished_order

    def count_connected_components(self) -> int:
        """計算連通分量數量"""
        visited: Set[int] = set()
        count = 0

        for vertex in self.adj:
            if vertex not in visited:
                component = self.bfs(vertex)
                visited.update(component)
                count += 1

        return count

    def is_bipartite(self) -> bool:
        """檢查圖是否為二分圖"""
        if not self.adj:
            return True

        color: Dict[int, bool] = {}
        queue = deque([(next(iter(self.adj)), True)])

        while queue:
            vertex, is_red = queue.popleft()

            if vertex in color:
                if color[vertex] != is_red:
                    return False
                continue

            color[vertex] = is_red

            for neighbor in self.adj[vertex]:
                queue.append((neighbor, not is_red))

        return True


def demo_bfs():
    """BFS 演示"""
    print("=== 廣度優先搜索 (BFS) 演示 ===\n")

    g = Graph()
    edges = [
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
    ]
    for u, v in edges:
        g.add_edge(u, v)

    print("圖結構：")
    print("       0")
    print("      / \\")
    print("     1   2")
    print("    / \\ / \\")
    print("   3   4 5   6")
    print()

    print(f"BFS 遍歷（從 0 開始）：{g.bfs(0)}")
    print(f"各節點層級：{g.bfs_with_levels(0)}")

    print(f"\n最短路徑（0 到 6）：{g.bfs_shortest_path(0, 6)}")
    print(f"最短路徑（0 到 3）：{g.bfs_shortest_path(0, 3)}")


def demo_dfs():
    """DFS 演示"""
    print("\n=== 深度優先搜索 (DFS) 演示 ===\n")

    g = Graph()
    edges = [
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
    ]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"DFS 遍歷（遞迴）：{g.dfs_recursive(0)}")
    print(f"DFS 遍歷（迭代）：{g.dfs_iterative(0)}")

    visit_order, finish_order = g.dfs_stack_with_order(0)
    print(f"訪問順序：{visit_order}")
    print(f"完成順序：{finish_order}")


def demo_graph_properties():
    """圖屬性演示"""
    print("\n=== 圖屬性演示 ===\n")

    g1 = Graph()
    for u, v in [(0, 1), (1, 2), (2, 0), (3, 4)]:
        g1.add_edge(u, v)
    print(f"圖（兩個連通分量）：連通分量數 = {g1.count_connected_components()}")

    g2 = Graph()
    for u, v in [(0, 1), (1, 2), (2, 0), (2, 3)]:
        g2.add_edge(u, v)
    print(f"圖（可二分）：{g2.is_bipartite()}")


if __name__ == "__main__":
    demo_bfs()
    demo_dfs()
    demo_graph_properties()