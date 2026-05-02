"""
集合覆蓋近似演算法 (Set Cover Approximation)

歷史背景：
- 集合覆蓋是 Karp 1972 年列出的 21 個 NP-完全問題之一
- 貪婪演算法的 O(log n)-近似由 Johnson、Lovász 等人證明
- 集合覆蓋在資源選擇、特徵選擇等領域廣泛應用
- 除非 NP ⊆ DTIME(n^O(log log n))，否則無法改進到 o(log n)

應用場景：
- 設施選址（選擇最少設施覆蓋所有需求點）
- 特徵選擇（機器學習）
- 感測器佈局
- 文獻檢索
"""

from typing import List, Set, Tuple, Dict
import heapq


class SetCoverApproximation:
    """集合覆蓋近似演算法"""

    def __init__(self, universe: Set[int]):
        """
        初始化

        Args:
            universe: 全域集合 U
        """
        self.universe = universe
        self.sets: List[Set[int]] = []
        self.set_ids: List[int] = []

    def add_set(self, set_id: int, s: Set[int]) -> None:
        """添加一個集合"""
        self.sets.append(s)
        self.set_ids.append(set_id)

    def greedy_set_cover(self) -> Tuple[List[int], int]:
        """
        貪婪集合覆蓋演算法

        原理：
        1. 初始化覆蓋集為空，未覆蓋元素為全域
        2. 每次選擇覆蓋最多未覆蓋元素的集合
        3. 將該集合加入覆蓋，更新未覆蓋元素
        4. 直到所有元素都被覆蓋

        近似比：O(log n)，其中 n = |U|
        時間複雜度：O(|U| * |S| * log |S|)

        Returns:
            (選擇的集合 ID 列表, 集合數)
        """
        uncovered = self.universe.copy()
        chosen = []
        chosen_ids = []

        # 計算每個集合的大小（預處理）
        set_sizes = [len(s) for s in self.sets]

        while uncovered:
            best_idx = -1
            best_new_covered = 0

            # 找覆蓋最多未覆蓋元素的集合
            for i in range(len(self.sets)):
                new_covered = len(self.sets[i] & uncovered)
                if new_covered > best_new_covered:
                    best_new_covered = new_covered
                    best_idx = i

            if best_idx == -1 or best_new_covered == 0:
                break  # 無法覆蓋剩餘元素

            chosen.append(best_idx)
            chosen_ids.append(self.set_ids[best_idx])
            uncovered -= self.sets[best_idx]

        return chosen_ids, len(chosen)

    def weighted_greedy_set_cover(self, weights: List[float]) -> Tuple[List[int], int, float]:
        """
        加權集合覆蓋的貪婪近似

        原理：
        每次選擇「每覆蓋一個新元素成本最低」的集合
        cost_effectiveness = weight / |new_elements_covered|

        近似比：O(log n)
        時間複雜度：O(|U| * |S|)

        Args:
            weights: 每個集合的權重（成本）

        Returns:
            (選擇的集合 ID 列表, 集合數, 總權重)
        """
        uncovered = self.universe.copy()
        chosen_ids = []
        total_weight = 0.0

        while uncovered:
            best_idx = -1
            best_ratio = float('inf')

            for i in range(len(self.sets)):
                new_covered = len(self.sets[i] & uncovered)
                if new_covered == 0:
                    continue
                ratio = weights[i] / new_covered
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_idx = i

            if best_idx == -1:
                break

            chosen_ids.append(self.set_ids[best_idx])
            total_weight += weights[best_idx]
            uncovered -= self.sets[best_idx]

        return chosen_ids, len(chosen_ids), total_weight


def build_sample_problem() -> Tuple[SetCoverApproximation, List[float]]:
    """建立示例問題"""
    universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    sc = SetCoverApproximation(universe)
    # 定義集合
    sets = [
        {1, 2, 3, 4, 5},
        {4, 5, 6, 7},
        {6, 7, 8, 9},
        {8, 9, 10},
        {1, 3, 5, 7, 9},
        {2, 4, 6, 8, 10}
    ]
    for i, s in enumerate(sets):
        sc.add_set(i, s)
    weights = [1.0] * len(sets)  # 等權重
    return sc, weights


if __name__ == "__main__":
    print("=== 集合覆蓋近似演算法 (Set Cover Approximation) 測試 ===\n")

    # 測試 1：示例問題
    print("1. 示例問題（10 個元素，6 個集合）：")
    sc1, weights1 = build_sample_problem()
    print(f"  全域：{sc1.universe}")
    for i, s in enumerate(sc1.sets):
        print(f"  集合 {i}: {s}")
    print()

    chosen, count = sc1.greedy_set_cover()
    print(f"  貪婪演算法結果：")
    print(f"    選擇的集合：{chosen}")
    print(f"    集合數：{count}")
    covered = set()
    for idx in chosen:
        covered |= sc1.sets[idx]
    print(f"    覆蓋的元素：{covered}")
    print()

    # 測試 2：加權版本
    print("2. 加權集合覆蓋：")
    weights = [2.0, 3.0, 3.0, 1.0, 5.0, 4.0]
    chosen_w, count_w, total_w = sc1.weighted_greedy_set_cover(weights)
    print(f"  集合權重：{weights}")
    print(f"  選擇的集合：{chosen_w}")
    print(f"  集合數：{count_w}")
    print(f"  總權重：{total_w}")
    print()

    # 測試 3：簡單案例
    print("3. 簡單案例（兩個集合覆蓋全域）：")
    sc3 = SetCoverApproximation({1, 2, 3, 4})
    sc3.add_set(0, {1, 2})
    sc3.add_set(1, {3, 4})
    chosen, count = sc3.greedy_set_cover()
    print(f"  選擇的集合：{chosen}")
    print(f"  集合數：{count}")
    print()

    # 測試 4：單一集合覆蓋全部
    print("4. 單一集合覆蓋全部：")
    sc4 = SetCoverApproximation({1, 2, 3})
    sc4.add_set(0, {1, 2, 3})
    chosen, count = sc4.greedy_set_cover()
    print(f"  選擇的集合：{chosen}")
    print(f"  集合數：{count}")
    print()

    # 測試 5：無法完全覆蓋（部分覆蓋）
    print("5. 集合無法完全覆蓋全域：")
    sc5 = SetCoverApproximation({1, 2, 3, 4, 5})
    sc5.add_set(0, {1, 2})
    sc5.add_set(1, {3, 4})
    chosen, count = sc5.greedy_set_cover()
    print(f"  選擇的集合：{chosen}")
    print(f"  集合數：{count}")
    covered = set()
    for idx in chosen:
        covered |= sc5.sets[idx]
    print(f"  實際覆蓋：{covered}")
    print()
    print("測試完成！")
