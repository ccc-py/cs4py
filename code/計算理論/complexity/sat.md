# SAT 問題求解器 (Boolean Satisfiability Problem)

## 歷史背景

SAT 是第一個被證明為 NP-完備的問題（Cook-Levin 定理）。

### 重要里程碑

- **1971 年**：Stephen Cook 證明 SAT 是 NP-完備的
- **1973 年**：Leonid Levin 獨立證明了相同結果
- **應用**：電路設計驗證、自動定理證明、排程問題等

## 核心概念

### SAT 問題

> 給定一個布林公式（CNF 形式），是否存在一組變數賦值使其為真？

### CNF (Conjunctive Normal Form)

合取範式：多個子句的合取，每個子句是文字的析取。

**例子**：
```
(x1 ∨ x2 ∨ ¬x3) ∧ (¬x1 ∨ x2) ∧ (x3 ∨ ¬x2)
```

### 3-SAT

每個子句恰好有 3 個文字。3-SAT 是 NP-完備的，但 2-SAT 在 P 中。

## 程式碼說明

### SATSolver 類別

`sat.py` 實作了 DPLL 演算法（Davis-Putnam-Logemann-Loveland）：

#### 演算法步驟

1. **單位傳播 (Unit Propagation)**：
   - 如果子句只有一個文字，該文字必須為真
   - 簡化公式後重複

2. **純文字消除 (Pure Literal Elimination)**：
   - 如果變數只以一種極性出現，可將其設為真

3. **分支 (Branching)**：
   - 選擇未賦值變數
   - 嘗試 True，遞迴求解
   - 失敗則嘗試 False

### 關鍵方法

#### `_unit_propagation(clauses, assignment)` - 單位傳播

```python
# 找出單位子句（只有一個未賦值文字）
if len(unassigned) == 1:
    unit_clauses.append(unassigned[0])

# 根據單位文字設定賦值
for lit in unit_clauses:
    var = lit.lstrip('-')
    value = not lit.startswith('-')
    assignment[var] = value
```

#### `_dpll(assignment)` - DPLL 主演算法

```python
# 1. 單位傳播
clauses, assign = self._unit_propagation(...)

# 2. 純文字消除
pure_lit = self._find_pure_literal(...)

# 3. 分支
var = next(iter(unassigned))
result = self._dpll(assign_true)  # 嘗試 True
if result is None:
    result = self._dpll(assign_false)  # 嘗試 False
```

## 使用範例

```python
from theory.complexity.sat import SATSolver, create_example_3sat

# 建立 3-SAT 例子
clauses = create_example_3sat()
print(clauses)
# [['x1', 'x2', 'x3'], ['-x1', 'x2', 'x4'], ['x1', '-x2', 'x3']]

# 求解
solver = SATSolver(clauses)
result = solver.solve()
print(result)
# 例如：{'x1': True, 'x2': True, 'x3': True, 'x4': False}
```

## 執行測試

```bash
python theory/complexity/sat.py
```

輸出：
```
=== SAT 求解器測試 ===

測試：可滿足的 3-SAT 公式
  子句: [['x1', 'x2', 'x3'], ['-x1', 'x2', 'x4'], ['x1', '-x2', 'x3']]
  結果: {'x1': True, 'x2': True, 'x3': True, 'x4': False}
  可滿足: True

測試：不可滿足的公式 (x) ∧ (¬x)
  子句: [['x'], ['-x']]
  結果: None
  可滿足: False

測試：空公式（平凡可滿足）
  結果: {}
  可滿足: True
```

## DPLL 演算法複雜度

- **最壞情況**：O(2ⁿ)（指數時間）
- **實務上**：現代 SAT 求解器（如 MiniSat, Z3）可處理數萬個變數
- **啟發式**：變數選擇、子句學習、重啟等技術

## 參考資料

- Cook, S. A. (1971). [The complexity of theorem proving procedures](https://doi.org/10.1145/800157.805047). *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*, 151-158.
- Davis, M., Logemann, G., & Loveland, D. (1962). A machine program for theorem-proving. *Communications of the ACM*, 5(7), 394-397.
- Russell, S. J., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
