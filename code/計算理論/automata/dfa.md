# 確定性有限狀態自動機 (DFA)

## 歷史背景

確定性有限狀態自動機 (Deterministic Finite Automaton, DFA) 是計算理論中最基礎的計算模型之一。

### 重要里程碑

- **1943 年**：McCulloch 和 Pitts 提出神經網路模型，奠定了有限狀態機的基礎
- **1956 年**：Stephen Kleene 形式化了正規語言和正規表達式的理論
- **1959 年**：Michael O. Rabin 和 Dana Scott 證明了 DFA 與 NFA 的等價性，並因此獲得圖靈獎

## 核心概念

### 形式定義

DFA 是一個五元組 (Q, Σ, δ, q₀, F)：

1. **Q**：有限狀態集合
2. **Σ**：有限字母表（輸入符號集合）
3. **δ**：轉移函數，Q × Σ → Q（確定性：每個狀態對每個符號有且僅有一個轉移）
4. **q₀**：起始狀態，q₀ ∈ Q
5. **F**：接受狀態集合，F ⊆ Q

### 運作原理

1. 從起始狀態 q₀ 開始
2. 依序讀入輸入字串的每個符號
3. 根據轉移函數 δ 移動到下一個狀態
4. 讀完所有符號後，若最終狀態屬於 F，則接受該字串；否則拒絕

### 確定性特性

「確定性」意味著：
- 對於每個狀態和每個輸入符號，有且僅有一個下一個狀態
- 沒有 ε-轉移（不需要讀入符號的轉移）
- 給定當前狀態和輸入，下一個狀態是唯一確定的

## 程式碼說明

### DFA 類別

`dfa.py` 中的 `DFA` 類別實作了完整的 DFA 功能：

- `__init__`: 初始化五個組成元素
- `process`: 處理輸入字串並返回最終狀態
- `accepts`: 判斷字串是否被接受
- `get_all_reachable_states`: 獲取所有可達狀態

### 範例：能被 3 整除的二進位數

`create_dfa_divisible_by_3()` 建立了一個 DFA，接受所有二進位表示且能被 3 整除的數字。

**設計思路**：
- 狀態代表當前數值除以 3 的餘數 (0, 1, 2)
- 讀入一個 bit 時，新數值 = 舊數值 × 2 + bit
- 新餘數 = (舊餘數 × 2 + bit) % 3

**轉移表**：

| 當前狀態 | 輸入 0 | 輸入 1 |
|---------|--------|--------|
| q0 (餘0) | q0    | q1     |
| q1 (餘1) | q2    | q0     |
| q2 (餘2) | q1    | q2     |

### 範例：以 '01' 結尾的字串

`create_dfa_ends_with_01()` 建立了一個 DFA，接受所有以 '01' 結尾的字串。

**狀態設計**：
- q0: 尚未看到模式 '01'
- q1: 最後看到的符號是 '0'
- q2: 最後看到 '01'（接受狀態）

## 使用範例

```python
from theory.automata.dfa import DFA, create_dfa_divisible_by_3

# 建立 DFA
dfa = create_dfa_divisible_by_3()

# 測試字串
print(dfa.accepts("110"))  # True (6 能被 3 整除)
print(dfa.accepts("101"))  # False (5 不能被 3 整除)

# 查看最終狀態
print(dfa.process("110"))  # 'q0' (餘數為 0)
```

## 執行測試

```bash
python theory/automata/dfa.py
```

輸出：
```
=== 測試：能被 3 整除的二進位數 ===
0 (十進位: 0) -> DFA: True, 實際: True, 正確: True
11 (十進位: 3) -> DFA: True, 實際: True, 正確: True
110 (十進位: 6) -> DFA: True, 實際: True, 正確: True
1001 (十進位: 9) -> DFA: True, 實際: True, 正確: True
1010 (十進位: 10) -> DFA: False, 實際: False, 正確: True
1111 (十進位: 15) -> DFA: True, 實際: True, 正確: True

=== 測試：以 '01' 結尾的字串 ===
'01' -> DFA: True, 預期: True, 正確: True
'101' -> DFA: True, 預期: True, 正確: True
'001' -> DFA: True, 預期: True, 正確: True
'0' -> DFA: False, 預期: False, 正確: True
'1' -> DFA: False, 預期: False, 正確: True
'0101' -> DFA: True, 預期: True, 正確: True
'010' -> DFA: False, 預期: False, 正確: True
```

## 參考資料

- Rabin, M. O., & Scott, D. (1959). [Finite automata and their decision problems](https://doi.org/10.1147/rd.32.0114). *IBM Journal of Research and Development*, 3(2), 114-125.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
