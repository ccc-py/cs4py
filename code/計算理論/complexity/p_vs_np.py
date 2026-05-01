"""
P vs NP 問題演示

P vs NP 是理論計算機科學中最重要的未解問題之一。

核心問題：若答案可以在多項式時間內驗證，是否一定可以在多項式時間內求解？

本模組展示：
- P 類問題：可在多項式時間求解
- NP 類問題：可在多項式時間驗證
- NP-Complete 問題：NP 中最困難的問題
"""

from typing import List, Set, Dict, Any
import subprocess
import sys


class PSolver:
    """P 類問題：多項式時間可求解"""

    @staticmethod
    def subset_sum_dp(items: List[int], target: int) -> Set[int]:
        """
        子集合問題（動態規劃解法）

        在 P 中：O(n * target) 時間

        問題：是否存在子集合的和為 target？
        """
        n = len(items)
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        dp[0][0] = True

        for i in range(1, n + 1):
            dp[i][0] = True
            for s in range(1, target + 1):
                if s < items[i - 1]:
                    dp[i][s] = dp[i - 1][s]
                else:
                    dp[i][s] = dp[i - 1][s] or dp[i - 1][s - items[i - 1]]

        if not dp[n][target]:
            return set()

        result = set()
        s = target
        for i in range(n, 0, -1):
            if not dp[i - 1][s]:
                result.add(i - 1)
                s -= items[i - 1]

        return result


class NPSolver:
    """NP 類問題：多項式時間可驗證"""

    @staticmethod
    def subset_sum_verify(items: List[int], subset: Set[int], target: int) -> bool:
        """
        驗證子集合問題的候選解

        在 NP 中：O(n) 時間驗證
        """
        if sum(items[i] for i in subset) == target:
            return True
        return False


class NPCompleteDemonstration:
    """展示 NP-Complete 問題的特性"""

    @staticmethod
    def sat_to_clique_reduction():
        """
        展示從 SAT 到 CLIQUE 的歸約概念

        這是 Cook-Levin 定理的簡化版本：
        - SAT是第一個被證明為 NP-Complete 的問題
        - 所有 NP 問題都可以歸約到 SAT
        """
        print("=== NP-Complete 問題歸約展示 ===")
        print()
        print("Cook-Levin 定理 (1971):")
        print("  SAT 是第一個 NP-Complete 問題")
        print()
        print("所有 NP 問題都可以在多項式時間內歸約到 SAT：")
        print("  圖靈機 → SAT 公式 → 求解 SAT")
        print()
        print("因此，如果我們能快速求解 SAT，就能快速求解所有 NP 問題")
        print()

    @staticmethod
    def hierarchy_visualization():
        """顯示複雜度類別階層"""
        print("=== 複雜度類別階層 ===")
        print()
        classes = [
            ("L", "對數空間", "log space"),
            ("NL", "非確定性對數空間", "non-deterministic log space"),
            ("P", "多項式時間（可快速求解）", "polynomial time"),
            ("NP", "多項式時間（可快速驗證）", "non-deterministic polynomial time"),
            ("PSPACE", "多項式空間", "polynomial space"),
            ("EXPTIME", "指數時間", "exponential time"),
        ]
        print("已知：L ⊊ NL ⊊ PSPACE ⊊ EXPTIME")
        print("未解：P vs NP")
        print()
        for cls, cn, en in classes:
            print(f"  {cls:8} - {cn} ({en})")


def demonstrate_p_vs_np():
    """演示 P vs NP 的核心概念"""
    print("=== P vs NP 問題演示 ===")
    print()

    print("【P 類問題】可在多項式時間內求解")
    items = [3, 34, 4, 12, 5, 2]
    target = 9
    result = PSolver.subset_sum_dp(items, target)
    print(f"  子集合問題：items={items}, target={target}")
    print(f"  解：索引 {result}")
    print(f"  驗證：sum = {sum(items[i] for i in result)}")
    print()

    print("【NP 類問題】可在多項式時間內驗證")
    print("  假設有人聲稱上述問題的解是 {0, 2}（索引）")
    print(f"  驗證：3 + 4 = 7 ≠ {target}，錯誤！")
    print(f"  驗證：3 + 4 + 2 = 9 = {target}，正確！")
    print()

    print("【核心問題】")
    print("  為什麼有些問題很難求解但容易驗證？")
    print("  P = NP 嗎？還是 P ≠ NP？")
    print("  這是千禧年七大難題之一，獎金 100 萬美元！")


def check_installed(package: str) -> bool:
    """檢查套件是否已安裝"""
    try:
        subprocess.check_output(
            [sys.executable, "-m", "pip", "show", package],
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    print("P vs NP 問題演示程式")
    print("=" * 40)
    print()

    demonstrate_p_vs_np()
    print()
    NPCompleteDemonstration.sat_to_clique_reduction()
    NPCompleteDemonstration.hierarchy_visualization()