"""
平面性測試與平面圖 (Planarity Testing)

歷史背景：
- 平面圖的概念可追溯到 Euler (1750 年代)
- Kuratowski 於 1930 年提出平面圖的特徵定理
- John Hopcroft 和 Robert Tarjan 於 1974 年提出第一個線性時間演算法
- 平面性測試是圖繪製和電路設計的重要問題

應用場景：
- 電路佈局（避免線路交叉）
- 地圖繪製
- 圖視覺化
- VLSI 設計
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, deque


class PlanarGraph:
    """平面圖測試類別"""

    def __init__(self, n: int):
        """
        初始化圖

        Args:
            n: 節點數（節點編號 0 到 n-1）
        """
        self.n = n
        self.graph: List[List[int]] = [[] for _ in range(n)]
        self.edges: List[Tuple[int, int]] = []

    def add_edge(self, u: int, v: int) -> None:
        """添加無向邊"""
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.edges.append((min(u, v), max(u, v)))

    def is_planar_simple(self) -> Tuple[bool, Optional[str]]:
        """
        簡化版平面性測試（僅適用於小圖）

        使用 Kuratowski 定理的簡化檢查：
        1. 檢查歐拉公式：對於連通平面圖，V - E + F = 2
           推論：若 V >= 3，則 E <= 3V - 6
           若 V >= 3 且無三角形，則 E <= 2V - 4
        2. 檢查是否包含 K5 或 K3,3 作為子圖（僅檢查小圖）

        Returns:
            (是否為平面圖, 原因或 None)
        """
        v = self.n
        e = len(self.edges)

        # 基本必要條件：歐拉不等式
        if v >= 3 and e > 3 * v - 6:
            return False, f"邊數 {e} > 3V-6 = {3*v-6}，違反歐拉公式"

        # 檢查是否為 K5 (5 個節點，每對都有邊)
        if self._is_complete_graph(5):
            return False, "包含 K5 (完全圖 K5)"

        # 檢查是否為 K3,3 (二分完全圖)
        if self._is_k33():
            return False, "包含 K3,3 (完全二分圖 K3,3)"

        return True, None

    def _is_complete_graph(self, k: int) -> bool:
        """檢查是否包含 Kk 作為子圖（簡化版，僅檢查精確匹配）"""
        if self.n != k:
            return False
        expected_edges = k * (k - 1) // 2
        return len(self.edges) == expected_edges

    def _is_k33(self) -> bool:
        """檢查是否為 K3,3（簡化版）"""
        if self.n != 6:
            return False
        # K3,3 有 9 條邊
        if len(self.edges) != 9:
            return False
        # 簡化檢查：所有節點度數應為 3
        degrees = [len(self.graph[i]) for i in range(self.n)]
        return all(d == 3 for d in degrees)

    def get_planar_embedding(self) -> Optional[List[Tuple[int, int]]]:
        """
        嘗試獲取平面嵌入（簡化版）

        Returns:
            平面嵌入的邊列表，若非平面圖則返回 None
        """
        is_planar, _ = self.is_planar_simple()
        if not is_planar:
            return None

        # 簡化實作：直接返回原始邊（假設已經是平面嵌入）
        return self.edges.copy()

    def count_faces(self) -> Optional[int]:
        """
        計算平面圖的面數（若為平面圖）

        使用歐拉公式：V - E + F = 2
        => F = 2 - V + E

        Returns:
            面數，若非連通或無法確定則返回 None
        """
        is_planar, _ = self.is_planar_simple()
        if not is_planar:
            return None

        # 檢查連通性
        visited = [False] * self.n
        q = deque([0])
        visited[0] = True
        count = 1

        while q:
            u = q.popleft()
            for v in self.graph[u]:
                if not visited[v]:
                    visited[v] = True
                    count += 1
                    q.append(v)

        if count != self.n:
            return None  # 非連通

        v = self.n
        e = len(self.edges)
        return 2 - v + e


def build_k5() -> PlanarGraph:
    """建立 K5（非平面圖）"""
    g = PlanarGraph(5)
    for i in range(5):
        for j in range(i + 1, 5):
            g.add_edge(i, j)
    return g


def build_k33() -> PlanarGraph:
    """建立 K3,3（非平面圖）"""
    g = PlanarGraph(6)
    # 左側：0,1,2；右側：3,4,5
    for i in range(3):
        for j in range(3, 6):
            g.add_edge(i, j)
    return g


def build_planar_example() -> PlanarGraph:
    """建立一個平面圖（網格的一部分）"""
    g = PlanarGraph(6)
    # 形成一個六邊形（平面）
    for i in range(6):
        g.add_edge(i, (i + 1) % 6)
    return g


if __name__ == "__main__":
    print("=== 平面性測試 (Planarity Testing) 測試 ===\n")

    # 測試 1：K5（非平面圖）
    print("1. K5（完全圖 5 個節點）：")
    k5 = build_k5()
    is_planar, reason = k5.is_planar_simple()
    print(f"  是否為平面圖：{is_planar}")
    if reason:
        print(f"  原因：{reason}")
    print()

    # 測試 2：K3,3（非平面圖）
    print("2. K3,3（完全二分圖）：")
    k33 = build_k33()
    is_planar, reason = k33.is_planar_simple()
    print(f"  是否為平面圖：{is_planar}")
    if reason:
        print(f"  原因：{reason}")
    print()

    # 測試 3：平面圖（六邊形）
    print("3. 平面圖（六邊形）：")
    planar = build_planar_example()
    is_planar, reason = planar.is_planar_simple()
    print(f"  是否為平面圖：{is_planar}")
    faces = planar.count_faces()
    print(f"  面數：{faces}")
    print()

    # 測試 4：樹（一定是平面圖）
    print("4. 樹（4 個節點的鏈）：")
    tree = PlanarGraph(4)
    tree.add_edge(0, 1)
    tree.add_edge(1, 2)
    tree.add_edge(2, 3)
    is_planar, reason = tree.is_planar_simple()
    print(f"  是否為平面圖：{is_planar}")
    faces = tree.count_faces()
    print(f"  面數：{faces}")
    print()

    # 測試 5：歐拉公式驗證
    print("5. 歐拉公式驗證（正方形）：")
    square = PlanarGraph(4)
    # 正方形：0-1-2-3-0
    for i in range(4):
        square.add_edge(i, (i + 1) % 4)
    # 加上對角線 0-2（仍為平面圖）
    square.add_edge(0, 2)
    is_planar, _ = square.is_planar_simple()
    faces = square.count_faces()
    print(f"  V=4, E=5, F={faces}")
    print(f"  V-E+F = {4-5+faces if faces else 'N/A'} (= 2 表示正確)")
    print()

    # 測試 6：邊數過多的圖
    print("6. 邊數過多的圖（非平面）：")
    dense = PlanarGraph(4)
    # K4 有 6 條邊，對於 V=4，3V-6 = 6，剛好是界限
    for i in range(4):
        for j in range(i + 1, 4):
            dense.add_edge(i, j)
    is_planar, reason = dense.is_planar_simple()
    print(f"  是否為平面圖：{is_planar}")
    if reason:
        print(f"  原因：{reason}")
    print()
    print("測試完成！")
