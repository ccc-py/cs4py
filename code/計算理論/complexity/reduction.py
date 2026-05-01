"""
歸約 (Reduction) 演算法展示

歸約是計算複雜度理論中的核心概念：
將一個問題轉換為另一個問題，在多項式時間內完成。

如果 A 可以歸約到 B：
- 求解 B ⟹ 求解 A
- B 在 P 中 ⟹ A 在 P 中
- A 不在 P 中 ⟹ B 不在 P 中
"""

from typing import List, Dict, Any, Callable, Tuple
import time


class SATTo3SATReduction:
    """將 SAT 歸約為 3-SAT"""

    @staticmethod
    def reduce(clauses: List[List[str]]) -> List[List[str]]:
        """
        將任意 CNF 公式轉換為等價的 3-CNF 公式

        轉換規則：
        1. 子句若少於 3 個文字：填充至 3 個
        2. 子句若多於 3 個文字：引入新變數分割

        時間複雜度：O(m)，其中 m 是子句數
        """
        result = []

        for clause in clauses:
            n = len(clause)

            if n == 0:
                continue
            elif n == 1:
                x = clause[0]
                result.append([x, x, x])
            elif n == 2:
                result.append(clause + [clause[0]])
            elif n == 3:
                result.append(clause[:])
            else:
                new_vars = []
                rest = clause[:]

                while len(rest) > 3:
                    y = f"_y{len(result)}"
                    new_vars.append(y)
                    result.append([rest[0], rest[1], y])
                    rest = rest[2:] + [y]

                if len(rest) == 3:
                    result.append(rest)
                else:
                    y1, y2 = f"_y{len(result)}", f"_y{len(result)+1}"
                    result.append([rest[0], y1, y2])
                    result.append([rest[1], y1, y2[1:]])

        return result


class SATToCLIQUE:
    """將 3-SAT 歸約為 CLIQUE"""

    @staticmethod
    def reduce(clauses: List[List[str]]) -> Tuple[List[List[int]], int]:
        """
        將 3-SAT 公式歸約為 CLIQUE 問題

        建圖方式：
        - 每個子句建立一個三頂點的團
        - 同一變數的正反文字不能相連

        歸約完成後：
        - 存在大小 k 的團 ⟺ 公式可滿足

        時間複雜度：O(m + n)，其中 m 是子句數，n 是變數數
        """
        k = len(clauses)
        vertices = []
        edges = []
        var_to_indices = {}

        for i, clause in enumerate(clauses):
            base = i * 3
            for j, lit in enumerate(clause):
                idx = base + j
                vertices.append((i, j, lit))

                var = lit.lstrip("-")
                if var not in var_to_indices:
                    var_to_indices[var] = []
                var_to_indices[var].append((i, j))

        n_vertices = len(vertices)
        adj = [[0] * n_vertices for _ in range(n_vertices)]

        for a in range(n_vertices):
            i_a, j_a, lit_a = vertices[a]
            var_a = lit_a.lstrip("-")
            neg_a = lit_a.startswith("-")

            for b in range(a + 1, n_vertices):
                i_b, j_b, lit_b = vertices[b]
                var_b = lit_b.lstrip("-")
                neg_b = lit_b.startswith("-")

                if i_a == i_b:
                    continue

                if var_a == var_b and neg_a != neg_b:
                    continue

                adj[a][b] = 1
                adj[b][a] = 1

        return adj, k


class UndirectedToDirected:
    """將無向哈密爾頓圈歸約為有向哈密爾頓圈"""

    @staticmethod
    def reduce(n: int) -> int:
        """
        將 n 頂點無向哈密爾頓圈問題歸約為有向版本

        轉換：每個頂點替換為 2 個有向頂點

        時間複雜度：O(n)
        """
        return n * 2


class Reduction演示:
    """展示各種歸約"""

    @staticmethod
    def show_sat_to_3sat():
        """展示 SAT → 3-SAT 歸約"""
        print("=== SAT → 3-SAT 歸約展示 ===\n")

        clauses = [
            ["x1", "x2", "x3", "x4"],
            ["-x1", "x3"],
            ["x2", "-x3"],
        ]
        print(f"原始子句（SAT）：{clauses}")

        reduced = SATTo3SATReduction.reduce(clauses)
        print(f"轉換後（3-SAT）：{reduced}")
        print()
        print("轉換說明：")
        print("  ['x1', 'x2', 'x3', 'x4'] → 引入輔助變數拆分")
        print("  ['-x1', 'x3'] → 填充為 ['-x1', 'x3', '-x1']")
        print("  ['x2', '-x3'] → 填充為 ['x2', '-x3', 'x2']")

    @staticmethod
    def show_sat_to_clique():
        """展示 SAT → CLIQUE 歸約"""
        print("\n=== SAT → CLIQUE 歸約展示 ===\n")

        clauses = [
            ["x1", "x2", "x3"],
            ["-x1", "-x2"],
        ]
        print(f"原始 3-SAT 子句：{clauses}")
        print(f"預期團大小：k = {len(clauses)}\n")

        graph, k = SATToCLIQUE.reduce(clauses)
        print(f"建出的圖：")
        print(f"  頂點數：{len(graph)}")
        print(f"  目標團大小：k = {k}")
        print(f"  鄰接矩陣：")
        for row in graph:
            print(f"    {row}")

    @staticmethod
    def show_complexity_implications():
        """展示歸約的複雜度含義"""
        print("\n=== 歸約的複雜度含義 ===\n")

        reductions = [
            ("SAT → 3-SAT", "SAT ≡ₚ 3-SAT", "證明 3-SAT 是 NP-Complete 的基礎"),
            ("3-SAT → CLIQUE", "3-SAT ≡ₚ CLIQUE", "Karp 的經典歸約之一"),
            ("CLIQUE → VERTEX-COVER", "CLIQUE ≤ₚ VERTEX-COVER", "互補關係"),
            ("HAM-CYCLE → TSP", "HAM-CYCLE ≡ₚ TSP", "TSP 是 NP-Complete"),
        ]

        print("已知 NP-Complete 問題之間的歸約：")
        for from_prob, relation, note in reductions:
            print(f"  {from_prob}")
            print(f"    {relation}")
            print(f"    → {note}")
            print()


class PolynomialTimeReducer:
    """多項式時間歸約工具"""

    @staticmethod
    def verify_polynomial_time(func: Callable) -> bool:
        """
        驗證函數是否可能是多項式時間

        簡單檢查：運行多次測量時間增長
        """
        test_sizes = [10, 20, 40, 80]
        times = []

        print(f"測量 {func.__name__} 的執行時間：")

        for n in test_sizes:
            start = time.time()
            try:
                if func.__name__ == "reduce":
                    SATTo3SATReduction.reduce([[f"x{i}" for i in range(n)]])
                result = True
            except:
                result = False
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  n={n}: {elapsed:.6f} 秒")

        if len(times) >= 2 and times[-1] > 0:
            ratio = times[-1] / times[0] if times[0] > 0 else float('inf')
            print(f"  時間增長比率（80/10）: {ratio:.2f}x")
            if ratio < 100:
                print("  → 可能為多項式時間")
            else:
                print("  → 可能為指數時間")

        return result


def demonstrate_reductions():
    """演示歸約"""
    Reduction演示.show_sat_to_3sat()
    Reduction演示.show_sat_to_clique()
    Reduction演示.show_complexity_implications()

    print("\n=== 多項式時間驗證 ===")
    PolynomialTimeReducer.verify_polynomial_time(SATTo3SATReduction.reduce)


if __name__ == "__main__":
    print("歸約演示程式")
    print("=" * 50)
    print()
    demonstrate_reductions()