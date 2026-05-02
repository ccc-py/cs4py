"""
圖著色 (Graph Coloring / Vertex Coloring)

歷史背景：
- 圖著色問題源於 1852 年的四色猜想（Four Color Conjecture）
- Francis Guthrie 提出：任何平面圖可以用 4 種顏色著色
- 1976 年 Appel 和 Haken 使用電腦證明了四色定理
- 圖著色是 NP-完全問題（Karp, 1972）

應用場景：
- 課程排課（避免時間衝突）
- 暫存器分配（編譯器優化）
- 無線頻道分配
- 地圖著色
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict


class GraphColoring:
    """圖著色類別"""

    def __init__(self, n: int):
        """
        初始化圖

        Args:
            n: 節點數（節點編號 0 到 n-1）
        """
        self.n = n
        self.graph: List[List[int]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int) -> None:
        """添加無向邊"""
        self.graph[u].append(v)
        self.graph[v].append(u)

    def welsh_powell(self) -> Tuple[int, Dict[int, int]]:
        """
        Welsh-Powell 貪婪演算法

        步驟：
        1. 將節點按度數（相鄰節點數）從大到小排序
        2. 依序對每個未著色節點：
           a. 給予最小的可行顏色（未出現在鄰居中）
        3. 返回使用的顏色數和著色方案

        時間複雜度：O(V^2)
        空間複雜度：O(V + E)

        Returns:
            (使用的顏色數, 節點到顏色的映射)
        """
        # 按度數降序排序
        nodes_by_degree = sorted(range(self.n), key=lambda x: len(self.graph[x]), reverse=True)

        color: Dict[int, int] = {}  # 節點 -> 顏色
        used_colors: Set[int] = set()

        for node in nodes_by_degree:
            if node in color:
                continue

            # 找出鄰居使用的顏色
            neighbor_colors = {color[nei] for nei in self.graph[node] if nei in color}

            # 找出最小可行顏色
            c = 0
            while c in neighbor_colors:
                c += 1

            color[node] = c
            used_colors.add(c)

        return len(used_colors), color

    def backtrack_coloring(self, max_colors: int) -> Tuple[bool, Optional[Dict[int, int]]]:
        """
        回溯法求精確解（判斷是否能用 max_colors 種顏色著色）

        原理：
        1. 嘗試為每個節點分配顏色 0 到 max_colors-1
        2. 確保相鄰節點顏色不同
        3. 若找到解則返回 True 和著色方案

        時間複雜度：O(max_colors^V)（指數時間）
        空間複雜度：O(V)

        Args:
            max_colors: 最多允許使用的顏色數

        Returns:
            (是否能著色, 著色方案或 None)
        """
        color: Dict[int, int] = {}
        result = self._backtrack_helper(0, color, max_colors)
        return result, color if result else None

    def _backtrack_helper(self, node: int, color: Dict[int, int], max_colors: int) -> bool:
        """回溯輔助函數"""
        if node == self.n:
            return True  # 所有節點都已著色

        for c in range(max_colors):
            if self._is_safe(node, c, color):
                color[node] = c
                if self._backtrack_helper(node + 1, color, max_colors):
                    return True
                del color[node]  # 回溯

        return False

    def _is_safe(self, node: int, c: int, color: Dict[int, int]) -> bool:
        """檢查給定顏色是否安全（鄰居都沒有此顏色）"""
        for neighbor in self.graph[node]:
            if neighbor in color and color[neighbor] == c:
                return False
        return True

    def chromatic_number_exact(self, max_try: int = 10) -> Tuple[int, Dict[int, int]]:
        """
        估算色數（chromatic number）

        從 1 開始嘗試，找到最小的可用顏色數

        Args:
            max_try: 最多嘗試幾種顏色

        Returns:
            (色數, 著色方案)
        """
        for k in range(1, min(max_try + 1, self.n + 1)):
            success, coloring = self.backtrack_coloring(k)
            if success:
                return k, coloring
        return max_try, {}

    def greedy_coloring(self) -> Tuple[int, Dict[int, int]]:
        """
        簡單貪婪著色（按節點順序）

        Returns:
            (使用的顏色數, 著色方案)
        """
        color: Dict[int, int] = {}

        for node in range(self.n):
            neighbor_colors = {color[nei] for nei in self.graph[node] if nei in color}
            c = 0
            while c in neighbor_colors:
                c += 1
            color[node] = c

        return max(color.values()) + 1 if color else 0, color


def build_sample_graph() -> GraphColoring:
    """建立示例圖（一個環形和一個三角形相連）"""
    gc = GraphColoring(6)
    # 形成一個六邊形（需要 2 色，因為是偶環）
    for i in range(6):
        gc.add_edge(i, (i + 1) % 6)
    return gc


if __name__ == "__main__":
    print("=== 圖著色 (Graph Coloring) 測試 ===\n")

    # 測試 1：六邊形（偶環，二分圖，2 色）
    print("1. 六邊形（偶環，需要 2 色）：")
    gc1 = build_sample_graph()
    colors_used, coloring = gc1.welsh_powell()
    print(f"  Welsh-Powell 使用顏色數：{colors_used}")
    print(f"  著色方案：{coloring}")
    print()

    # 測試 2：三角形（奇環，需要 3 色）
    print("2. 三角形（奇環，需要 3 色）：")
    gc2 = GraphColoring(3)
    gc2.add_edge(0, 1)
    gc2.add_edge(1, 2)
    gc2.add_edge(2, 0)
    colors_used, coloring = gc2.welsh_powell()
    print(f"  Welsh-Powell 使用顏色數：{colors_used}")
    print(f"  著色方案：{coloring}")
    print()

    # 測試 3：回溯法求精確解
    print("3. 回溯法求色數（三角形）：")
    chrom, coloring = gc2.chromatic_number_exact()
    print(f"  色數（chromatic number）：{chrom}")
    print(f"  著色方案：{coloring}")
    print()

    # 測試 4：完全圖 K4（需要 4 色）
    print("4. 完全圖 K4（需要 4 色）：")
    gc4 = GraphColoring(4)
    for i in range(4):
        for j in range(i + 1, 4):
            gc4.add_edge(i, j)
    colors_used, coloring = gc4.welsh_powell()
    print(f"  Welsh-Powell 使用顏色數：{colors_used}")
    print(f"  著色方案：{coloring}")
    chrom, _ = gc4.chromatic_number_exact()
    print(f"  精確色數：{chrom}")
    print()

    # 測試 5：二分圖（二部圖，只需 2 色）
    print("5. 二分圖（0,1,2 連到 3,4,5）：")
    gc5 = GraphColoring(6)
    for i in range(3):
        for j in range(3, 6):
            gc5.add_edge(i, j)
    colors_used, coloring = gc5.welsh_powell()
    print(f"  Welsh-Powell 使用顏色數：{colors_used}")
    print(f"  著色方案：{coloring}")
    print()

    # 測試 6：單節點圖
    print("6. 單節點圖：")
    gc6 = GraphColoring(1)
    colors_used, coloring = gc6.welsh_powell()
    print(f"  Welsh-Powell 使用顏色數：{colors_used}")
    print(f"  著色方案：{coloring}")
    print()
    print("測試完成！")
