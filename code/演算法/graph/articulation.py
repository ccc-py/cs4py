"""
使用 Tarjan 算法检测无向图中的割点（关节点）和桥（割边）
基于深度优先搜索（DFS），维护发现时间和 low-link 值，线性时间复杂度 O(V+E)
"""

from typing import List, Tuple, Set


class TarjanGraph:
    """封装 Tarjan 算法所需的图结构和计算方法"""

    def __init__(self, num_nodes: int, edges: List[Tuple[int, int]]) -> None:
        """
        初始化无向图

        Args:
            num_nodes: 图的节点总数，节点编号为 0 ~ num_nodes-1
            edges: 边列表，每条边为 (u, v) 表示无向边连接 u 和 v
        """
        self.num_nodes = num_nodes
        self.adj: List[List[int]] = [[] for _ in range(num_nodes)]
        # 无向图需双向添加边
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

    def find_articulation_bridges(self) -> Tuple[Set[int], Set[Tuple[int, int]], List[int], List[int]]:
        """
        执行 Tarjan 算法，返回割点、桥、发现时间和 low-link 值

        Returns:
            tuple: (割点集合, 桥集合, 发现时间列表, low-link 值列表)
        """
        # 发现时间：-1 表示未访问
        disc: List[int] = [-1] * self.num_nodes
        # low-link 值：初始为 -1
        low: List[int] = [-1] * self.num_nodes
        # 父节点数组：-1 表示无父节点（根节点）
        parent: List[int] = [-1] * self.num_nodes
        # 割点集合
        articulation: Set[int] = set()
        # 桥集合，存储为有序元组避免重复
        bridges: Set[Tuple[int, int]] = set()
        # 时间戳计数器
        timer: int = 0

        def dfs(u: int) -> None:
            """深度优先遍历，计算当前节点的发现时间和 low-link 值"""
            nonlocal timer
            children: int = 0  # 根节点的子节点数
            disc[u] = low[u] = timer
            timer += 1

            for v in self.adj[u]:
                if disc[v] == -1:  # 未访问的邻居，为树边
                    children += 1
                    parent[v] = u
                    dfs(v)

                    # 用子节点的 low 值更新当前节点的 low
                    low[u] = min(low[u], low[v])

                    # 检查根节点是否为割点：根节点有 2 个及以上子节点
                    if parent[u] == -1 and children > 1:
                        articulation.add(u)
                    # 检查非根节点是否为割点：子节点的 low >= 当前节点的发现时间
                    if parent[u] != -1 and low[v] >= disc[u]:
                        articulation.add(u)

                    # 检查是否为桥：子节点的 low > 当前节点的发现时间
                    if low[v] > disc[u]:
                        bridges.add((min(u, v), max(u, v)))

                elif v != parent[u]:  # 已访问的邻居，且不是父节点，为回边
                    low[u] = min(low[u], disc[v])

        # 遍历所有未访问的节点，处理非连通图
        for i in range(self.num_nodes):
            if disc[i] == -1:
                dfs(i)

        return articulation, bridges, disc, low


if __name__ == "__main__":
    # 示例图：包含 6 个节点，两个双连通组件通过桥连接
    # 组件1：0-1-2 三角形（0-1,1-2,2-0）
    # 组件2：3-4-5 三角形（3-4,4-5,5-3）
    # 桥：1-3 连接两个组件
    edges = [
        (0, 1), (1, 2), (2, 0),
        (1, 3),
        (3, 4), (4, 5), (5, 3)
    ]
    num_nodes = 6
    detector = TarjanGraph(num_nodes, edges)
    articulation_points, bridges, disc, low = detector.find_articulation_bridges()

    print("=== Tarjan 算法示例 ===")
    print(f"节点数: {num_nodes}")
    print(f"发现时间 (disc): {disc}")
    print(f"Low-link 值 (low): {low}")
    print(f"割点集合: {sorted(articulation_points)}")
    print(f"桥集合: {sorted(bridges)}")
