# 簡易計算機語言 (Simple Calculator Language)

## 歷史背景

表達式求值是編譯器理論中最基礎的問題之一。1961 年 Edsger Dijkstra 提出了 shunting-yard 演算法，用於將中綴表達式轉換為後綴表示法。同年 Tony Hildebrandt 等人提出了遞迴下降解析器的概念，這成為現代編譯器前端最常用的解析方法之一。

從簡單的桌面計算機到複雜的腳本語言（Python、JavaScript），表達式求值器都是其核心組件。現代編譯器雖然使用更複雜的解析器生成工具（如 YACC、ANTLR），但遞迴下降解析器仍然是理解語法分析的最佳入門途徑。

## 核心原理

### 編譯器前端三階段

```
原始碼 → 詞法分析 → Token 序列 → 語法分析 → AST → 語義分析 → 結果
```

### 詞法分析（Tokenization）

將輸入字串分解為有意義的詞素（token）：

```
"3 + 4 * 2" → [NUMBER(3), PLUS, NUMBER(4), MUL, NUMBER(2), EOF]
```

詞法分析器識別：
- 數字：整數和浮點數
- 識別字：變數名、函數名
- 運算子：+, -, *, /, ^, (, )

### 語法分析（Parsing）

使用遞迴下降法，為每個優先順序級別建立一個函數：

```
expr    → term (('+' | '-') term)*       # 最低優先順序
term    → power (('*' | '/') power)*     # 中等優先順序
power   → unary ('^' unary)*             # 高優先順序，右結合
unary   → ('+' | '-') unary | call       # 一元運算
call    → primary ('(' args ')')?        # 函數呼叫
primary → NUMBER | IDENT | '(' expr ')'  # 基本元素
```

### 抽象語法樹（AST）

解析結果是一棵樹狀數據結構：

```
3 + 4 * 2
    → BinOp(+, Num(3), BinOp(*, Num(4), Num(2)))

     +
    / \
   3   *
      / \
     4   2
```

AST 保留了優先順序信息：乘法在加法之前計算。

### 語義分析（Evaluation）

遞迴遍歷 AST 計算值：
- NumberNode：返回值
- BinOpNode：遞迴計算左右子樹，應用運算子
- VarNode：查找變數
- FuncCallNode：呼叫函數

## 優先順序與結合性

| 運算子 | 優先順序 | 結合性 |
|--------|---------|--------|
| `()` | 最高 | N/A |
| `^` | 高 | 右結合 |
| `*` `/` | 中 | 左結合 |
| `+` `-` | 低 | 左結合 |

右結合意味著 `2 ^ 3 ^ 2` = `2 ^ (3 ^ 2)` = `2 ^ 9` = `512`

## 使用範例

```python
from calc.calculator import Calculator

calc = Calculator()

# 基本運算
calc.evaluate("3 + 4 * 2")        # => 11
calc.evaluate("(3 + 4) * 2")      # => 14
calc.evaluate("2 ^ 3 ^ 2")        # => 512

# 變數
calc.evaluate("x = 10")
calc.evaluate("x * 2 + 5")        # => 25

# 函數
calc.evaluate("sqrt(144)")        # => 12
calc.evaluate("sin(0)")           # => 0.0
```

## 參考資料

- Dijkstra, E. W. (1961). Making a Translator for ALGOL 60.
- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools.
- N. Wirth (1976). Algorithms + Data Structures = Programs.
