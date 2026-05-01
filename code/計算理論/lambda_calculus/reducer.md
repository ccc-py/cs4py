# Lambda 演算化簡器 (Lambda Calculus Reducer)

## 歷史背景

Lambda 演算的化簡（reduction）是函數式程式設計的核心概念。

### 重要里程碑

- **1930 年代**：Alonzo Church 提出 β-化簡規則
- **1936 年**：Church 和 Rosser 證明化簡的收斂性（Church-Rosser 定理）
- **1970 年代**：Lambda 演算成為函數式語言（如 Lisp, ML, Haskell）的理論基礎

## 核心概念

### β-化簡 (Beta Reduction)

β-化簡是 Lambda 演算中唯一的計算規則：

```
(λx.M) N → M[x := N]
```

意思是：將函數體 M 中所有的自由變數 x 替換為 N。

### 範例

| 化簡前 | 化簡後 | 說明 |
|--------|--------|------|
| `(λx.x) y` | `y` | 恆等函數應用 |
| `(λx.λy.x) a b` | `a` | 常數函數應用 |
| `(λf.λx.f (f x)) s z` | `s (s z)` | Church 數 2 應用 |

### Church-Rosser 定理

> 如果一個 Lambda 項可以化簡為兩個不同的項，那麼存在一個項可以同時從這兩個項化簡而來。

**推論**：化簡順序不影響最終結果（如果存在正規型 normal form）。

## 程式碼說明

### 主要函數

#### `beta_reduce(term)` - 單步化簡

使用**最左最外**策略（對應非嚴格求值）：

```python
elif isinstance(term, Application):
    # 檢查是否為 redex (λx.M) N
    if isinstance(term.func, Abstraction):
        # 進行 β-化簡
        func = term.func
        arg = term.arg
        new_term = substitute(func.body, func.param, arg)
        return new_term, True
```

#### `substitute(term, var, value)` - 替換

將 term 中的自由變數 var 替換為 value：

**關鍵：避免變數捕捉 (variable capture)**

```python
elif isinstance(term, Abstraction):
    if term.param == var:
        # var 被綁定，不替換
        return term
    else:
        # 檢查變數捕捉
        if term.param in free_variables(value):
            # 需要 α-轉換
            new_param = fresh_variable(value, term.param)
            ...
```

#### `reduce(term, max_steps)` - 完全化簡

反覆進行 β-化簡直到無法化簡（達到正規型）：

```python
while steps < max_steps:
    new_term, reduced = beta_reduce(current)
    if not reduced:
        break
    current = new_term
```

### 變數捕捉問題

**什麼是變數捕捉？**

```python
(λx.λy.x) y
→ (λy.y)  # 錯誤！原本的 y 應該是自由的，卻變成了綁定的
```

**正確做法：α-轉換**

```python
(λx.λy.x) y
→ 先 α-轉換：λx.λz.x（將 y 改為 z）
→ (λz.x)[x := y]
→ λz.y  # 正確！
```

## 使用範例

```python
from theory.lambda_calculus.parser import parse_lambda
from theory.lambda_calculus.reducer import reduce, reduce_and_trace

# 化簡恆等函數應用
expr = parse_lambda("(λx.x) y")
result = reduce(expr)
print(result)  # y

# 化簡常數函數
expr = parse_lambda("(λx.λy.x) a b")
result = reduce(expr)
print(result)  # a

# 追蹤化簡過程
expr = parse_lambda("(λx.λy.x y) a b")
print("化簡過程：")
for step, before, after in reduce_and_trace(expr):
    print(f"  步驟 {step}: {before} → {after}")
```

## 執行測試

```bash
python theory/lambda_calculus/reducer.py
```

輸出：
```
=== Lambda 演算化簡器測試 ===

測試：恆等函數 (λx.x) y
  原始: (λx.x) y
  化簡: y

測試：常數函數 (λx.λy.x) a b
  原始: (λx.λy.x) a b
  化簡: a

測試：追蹤化簡過程 (λx.λy.x y) a b
  原始: λx.λy.x y
  步驟 1: (λx.λy.x y) a → λy.a y
  步驟 2: (λy.a y) b → a b

測試：Church 數 2 (λf.λx.f (f x)) 應用於 s 和 z
  原始: (λf.λx.f (f x)) s z
  化簡: s (s z)

測試：自由變數
  'λx.x y' 的自由變數: {'y'}
```

## 化簡策略比較

| 策略 | 說明 | 對應程式語言 |
|------|------|-------------|
| 最左最外 (Normal Order) | 總是先化簡最外層 | Lazy evaluation (Haskell) |
| 最左最內 (Applicative Order) | 總是先化簡最內層 | Eager evaluation (Python, C) |

## 參考資料

- Church, A. (1936). [An unsolvable problem of elementary number theory](https://doi.org/10.2307/2371045). *American Journal of Mathematics*, 58(2), 345-363.
- Barendregt, H. P. (1984). *The Lambda Calculus: Its Syntax and Semantics* (2nd ed.). North-Holland.
- Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press.
- Sussman, G. J., & Wisdom, J. (2013). *Functional Programming in Scheme*. MIT Press.
