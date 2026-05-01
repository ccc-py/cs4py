# 下推自動機 (PDA)

## 歷史背景

下推自動機 (Pushdown Automaton, PDA) 在 1950 年代末期被提出，用於形式化描述上下文無關語言的運算模型。

### 重要里程碑

- **1960 年代**：Chomsky 提出上下文無關文法 (CFG)
- **1967 年**：Hopcroft 和 Ullman 證明了 PDA 與 CFG 的等價性
- **應用**：PDA 是編譯器語法分析的理論基礎（如 LL、LR 分析器）

## 核心概念

### 形式定義

PDA 是一個七元組 (Q, Σ, Γ, δ, q₀, Z₀, F)：

1. **Q**：有限狀態集合
2. **Σ**：輸入字母表
3. **Γ**：堆疊字母表
4. **δ**：轉移函數，Q × (Σ ∪ {ε}) × (Γ ∪ {ε}) → P(Q × Γ*)
5. **q₀**：起始狀態
6. **Z₀**：起始堆疊符號
7. **F**：接受狀態集合

### PDA 的擴展能力

相比於有限狀態自動機（沒有記憶體），PDA 增加了一個**堆疊**：

```
┌─────────┐     讀入符號     ┌─────────┐
│         │ ──────────────> │         │
│  PDA    │                 │  堆疊   │
│  狀態    │ <────────────── │  (後進  │
│         │   推入/彈出      │   先出) │
└─────────┘                 └─────────┘
```

### 堆疊操作

- **推入 (Push)**：將符號放入堆疊頂端
- **彈出 (Pop)**：移除堆疊頂端的符號
- **空操作**：不改變堆疊

### 確定性 vs 非確定性

- **DPDA**（確定性）：對於每個組態，最多一個轉移
- **NPDA**（非確定性）：可以有多個轉移（更強大）

**重要結論**：NPDA 比 DPDA 更強大，存在某些上下文無關語言只能被 NPDA 識別。

## 程式碼說明

### PDA 類別

`pda.py` 中的 `PDA` 類別實作了非確定性 PDA：

- `__init__`: 初始化七個組成元素
- `_get_transitions`: 獲取所有可能的轉移
- `accepts`: 使用 BFS 遍歷所有可能的組態
- `_apply_operation`: 應用堆疊操作

### 範例：括號平衡

`create_pda_balanced_parens()` 建立 PDA 來識別括號平衡的字符串：

**策略**：
1. 讀入 '(' → 推入堆疊
2. 讀入 ')' → 彈出堆疊頂端的 '('
3. 讀完後，堆疊應該只剩下 Z0（起始符號）

**為什麼需要 PDA？**
- 有限狀態自動機無法識別括號平衡（需要無限記憶體）
- PDA 的堆疊提供了「有限但可變」的記憶體

### 範例：w c w^R（回文）

`create_pda_palindrome()` 建立 PDA 來識別形如 "w c w 的反轉" 的字串：

**策略**：
1. q0: 讀入 w 的符號，推入堆疊
2. 讀到 'c'，進入 q1（不消耗堆疊）
3. q1: 讀入 w^R 的符號，與堆疊頂端匹配並彈出
4. 最後堆疊應該只剩下 Z0

**這是經典的非正規語言例子**，證明了 PDA 比 FSA 更強大。

## 使用範例

```python
from theory.automata.pda import create_pda_balanced_parens, create_pda_palindrome

# 測試括號平衡
pda = create_pda_balanced_parens()
print(pda.accepts("()"))      # True
print(pda.accepts("(())"))    # True
print(pda.accepts("(()"))     # False

# 測試 w c w^R
pda2 = create_pda_palindrome()
print(pda2.accepts("c"))      # True (w 為空)
print(pda2.accepts("0c0"))    # True
print(pda2.accepts("01c10"))  # True
print(pda2.accepts("0c1"))    # False
```

## 執行測試

```bash
python theory/automata/pda.py
```

輸出：
```
=== 測試：括號平衡 ===
'()' -> PDA: True, 預期: True, 正確: True
'(())' -> PDA: True, 預期: True, 正確: True
'()()' -> PDA: True, 預期: True, 正確: True
'(()' -> PDA: False, 預期: False, 正確: True
'())' -> PDA: False, 預期: False, 正確: True
'' -> PDA: False, 預期: False, 正確: True

=== 測試：w c w^R（回文）===
'c' -> PDA: True, 預期: True, 正確: True
'0c0' -> PDA: True, 預期: True, 正確: True
'1c1' -> PDA: True, 預期: True, 正確: True
'01c10' -> PDA: True, 預期: True, 正確: True
'10c01' -> PDA: True, 預期: True, 正確: True
'0c1' -> PDA: False, 預期: False, 正確: True
'01c01' -> PDA: False, 預期: False, 正確: True
```

## 語言層次結構

```
正規語言 (Regular)     ← FSA/NFA/DFA 識別
    ↓ (嚴格包含)
上下文無關語言 (CFL)   ← PDA 識別
    ↓ (嚴格包含)
上下文有關語言 (CSL)   ← 線性有界自動機識別
    ↓ (嚴格包含)
遞歸可列舉語言 (RE)   ← 圖靈機識別
```

## 參考資料

- Hopcroft, J. E., & Ullman, J. D. (1967). *Formal Languages and Their Relation to Automata*. Addison-Wesley.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
