# 非確定性有限狀態自動機 (NFA)

## 歷史背景

非確定性有限狀態自動機 (Nondeterministic Finite Automaton, NFA) 由 Rabin 和 Scott 在 1959 年與 DFA 同時提出。

### NFA vs DFA

雖然 NFA 在定義上允許「非確定性」，但 Rabin 和 Scott 證明了：
- **NFA 和 DFA 識別的語言類別完全相同**（都是正規語言）
- 任何 NFA 都可以透過「子集構造法」轉換成等價的 DFA
- DFA 的狀態數可能是指數級增長（2^n）

## 核心概念

### 形式定義

NFA 是一個五元組 (Q, Σ, δ, q₀, F)：

1. **Q**：有限狀態集合
2. **Σ**：有限字母表（不包含 ε）
3. **δ**：轉移函數，Q × (Σ ∪ {ε}) → P(Q)（狀態的冪集）
4. **q₀**：起始狀態（可以是單一狀態或狀態集合）
5. **F**：接受狀態集合，F ⊆ Q

### NFA 的兩個關鍵特性

#### 1. 非確定性轉移

對於同一個狀態和輸入符號，可以有多個下一個狀態：

```
狀態 q 讀入符號 'a' → 可以到達 {q1, q2, q3}
```

#### 2. ε-轉移

不需要讀入任何符號就可以進行的轉移：

```
狀態 q1 --ε--> q2
```

這使得 NFA 可以在不消耗輸入的情況下「自由移動」。

### ε-閉包 (Epsilon Closure)

ε-閉包是 NFA 處理的關鍵概念：

> 從某個狀態集合出發，透過零個或多個 ε-轉移可以到達的所有狀態的集合。

**計算方法**（類似圖的 DFS/BFS）：
1. 將初始狀態加入閉包
2. 對閉包中的每個狀態，找出所有 ε-轉移的目標狀態
3. 將新狀態加入閉包，重複直到沒有新狀態

### NFA 接受的定義

字串 w 被 NFA 接受，當且僅當：
- 存在至少一條從起始狀態到某個接受狀態的路徑
- 該路徑上的標籤連起來等於 w

## 程式碼說明

### NFA 類別

`nfa.py` 中的 `NFA` 類別實作了 NFA 的核心功能：

- `__init__`: 初始化（注意起始狀態會轉為集合）
- `epsilon_closure`: 計算 ε-閉包（使用堆疊實作）
- `process`: 處理輸入並返回所有可能的最終狀態
- `accepts`: 只要有任何最終狀態屬於接受狀態就返回 True

### 範例：包含 '01' 的字串

`create_nfa_contains_01()` 展示了 NFA 的簡潔性：

**設計思路**：
1. q0 可以透過讀入 '0' 轉移到 q0（跳過前綴）或 q1（開始匹配）
2. q1 讀入 '1' 到達 q2（完成 '01' 匹配）
3. q2 透過 ε-轉移到達接受狀態 q3
4. q3 可以讀入任意符號（接受後綴）

**與 DFA 的比較**：
- DFA 需要 4 個狀態來識別「包含 01」
- 這個 NFA 也是 4 個狀態，但邏輯更直觀

### 範例：以 '01' 結尾

`create_nfa_ends_with_01()` 展示了 NFA 的優勢：

**關鍵設計**：
- q0 讀入 '0' 時，可以「分支」：留在 q0（繼續掃描）或去 q1（開始匹配）
- 只有當最後兩個符號確實是 '01' 時，才會到達接受狀態 q2

**對應的 DFA** 需要 3 個狀態，但 NFA 的構造更直觀。

## 使用範例

```python
from theory.autata.nfa import NFA, create_nfa_contains_01

# 建立 NFA
nfa = create_nfa_contains_01()

# 測試字串
print(nfa.accepts("101"))      # True（包含 '01'）
print(nfa.accepts("111"))      # False（不包含 '01'）

# 查看所有可能的最終狀態
final_states = nfa.process("1010")
print(final_states)  # {'q3'} 或其他接受狀態
```

## 執行測試

```bash
python theory/automata/nfa.py
```

輸出：
```
=== 測試：包含 '01' 的字串 ===
'01' -> NFA: True, 預期: True, 正確: True
'101' -> NFA: True, 預期: True, 正確: True
'001' -> NFA: True, 預期: True, 正確: True
'0' -> NFA: False, 預期: False, 正確: True
'1' -> NFA: False, 預期: False, 正確: True
'0101' -> NFA: True, 預期: True, 正確: True
'111' -> NFA: False, 預期: False, 正確: True
'010' -> NFA: True, 預期: True, 正確: True

=== 測試：以 '01' 結尾的字串 ===
'01' -> NFA: True, 預期: True, 正確: True
'101' -> NFA: True, 預期: True, 正確: True
'001' -> NFA: True, 預期: True, 正確: True
'0' -> NFA: False, 預期: False, 正確: True
'1' -> NFA: False, 預期: False, 正確: True
'0101' -> NFA: False, 預期: False, 正確: True
'010' -> NFA: False, 預期: False, 正確: True

=== 比較 NFA 和 DFA（以 '01' 結尾）===
'01' -> DFA: True, NFA: True, 一致: True
'101' -> DFA: True, NFA: True, 一致: True
'001' -> DFA: True, NFA: True, 一致: True
'0' -> DFA: False, NFA: False, 一致: True
'1' -> DFA: False, NFA: False, 一致: True
'0101' -> DFA: False, NFA: False, 一致: True
'010' -> DFA: False, NFA: False, 一致: True
```

## 參考資料

- Rabin, M. O., & Scott, D. (1959). [Finite automata and their decision problems](https://doi.org/10.1147/rd.32.0114). *IBM Journal of Research and Development*, 3(2), 114-125.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
