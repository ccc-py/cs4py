# Rabin-Karp 字串匹配演算法

## 歷史背景

Rabin-Karp 演算法由 Michael O. Rabin 和 Richard M. Karp 於 1987 年發表，是一種基於雜湊（Hash）技術的字串匹配演算法。與 KMP 或 Boyer-Moore 等演算法不同，Rabin-Karp 的核心思想是將字串視為數字，利用雜湊函數快速比較字串是否相等。

此演算法的一個重要特點是**適合多模式匹配**：可以在 O(n + km) 的時間內同時搜尋 k 個模式，而大多數其他演算法需要對每個模式分別執行。

## 核心原理

### 滾動雜湊（Rolling Hash）

滾動雜湊是一種特殊的雜湊函數，可以在 O(1) 時間內更新雜湊值：當視窗向右滑動一個字元時，可以「移除」最左邊的字元貢獻，「加入」新字元的貢獻，而不需要重新計算整個視窗的雜湊值。

### 多項式雜湊（Polynomial Hash）

將字串視為一個以 `base` 為基底的數：

```
hash("abc") = (a * base^2 + b * base^1 + c * base^0) mod m
```

其中：
- `base` 通常選用 256（字元集大小）或一個大質數
- `m` 是一個大質數（如 10^9+7），用來避免溢位

### 滾動更新公式

假設當前視窗的雜湊值為 `H`，視窗長度為 `m`：

當視窗從位置 `i` 滑動到 `i+1` 時：
```
H_new = (H * base - char_at_i * base^m + char_at_i+m) mod m
```

### 雜湊碰撞（Hash Collision）

由於雜湊值可能重複（不同的字串可能有相同的雜湊值），當雜湊匹配時，仍需要進行**逐字驗證**以確保真正匹配。

為了減少碰撞機率，可以使用：
1. **雙雜湊（Double Hash）**：使用兩組不同的 base 和 mod
2. **大質數模數**：選用更大的質數作為模數

### 時間複雜度

- **平均情況**：O(n + m)，其中 n 是文字長度，m 是模式長度
- **最壞情況**：O(nm)，當發生大量雜湊碰撞時
- **多模式匹配**：O(n + km)，k 個模式

### 空間複雜度

O(1)（單模式）或 O(k)（多模式）

## 使用範例

```python
from rabin_karp import rabin_karp_search, rabin_karp_multi_search

text = "ABABDABACDABABCABAB"

# 單一模式搜尋
pattern = "ABABCABAB"
matches = rabin_karp_search(text, pattern)
print(f"匹配位置: {matches}")  # [10]

# 多模式搜尋
patterns = ["AB", "BA", "CA"]
result = rabin_karp_multi_search(text, patterns)
print(result)
# 輸出: {'AB': [0, 2, 5, 7, 10, 12, 14, 16], 'BA': [1, 3, 8, 13, 15], 'CA': [9]}
```

## 應用場景

1. **重複內容檢測**：檢查文件中是否有重複的段落
2. **多模式匹配**：同時在一個文字中搜尋多個關鍵字
3. **抄襲檢測**：比較兩份文件的相似度
4. **DNA 序列匹配**：在基因序列中搜尋特定模式

## 參考資料

1. Rabin, M. O., & Karp, R. M. (1987). *Efficient randomized pattern-matching algorithms*. IBM Journal of Research and Development, 31(2), 249-260.
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 32.2)
3. [Rabin-Karp Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm)
4. [Rabin-Karp Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/)
