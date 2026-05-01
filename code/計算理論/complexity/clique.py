"""
團問題 (Clique Problem)

團是圖論中的經典 NP-Complete 問題。

問題描述：
給定一個圖 G=(V,E) 和整數 k，
是否存在大小為 k 的團（完全子圖）？

歷史背景：
- 1972 年：Karp 證明了 Clique 是 NP-Complete 的
- 應用：社交網絡分析、生物資訊學、電路設計
"""

from typing import List, Tuple, Set
import itertools


def brute_force_clique(vertices: List[int], edges: List[Tuple[int, int]], k: int) -> Tuple[bool, Set[int]]:
    """
    暴力求解團問題（列舉所有 k-頂點子集）

    時間複雜度：O(C(|V|, k) × k²)，僅適用於小圖。
    """
    # 建立鄰接表
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # 列舉所有 k-頂點組合
    for combo in itertools.combinations(vertices, k):
        # 檢查是否為團（每對頂點都有邊）
        is_clique = True
        for i in range(len(combo)):
            for j in range(i + 1, len(combo)):
                if combo[j] not in adj[combo[i]]:
                    is_clique = False
                    break
            if not is_clique:
                break

        if is_clique:
            return True, set(combo)

    return False, set()


def greedy_clique(vertices: List[int], edges: List[Tuple[int, int]]) -> Set[int]:
    """
    貪婪啟發式：反覆選擇與當前團中所有頂點相連的頂點。

    不保證最優解，但速度快 O(|V|²)。
    """
    # 建立鄰接表
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # 從最大度數的頂點開始
    clique = set()
    candidates = set(vertices)

    while candidates:
        # 選擇與 clique 中最多頂點相連的候選人
        best = None
        best_count = -1

        for v in candidates:
            # 計算與 clique 中頂點的連接數
            count = sum(1 for u in clique if u in adj[v])
            if count > best_count:
                best_count = count
                best = v

        # 如果 best 與 clique 中所有頂點相連，加入
        if best and all(best in adj[u] for u in clique):
            clique.add(best)
            candidates.remove(best)
        else:
            break

    return clique


def create_example_graph() -> Tuple[List[int], List[Tuple[int, int]]]:
    """
    建立一個範例圖。

    頂點：0, 1, 2, 3, 4
    邊：(0,1), (0,2), (1,2), (2,3), (2,4), (3,4)
    最大團：{0,1,2} 大小為 3
    """
    vertices = [0, 1, 2, 3, 4]
    edges = [(0,1), (0,2), (1,2), (2,3), (2,4), (3,4)]
    return vertices, edges


if __name__ == "__main__":
    print("=== 團問題 (Clique Problem) 測試 ===")
    print()

    # 建立範例
    vertices, edges = create_example_graph()
    print(f"頂點：{vertices}")
    print(f"邊：{edges}")
    print()

    # 暴力求解 k=3
    print("暴力求解 k=3：")
    exists, clique = brute_force_clique(vertices, edges, 3)
    print(f"  是否存在大小為 3 的團：{exists}")
    if exists:
        print(f"  團：{clique}")
    print()

    # 暴力求解 k=4
    print("暴力求解 k=4：")
    exists, clique = brute_force_clique(vertices, edges, 4)
    print(f"  是否存在大小為 4 的團：{exists}")
    print()

    # 貪婪啟發式
    print("貪婪啟發式：")
    clique = greedy_clique(vertices, edges)
    print(f"  找到的團：{clique}")
    print(f"  大小：{len(clique)}")
