"""
SAT 問題求解器 (Boolean Satisfiability Problem)

SAT 是第一個被證明為 NP-完備的問題（Cook-Levin 定理）。

SAT 問題：給定一個布林公式，是否存在一組變數賦值使其為真？

3-SAT：每個子句恰好有 3 個文字（3-CNF）。
- 3-SAT 是 NP-完備的
- 2-SAT 可以在多項式時間內求解（在 P 中）

歷史背景：
- 1971 年：Stephen Cook 證明 SAT 是 NP-完備的
- 1973 年：Leonid Levin 獨立證明了相同結果
- 應用：電路設計驗證、自動定理證明、排程問題等

參考：Cook, S. A. (1971). The complexity of theorem proving procedures.
"""

from typing import Dict, List, Tuple, Optional


class SATSolver:
    """SAT 求解器（使用簡單的 DPLL 演算法）"""

    def __init__(self, clauses: List[List[str]]):
        """
        初始化 SAT 求解器

        Args:
            clauses: CNF 公式，格式: [[literal1, literal2, ...], ...]
                     每個子句是文字的列表（如 "x" 或 "-x" 表示 ¬x）
        """
        self.clauses = clauses
        self.variables = self._extract_variables(clauses)

    def _extract_variables(self, clauses: List[List[str]]) -> set:
        """提取所有變數"""
        vars = set()
        for clause in clauses:
            for lit in clause:
                var = lit.lstrip('-')
                vars.add(var)
        return vars

    def solve(self) -> Optional[Dict[str, bool]]:
        """
        求解 SAT 問題

        Returns:
            滿足賦值（字典）如果可滿足，否則 None
        """
        assignment = {}
        return self._dpll(assignment)

    def _dpll(self, assignment: Dict[str, bool]) -> Optional[Dict[str, bool]]:
        """
        DPLL 演算法（Davis-Putnam-Logemann-Loveland）

        步驟：
        1. 單位傳播 (Unit propagation)
        2. 純文字消除 (Pure literal elimination)
        3. 選擇變數並分支
        """
        # 複製賦值（避免修改原字典）
        assign = assignment.copy()

        # 單位傳播
        while True:
            unit_result = self._unit_propagation(self.clauses, assign)
            if unit_result is None:
                return None  # 衝突
            clauses, assign = unit_result

            # 檢查是否所有子句都滿足
            if not clauses:
                return assign

            # 純文字消除
            pure_lit = self._find_pure_literal(clauses, assign)
            if pure_lit:
                var = pure_lit.lstrip('-')
                value = not pure_lit.startswith('-')
                assign[var] = value
                continue

            break

        # 選擇未賦值的變數
        unassigned = self.variables - set(assign.keys())
        if not unassigned:
            # 所有變數都已賦值，檢查是否滿足
            return assign if self._check_satisfaction(assign) else None

        # 分支：嘗試 True
        var = next(iter(unassigned))
        assign_true = assign.copy()
        assign_true[var] = True
        result = self._dpll(assign_true)
        if result is not None:
            return result

        # 嘗試 False
        assign_false = assign.copy()
        assign_false[var] = False
        return self._dpll(assign_false)

    def _unit_propagation(self, clauses, assignment):
        """單位傳播：如果子句只有一個文字，該文字必須為真"""
        clauses = [c.copy() for c in clauses]  # 複製

        while True:
            unit_clauses = []
            for clause in clauses:
                unassigned = [lit for lit in clause
                              if lit.lstrip('-') not in assignment]
                if len(unassigned) == 1:
                    unit_clauses.append(unassigned[0])

            if not unit_clauses:
                break

            for lit in unit_clauses:
                var = lit.lstrip('-')
                value = not lit.startswith('-')

                # 如果已賦值且衝突
                if var in assignment and assignment[var] != value:
                    return None

                assignment[var] = value

                # 簡化子句
                new_clauses = []
                for clause in clauses:
                    new_clause = []
                    skip = False
                    for l in clause:
                        v = l.lstrip('-')
                        val = not l.startswith('-')
                        if v == var:
                            if val == value:
                                # 文字為真，整個子句滿足
                                skip = True
                                break
                            # 文字為假，移除
                        else:
                            new_clause.append(l)
                    if not skip and new_clause:
                        new_clauses.append(new_clause)
                clauses = new_clauses

        return clauses, assignment

    def _find_pure_literal(self, clauses, assignment):
        """找出純文字（某變數的所有出現都是同一極性）"""
        pos_occurrences = set()
        neg_occurrences = set()

        for clause in clauses:
            for lit in clause:
                var = lit.lstrip('-')
                if var not in assignment:
                    if lit.startswith('-'):
                        neg_occurrences.add(var)
                    else:
                        pos_occurrences.add(var)

        # 純文字：只出現在一種極性
        for var in pos_occurrences:
            if var not in neg_occurrences:
                return var  # 正文字
        for var in neg_occurrences:
            if var not in pos_occurrences:
                return '-' + var  # 負文字

        return None

    def _check_satisfaction(self, assignment):
        """檢查賦值是否滿足所有子句"""
        for clause in self.clauses:
            satisfied = False
            for lit in clause:
                var = lit.lstrip('-')
                value = not lit.startswith('-')
                if var in assignment and assignment[var] == value:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True


def create_example_3sat():
    """建立一個 3-SAT 例子"""
    # (x1 ∨ x2 ∨ x3) ∧ (¬x1 ∨ x2 ∨ x4) ∧ (x1 ∨ ¬x2 ∨ x3)
    clauses = [
        ['x1', 'x2', 'x3'],
        ['-x1', 'x2', 'x4'],
        ['x1', '-x2', 'x3'],
    ]
    return clauses


def create_unsatisfiable():
    """建立一個不可滿足的例子"""
    # (x) ∧ (¬x)
    clauses = [
        ['x'],
        ['-x'],
    ]
    return clauses


if __name__ == "__main__":
    print("=== SAT 求解器測試 ===")
    print()

    # 測試：可滿足的例子
    print("測試：可滿足的 3-SAT 公式")
    clauses = create_example_3sat()
    print(f"  子句: {clauses}")
    solver = SATSolver(clauses)
    result = solver.solve()
    print(f"  結果: {result}")
    print(f"  可滿足: {result is not None}")
    print()

    # 測試：不可滿足的例子
    print("測試：不可滿足的公式 (x) ∧ (¬x)")
    clauses = create_unsatisfiable()
    print(f"  子句: {clauses}")
    solver = SATSolver(clauses)
    result = solver.solve()
    print(f"  結果: {result}")
    print(f"  可滿足: {result is not None}")
    print()

    # 測試：空公式
    print("測試：空公式（平凡可滿足）")
    solver = SATSolver([])
    result = solver.solve()
    print(f"  結果: {result}")
    print(f"  可滿足: {result is not None}")
