# 哥德尔数编码 (Gödel Numbering)

## 歷史背景

哥德尔数 (Gödel Numbering) 是哥德尔在 1931 年提出的关键技术。

### 重要里程碑

- **1931 年**：Gödel 使用哥德尔数证明不完备定理
- **核心想法**：将形式系统「算术化」
- **意义**：允许在算术中「谈论」符号、公式、证明

## 核心概念

### 编码方法

#### 1. 符号编码

先给每个基本符号分配一个自然数：

| 符号 | 编码 |
|------|------|
| 0    | 1    |
| s    | 2    |
| +    | 3    |
| ×    | 4    |
| =    | 5    |
| (    | 6    |
| )    | 7    |
| x    | 8    |
| '    | 9    |
| ¬    | 10   |
| →    | 11   |

#### 2. 公式编码

公式 = 符号序列 s₁s₂...sₙ

哥德尔数 = 2^code(s₁) × 3^code(s₂) × ... × pₙ^code(sₙ)

**例子**：公式「0 = 0」
- 符号：0, =, 0
- 编码：2¹ × 3⁵ × 5¹ = 2 × 243 × 5 = 2430

#### 3. 证明编码

证明 = 公式序列 [g₁, g₂, ..., gₖ]

证明的哥德尔数 = 2^g₁ × 3^g₂ × ... × pₖ^gₖ

**关键**：每个证明都有唯一的哥德尔数！

## 程式碼說明

### 主要函數

#### `formula_to_godel(formula)` - 公式编码

```python
def formula_to_godel(formula):
    godel_num = 1
    for i, symbol in enumerate(formula):
        prime = nth_prime(i)
        code = symbol_to_code(symbol)
        godel_num *= prime ** code
    return godel_num
```

**技巧**：第 i 个符号用第 i 个质数来编码。

#### `godel_to_formula(godel_num)` - 公式解码

通过质因数分解还原符号序列。

#### `proof_to_godel(proof)` - 证明编码

将整个证明（公式序列）编码为一个数字。

### 质因数分解

哥德尔数完全由质因数分解决定：
- 指数 = 符号的编码
- 底数 = 第 i 个质数

## 使用範例

```python
from theory.computability.godel_number import formula_to_godel, godel_to_formula

# 编码公式「0 = 0」
formula = ['0', '=', '0']
godel_num = formula_to_godel(formula)
print(godel_num)  # 2430

# 解码回来
decoded = godel_to_formula(godel_num)
print(decoded)  # ['0', '=', '0']
```

## 執行測試

```bash
python theory/computability/godel_number.py
```

輸出：
```
=== 哥德尔数编码演示 ===

公式：「0 = 0」
  符号序列：['0', '=', '0']
  哥德尔数：2430
  质因数分解：p0^1 × p1^5 × p2^1

  解码回来：['0', '=', '0']
  是否相同：True

公式：「s(0) + 0 = s(0)」
  符号序列：['s', '(', '0', ')', '+', '0', '=', 's', '(', '0', ')']
  哥德尔数：很大...
  质因数分解：p0^2 × p1^6 × p2^1 × p3^7 × ...

  解码回来：['s', '(', '0', ')', '+', '0', '=', 's', '(', '0', ')']
  是否相同：True

证明：[「0=0」, 「s(0)=s(0)」]
  证明的哥德尔数：很大...

  解码回来：[['0', '=', '0'], ['s', '(', '0', ')', '=', 's', '(', '0', ')']]

============================================================

=== 符号编码表 ===

  '0' → 1
  's' → 2
  '+' → 3
  '×' → 4
  '=' → 5
  '(' → 6
  ')' → 7
  'x' → 8
  "'" → 9
  '¬' → 10
  '→' → 11
  '∀' → 12
  '∃' → 13
  ',' → 14
  '⊢' → 15
```

## 哥德尔数的意义

1. **算术化**：将形式系统转化为算术命题
2. **自指**：允许构造「本命题不可证明」这样的命题
3. **不完备定理的基础**：G ↔ ¬Proof_S(⌈G⌉)

## 參考資料

- Gödel, K. (1931). [Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I](https://doi.org/10.1007/BF01700692). *Monatshefte für Mathematik und Physik*, 38, 173-198.
- Nagel, E., & Newman, J. R. (1958). *Gödel's Proof*. New York University Press.
- Smullyan, R. M. (1992). *Gödel's Incompleteness Theorems*. Oxford University Press.
- Hofstadter, D. R. (1979). *Gödel, Escher, Bach: An Eternal Golden Braid*. Basic Books.
