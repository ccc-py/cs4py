# 圖靈機 (Turing Machine)

## 歷史背景

圖靈機 (Turing Machine) 由 Alan Turing 在 1936 年提出，是計算理論中最重要、最強大的計算模型。

### 重要里程碑

- **1936 年**：Alan Turing 發表《On Computable Numbers》，提出圖靈機概念
- **1936 年**：Alonzo Church 獨立提出 Lambda 演算，兩者等價（Church-Turing Thesis）
- **1945 年**：John von Neumann 基於圖靈機概念設計了現代計算機架構

### Turing 的貢獻

Alan Turing 被譽為「計算機科學之父」：
- 提出通用圖靈機 (Universal Turing Machine)
- 證明了停機問題的不可判定性
- 二戰期間破解德軍 Enigma 密碼

## 核心概念

### 形式定義

圖靈機是一個七元組 (Q, Σ, Γ, δ, q₀, q_accept, q_reject)：

1. **Q**：有限狀態集合
2. **Σ**：輸入字母表（不包含空白符號 B）
3. **Γ**：帶字母表（包含 Σ 和空白符號 B）
4. **δ**：轉移函數，Q × Γ → Q × Γ × {L, R, S}
5. **q₀**：起始狀態
6. **q_accept**：接受狀態
7. **q_reject**：拒絕狀態

### 圖靈機的組成

```
┌─────────────────────────────────────────┐
│               控制單元                  │
│           (有限狀態控制器)               │
└──────────────┬──────────────────────────┘
               │ 讀寫頭
               ▼
┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│  │  │ 0│ 1│ 1│ 0│  │  │  │  │  │  無限長帶子
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  ←──┴──→
   可左移或右移
```

### 轉移函數的意義

δ(q, a) = (q', b, D) 表示：
- 當前處於狀態 q
- 讀寫頭讀到符號 a
- 轉移到狀態 q'
- 將當前格寫入符號 b
- 讀寫頭移動方向 D（L = 左, R = 右, S = 靜止）

### Church-Turing Thesis

> 任何可計算的函數都可以被圖靈機計算。

這是一個**假設**（不是定理），但至今未被推翻。

## 程式碼說明

### TuringMachine 類別

`turing.py` 中的 `TuringMachine` 類別實作了圖靈機模擬器：

- `__init__`: 初始化七個組成元素
- `run`: 執行圖靈機，記錄執行過程
- `accepts`: 判斷字串是否被接受

### 範例：{0^n 1^n | n ≥ 1}

`create_tm_0n1n()` 建立圖靈機來識別這個經典的上下文相關語言：

**策略**（配對法）：
1. q0: 將一個 0 標記為 X，去 q1
2. q1: 向右跳過 0、X、Y，找到一個 1 標記為 Y，去 q2
3. q2: 向左回到起點的 X，去 q0
4. 重複直到所有符號都被標記

**為什麼需要圖靈機？**
- 有限狀態自動機無法識別 {0^n 1^n}
- 下推自動機也無法識別（需要兩個計數器）
- 圖靈機有無限記憶體（帶子），可以處理這類語言

### 範例：偶數長度回文

`create_tm_palindrome()` 建立圖靈機來識別偶數長度的回文：

**策略**（兩端標記法）：
1. q0: 讀第一個符號，標記為 X，去 q1 或 q3
2. q1/q3: 向右掃到空白，然後向左找最後一個相同符號
3. 找到則標記為 X，回到 q0
4. 重複直到所有符號標記完

## 使用範例

```python
from theory.automata.turing import create_tm_0n1n, create_tm_palindrome

# 測試 {0^n 1^n}
tm = create_tm_0n1n()
print(tm.accepts("01"))        # True
print(tm.accepts("0011"))     # True
print(tm.accepts("000111"))   # True
print(tm.accepts("001"))      # False

# 查看執行過程
accepted, steps, snapshots = tm.run("0011")
print(f"接受: {accepted}, 步數: {steps}")
for state, head, tape in snapshots[:5]:
    print(f"  狀態 {state}, 讀寫頭位置 {head}, 帶子: {tape}")
```

## 執行測試

```bash
python theory/automata/turing.py
```

輸出：
```
=== 測試：語言 {0^n 1^n} ===
'01' -> TM: True, 預期: True, 正確: True
'0011' -> TM: True, 預期: True, 正確: True
'000111' -> TM: True, 預期: True, 正確: True
'001' -> TM: False, 預期: False, 正確: True
'0101' -> TM: False, 預期: False, 正確: True
'0' -> TM: False, 預期: False, 正確: True
'1' -> TM: False, 預期: False, 正確: True

=== 測試：偶數長度回文 ===
'00' -> TM: True, 預期: True, 正確: True
'11' -> TM: True, 預期: True, 正確: True
'0110' -> TM: True, 預期: True, 正確: True
'1001' -> TM: True, 預期: True, 正確: True
'01' -> TM: False, 預期: False, 正確: True
'10' -> TM: False, 預期: False, 正確: True
'0011' -> TM: False, 預期: False, 正確: True
'0101' -> TM: False, 預期: False, 正確: True
```

## 語言層次與計算能力

```
正規語言          ← FSA/NFA/DFA
    ↓ (嚴格包含)
上下文無關語言     ← PDA
    ↓ (嚴格包含)
上下文有關語言     ← 線性有界自動機 (LBA)
    ↓ (嚴格包含)
遞歸可列舉語言     ← 圖靈機 (Turing Machine)
    ↓ (嚴格包含)
所有語言           ← 存在不可計算的語言
```

## 參考資料

- Turing, A. M. (1936). [On Computable Numbers, with an Application to the Entscheidungsproblem](https://doi.org/10.1112/plms/s2-42.1.230). *Proceedings of the London Mathematical Society*, 42, 230-265.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- Petzold, C. (2008). *The Annotated Turing: A Guided Tour Through Alan Turing's Historic Paper on Computability*. Wiley.
