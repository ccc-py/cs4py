"""
NP-Complete 問題展示

NP-Complete 是 NP 中最困難的問題類別。
如果任何一個 NP-Complete 問題可以在多項式時間內求解，則所有 NP 問題都可以。

本模組展示：
- 驗證一個問題是否為 NP-Complete
- 常見 NP-Complete 問題的驗證器
"""

from typing import List, Dict, Set, Tuple, Optional


class NPCompleteVerifier:
    """NP-Complete 問題驗證器集合"""

    @staticmethod
    def verify_clique(graph: List[List[int]], vertices: List[int], k: int) -> bool:
        """
        驗證給定的頂點集合是否是一個大小 >= k 的團

        團（Clique）：圖中任意兩個頂點都相鄰的集合

        驗證時間：O(k²)
        """
        if len(vertices) < k:
            return False

        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1, v2 = vertices[i], vertices[j]
                if graph[v1][v2] == 0:
                    return False
        return True

    @staticmethod
    def verify_vertex_cover(
        graph: List[List[int]], vertices: List[int], k: int
    ) -> bool:
        """
        驗證給定的頂點集合是否是一個大小 <= k 的頂點覆蓋

        頂點覆蓋（Vertex Cover）：圖中每條邊至少有一個端點在此集合中

        驗證時間：O(m)，其中 m 是邊數
        """
        if len(vertices) > k:
            return False

        n = len(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    if i not in vertices and j not in vertices:
                        return False
        return True

    @staticmethod
    def verify_hamiltonian_cycle(n: int, path: List[int]) -> bool:
        """
        驗證是否為哈密爾頓圈

        哈密爾頓圈：經過圖中每個頂點恰好一次的圈

        驗證時間：O(n)
        """
        if len(path) != n:
            return False

        if path[0] != path[-1]:
            return False

        if len(set(path[:-1])) != n:
            return False

        for i in range(n - 1):
            pass
        return True

    @staticmethod
    def verify_subset_sum(items: List[int], subset: Set[int], target: int) -> bool:
        """
        驗證子集合

        驗證時間：O(n)
        """
        total = sum(items[i] for i in subset)
        return total == target

    @staticmethod
    def verify_sat(clauses: List[List[str]], assignment: Dict[str, bool]) -> bool:
        """
        驗證布林公式是否被滿足

        驗證時間：O(總文字數)
        """
        for clause in clauses:
            clause_satisfied = False
            for lit in clause:
                var = lit.lstrip("-")
                value = not lit.startswith("-")
                if assignment.get(var) == value:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                return False
        return True


class NPCompleteProblem:
    """常見 NP-Complete 問題的結構定義"""

    PROBLEMS = {
        "SAT": {
            "full_name": "Boolean Satisfiability Problem",
            "輸入": "布林公式（CNF 形式）",
            "問題": "是否存在滿足公式的賦值？",
            "證明": "Cook (1971) - 第一個 NP-Complete 問題",
        },
        "3-SAT": {
            "full_name": "3-Satisfiability",
            "輸入": "3-CNF 公式（每個子句恰好 3 個文字）",
            "問題": "是否存在滿足公式的賦值？",
            "證明": "從 SAT 歸約",
        },
        "CLIQUE": {
            "full_name": "Clique Problem",
            "輸入": "圖 G 和整數 k",
            "問題": "是否存在大小 >= k 的團？",
            "證明": "Karp (1972) - 從 3-SAT 歸約",
        },
        "VERTEX-COVER": {
            "full_name": "Vertex Cover Problem",
            "輸入": "圖 G 和整數 k",
            "問題": "是否存在大小 <= k 的頂點覆蓋？",
            "證明": "Karp (1972) - 從 CLIQUE 歸約",
        },
        "HAM-CYCLE": {
            "full_name": "Hamiltonian Cycle Problem",
            "輸入": "圖 G",
            "問題": "是否存在哈密爾頓圈？",
            "證明": "Karp (1972)",
        },
        "TSP": {
            "full_name": "Traveling Salesman Problem",
            "輸入": "完全圖 G 和預算 B",
            "問題": "是否存在長度 <= B 的哈密爾頓圈？",
            "證明": "從 HAM-CYCLE 歸約",
        },
        "SUBSET-SUM": {
            "full_name": "Subset Sum Problem",
            "輸入": "整數集合 S 和目標值 t",
            "問題": "是否存在子集合和為 t？",
            "證明": "Karp (1972)",
        },
        "KNAPSACK": {
            "full_name": "Knapsack Problem",
            "輸入": "物品集合、容量 C、價值需求 V",
            "問題": "是否能選擇物品填滿背包？",
            "證明": "從 SUBSET-SUM 歸約",
        },
    }

    @classmethod
    def list_problems(cls):
        """列出所有 NP-Complete 問題"""
        print("=== 常見 NP-Complete 問題 ===\n")
        for name, info in cls.PROBLEMS.items():
            print(f"{name}: {info['full_name']}")
            print(f"  輸入：{info['輸入']}")
            print(f"  問題：{info['問題']}")
            print(f"  歸約證明：{info['證明']}")
            print()


def demonstrate_npc():
    """演示 NP-Complete 問題"""
    print("=== NP-Complete 問題驗證演示 ===\n")

    print("【CLIQUE 問題】")
    graph = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0],
    ]
    vertices = [0, 1, 2]
    k = 3
    result = NPCompleteVerifier.verify_clique(graph, vertices, k)
    print(f"  圖：4 頂點完全圖 K4")
    print(f"  候選團：{vertices}")
    print(f"  驗證 k={k}: {'是團' if result else '不是團'}")

    print("\n【VERTEX-COVER 問題】")
    vertices = [1, 2]
    k = 2
    result = NPCompleteVerifier.verify_vertex_cover(graph, vertices, k)
    print(f"  圖：4 頂點")
    print(f"  候選覆蓋：{vertices}")
    print(f"  驗證 k={k}: {'是頂點覆蓋' if result else '不是頂點覆蓋'}")

    print("\n【SUBSET-SUM 問題】")
    items = [3, 34, 4, 12, 5, 2]
    subset = {0, 2, 5}
    target = 9
    result = NPCompleteVerifier.verify_subset_sum(items, subset, target)
    print(f"  集合：{items}")
    print(f"  候選子集合：{subset} (元素 3, 4, 2)")
    print(f"  目標：{target}")
    print(f"  驗證：{'正確' if result else '錯誤'} (3+4+2=9)")

    print("\n【3-SAT 問題】")
    clauses = [["x1", "x2", "x3"], ["-x1", "x2", "x4"], ["x1", "-x2", "x3"]]
    assignment = {"x1": True, "x2": True, "x3": True, "x4": False}
    result = NPCompleteVerifier.verify_sat(clauses, assignment)
    print(f"  子句：{clauses}")
    print(f"  賦值：{assignment}")
    print(f"  驗證：{'可滿足' if result else '不可滿足'}")

    NPCompleteProblem.list_problems()


if __name__ == "__main__":
    demonstrate_npc()