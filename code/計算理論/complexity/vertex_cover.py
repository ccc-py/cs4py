"""
頂點覆蓋問題 (Vertex Cover Problem)

頂點覆蓋是圖論中的經典 NP-Hard 問題。

問題描述：
給定一個圖 G=(V,E) 和整數 k，
是否存在大小為 k 的頂點集合 S ⊆ V，
使得每條邊都至少有一個端點在 S 中？

歷史背景：
- 1972 年：Karp 證明了 Vertex Cover 是 NP-Hard 的
- 應用：網絡安全、生物資訊學、電路測試
"""

from typing import List, Tuple, Set
import itertools


def brute_force_vertex_cover(vertices: List[int], edges: List[Tuple[int, int]], k: int) -> Tuple[bool, Set[int]]:
    """
    暴力求解頂點覆蓋問題（列舉所有 k-頂點子集）

    時間複雜度：O(C(|V|, k) × |E|)，僅適用於小圖。
    """
    for combo in itertools.combinations(vertices, k):
        cover = set(combo)
        # 檢查是否覆蓋所有邊
        is_cover = True
        for u, v in edges:
            if u not in cover and v not in cover:
                is_cover = False
                break
        if is_cover:
            return True, cover

    return False, set()


def greedy_vertex_cover(vertices: List[int], edges: List[Tuple[int, int]]) -> Set[int]:
    """
    貪婪啟發式：反覆選擇度數最大的頂點

    不保證最優解，但速度快 O(|V|²)。
    """
    # 建立鄰接表
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    uncovered_edges = set(edges)
    cover = set()

    while uncovered_edges:
        # 選擇度數最大的頂點（在剩餘邊中）
        best = None
        best_degree = -1

        for v in vertices:
            if v in cover:
                continue
            degree = sum(1 for u, w in uncovered_edges if u == v or w == v)
            if degree > best_degree:
                best_degree = degree
                best = v

        if best is None:
            break

        cover.add(best)
        # 移除與 best 相連的邊
        uncovered_edges = {(u, w) for u, w in uncovered_edges if u != best and w != best}

    return cover


def create_example_graph() -> Tuple[List[int], List[Tuple[int, int]]]:
    """
    建立一個範例圖。

    頂點：0, 1, 2, 3, 4
    邊：(0,1), (0,2), (1,2), (2,3), (3,4)
    最小頂點覆蓋：{0,2,3} 大小為 3
    """
    vertices = [0, 1, 2, 3, 4]
    edges = [(0,1), (0,2), (1,2), (2,3), (3,4)]
    return vertices, edges


if __name__ == "__main__":
    print("=== 頂點覆蓋問題 (Vertex Cover) 測試 ===")
    print()

    # 建立範例
    vertices, edges = create_example_graph()
    print(f"頂點：{vertices}")
    print(f"邊：{edges}")
    print()

    # 暴力求解 k=3
    print("暴力求解 k=3：")
    exists, cover = brute_force_vertex_cover(vertices, edges, 3)
    print(f"  是否存在大小為 3 的頂點覆蓋：{exists}")
    if exists:
        print(f"  頂點覆蓋：{cover}")
    print()

    # 暴力求解 k=2
    print("暴力求解 k=2：")
    exists, cover = brute_force_vertex_cover(vertices, edges, 2)
    print(f"  是否存在大小為 2 的頂點覆蓋：{exists}")
    print()

    # 貪婪啟發式
    print("貪婪啟發式：")
    cover = greedy_vertex_cover(vertices, edges)
    print(f"  找到的頂點覆蓋：{cover}")
    print(f"  大小：{len(cover)}")
