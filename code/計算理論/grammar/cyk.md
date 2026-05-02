# CYK 演算法 (Cocke-Younger-Kasami Algorithm)

## 歷史背景

CYK 演算法是判定字串是否屬於上下文無關語言的經典演算法，由三位研究者獨立提出：

- **1965 年**：**John Cocke** 首次提出該演算法，作為他的編譯器優化研究的一部分
- **1967 年**：**Daniel H. Younger** 在博士論文中獨立重新發現
- **1967 年**：**Tadao Kasami** 也獨立提出了相同的演算法

因此該演算法被命名為 Cocke-Younger-Kasami (CYK) 演算法。它是動態規劃在編譯器語法分析中的早期應用之一。

## 核心原理

### Chomsky Normal Form (CNF)

CYK 演算法要求文法必須是 **Chomsky Normal Form (CNF)** 形式。CNF 的產生規則只能是以下三種：

1. **A → BC**：兩個非終端符號（二元規則）
2. **A → a**：單一終端符號（一元規則）
3. **S → ε**：只有起始符號可以有空產生

### CYK 演算法步驟

給定字串 w = a₁a₂...aₙ 和 CNF 形式的 CFG：

1. **建立表格**：建立一個 n × n 的表格 T，其中 T[i][j] 表示從位置 i 開始、長度為 j 的子字串可以由哪些非終端符號推導

2. **初始化**（長度為 1）：對於每個位置 i，找出能產生 aᵢ 的非終端符號 A（A → aᵢ）

3. **動態規劃**（長度 ≥ 2）：對於每個長度 l 和起始位置 i，嘗試所有分割點 k：
   - 如果 T[i][k] 包含 B，且 T[i+k][l-k] 包含 C
   - 且存在規則 A → BC
   - 則將 A 加入 T[i][l]

4. **判定**：檢查起始符號 S 是否在 T[0][n] 中

### 時間複雜度

CYK 演算法的時間複雜度為 **O(n³)**，其中 n 是字串長度。

## 使用範例

```python
from cyk import cyk, create_grammar_anbn, create_grammar_balanced_parens

# 測試 {a^n b^n} 文法
grammar = create_grammar_anbn()
test_cases = ["", "ab", "aabb", "abab", "aaabbb", "aab"]
for s in test_cases:
    result = cyk(s, grammar)
    print(f"  '{s}': {result}")

# 測試平衡括號文法
grammar = create_grammar_balanced_parens()
test_cases = ["", "()", "(())", "()()", "(()", "())"]
for s in test_cases:
    result = cyk(s, grammar)
    print(f"  '{s}': {result}")
```

### CNF 轉換範例

原始文法（平衡括號）：
```
S → (S)S | ε
```

轉換為 CNF：
```
S → AB | ε
A → (
B → SB2
B2 → )
```

## 參考資料

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.

2. Younger, D. H. (1967). *Recognition and parsing of context-free languages in time n³*. Information and Control, 10(2), 189-208.

3. Kasami, T. (1965). *An efficient recognition and syntax-analysis algorithm for context-free languages*. Scientific Report AFCRL-65-758, Air Force Cambridge Research Lab.

4. Cocke, J., & Schwartz, J. T. (1970). *Programming languages and their compilers*. Courant Institute of Mathematical Sciences, New York University.
