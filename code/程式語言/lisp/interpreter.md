# Lisp 解譯器 (Minimal Lisp Interpreter)

## 歷史背景

Lisp 由 John McCarthy 於 1958 年在 MIT 發明，是僅次於 Fortran 的第二古老的高階程式語言。McCarthy 基於 Lambda 演算設計了 Lisp，使其成為第一個函數式程式語言。1960 年他發表了開創性論文「Recursive Functions of Symbolic Expressions and Their Computation by Machine」，展示了如何用七個核心形式（quote, atom, eq, car, cdr, cons, cond）實現一個完整的圖靈完備語言。

Lisp 的「同像性」（homoiconicity）——程式碼即數據——使其成為元程式設計和巨集系統的鼻祖，深刻影響了後續的語言設計。

## 核心原理

### S-Expression

Lisp 的核心數據結構是符號表達式（S-expression）：
- 原子：數字、符號
- 列表：`(A B C)` 可以是數據也可以是程式碼

### Eval/Apply 循環

Lisp 評估器的核心是兩個遞迴函數：

```
eval(expr, env):
  1. 如果是原子值：返回
  2. 如果是符號：在環境中查找
  3. 如果是引用：返回未評估的表達式
  4. 如果是列表：
     a. 特殊形式：if, define, lambda 等
     b. 一般呼叫：eval 第一個元素，eval 參數，apply

apply(func, args, env):
  1. 如果是內建函數：直接呼叫
  2. 如果是 Procedure：建立新環境，eval body
```

### 環境模型

環境是一個鏈式結構：
- 每個環境是一個幀（幀 = 變數名 → 值的映射）
- 每個幀指向一個外部環境
- 查找變數時沿鏈向上搜尋

### 閉包

閉包 = 函數代碼 + 定義時的環境：
```lisp
(define (make-adder n)
  (lambda (x) (+ x n)))
```
`make-adder` 返回的函數保留了 `n` 的值，即使 `make-adder` 已返回。

## 特殊形式

| 形式 | 語法 | 說明 |
|------|------|------|
| quote | `(quote x)` | 返回未評估的 x |
| if | `(if test then else)` | 條件分支 |
| define | `(define name value)` | 定義變數或函數 |
| set! | `(set! name value)` | 修改已定義變數 |
| lambda | `(lambda (params) body)` | 匿名函數 |
| begin | `(begin expr ...)` | 序列執行 |
| let | `(let ((name val) ...) body)` | 局部綁定 |
| cond | `(cond (test result) ... (else result))` | 多重條件 |

## 使用範例

```python
from lisp.interpreter import run, global_env

env = global_env()

# 基本運算
run("(+ 1 2 3)", env)  # => 6

# 定義函數
run("(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1)))))", env)
run("(factorial 5)", env)  # => 120

# 閉包
run("(define (make-adder n) (lambda (x) (+ x n)))", env)
run("(define add5 (make-adder 5))", env)
run("(add5 10)", env)  # => 15
```

## 參考資料

- McCarthy, J. (1960). Recursive Functions of Symbolic Expressions and Their Computation by Machine.
- Abelson, H., & Sussman, G. J. (1996). Structure and Interpretation of Computer Programs.
