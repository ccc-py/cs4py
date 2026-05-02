# Trie（前綴樹 / 字典樹）

## 歷史背景

Trie 這個名稱來自於 **re**<b>trie</b>val（檢索）一詞，由 Edward Fredkin 於 1960 年提出，後來由 René de la Briandais 和 Donald Knuth 等人進一步發展。Trie 是一種專門用於處理字串集合的樹狀資料結構，特別適合前綴相關的操作。

Trie 的應用非常廣泛，包括：
- **自動完成（Autocomplete）**：搜尋引擎和輸入法中的建議功能
- **拼字檢查（Spell Checker）**：檢查單字是否正確
- **IP 路由匹配**：最長前綴匹配
- **打字建議**：根據輸入前綴提供建議

## 結構說明

Trie 是一棵多叉樹，每個節點代表一個字元，從根節點到某個節點的路徑形成一個字串。

### 節點結構

```
TrieNode:
  - children: Dict[str, TrieNode]  # 子節點映射
  - is_end_of_word: bool           # 是否為單字結尾
  - frequency: int                 # 單字出現次數
```

### Trie 特性

1. **根節點為空**：不代表任何字元
2. **每條邊代表一個字元**：從父節點到子節點的邊上標記著一個字元
3. **路徑即字串**：從根到某節點的路徑形成一個字串
4. **標記結尾**：用 `is_end_of_word` 標記該節點是否為某個單字的結尾

### 視覺化範例

插入單字 "app", "apple", "apt" 後的 Trie 結構：

```
        (root)
        /    \
       a      ...
      /
     p
    / \
   p   t
  /     \
 e       (apt 結尾)
/
(apple 結尾)
```

## 操作複雜度

| 操作 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 插入 (insert) | O(m) | O(m) |
| 搜尋 (search) | O(m) | O(1) |
| 前綴匹配 (starts_with) | O(m) | O(1) |
| 取得前綴字串 (get_words_with_prefix) | O(m + k) | O(m + k) |

其中 m 是字串長度，k 是匹配的單字數量。

### 與其他資料結構比較

- **雜湊表（Hash Table）**：搜尋單字 O(1)，但無法高效處理前綴查詢
- **平衡二元搜尋樹**：搜尋 O(m log n)，同樣缺乏前綴查詢能力
- **Trie**：雖然空間開銷較大，但前綴查詢效率極高

## 使用範例

```python
from trie import Trie

# 建立 Trie
trie = Trie()

# 插入單字
words = ["apple", "app", "application", "apt", "banana"]
for word in words:
    trie.insert(word)

# 搜尋單字
print(trie.search("app"))      # True
print(trie.search("appl"))     # False

# 前綴匹配
print(trie.starts_with("app"))  # True
print(trie.starts_with("cat"))  # False

# 取得所有以某前綴開頭的單字
print(trie.get_words_with_prefix("app"))
# 輸出: ['app', 'apple', 'application']

# 單字頻率統計
trie.insert("apple")
trie.insert("apple")
print(trie.get_frequency("apple"))  # 3
```

## 參考資料

1. Fredkin, E. (1960). *Trie memory*. Communications of the ACM, 3(9), 490-499.
2. Knuth, D. E. (1997). *The Art of Computer Programming, Vol. 3: Sorting and Searching* (2nd ed.). Addison-Wesley.
3. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
4. [Trie - Wikipedia](https://en.wikipedia.org/wiki/Trie)
5. [Trie Data Structure - GeeksforGeeks](https://www.geeksforgeeks.org/trie-insert-search-delete/)
