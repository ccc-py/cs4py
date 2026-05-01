# Lambda 演算編碼 (Church Encoding)

## 歷史背景

Church 編碼 (Church Encoding) 由 Alonzo Church 在 1930 年代提出，展示了如何只用 Lambda 演算表示各種資料型態。

### 重要里程碑

- **1930 年代**：Church 提出用 Lambda 項表示數字、布林值等
- **1936 年**：Church 使用 Lambda 演算證明 Entscheidungsproblem 不可判定
- **Y Combinator**：由 Haskell Curry 發現，用於在無遞迴定義的語言中實作遞迴

## 核心概念

### Church 數字 (Church Numerals)

將自然數表示為函數應用的次數：

```
0 = λf.λx.x
1 = λf.λx.f x
2 = λf.λx.f (f x)
3 = λf.λx.f (f (f x))
...
n = λf.λx.f^n x
```

**直覺**：數字 n 是一個函數，接受 f 和 x，將 f 應用於 x 共 n 次。

### Church 布林值 (Church Booleans)

```
True  = λx.λy.x  (選擇第一個)
False = λx.λy.y  (選擇第二個)
```

**直覺**：布林值是一個二元選擇函數，True 選第一個參數，False 選第二個。

### Church 有序對 (Church Pairs)

```
Pair = λx.λy.λf.f x y
First = λp.p (λx.λy.x)
Second = λp.p (λx.λy.y)
```

**直覺**：有序對是一個函數，接受一個「選擇函數」f，並將兩個元素傳給 f。

## 程式碼說明

### Church 數字操作

#### 後繼函數 (Succ)

```python
def church_succ():
    """λn.λf.λx.f ((n f) x)"""
```

將 n 加 1：對 f 多做一次應用。

#### 加法 (Add)

```python
def church_add():
    """λm.λn.λf.λx.((m f) ((n f) x))"""
```

m + n：將 f 應用 m+n 次。

#### 乘法 (Mult)

```python
def church_mult():
    """λm.λn.λf.m (n f)"""
```

m × n：f 被應用 m×n 次。

### Y Combinator

```python
def y_combinator():
    """λf.(λx.f (x x)) (λx.f (x x))"""
```

**用途**：在無遞迴定義的語言中實作遞迴。

**原理**：Y f = f (Y f)，所以 Y 可以無限展開。

### 布林值操作

#### And

```python
def church_and():
    """λp.λq.p q p"""
```

- 如果 p 是 True：p q p = q（結果由 q 決定）
- 如果 p 是 False：p q p = p = False

#### Or

```python
def church_or():
    """λp.λq.p p q"""
```

- 如果 p 是 True：p p q = p = True
- 如果 p 是 False：p p q = q（結果由 q 決定）

## 使用範例

```python
from theory.lambda_calculus.encoder import (
    church_zero, church_one, church_two,
    church_succ, church_add, church_mult,
    church_true, church_false,
    y_combinator, reduce
)

# Church 數字
zero = church_zero()
one = church_one()
two = church_two()

# 後繼：succ zero = one
succ = church_succ()
result = reduce(Application(succ, zero))
print(result)  # λf.λx.f x (即 one)

# 加法：1 + 2 = 3
add = church_add()
one_plus_two = Application(Application(add, one), two)
result = reduce(one_plus_two)

# 布林值
true_val = church_true()
false_val = church_false()

# Y Combinator
y = y_combinator()
print(y)  # λf.(λx.f (x x)) (λx.f (x x))
```

## 執行測試

```bash
python theory/lambda_calculus/encoder.py
```

輸出：
```
=== Church 編碼測試 ===

測試：Church 數字
  Zero: λf.λx.x
  One: λf.λx.f x
  Two: λf.λx.f (f x)

測試：後繼函數
  succ zero: λf.λx.f x
  預期: λf.λx.f x
  是否相同: True

測試：加法
  1 + 2 = λf.λx.f (f (f x))

測試：乘法
  2 * 3 = λf.λx.f (f (f (f (f (f x)))))

測試：Church 布林值
  True: λx.λy.x
  False: λx.λy.y

測試：Church 有序對
  first (pair 3 5) = λf.λx.f (f (f x))

測試：Y Combinator
  Y = λf.(λx.f (x x)) (λx.f (x x))
  (Y 可以用於實作遞迴)
```

## Church 數字的運算

| 運算 | Lambda 項 | 說明 |
|------|-----------|------|
| 0 | `λf.λx.x` | 零次應用 |
| 1 | `λf.λx.f x` | 一次應用 |
| Succ | `λn.λf.λx.f ((n f) x)` | 後繼 |
| Add | `λm.λn.λf.λx.((m f) ((n f) x))` | 加法 |
| Mult | `λm.λn.λf.m (n f)` | 乘法 |

## 參考資料

- Church, A. (1936). [An unsolvable problem of elementary number theory](https://doi.org/10.2307/2371045). *American Journal of Mathematics*, 58(2), 345-363.
- Barendregt, H. P. (1984). *The Lambda Calculus: Its Syntax and Semantics* (2nd ed.). North-Holland.
- Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press.
- Vanier, J. (2015). [The Y Combinator (Slight Return)](https://mvanier.livejournal.com/2897.html).
