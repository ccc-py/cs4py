"""
一般圖匹配 (General Graph Matching - Edmonds' Blossom Algorithm)

歷史背景：
- 一般圖最大匹配問題由 Claude Berge 於 1957 年提出
- Jack Edmonds 於 1965 年提出開創性的 Blossom Algorithm
- Edmonds 證明了此問題屬於 P 類（多項式時間可解）
- 此演算法對圖論和組合優化有深遠影響

應用場景：
- 配對問題（如腎臟交換、學生選校）
- 網路設計
- 資源分配
- 化學分子結構分析
"""

from typing import List, Dict, Set, Optional, Tuple, Deque
from collections import defaultdict, deque


class BlossomMatching:
    """一般圖最大匹配（Edmonds' Blossom Algorithm）"""

    def __init__(self, n: int):
        """
        初始化圖

        Args:
            n: 節點數（節點編號 0 到 n-1）
        """
        self.n = n
        self.graph: List[List[int]] = [[] for _ in range(n)]
        self.match: List[int] = [-1] * n  # match[u] = v 表示 u 匹配到 v

    def add_edge(self, u: int, v: int) -> None:
        """添加無向邊"""
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bfs_augmenting_path(self, start: int) -> Optional[List[int]]:
        """
        使用 BFS 尋找從 start 出發的交錯路徑（alternating path）
        並處理 blossom 收縮

        Returns:
            擴充路徑（從 start 到未匹配節點），若無則返回 None
        """
        # BFS 從未匹配節點開始
        parent: List[int] = [-1] * self.n
        base: List[int] = list(range(self.n))  # 每個節點的基底（用於 blossom）
        q: Deque[int] = deque()

        # 初始化：將 start 加入佇列
        q.append(start)
        parent[start] = start

        while q:
            v = q.popleft()

            for u in self.graph[v]:
                # 如果 u 未匹配
                if self.match[u] == -1 and u != start:
                    # 找到擴充路徑
                    path = self._construct_path(parent, base, v, u)
                    return path

                # 如果 u 已匹配，檢查是否形成 blossom
                w = self.match[u]
                if w == -1:
                    continue

                # 檢查 v 和 w 是否在相同的基底樹中
                base_v = self._find_base(base, v)
                base_w = self._find_base(base, w)

                if base_v == base_w:
                    # 發現 blossom，進行收縮
                    self._contract_blossom(base, parent, v, w, base_v)
                elif parent[u] == -1:
                    # u 尚未訪問，加入搜尋樹
                    parent[u] = v
                    parent[w] = u
                    q.append(w)

        return None

    def _find_base(self, base: List[int], x: int) -> int:
        """尋找 x 的基底（使用路徑壓縮）"""
        while base[x] != x:
            base[x] = base[base[x]]
            x = base[x]
        return x

    def _contract_blossom(self, base: List[int], parent: List[int],
                          v: int, w: int, blossom_base: int) -> None:
        """收縮 blossom（將整個 blossom 收縮為一個節點）"""
        # 將 v 和 w 路徑上的所有節點基底設為 blossom_base
        for node in [v, w]:
            curr = node
            while base[curr] != blossom_base:
                base[curr] = blossom_base
                curr = parent[curr]

    def _construct_path(self, parent: List[int], base: List[int],
                        v: int, u: int) -> List[int]:
        """建構從 start 到 u 的擴充路徑"""
        # 先找到 v 到基底的路徑
        path_v = []
        curr = v
        while parent[curr] != curr:
            path_v.append(curr)
            curr = parent[curr]
        path_v.append(curr)
        path_v.reverse()

        # u 是未匹配節點，需要找到 u 的配對
        # 路徑：start -> ... -> v -> u
        path = path_v + [u]
        return path

    def edmonds_blossom(self) -> int:
        """
        Edmonds' Blossom Algorithm 求一般圖最大匹配

        原理：
        1. 初始化匹配為空
        2. 對每個未匹配節點，嘗試找擴充路徑：
           a. 使用 BFS 找交錯路徑
           b. 遇到 blossom（奇環）時，將其收縮
           c. 找到擴充路徑後，翻轉匹配狀態
        3. 返回最大匹配數

        時間複雜度：O(V^3)
        空間複雜度：O(V + E)

        Returns:
            最大匹配數
        """
        match_count = 0

        for u in range(self.n):
            if self.match[u] != -1:
                continue  # 已匹配

            # 嘗試找從 u 出發的擴充路徑
            path = self.bfs_augmenting_path(u)
            if path is None:
                continue

            # 沿著路徑翻轉匹配
            for i in range(0, len(path) - 1, 2):
                a, b = path[i], path[i + 1]
                self.match[a] = b
                self.match[b] = a

            match_count += len(path) // 2

        return match_count

    def get_matching(self) -> List[Tuple[int, int]]:
        """獲取當前匹配"""
        result = []
        seen = set()
        for u in range(self.n):
            v = self.match[u]
            if v != -1 and u not in seen:
                result.append((min(u, v), max(u, v)))
                seen.add(u)
                seen.add(v)
        return result


def build_sample_graph() -> BlossomMatching:
    """建立示例圖（包含一個 blossom）"""
    # 圖結構：
    # 0-1-2-3-4-5 形成一個路徑，加上 2-6-3 形成一個三角形（blossom）
    bm = BlossomMatching(7)
    bm.add_edge(0, 1)
    bm.add_edge(1, 2)
    bm.add_edge(2, 3)
    bm.add_edge(3, 4)
    bm.add_edge(4, 5)
    bm.add_edge(2, 6)  # 形成 blossom
    bm.add_edge(6, 3)  # 三角形 2-3-6
    return bm


if __name__ == "__main__":
    print("=== 一般圖匹配 (General Graph Matching - Blossom) 測試 ===\n")

    # 測試 1：簡單路徑圖
    print("1. 簡單路徑圖（0-1-2-3）：")
    bm1 = BlossomMatching(4)
    bm1.add_edge(0, 1)
    bm1.add_edge(1, 2)
    bm1.add_edge(2, 3)
    result = bm1.edmonds_blossom()
    print(f"最大匹配數：{result}")
    print(f"匹配對：{bm1.get_matching()}")
    print()

    # 測試 2：包含 Blossom 的圖
    print("2. 包含 Blossom（奇環）的圖：")
    bm2 = build_sample_graph()
    result = bm2.edmonds_blossom()
    print(f"最大匹配數：{result}")
    print(f"匹配對：{bm2.get_matching()}")
    print()

    # 測試 3：完全圖 K4
    print("3. 完全圖 K4：")
    bm3 = BlossomMatching(4)
    for i in range(4):
        for j in range(i + 1, 4):
            bm3.add_edge(i, j)
    result = bm3.edmonds_blossom()
    print(f"最大匹配數：{result}")
    print(f"匹配對：{bm3.get_matching()}")
    print()

    # 測試 4：星形圖
    print("4. 星形圖（中心 0 連接到 1,2,3,4）：")
    bm4 = BlossomMatching(5)
    for i in range(1, 5):
        bm4.add_edge(0, i)
    result = bm4.edmonds_blossom()
    print(f"最大匹配數：{result}")
    print(f"匹配對：{bm4.get_matching()}")
    print()

    # 測試 5：空圖
    print("5. 空圖（無邊）：")
    bm5 = BlossomMatching(3)
    result = bm5.edmonds_blossom()
    print(f"最大匹配數：{result}")
    print(f"匹配對：{bm5.get_matching()}")
    print()
    print("測試完成！")
