"""
二分图最大匹配 - Hopcroft-Karp 算法实现
时间复杂度 O(E√V)，适用于大规模二分图匹配场景，如任务分配、资源调度等
"""

from typing import List, Tuple, Dict, Set
from collections import deque


class HopcroftKarp:
    """Hopcroft-Karp 算法实现二分图最大匹配"""

    def __init__(self, num_u: int, num_v: int, edges: List[Tuple[int, int]]) -> None:
        """
        初始化二分图

        Args:
            num_u: 左部节点（U部）数量，节点编号为 0 ~ num_u-1
            num_v: 右部节点（V部）数量，节点编号为 0 ~ num_v-1
            edges: 边列表，每条边为 (u, v) 表示 U部u 到 V部v 的有向边（二分图仅允许跨部边）
        """
        self.num_u = num_u
        self.num_v = num_v
        self.adj: List[List[int]] = [[] for _ in range(num_u)]
        for u, v in edges:
            self.adj[u].append(v)

    def max_matching(self) -> Tuple[int, Dict[int, int]]:
        """
        计算二分图的最大匹配

        Returns:
            tuple: (最大匹配数, 匹配字典：U部节点 -> V部节点)
        """
        # match_u[u] = v 表示U部u匹配到V部v，-1表示未匹配
        match_u: List[int] = [-1] * self.num_u
        # match_v[v] = u 表示V部v匹配到U部u，-1表示未匹配
        match_v: List[int] = [-1] * self.num_v
        # BFS距离数组，最后一个元素为虚拟节点，用于标记未匹配的V部节点
        distance: List[int] = [0] * (self.num_u + 1)
        matching: int = 0

        def bfs() -> bool:
            """BFS构建分层图，返回是否存在增广路"""
            q: deque = deque()
            for u in range(self.num_u):
                if match_u[u] == -1:
                    distance[u] = 0
                    q.append(u)
                else:
                    distance[u] = float('inf')
            distance[self.num_u] = float('inf')  # 虚拟节点初始化为无穷大

            while q:
                u = q.popleft()
                if distance[u] < distance[self.num_u]:
                    for v in self.adj[u]:
                        if match_v[v] == -1:
                            # 找到未匹配的V部节点，更新虚拟节点距离
                            distance[self.num_u] = distance[u] + 1
                        elif distance[match_v[v]] == float('inf'):
                            # 未访问过的匹配U部节点，加入队列
                            distance[match_v[v]] = distance[u] + 1
                            q.append(match_v[v])
            return distance[self.num_u] != float('inf')

        def dfs(u: int) -> bool:
            """DFS寻找增广路并更新匹配"""
            if u != self.num_u:  # 不是虚拟节点
                for v in self.adj[u]:
                    if match_v[v] == -1 or \
                       (distance[match_v[v]] == distance[u] + 1 and dfs(match_v[v])):
                        match_u[u] = v
                        match_v[v] = u
                        return True
                distance[u] = float('inf')
                return False
            return True

        # 迭代寻找增广路直到无更多匹配
        while bfs():
            for u in range(self.num_u):
                if match_u[u] == -1 and dfs(u):
                    matching += 1

        # 构建匹配结果字典
        match_dict: Dict[int, int] = {u: v for u, v in enumerate(match_u) if v != -1}
        return matching, match_dict


if __name__ == "__main__":
    # 任务分配示例：3个工人（U部），3个任务（V部）
    # 工人0可胜任任务0、1；工人1可胜任任务1、2；工人2可胜任任务0、2
    num_u = 3  # 工人数量
    num_v = 3  # 任务数量
    edges = [
        (0, 0), (0, 1),
        (1, 1), (1, 2),
        (2, 0), (2, 2)
    ]

    hk = HopcroftKarp(num_u, num_v, edges)
    max_match, matches = hk.max_matching()

    print("=== 二分图最大匹配示例（任务分配）===")
    print(f"工人数量: {num_u}, 任务数量: {num_v}")
    print(f"最大匹配数: {max_match}")
    print("匹配结果（工人 -> 任务）:")
    for u, v in sorted(matches.items()):
        print(f"  工人{u} -> 任务{v}")
