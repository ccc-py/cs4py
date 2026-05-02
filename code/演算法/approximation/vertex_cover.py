"""
頂點覆蓋近似演算法 (Vertex Cover Approximation)

歷史背景：
- 頂點覆蓋是 Karp 1972 年列出的 21 個 NP-完全問題之一
- 2-近似演算法（基於最大匹配）由 Gavril 和 Yannakakis 提出
- 雖然無法在多項式時間得到最優解，但近似解在實務上很有用

應用場景：
- 網路安全（監控關鍵節點）
- 生物資訊（蛋白質交互網路）
- 社會網路分析
- 感測器覆蓋問題
"""

from typing import List, Set, Tuple, Dict
from collections import defaultdict


class VertexCoverApproximation:
    """頂點覆蓋近似演算法"""

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
        self.edges.append((u, v))

    def greedy_vertex_cover(self) -> Tuple[Set[int], int]:
        """
        貪婪演算法求頂點覆蓋的近似解

        原理：
        1. 初始化覆蓋集為空
        2. 當還有未覆蓋的邊：
           a. 選擇度數最大的節點加入覆蓋
           b. 移除所有與該節點相連的邊
        3. 返回覆蓋集

        近似比：無保證（可能很差）
        時間複雜度：O(V * E)

        Returns:
            (頂點覆蓋集, 覆蓋集大小)
        """
        covered_edges = set(self.edges)
        cover: Set[int] = set()

        while covered_edges:
            # 計算每個節點的剩餘度數
            degree: Dict[int, int] = defaultdict(int)
            for u, v in covered_edges:
                degree[u] += 1
                degree[v] += 1

            # 選擇度數最大的節點
            if not degree:
                break
            max_node = max(degree.keys(), key=lambda x: degree[x])
            cover.add(max_node)

            # 移除與 max_node 相連的邊
            covered_edges = {(u, v) for u, v in covered_edges
                            if u != max_node and v != max_node}

        return cover, len(cover)

    def matching_2approx(self) -> Tuple[Set[int], int]:
        """
        基於最大匹配的 2-近似演算法

        原理：
        1. 找出圖的一個最大匹配 M
        2. 將 M 中每條邊的兩個端點都加入覆蓋集
        3. 返回覆蓋集

        性質：
        - 得到的覆蓋集大小 <= 2 * OPT（最優解大小）
        - 這是一個 2-近似演算法

        時間複雜度：O(V * E)
        空間複雜度：O(V + E)

        Returns:
            (頂點覆蓋集, 覆蓋集大小)
        """
        # 找最大匹配的簡化版（貪婪）
        matched: Set[int] = set()
        matching: List[Tuple[int, int]] = []

        for u, v in self.edges:
            if u not in matched and v not in matched:
                matched.add(u)
                matched.add(v)
                matching.append((u, v))

        # 將匹配中的邊的兩個端點都加入覆蓋
        cover: Set[int] = set()
        for u, v in matching:
            cover.add(u)
            cover.add(v)

        return cover, len(cover)

    def lp_rounding_approx(self) -> Tuple[Set[int], int]:
        """
        基於線性規劃鬆弛的 2-近似（概念版）

        原理：
        1. 線性規劃鬆弛：
           minimize sum(x_v) for all v
           subject to: x_u + x_v >= 1 for all edges (u,v)
                      0 <= x_v <= 1

        2. 取整：若 x_v >= 0.5，則將 v 加入覆蓋

        近似比：2-近似

        Returns:
            (頂點覆蓋集, 覆蓋集大小)
        """
        # 簡化實作：使用 matching_2approx 的結果作為示範
        # 實際的 LP rounding 需要解線性規劃
        return self.matching_2approx()


def build_sample_graph() -> VertexCoverApproximation:
    """建立示例圖（六邊形）"""
    vc = VertexCoverApproximation(6)
    for i in range(6):
        vc.add_edge(i, (i + 1) % 6)
    return vc


if __name__ == "__main__":
    print("=== 頂點覆蓋近似演算法 (Vertex Cover Approximation) 測試 ===\n")

    # 測試 1：六邊形
    print("1. 六邊形（6 個節點的環）：")
    vc1 = build_sample_graph()
    print(f"  邊數：{len(vc1.edges)}")

    cover1, size1 = vc1.greedy_vertex_cover()
    print(f"  貪婪演算法：覆蓋集 = {cover1}，大小 = {size1}")

    cover2, size2 = vc1.matching_2approx()
    print(f"  2-近似（匹配）：覆蓋集 = {cover2}，大小 = {size2}")
    print()

    # 測試 2：星形圖
    print("2. 星形圖（中心 0 連到 1,2,3,4）：")
    vc2 = VertexCoverApproximation(5)
    for i in range(1, 5):
        vc2.add_edge(0, i)
    print(f"  邊數：{len(vc2.edges)}")

    cover1, size1 = vc2.greedy_vertex_cover()
    print(f"  貪婪演算法：覆蓋集 = {cover1}，大小 = {size1}")

    cover2, size2 = vc2.matching_2approx()
    print(f"  2-近似（匹配）：覆蓋集 = {cover2}，大小 = {size2}")
    print(f"  最優解應為 {{0}}，大小 = 1")
    print()

    # 測試 3：完全圖 K4
    print("3. 完全圖 K4：")
    vc3 = VertexCoverApproximation(4)
    for i in range(4):
        for j in range(i + 1, 4):
            vc3.add_edge(i, j)
    print(f"  邊數：{len(vc3.edges)}")

    cover1, size1 = vc3.greedy_vertex_cover()
    print(f"  貪婪演算法：覆蓋集大小 = {size1}")

    cover2, size2 = vc3.matching_2approx()
    print(f"  2-近似（匹配）：覆蓋集大小 = {size2}")
    print(f"  最優解大小 = 3")
    print()

    # 測試 4：路徑圖（0-1-2-3）
    print("4. 路徑圖（4 個節點）：")
    vc4 = VertexCoverApproximation(4)
    vc4.add_edge(0, 1)
    vc4.add_edge(1, 2)
    vc4.add_edge(2, 3)
    print(f"  邊數：{len(vc4.edges)}")

    cover1, size1 = vc4.greedy_vertex_cover()
    print(f"  貪婪演算法：覆蓋集 = {cover1}，大小 = {size1}")

    cover2, size2 = vc4.matching_2approx()
    print(f"  2-近似（匹配）：覆蓋集 = {cover2}，大小 = {size2}")
    print(f"  最優解大小 = 2")
    print()

    # 測試 5：空圖
    print("5. 空圖（無邊）：")
    vc5 = VertexCoverApproximation(3)
    cover1, size1 = vc5.greedy_vertex_cover()
    cover2, size2 = vc5.matching_2approx()
    print(f"  貪婪演算法：覆蓋集大小 = {size1}")
    print(f"  2-近似（匹配）：覆蓋集大小 = {size2}")
    print()
    print("測試完成！")
