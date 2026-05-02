# 後綴樹 (Suffix Tree)

## 歷史背景

後綴樹是字串處理中最強大的資料結構之一，能在線性時間內解決許多複雜的字串問題。

### 發展歷程

- **1973 年**：Weiner 首次提出後綴樹
- **1976 年**：McCreight 提出改進的建構演算法
- **1995 年**：Ukkonen 提出簡化的線性時間演算法
- **現代應用**：DNA 序列分析、資料壓縮、搜尋引擎

## 演算法原理

### 後綴樹定義

```
給定字串 S（長度 n），後綴樹是：
- 一棵 Trie，包含所有後綴 S[i:]（i 從 0 到 n-1）
- 壓縮：將只有單一子節點的路徑壓縮為一條邊
- 時間複雜度建構：O(n)（使用 Ukkonen 演算法）
```

### 簡化版：後綴 Trie

```
不壓縮的版本（本實作）：
- 每個後綴插入到 Trie 中
- 時間複雜度：O(n²)
- 空間複雜度：O(n²)

適合教學用途，便於理解後綴樹的概念。
```

### Ukkonen 演算法（概念）

```
線性時間建構的關鍵：
1. 主動點（active point）：追蹤當前插入位置
2. 後綴連結（suffix link）：加速跳轉
3. 規則（Rule 1, 2, 3）：處理不同情況
4. 單次掃描：邊掃描邊擴展

時間複雜度：O(n)
```

## 程式碼說明

### 後綴 Trie 建構

```python
def build(self):
    n = len(text)
    for i in range(n):
        self._insert_suffix(i)

def _insert_suffix(self, start):
    node = self.root
    for i in range(start, len(text)):
        ch = text[i]
        if ch not in node.children:
            node.children[ch] = SuffixTrieNode()
        node = node.children[ch]
    node.is_end = True
```

### 搜尋模式

```python
def search(self, pattern):
    node = self.root
    for ch in pattern:
        if ch not in node.children:
            return False
        node = node.children[ch]
    return True  # 找到該模式
```

### 最長重複子字串

```python
def find_longest_repeated(self):
    # DFS 找最深的內部節點
    # 內部節點有多個分支，表示對應字串重複出現
    result = ""
    self._dfs_longest(self.root, "", ...)
    return result
```

## 應用場景

### 1. 子字串搜尋

```
在文字中搜尋模式，時間 O(m)（m 為模式長度）。
```

### 2. 最長公共子字串

```
給定兩個字串，找最長的公共子字串。
後綴樹中加入字串識別，找最深的共同節點。
```

### 3. DNA 序列分析

```
比較 DNA 序列，尋找重複片段或共同序列。
```

## 圖例

```
字串 "banana" 的後綴（簡化 Trie）：

        根
      /  |  \
     b   a   n   (後綴 "banana", "anana", "nana", ...)
    /    |
   a     n
  /      |
 n       a
...      ...

壓縮後的後綴樹會合併單一路徑。
```

## 問題比較

| 操作 | 後綴 Trie | 後綴樹 | 說明 |
|------|----------|--------|------|
| 建構 | O(n²) | O(n) | 後綴樹更快 |
| 搜尋 | O(m) | O(m) | 相同 |
| 空間 | O(n²) | O(n) | 後綴樹更省空間 |

## 參考資料

- Weiner, P. (1973). *Linear pattern matching algorithms*. IEEE Symposium on Switching and Automata Theory, 1-11.
- Ukkonen, E. (1995). *On-line construction of suffix trees*. Algorithmica, 14(3), 249-260.
- Gusfield, D. (1997). *Algorithms on Strings, Trees, and Sequences*. Cambridge University Press.
