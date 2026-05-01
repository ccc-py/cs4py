# Lambda 演算解析器 (Lambda Calculus Parser)

## 歷史背景

Lambda 演算 (Lambda Calculus) 由 Alonzo Church 在 1930 年代提出，是計算理論的兩大支柱之一（另一個是圖靈機）。

### 重要里程碑

- **1930 年代**：Alonzo Church 提出 Lambda 演算
- **1936 年**：Alan Turing 證明 Lambda 演算與圖靈機等價（Church-Turing Thesis）
- **1958 年**：John McCarthy 基於 Lambda 演算設計了 Lisp 語言
- **1970 年代**：Lambda 演算成為函數式程式設計的理論基礎

## 核心概念

### Lambda 演算的語法

Lambda 項 (Lambda Term) 由三種形式組成：

1. **變數 (Variable)**：`x`, `y`, `z` 等
2. **抽象 (Abstraction)**：`λx.M`
   - 表示一個函數，參數為 `x`，函數體為 `M`
   - 類似於其他語言中的 `lambda x: M` 或 `function(x) { return M; }`
3. **應用 (Application)**：`M N`
   - 將函數 `M` 應用於參數 `N`
   - 類似於其他語言中的 `M(N)`

### 範例

| Lambda 表達式 | 意義 |
|---------------|------|
| `λx.x`        | 恆等函數 (Identity function) |
| `λx.λy.x`     | 常數函數 (K combinator) |
| `λf.λx.f (f x)` | 將函數應用兩次 (Church 數 2) |

### 變數綁定

在 `λx.M` 中：
- `x` 是**綁定變數** (bound variable)
- `M` 是函數體
- 如果 `M` 中出現 `x`，則它表示參數 `x`

## 程式碼說明

### LambdaTerm 類別層次

`parser.py` 定義了 Lambda 項的抽象語法樹 (AST)：

```python
LambdaTerm (基礎類別)
├── Variable      # 變數
├── Abstraction   # 抽象 (λx.M)
└── Application   # 應用 (M N)
```

### 各類別說明

#### Variable（變數）

```python
class Variable(LambdaTerm):
    def __init__(self, name: str):
        self.name = name
```

表示一個變數，如 `x`、`y`。

#### Abstraction（抽象）

```python
class Abstraction(LambdaTerm):
    def __init__(self, param: str, body: LambdaTerm):
        self.param = param
        self.body = body
```

表示一個函數定義，如 `λx.x`。

#### Application（應用）

```python
class Application(LambdaTerm):
    def __init__(self, func: LambdaTerm, arg: LambdaTerm):
        self.func = func
        self.arg = arg
```

表示函數呼叫，如 `(λx.x) y`。

### LambdaParser 解析器

使用遞迴下降法解析 Lambda 表達式：

**語法規則**：
```
expr    ::= term expr'          # 應用（左結合）
expr'   ::= term expr' | ε
term    ::= variable | abstraction | '(' expr ')'
variable ::= [a-zA-Z][a-zA-Z0-9]*
abstraction ::= 'λ' variable '.' expr
```

**關鍵方法**：
- `_parse_expr`: 解析表達式（處理應用）
- `_parse_term`: 解析項（處理變數、抽象、括號）
- `_parse_variable`: 解析變數
- `_parse_abstraction`: 解析抽象

## 使用範例

```python
from theory.lambda_calculus.parser import parse_lambda

# 解析變數
expr = parse_lambda("x")
print(expr)  # x

# 解析抽象（函數定義）
expr = parse_lambda("λx.x")
print(expr)  # λx.x

# 解析應用（函數呼叫）
expr = parse_lambda("(λx.x) y")
print(expr)  # (λx.x) y

# 解析巢狀抽象
expr = parse_lambda("λx.λy.x y")
print(expr)  # λx.λy.x y

# 查看 AST 結構
print(repr(expr))
# Abs(x, Var(x)) 或類似結構
```

## 執行測試

```bash
python theory/lambda_calculus/parser.py
```

輸出：
```
=== Lambda 演算解析器測試 ===

測試：變數
  'x' -> x
  類型: Variable

測試：抽象 (λx.x)
  'λx.x' -> λx.x
  類型: Abstraction

測試：應用 ((λx.x) y)
  '(λx.x) y' -> (λx.x) y
  類型: Application

測試：複雜表達式 (λx.λy.x y)
  'λx.λy.x y' -> λx.λy.x y
  repr: Abs(x, Abs(y, App(Var(x), Var(y))))

測試：使用 \ 代替 λ
  '\x.x' -> λx.x

測試：巢狀抽象 (λx.λy.λz.x (y z))
  'λx.λy.λz.x (y z)' -> λx.λy.λz.x (y z)
  repr: Abs(x, Abs(y, Abs(z, App(Var(x), App(Var(y), Var(z))))))
```

## Lambda 演算的計算

解析只是第一步，後續需要：
1. **化簡 (Reduction)**：透過 β-化簡計算 Lambda 項
2. **編碼 (Encoding)**：用 Lambda 演算表示數字、布林值、資料結構

## 參考資料

- Church, A. (1936). [An unsolvable problem of elementary number theory](https://doi.org/10.2307/2371045). *American Journal of Mathematics*, 58(2), 345-363.
- Barendregt, H. P. (1984). *The Lambda Calculus: Its Syntax and Semantics* (2nd ed.). North-Holland.
- Pierce, B. C. (2002). *Types and Programming Languages*. MIT Press.
- Sussman, G. J., & Wisdom, J. (2013). *Functional Programming in Scheme*. MIT Press.
