# 正規表達式引擎（從頭實作）

## 歷史背景

正規表達式 (Regular Expression) 是計算機科學中最廣泛使用的模式匹配工具之一。

### 重要里程碑

- **1951 年**：Stephen Kleene 提出正規表達式，用於描述正規語言
- **1968 年**：Ken Thompson 在 QED 編輯器中實作了第一個正規表達式引擎（使用 Thompson 構造法）
- **1980 年代**：Henry Spencer 實作了更高效的引擎（使用 DFA 方法）
- **1997 年**：Philip Hazel 開發 PCRE (Perl Compatible Regular Expressions)

### Thompson 構造法

Ken Thompson 在 1968 年提出將正規表達式轉換為 NFA 的方法：
- 基本字元 → 兩個狀態的 NFA
- 聯集 (|) → ε-轉移合併
- 連接 (concatenation) → 接受態連到起始態
- Kleene 星號 (*) → 添加循環 ε-轉移

## 核心概念

### 正規表達式的語法

本實作支援：
- **字面字元**：`a`, `b`, `0`, `1` 等（匹配自身）
- **點號 `.`**：匹配任意單一字元
- **星號 `*`**：零次或多次（Kleene 星號）
- **豎線 `|`**：或 (alternation)
- **括號 `()`**：分組
- **反斜線 `\`**：跳脫字元

### 編譯流程

```
正規表達式字串
    ↓ (解析)
抽象語法樹 (AST)
    ↓ (Thompson 構造法)
NFA (非確定性有限狀態自動機)
    ↓ (模擬執行)
匹配結果
```

### 為什麼使用 NFA？

- **靈活**：容易支援擴展語法
- **直觀**：Thompson 構造法簡單易懂
- **記憶體效率**：通常比 DFA 小

缺點：最壞情況可能是指數時間（但實務上很少遇到）

## 程式碼說明

### RegexParser 類別

`engine.py` 中的 `RegexParser` 將正規表達式字串解析為 NFA：

**解析順序**（運算符優先級從低到高）：
1. `|` (聯集) - 最低優先級
2. 連接 (concatenation) - 隱式
3. `*` (Kleene 星號) - 最高優先級

**關鍵方法**：
- `_parse_expr`: 解析由 `|` 分隔的運算式
- `_parse_term`: 解析連接的項
- `_parse_factor`: 解析帶 `*` 的因子
- `_parse_primary`: 解析基本單元（字面、分組、跳脫）

### NFA 構造方法

#### 1. 字面字元：`a`
```
→ (q0) --a--> (q1) →
```

#### 2. 聯集：`a|b`
```
→ (start) --ε--> (q0) --a--> (q1) --ε--> (accept)
            `--ε--> (q2) --b--> (q3) --ε-->'
```

#### 3. 連接：`ab`
```
→ (q0) --a--> (q1) --ε--> (q2) --b--> (q3) →
```

#### 4. Kleene 星號：`a*`
```
→ (start) --ε--> (q0) --a--> (q1) --ε--> (accept)
     ↑                                    ↓
     └───────────────ε───────────────────┘
     └───────────────ε───────────────────┘
```

### RegexEngine 類別

封裝正規表達式引擎：
- `__init__`: 解析 pattern 並建立 NFA
- `match`: 檢查整個字串是否匹配
- `search`: 搜尋字串中是否有子串匹配

## 使用範例

```python
from theory.regex.engine import RegexEngine

# 建立引擎
engine = RegexEngine('a*')

# 匹配
print(engine.match(""))      # True (零個 a)
print(engine.match("a"))     # True
print(engine.match("aaa"))   # True
print(engine.match("b"))     # False

# 搜尋
engine2 = RegexEngine('ab')
print(engine2.search("xabx"))  # True
print(engine2.search("xax"))   # False
```

## 執行測試

```bash
python theory/regex/engine.py
```

輸出：
```
=== 正規表達式引擎測試 ===

測試: 'a*' (零個或多個 a)
  '': True
  'a': True
  'aa': True
  'aaa': True
  'b': False
  'ab': False

測試: 'a|b' (a 或 b)
  'a': True
  'b': True
  'c': False
  'ab': False
  '': False

測試: 'ab*' (a 後接零個或多個 b)
  '': False
  'a': True
  'ab': True
  'abb': True
  'aba': False
```

## 與 Python re 模組的比較

| 特性 | 本實作 | Python re |
|------|--------|-----------|
| 實作方式 | NFA (Thompson) | 未知（通常是 VM） |
| 支援語法 | 基本 | 非常完整 |
| 回溯 | 無（NFA 模擬） | 有（可能指數時間） |
| 教學價值 | 高 | 低 |

## 參考資料

- Thompson, K. (1968). [Programming Techniques: Regular expression search algorithm](https://doi.org/10.1145/363347.363387). *Communications of the ACM*, 11(6), 419-422.
- Kleene, S. C. (1951). Representation of events in nerve nets and finite automata. In *Automata Studies* (pp. 3-41). Princeton University Press.
- Friedl, J. E. (2006). *Mastering Regular Expressions* (3rd ed.). O'Reilly Media.
