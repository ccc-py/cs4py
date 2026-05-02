"""
最短路徑演算法：Bellman-Ford 與 Floyd-Warshall

歷史背景：
- Bellman-Ford 演算法由 Richard Bellman 和 Lester Ford 分別於 1958 和 1956 年提出
- Floyd-Warshall 演算法由 Robert Floyd 於 1962 年提出，基於 Warshall 的傳遞閉包演算法
- Bellman-Ford 可處理負權邊並檢測負環，Floyd-Warshall 解決所有點對最短路徑問題
"""

from typing import List, Dict, Tuple, Optional, Any


def bellman_ford(
    vertices: List[Any],
    edges: List[Tuple[Any, Any, float]],
    source: Any
) -> Tuple[Optional[Dict[Any, float]], Optional[Dict[Any, List[Any]]]]:
    """
    Bellman-Ford 單源最短路徑演算法

    原理：
    1. 初始化距離：起點為 0，其餘為無限大
    2. 重複 |V|-1 次：對每條邊進行鬆弛操作
    3. 再檢查一次：若還能鬆弛，說明存在負環

    時間複雜度：O(V * E)
    空間複雜度：O(V)
    可處理負權邊：是
    可檢測負環：是

    Args:
        vertices: 頂點列表
        edges: 邊列表，每條邊為 (u, v, weight) 元組
        source: 起點

    Returns:
        (距離字典, 路徑字典) 或 (None, None) 若存在負環
    """
    # 初始化距離
    dist: Dict[Any, float] = {v: float('inf') for v in vertices}
    dist[source] = 0

    # 前驅節點，用於重建路徑
    pred: Dict[Any, Optional[Any]] = {v: None for v in vertices}

    # 鬆弛操作 |V| - 1 次
    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        # 若本次沒有更新，提前結束
        if not updated:
            break

    # 檢查負環：再執行一次，若還能更新則存在負環
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None, None  # 存在負環

    # 重建路徑
    def build_path(v: Any) -> List[Any]:
        path = []
        curr = v
        while curr is not None:
            path.append(curr)
            curr = pred[curr]
        path.reverse()
        return path

    paths: Dict[Any, List[Any]] = {v: build_path(v) if dist[v] < float('inf') else [] for v in vertices}

    return dist, paths


def floyd_warshall(
    vertices: List[Any],
    edges: List[Tuple[Any, Any, float]]
) -> Tuple[Optional[List[List[float]]], Optional[List[List[int]]]]:
    """
    Floyd-Warshall 所有點對最短路徑演算法

    原理：
    1. 初始化距離矩陣：對角線為 0，有邊則為權重，否則為無限大
    2. 對每個中間點 k，嘗試透過 k 縮短路徑
    3. 使用動態規劃：d[i][j] = min(d[i][j], d[i][k] + d[k][j])

    時間複雜度：O(V³)
    空間複雜度：O(V²)
    可處理負權邊：是（但不能有負環）

    Args:
        vertices: 頂點列表
        edges: 邊列表，每條邊為 (u, v, weight) 元組

    Returns:
        (距離矩陣, 下一跳矩陣) 或 (None, None) 若存在負環
    """
    n = len(vertices)
    # 建立頂點索引映射
    idx = {v: i for i, v in enumerate(vertices)}

    # 初始化距離矩陣和下一跳矩陣
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    next_vertex = [[None] * n for _ in range(n)]  # type: ignore

    # 初始化：對角線為 0
    for i in range(n):
        dist[i][i] = 0
        next_vertex[i][i] = vertices[i]

    # 初始化邊
    for u, v, w in edges:
        i, j = idx[u], idx[v]
        dist[i][j] = w
        next_vertex[i][j] = v

    # Floyd-Warshall 核心演算法
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_vertex[i][j] = next_vertex[i][k]

    # 檢查負環：若存在 dist[i][i] < 0，則有負環
    for i in range(n):
        if dist[i][i] < 0:
            return None, None

    return dist, next_vertex


def reconstruct_path_floyd(
    next_vertex: List[List[Any]],
    vertices: List[Any],
    start: Any,
    end: Any
) -> List[Any]:
    """
    根據 Floyd-Warshall 的 next_vertex 矩陣重建路徑

    Args:
        next_vertex: Floyd-Warshall 的下一跳矩陣
        vertices: 頂點列表
        start: 起點
        end: 終點

    Returns:
        從 start 到 end 的最短路徑
    """
    if next_vertex is None:
        return []

    idx = {v: i for i, v in enumerate(vertices)}
    si, ei = idx[start], idx[end]

    if next_vertex[si][ei] is None:
        return []

    path = [start]
    curr = si
    while curr != ei:
        next_v = next_vertex[curr][ei]
        if next_v is None:
            return []
        path.append(next_v)
        curr = idx[next_v]

    return path


if __name__ == "__main__":
    print("=== Bellman-Ford 演算法測試 ===\n")

    # 測試 Bellman-Ford：正權邊
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 3),
        ('B', 'D', 2),
        ('B', 'E', 3),
        ('C', 'B', 1),
        ('C', 'D', 4),
        ('C', 'E', 5),
        ('E', 'D', 1),
    ]

    dist, paths = bellman_ford(vertices, edges, 'A')

    if dist:
        print("從 A 出發的最短路徑：")
        for v in vertices:
            print(f"  A -> {v}: 距離 = {dist[v]}, 路徑 = {paths[v]}")

    print("\n=== Bellman-Ford 負環檢測測試 ===\n")

    # 測試負環
    vertices_neg = ['A', 'B', 'C']
    edges_neg = [
        ('A', 'B', 1),
        ('B', 'C', -2),
        ('C', 'A', -1),  # 形成負環 A->B->C->A，總權重 = 1 + (-2) + (-1) = -2
    ]

    dist_neg, paths_neg = bellman_ford(vertices_neg, edges_neg, 'A')
    if dist_neg is None:
        print("檢測到負環！")

    print("\n=== Floyd-Warshall 演算法測試 ===\n")

    # 測試 Floyd-Warshall
    vertices2 = ['A', 'B', 'C', 'D']
    edges2 = [
        ('A', 'B', 3),
        ('A', 'C', 8),
        ('A', 'D', 5),
        ('B', 'C', 2),
        ('C', 'B', 1),
        ('C', 'D', 2),
        ('D', 'A', 1),
        ('D', 'C', 4),
    ]

    dist_matrix, next_matrix = floyd_warshall(vertices2, edges2)

    if dist_matrix:
        print("所有點對最短路徑距離：")
        print("    ", "  ".join(vertices2))
        for i, v in enumerate(vertices2):
            row = [f"{dist_matrix[i][j]:3.0f}" if dist_matrix[i][j] < float('inf') else "  ∞" for j in range(len(vertices2))]
            print(f"{v}:  {row}")

        print("\n路徑範例：")
        for i, v in enumerate(vertices2):
            for j, w in enumerate(vertices2):
                if v != w:
                    path = reconstruct_path_floyd(next_matrix, vertices2, v, w)
                    print(f"  {v} -> {w}: {path} (距離: {dist_matrix[i][j]})")
    else:
        print("檢測到負環！")
