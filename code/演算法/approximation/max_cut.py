"""
最大割近似演算法 (MAX-CUT Approximation)

歷史背景：
- MAX-CUT 是 Karp 1972 年列出的 NP-完全問題之一
- Goemans 和 Williamson 於 1995 年提出 0.878-近似（基於半正定規劃）
- 隨機演算法可達到 0.5-近似（簡單且快速）
- 是電路設計和統計物理中的重要問題

應用場景：
- 電路佈局（最小化交叉）
- 圖分割（社群發現）
- 統計物理（Ising 模型）
- 聚類分析
"""

from typing import List, Tuple, Set
import random


class MaxCutApproximation:
    """最大割近似演算法"""

    def __init__(self, n: int):
        """
        初始化圖

        Args:
            n: 節點數（節點編號 0 到 n-1）
        """
        self.n = n
        self.graph: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
        self.total_weight = 0.0

    def add_edge(self, u: int, v: int, w: float = 1.0) -> None:
        """添加無向邊（可選權重）"""
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))
        self.total_weight += w

    def random_cut(self) -> Tuple[Set[int], Set[int], float]:
        """
        隨機 0.5-近似演算法

        原理：
        1. 每個節點獨立地以 1/2 機率分配到集合 S
           其餘節點分配到 T
        2. 計算割的大小（跨越 S 和 T 的邊權重和）

        期望割大小 >= 總權重 / 2
        因此這是一個 0.5-近似演算法

        時間複雜度：O(E)
        空間複雜度：O(V)

        Returns:
            (集合 S, 集合 T, 割大小)
        """
        random.seed()  # 使用系統隨機種子
        S = set()
        T = set()

        for v in range(self.n):
            if random.random() < 0.5:
                S.add(v)
            else:
                T.add(v)

        cut_size = self._compute_cut_size(S)
        return S, T, cut_size

    def _compute_cut_size(self, S: Set[int]) -> float:
        """計算割的大小（S 與 V\\S 之間的邊權重和）"""
        cut = 0.0
        for u in S:
            for v, w in self.graph[u]:
                if v not in S:  # v 在 T 中
                    cut += w
        return cut  # 每條邊被計算一次

    def greedy_local_search(self, iterations: int = 100) -> Tuple[Set[int], Set[int], float]:
        """
        貪婪局部搜尋改進

        原理：
        1. 從隨機割開始
        2. 反覆嘗試將一個節點從 S 移到 T（或反之）
           若割大小增加，則接受該移動
        3. 重複直到無法改進或達到迭代上限

        這可以改進隨機割的結果，但無近似比保證

        Args:
            iterations: 最大迭代次數

        Returns:
            (集合 S, 集合 T, 割大小)
        """
        # 初始化隨機割
        S = set()
        T = set()
        for v in range(self.n):
            if random.random() < 0.5:
                S.add(v)
            else:
                T.add(v)

        cut_size = self._compute_cut_size(S)

        # 局部搜尋
        for _ in range(iterations):
            improved = False

            # 嘗試移動每個節點
            nodes = list(range(self.n))
            random.shuffle(nodes)

            for v in nodes:
                # 計算移動 v 的增益
                gain = self._compute_move_gain(v, S, T)

                if gain > 0:
                    # 執行移動
                    if v in S:
                        S.remove(v)
                        T.add(v)
                    else:
                        T.remove(v)
                        S.add(v)
                    cut_size += gain
                    improved = True

            if not improved:
                break

        return S, T, cut_size

    def _compute_move_gain(self, v: int, S: Set[int], T: Set[int]) -> float:
        """計算將 v 從當前集合移到另一集合的增益"""
        gain = 0.0

        if v in S:
            # v 在 S，考慮移到 T
            for u, w in self.graph[v]:
                if u in S:
                    gain -= w  # 失去這條割邊
                else:
                    gain += w  # 獲得這條割邊
        else:
            # v 在 T，考慮移到 S
            for u, w in self.graph[v]:
                if u in T:
                    gain -= w  # 失去這條割邊
                else:
                    gain += w  # 獲得這條割邊

        return gain


def build_sample_graph() -> MaxCutApproximation:
    """建立示例圖（4 個節點的環）"""
    mc = MaxCutApproximation(4)
    mc.add_edge(0, 1, 1.0)
    mc.add_edge(1, 2, 1.0)
    mc.add_edge(2, 3, 1.0)
    mc.add_edge(3, 0, 1.0)
    return mc


if __name__ == "__main__":
    print("=== 最大割近似演算法 (MAX-CUT Approximation) 測試 ===\n")

    # 測試 1：4 節點環
    print("1. 4 節點環（正方形）：")
    mc1 = build_sample_graph()
    print(f"  邊數：4")

    # 隨機割
    random.seed(42)
    S, T, cut = mc1.random_cut()
    print(f"  隨機割：S={S}, T={T}, 割大小={cut}")

    # 貪婪局部搜尋
    S, T, cut = mc1.greedy_local_search()
    print(f"  貪婪改進：S={S}, T={T}, 割大小={cut}")
    print(f"  最大割（精確）：2（所有邊都是割邊）")
    print()

    # 測試 2：完全圖 K4
    print("2. 完全圖 K4：")
    mc2 = MaxCutApproximation(4)
    for i in range(4):
        for j in range(i + 1, 4):
            mc2.add_edge(i, j, 1.0)
    print(f"  邊數：6")

    S, T, cut = mc2.random_cut()
    print(f"  隨機割：S={S}, T={T}, 割大小={cut}")

    S, T, cut = mc2.greedy_local_search(iterations=50)
    print(f"  貪婪改進：S={S}, T={T}, 割大小={cut}")
    print(f"  最大割（精確）：4（選 2+2 分割）")
    print()

    # 測試 3：星形圖
    print("3. 星形圖（中心 0 連到 1,2,3,4）：")
    mc3 = MaxCutApproximation(5)
    for i in range(1, 5):
        mc3.add_edge(0, i, 1.0)

    S, T, cut = mc3.random_cut()
    print(f"  隨機割：S={S}, T={T}, 割大小={cut}")

    S, T, cut = mc3.greedy_local_search()
    print(f"  貪婪改進：S={S}, T={T}, 割大小={cut}")
    print(f"  最大割：4（中心 + 任意兩個葉節點在同一側）")
    print()

    # 測試 4：單邊圖
    print("4. 單邊圖（0-1）：")
    mc4 = MaxCutApproximation(2)
    mc4.add_edge(0, 1, 1.0)

    S, T, cut = mc4.random_cut()
    print(f"  隨機割：S={S}, T={T}, 割大小={cut}")
    print(f"  最大割：1")
    print()

    # 測試 5：多輪隨機取最佳
    print("5. 多輪隨機（取最佳）：")
    mc5 = MaxCutApproximation(6)
    for i in range(5):
        mc5.add_edge(i, i + 1, 1.0)

    best_cut = 0.0
    for _ in range(100):
        _, _, cut = mc5.random_cut()
        best_cut = max(best_cut, cut)
    print(f"  100 輪隨機最佳割：{best_cut}")
    print(f"  最大割（6 邊環）：3")
    print()
    print("測試完成！")
