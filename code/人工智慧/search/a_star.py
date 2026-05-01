"""
A* 搜尋演算法 (A-Star Search Algorithm)

歷史背景：
- 1968 年由 Peter Hart, Nils Nilsson, Bertram Raphael 提出
- 結合 Dijkstra 演算法和貪婪最佳優先搜尋的優點
- 在啟發式函數滿足 admissible 條件時保證找到最短路徑
- 廣泛應用於路徑規劃、遊戲 AI、機器人導航等領域

核心概念：
- f(n) = g(n) + h(n)
- g(n)：從起點到當前節點的實際成本
- h(n)：從當前節點到目標的估計成本（啟發函數）
- 使用優先佇列確保每次擴展 f 值最小的節點
"""

from typing import List, Tuple, Dict, Optional, Set
import heapq
import math


class Node:
    """A* 搜尋中的節點"""

    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.g = 0.0  # 從起點到當前節點的實際成本
        self.h = 0.0  # 啟發式估計成本
        self.f = 0.0  # f = g + h
        self.parent: Optional['Node'] = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """計算兩點之間的曼哈頓距離"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic_euclidean(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """計算兩點之間的歐幾里得距離"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def astar(
    grid: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    diagonal: bool = False,
) -> Optional[List[Tuple[int, int]]]:
    """
    A* 搜尋演算法

    參數：
        grid: 二維網格，0 表示可通行，1 表示障礙物
        start: 起點座標 (row, col)
        end: 終點座標 (row, col)
        diagonal: 是否允許對角線移動

    返回：
        最短路徑的座標列表，若無路徑則返回 None

    時間複雜度：O(E log V)，E 為邊數，V 為節點數
    空間複雜度：O(V)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return None

    # 四個基本方向
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if diagonal:
        directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    # 優先佇列：(f_score, counter, node)
    counter = 0
    open_set = []
    start_node = Node(start)
    heapq.heappush(open_set, (start_node.f, counter, start_node))

    closed_set: Set[Tuple[int, int]] = set()
    g_scores: Dict[Tuple[int, int], float] = {start: 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current.position == end:
            # 重建路徑
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            return path[::-1]

        closed_set.add(current.position)

        for dr, dc in directions:
            nr, nc = current.position[0] + dr, current.position[1] + dc

            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] == 1:
                continue
            if (nr, nc) in closed_set:
                continue

            # 對角線移動成本為 sqrt(2)，直線為 1
            move_cost = math.sqrt(2) if diagonal and (dr != 0 and dc != 0) else 1.0
            tentative_g = current.g + move_cost

            neighbor = Node((nr, nc))
            neighbor.g = tentative_g
            neighbor.h = heuristic((nr, nc), end)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.parent = current

            # 若找到更短路徑則更新
            if tentative_g < g_scores.get((nr, nc), float('inf')):
                g_scores[(nr, nc)] = tentative_g
                counter += 1
                heapq.heappush(open_set, (neighbor.f, counter, neighbor))

    return None


def astar_weighted(
    grid: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    weight: float = 1.5,
) -> Optional[List[Tuple[int, int]]]:
    """
    加權 A* 搜尋

    使用 f(n) = g(n) + w * h(n)，w > 1 時加速搜尋但可能非最優
    w = 1 時等同標準 A*
    w 越大越偏向貪婪搜尋
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return None

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    counter = 0
    open_set = []
    start_node = Node(start)
    start_node.h = heuristic(start, end)
    start_node.f = start_node.g + weight * start_node.h
    heapq.heappush(open_set, (start_node.f, counter, start_node))

    closed_set: Set[Tuple[int, int]] = set()
    g_scores: Dict[Tuple[int, int], float] = {start: 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current.position == end:
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            return path[::-1]

        closed_set.add(current.position)

        for dr, dc in directions:
            nr, nc = current.position[0] + dr, current.position[1] + dc

            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] == 1:
                continue
            if (nr, nc) in closed_set:
                continue

            tentative_g = current.g + 1.0
            neighbor = Node((nr, nc))
            neighbor.g = tentative_g
            neighbor.h = heuristic((nr, nc), end)
            neighbor.f = neighbor.g + weight * neighbor.h
            neighbor.parent = current

            if tentative_g < g_scores.get((nr, nc), float('inf')):
                g_scores[(nr, nc)] = tentative_g
                counter += 1
                heapq.heappush(open_set, (neighbor.f, counter, neighbor))

    return None


def print_grid_with_path(grid: List[List[int]], path: Optional[List[Tuple[int, int]]]) -> str:
    """將網格和路徑以字串形式顯示"""
    result = []
    path_set = set(path) if path else set()

    for r in range(len(grid)):
        row_str = ""
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                row_str += "█ "
            elif (r, c) in path_set:
                row_str += "● "
            else:
                row_str += "· "
        result.append(row_str)

    return "\n".join(result)


def demo_simple():
    """簡單 A* 演示"""
    print("=== A* 搜尋演算法演示 ===\n")

    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
    ]

    start = (0, 0)
    end = (4, 4)

    print("網格（█=障礙物）：")
    print(print_grid_with_path(grid, None))
    print()

    path = astar(grid, start, end)

    if path:
        print(f"找到路徑（長度={len(path)}）：")
        print(print_grid_with_path(grid, path))
        print(f"\n路徑座標：{path}")
    else:
        print("無法找到路徑")


def demo_maze():
    """迷宮 A* 演示"""
    print("\n=== 迷宮 A* 搜尋 ===\n")

    maze = [
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0],
    ]

    start = (0, 0)
    end = (7, 7)

    print("迷宮：")
    print(print_grid_with_path(maze, None))
    print()

    path = astar(maze, start, end)

    if path:
        print(f"找到路徑（長度={len(path)}）：")
        print(print_grid_with_path(maze, path))
    else:
        print("無法找到路徑")


def demo_weighted():
    """加權 A* 比較"""
    print("\n=== 加權 A* 比較 ===\n")

    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ]

    start = (0, 0)
    end = (4, 7)

    for w in [1.0, 1.5, 2.0, 5.0]:
        path = astar_weighted(grid, start, end, weight=w)
        if path:
            print(f"w={w}: 路徑長度={len(path)}")
        else:
            print(f"w={w}: 無路徑")


if __name__ == "__main__":
    demo_simple()
    demo_maze()
    demo_weighted()
