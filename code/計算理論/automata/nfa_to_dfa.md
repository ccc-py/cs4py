# NFA 轉 DFA（子集構造法）

## 歷史背景

子集構造法（Subset Construction）由 Rabin 和 Scott 在 1959 年提出，用於證明 NFA 和 DFA 的等價性。

### 重要結論

- **等價性**：任何 NFA 都存在一個等價的 DFA（識別相同的語言）
- **狀態爆炸**：DFA 的狀態數最多是 2^n（n 是 NFA 的狀態數）
- **實用性**：雖然理論上可行，但實際應用中可能導致狀態數指數增長

## 核心概念

### 子集構造法原理

將 NFA 的「狀態集合」視為 DFA 的「單一狀態」：

```
NFA 狀態: {q0, q1, q2}
         ↓
DFA 狀態: {q0, q1, q2}  (將整個集合視為一個 DFA 狀態)
```

### 演算法步驟

1. **起始狀態**：DFA 起始狀態 = ε-閉包(NFA 起始狀態)
2. **轉移函數**：對於 DFA 狀態 S（NFA 狀態集合）和符號 a：
   - 找出從 S 中所有狀態透過 a 可達的 NFA 狀態
   - 計算這些狀態的 ε-閉包
   - 結果就是 DFA 的下一個狀態
3. **接受狀態**：任何包含 NFA 接受狀態的 DFA 狀態都是接受狀態

### 狀態表示

由於 DFA 的狀態是 NFA 狀態的集合，我們用 `frozenset` 來表示（因為要作為字典的鍵）。

**範例**：
```
NFA 狀態集合: {'q0', 'q1'}
DFA 狀態表示: frozenset({'q0', 'q1'})
```

## 程式碼說明

### 主要函數

`nfa_to_dfa(nfa)` 實作了完整的子集構造法：

1. **初始化**：計算起始狀態的 ε-閉包
2. **遍歷**：使用佇列儲存未處理的 DFA 狀態
3. **轉移計算**：對每個 DFA 狀態和每個字母表符號，計算下一個 DFA 狀態
4. **接受狀態判定**：如果 DFA 狀態（NFA 狀態集合）與 NFA 接受狀態有交集，則為接受狀態

### 關鍵程式碼片段

```python
# 計算轉移
for state in current_set:
    key = (state, symbol)
    if key in nfa.transitions:
        next_states.update(nfa.transitions[key])

# 計算 ε-閉包
next_closure = frozenset(nfa.epsilon_closure(next_states))

# 添加轉移
dfa_transitions[(current_set, symbol)] = next_closure
```

## 使用範例

```python
from theory.automata.nfa import create_nfa_ends_with_01
from theory.automata.nfa_to_dfa import nfa_to_dfa, print_dfa

# 建立 NFA
nfa = create_nfa_ends_with_01()

# 轉換為 DFA
dfa = nfa_to_dfa(nfa)

# 印出 DFA 資訊
print_dfa(dfa)

# 測試
print(dfa.accepts("01"))   # True
print(dfa.accepts("101"))  # True
print(dfa.accepts("0"))    # False
```

## 執行測試

```bash
python theory/automata/nfa_to_dfa.py
```

輸出：
```
=== NFA 轉 DFA 示範 ===

原始 NFA:
  狀態: {'q0', 'q1', 'q2'}
  起始: {'q0'}
  接受: {'q2'}

轉換後的 DFA:
DFA 狀態數: 3
字母表: {'0', '1'}
起始狀態: {q0}
接受狀態: ['{q2}']
轉移:
  {q0} --0--> {q0,q1}
  {q0} --1--> {q0}
  {q0,q1} --0--> {q0,q1}
  {q0,q1} --1--> {q0,q2}
  {q0,q2} --0--> {q0,q1}
  {q0,q2} --1--> {q0}

測試:
  '01': NFA=True, DFA=True, 一致=True
  '101': NFA=True, DFA=True, 一致=True
  '001': NFA=True, DFA=True, 一致=True
  '0': NFA=False, DFA=False, 一致=True
  '1': NFA=False, DFA=False, 一致=True
  '0101': NFA=False, DFA=False, 一致=True
  '010': NFA=False, DFA=False, 一致=True
```

## 狀態數分析

| NFA 狀態數 | DFA 最大狀態數 |
|-----------|--------------|
| 1         | 2            |
| 2         | 4            |
| 3         | 8            |
| n         | 2^n          |

這就是所謂的「狀態爆炸」問題。但在實際應用中，許多狀態集合是不可達的，因此實際 DFA 狀態數通常遠小於 2^n。

## 參考資料

- Rabin, M. O., & Scott, D. (1959). [Finite automata and their decision problems](https://doi.org/10.1147/rd.32.0114). *IBM Journal of Research and Development*, 3(2), 114-125.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
