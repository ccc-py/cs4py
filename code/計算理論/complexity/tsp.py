"""
旅行推銷員問題 (Traveling Salesman Problem, TSP)

TSP 是組合最佳化中的經典 NP-hard 問題。

問題描述：
給定一組城市和它們之間的距離，
尋找一條經過每個城市恰好一次並回到起始城市的最短路徑。

歷史背景：
- 1930 年代：TSP 在維也納和哈佛同時被研究
- 1972 年：Karp 證明了 TSP 是 NP-hard 的
- 至今：仍是組合最佳化中最著名的問題之一

參考：Karp, R. M. (1972). Reducibility among combinatorial problems.
"""

from typing import List, Tuple, Dict, Optional
import itertools


def brute_force_tsp(distances: List[List[int]]) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    暴力求解 TSP（列舉所有排列）

    時間複雜度：O(n!)，僅適用於小 n

    Args:
        distances: n×n 距離矩陣，distances[i][j] = 從 i 到 j 的距離

    Returns:
        (最短路徑, 最短距離) 或 (None, None) 如果無解
    """
    n = len(distances)
    if n == 0:
        return None, None

    cities = list(range(n))
    min_path = None
    min_dist = float('inf')

    # 固定起點為 0，只需排列剩餘 n-1 個城市
    for perm in itertools.permutations(cities[1:]):
        path = [0] + list(perm) + [0]  # 回到起點
        dist = 0
        for i in range(n):
            dist += distances[path[i]][path[i + 1]]
        if dist < min_dist:
            min_dist = dist
            min_path = path

    return min_path, min_dist


def nearest_neighbor_tsp(distances: List[List[int]]) -> Tuple[List[int], int]:
    """
    最近鄰居啟發式 (Nearest Neighbor Heuristic)

    從起點開始，每次選擇最近的未訪問城市。
    不保證最優解，但速度快 O(n²)。

    Returns:
        (路徑, 總距離)
    """
    n = len(distances)
    if n == 0:
        return [], 0

    visited = [False] * n
    path = [0]
    visited[0] = True
    total_dist = 0

    current = 0
    for _ in range(n - 1):
        # 找最近未訪問城市
        nearest = -1
        min_dist = float('inf')
        for city in range(n):
            if not visited[city] and distances[current][city] < min_dist:
                min_dist = distances[current][city]
                nearest = city

        if nearest == -1:
            break

        path.append(nearest)
        visited[nearest] = True
        total_dist += min_dist
        current = nearest

    # 回到起點
    path.append(0)
    total_dist += distances[current][0]

    return path, total_dist


def create_example_tsp() -> Tuple[List[List[int]], List[str]]:
    """
    建立一個 4 城市 TSP 範例

    城市：A(0), B(1), C(2), D(3)
    距離矩陣：
        A  B  C  D
    A   0  10 15 20
    B  10   0  35 25
    C  15  35   0 30
    D  20  25  30  0
    """
    distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    cities = ['A', 'B', 'C', 'D']
    return distances, cities


def is_valid_tsp_path(path: List[int], n: int) -> bool:
    """檢查是否為有效的 TSP 路徑"""
    if len(path) != n + 1:
        return False
    if path[0] != path[-1]:
        return False
    visited = set(path[1:-1])
    return len(visited) == n - 1


if __name__ == "__main__":
    print("=== 旅行推銷員問題 (TSP) 測試 ===")
    print()

    # 建立範例
    distances, cities = create_example_tsp()
    print("城市：", cities)
    print("距離矩陣：")
    for i, row in enumerate(distances):
        print(f"  {cities[i]}: {row}")
    print()

    # 暴力求解
    print("暴力求解（適用於小 n）：")
    path, dist = brute_force_tsp(distances)
    print(f"  最短路徑：{' -> '.join(cities[p] for p in path)}")
    print(f"  距離：{dist}")
    print()

    # 最近鄰居啟發式
    print("最近鄰居啟發式：")
    path, dist = nearest_neighbor_tsp(distances)
    print(f"  路徑：{' -> '.join(cities[p] for p in path)}")
    print(f"  距離：{dist}")
    print()

    # 比較
    print("比較：")
    opt_path, opt_dist = brute_force_tsp(distances)
    nn_path, nn_dist = nearest_neighbor_tsp(distances)
    print(f"  最優解：{opt_dist}")
    print(f"  啟發式：{nn_dist}")
    print(f"  比率：{nn_dist / opt_dist:.2f}x")
