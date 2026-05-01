# 停機問題 (Halting Problem)

## 歷史背景

停機問題 (Halting Problem) 是計算理論中最著名的不可判定問題。

### 重要里程碑

- **1936 年**：Alan Turing 證明停機問題不可判定
- **這是第一個被證明不可判定的問題**
- **隨後**：基於停機問題，可以證明許多其他問題也不可判定

## 核心概念

### 問題描述

> 給定一個程式 P 和輸入 I，是否存在一個演算法能判定 P 在執行於 I 時是否會最終停機？

### Turing 的證明（反證法）

1. **假設**存在一個停機判定器 `halts(P, I)` 可以正確判定任何程式 P 在輸入 I 時是否會停機。

2. **構造**一個悖論程式：

```python
def paradox_program(f):
    if halts(f, f):  # 如果 halts 說我會停機
        while True: pass  # 我就無限循環（不會停機）
    else:  # 如果 halts 說我不會停機
        return  # 我就停機
```

3. **考慮** `paradox_program(paradox_program)`：
   - 如果 `halts` 返回 `True`（會停機）→ `paradox_program` 進入無限循環 → **矛盾！**
   - 如果 `halts` 返回 `False`（不會停機）→ `paradox_program` 停機 → **矛盾！**

4. **結論**：`halts` 不可能存在。停機問題不可判定。

### 自我指涉

這個證明的關鍵是**自我指涉**（類似羅素悖論、李文海謬論）：
- 程式檢查自己的行為
- 然後做出相反的動作
- 產生無法解決的矛盾

## 程式碼說明

### `demonstrate_paradox()` - 演示悖論

展示 Turing 證明的邏輯，但不實際執行（因為會無限循環或崩潰）。

### `simple_halting_examples()` - 簡單例子

展示一些我們**可以手動分析**的程式：

| 程式 | 是否停機 | 說明 |
|------|----------|------|
| `return 1+1` | ✓ 會 | 簡單計算 |
| `for i in range(10): pass` | ✓ 會 | 有限迴圈 |
| `while True: pass` | ✗ 不會 | 無限迴圈 |
| Collatz 函數 | ? 未知 | 數學未解問題 |

### Collatz 猜想

```python
def collatz(n):
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
```

**猜想**：對於所有正整數 n，這個程式最終都會停機（到達 n=1）。

**狀態**：對所有測試過的 n（高達 2⁶⁸）都會停機，但尚未找到數學證明！

## 使用範例

```python
from theory.computability.halting import demonstrate_paradox, rice_theorem_simple

# 演示停機問題悖論
demonstrate_paradox()

# 了解 Rice 定理
rice_theorem_simple()
```

## 執行測試

```bash
python theory/computability/halting.py
```

輸出：
```
=== 停機問題悖論演示 ===

假設存在一個停機判定器 halts(program, input)
它應該能正確判定任意程式是否會停機。

現在構造一個悖論程式：

def paradox_program(f):
    if halts(f, f):
        while True: pass  # 無限循環
    else:
        return  # 停機

考慮 paradox_program(paradox_program)：

情況 1: 如果 halts 說它會停機 → 它進入無限循環 → 矛盾！
情況 2: 如果 halts 說它不會停機 → 它停機 → 矛盾！

結論：halts 不可能存在。停機問題不可判定。

這就是 Turing 的證明！

==================================================

=== 簡單程式的停機分析 ===

程式 1: def program1(): return 1 + 1
結果: 會停機 ✓

程式 2: def program2(): for i in range(10): pass
結果: 會停機 ✓

程式 3: def program3(): while True: pass
結果: 不會停機 (無限迴圈)

程式 4: Collatz 猜想
  def program4(n):
      while n != 1:
          if n % 2 ==0: n = n // 2
          else: n = 3 * n + 1
結果: 對於所有測試過的 n 都會停機，但尚未證明！
      （這就是著名的 Collatz 猜想）

==================================================

=== Rice 定理 ===

Rice 定理：任何關於程式行為的非平凡性質都是不可判定的。

例子：
  - 「程式是否會停機？」→ 不可判定
  - 「程式是否輸出 0？」→ 不可判定
  - 「程式是否會崩潰？」→ 不可判定

但這些是可判定的：
  - 「程式碼是否有語法錯誤？」→ 可判定（語法分析）
  - 「程式是否使用變數 x？」→ 可判定（程式分析）
```

## Rice 定理

> 任何關於程式**行為**的非平凡性質都是不可判定的。

**非平凡**：不是所有程式都有，也不是所有程式都沒有的性質。

**關於程式行為**：只看程式的輸入輸出行為，不看實作細節。

### 推論

從停機問題的不可判定性，可以推出許多其他問題也不可判定：
- 程式是否會輸出 0？
- 兩個程式是否等價？
- 程式是否會崩潰？
- 程式是否會進入某個特定狀態？

## 參考資料

- Turing, A. M. (1936). [On Computable Numbers, with an Application to the Entscheidungsproblem](https://doi.org/10.1112/plms/s2-42.1.230). *Proceedings of the London Mathematical Society*, 42, 230-265.
- Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
- Lynch, N. (1996). *Distributed Algorithms*. Morgan Kaufmann.
