# 上下文無關文法 (Context-Free Grammar, CFG)

## 歷史背景

上下文無關文法由**諾姆·喬姆斯基 (Noam Chomsky)** 於 1956 年提出，作為其變換生成文法 (Transformational-Generative Grammar) 理論的一部分。喬姆斯基將文法分為四個層次（喬姆斯基譜系），其中上下文無關文法對應於 Type-2 文法。

在 1960 年代，CFG 成為描述程式語言語法的標準工具。**巴科斯-諾爾范式 (Backus-Naur Form, BNF)** 就是 CFG 的一種表示法，由 John Backus 和 Peter Naur 在描述 ALGOL 60 語言時提出。

## 核心原理

上下文無關文法是一個**四元組** G = (V, Σ, R, S)：

- **V (非終端符號集合)**：也稱為變數，通常表示語法類別（如 S, A, E, T 等）
- **Σ (終端符號集合)**：字母表，實際出現在字串中的符號
- **R (產生規則集合)**：形式為 A → α，其中 A ∈ V，α ∈ (V ∪ Σ)*
- **S (起始符號)**：S ∈ V，推導的起點

### 推導 (Derivation)

從起始符號 S 開始，反覆應用產生規則，將非終端符號替換為其定義，最終得到只包含終端符號的字串。

```
S ⇒ aSb ⇒ aaSbb ⇒ aabb
```

### 範例文法

**平衡括號文法：**
```
S → (S)S | ε
```

**{aⁿbⁿ | n ≥ 0} 文法：**
```
S → aSb | ε
```

**簡單算術表達式文法：**
```
E → E + T | T
T → T * F | F
F → (E) | number
```

## 使用範例

```python
from cfg import CFG, create_grammar_anbn, create_grammar_balanced_parens

# 建立 {a^n b^n} 文法
cfg = create_grammar_anbn()
print(f"非終端符號: {cfg.nonterminals}")
print(f"終端符號: {cfg.terminals}")

# 檢查字串是否屬於語言
test_cases = ["", "ab", "aabb", "abab", "aaabbb"]
for s in test_cases:
    result = cfg.is_in_language(s)
    print(f"  '{s}': {result}")

# 建立平衡括號文法並生成字串
cfg = create_grammar_balanced_parens()
strings = cfg.generate(max_depth=5)
for s in set(strings):
    if s:
        print(f"  生成: '{s}'")
```

## 參考資料

1. Chomsky, N. (1956). *Three models for the description of language*. IRE Transactions on Information Theory, 2(3), 113-124.

2. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.

3. Backus, J. W. (1959). *The syntax and semantics of the proposed international algebraic language of the Zurich ACM-GAMM Conference*. Proceedings of the International Conference on Information Processing.
