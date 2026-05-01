# 正規表達式轉 NFA（Thompson 構造法）

## 歷史背景

Thompson 構造法由 Ken Thompson 在 1968 年提出，用於將正規表達式轉換為 NFA。

### 重要里程碑

- **1968 年**：Ken Thompson 在 QED 編輯器中實作了第一個正規表達式引擎
- **Thompson 構造法**：將正規表達式的每個運算符轉換為對應的 NFA 模板
- **時間複雜度**：O(n)，其中 n 是正規表達式的長度

## 核心概念

### Thompson 構造法的三個基本模板

#### 1. 單一字元：`a`

```
→ (q0) --a--> (q1) →
```

#### 2. 聯集：`e1 | e2`

```
→ (start) --ε--> (NFA1 起始) → ... → (NFA1 接受) --ε--> (accept)
            `--ε--> (NFA2 起始) → ... → (NFA2 接受) --ε-->'
```

#### 3. 連接：`e1 e2`

```
→ (NFA1 起始) → ... → (NFA1 接受) --ε--> (NFA2 起始) → ... → (NFA2 接受) →
```

#### 4. Kleene 星號：`e*`

```
         ┌───────────────────────────────────────┐
         │                                       ▼
→ (start) --ε--> (NFA 起始) → ... → (NFA 接受) --ε--> (accept)
         │                                       │
         └───────────────ε───────────────────────┘
```

### NFAFragment 類別

為了簡化 Thompson 構造法的實作，我們使用 `NFAFragment` 來表示 NFA 的「片段」：

```python
class NFAFragment:
    def __init__(self, states, start_state, accept_states, transitions, alphabet):
        self.states = states              # 狀態集合
        self.start_state = start_state    # 起始狀態
        self.accept_states = accept_states  # 接受狀態集合
        self.transitions = transitions    # 轉移函數
        self.alphabet = alphabet         # 字母表
```

### 為什麼需要 Fragment？

在 Thompson 構造法中，我們需要：
1. 取得 NFA 的「入口」（起始狀態）
2. 取得 NFA 的「出口」（接受狀態）
3. 將多個 NFA「拼接」在一起

`NFAFragment` 封裝了這些資訊，使得拼接操作更簡單。

## 程式碼說明

### Thompson 構造函數

#### `thompson_concat(nfa1, nfa2)` - 連接運算

```python
# 從 nfa1 的接受狀態透過 ε-轉移到 nfa2 的起始狀態
for s in nfa1.accept_states:
    transitions[(s, '')].add(nfa2.start_state)

# 新 NFA 的起始態 = nfa1.start_state
# 新 NFA 的接受態 = nfa2.accept_states
```

#### `thompson_union(nfa1, nfa2)` - 聯集運算

```python
# 建立新起始態，透過 ε 到兩個 NFA 的起始態
transitions[(new_start, '')] = {nfa1.start_state, nfa2.start_state}

# 兩個 NFA 的接受態透過 ε 到新接受態
for s in nfa1.accept_states:
    transitions[(s, '')].add(new_accept)
```

#### `thompson_star(nfa)` - Kleene 星號

```python
# 新起始態透過 ε 到原起始態和新接受態（零次匹配）
transitions[(new_start, '')] = {nfa.start_state, new_accept}

# 原接受態透過 ε 到原起始態（循環）和新接受態
for s in nfa.accept_states:
    transitions[(s, '')].update({nfa.start_state, new_accept})
```

### RegexToNFA 解析器

使用遞迴下降法解析正規表達式：

- `_parse_expr`: 解析 `|` 運算（最低優先級）
- `_parse_term`: 解析連接運算（隱式）
- `_parse_factor`: 解析 `*` 運算（最高優先級）
- `_parse_primary`: 解析基本單元（字面、括號）

## 使用範例

```python
from theory.regex.nfa_builder import RegexToNFA

# 建立解析器
regex = RegexToNFA('a|b')

# 轉換為 NFA
nfa = regex.parse()

# 測試
print(nfa.accepts("a"))   # True
print(nfa.accepts("b"))   # True
print(nfa.accepts("c"))   # False

# 查看 NFA 資訊
print(f"狀態數: {len(nfa.states)}")
print(f"接受態: {nfa.accept_states}")
```

## 執行測試

```bash
python theory/regex/nfa_builder.py
```

輸出：
```
=== Thompson 構造法測試 ===

測試: 'ab' (連接)
  狀態數: 4
  起始態: q0_a
  接受態: {'q1_b'}
  'ab': True
  'a': False
  'b': False
  'aba': False

測試: 'a|b' (聯集)
  'a': True
  'b': True
  'c': False
  '': False

測試: 'a*' (Kleene 星號)
  '': True
  'a': True
  'aa': True
  'aaa': True
  'b': False
```

## Thompson 構造法的優點

1. **線性時間**：O(n) 構造
2. **保證 NFA 大小**：NFA 狀態數與正規表達式長度成線性關係
3. **簡單易懂**：每個運算符對應一個簡單的模板

## 參考資料

- Thompson, K. (1968). [Programming Techniques: Regular expression search algorithm](https://doi.org/10.1145/363347.363387). *Communications of the ACM*, 11(6), 419-422.
- Aho, A. V., Sethi, R., & Ullman, J. D. (1986). *Compilers: Principles, Techniques, and Tools*. Addison-Wesley.
- Cox, R. (2007). [Regular Expression Matching Can Be Simple And Fast](https://swtch.com/~rsc/regexp/regexp1.html).
