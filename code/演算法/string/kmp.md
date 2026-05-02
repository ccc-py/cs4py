# KMP (Knuth-Morris-Pratt) 字串匹配演算法

## 歷史背景

KMP 演算法由 Donald Knuth、James H. Morris 和 Vaughan Pratt 於 1977 年共同發表，是字串匹配領域的經典演算法之一。此演算法的核心創新在於**失敗函數（Failure Function）**的引入，使得在不匹配時能夠利用已經匹配的部分資訊，避免重複比較。

此演算法解決了朴素字串匹配（Naive String Matching）中存在的低效問題：當發生不匹配時，朴素方法會將模式串向右滑動一格並重新比較，而 KMP 能夠根據失敗函數跳過不必要的比較。

## 核心原理

### 失敗函數（π 表 / 前綴表）

失敗函數 `fail[i]` 表示模式串 `pattern[0:i+1]` 中，最長的「相等前綴後綴」的長度。

- **前綴（Prefix）**：從頭開始的子字串（不包含完整字串本身）
- **後綴（Suffix）**：以結尾結束的子字串（不包含完整字串本身）
- **相等前綴後綴**：既是前綴又是後綴的子字串

**範例：**

對於模式串 `"ABABCABAB"`：

| i | 字元 | 最長相等前綴後綴 | fail[i] |
|---|------|-----------------|---------|
| 0 | A    | 無              | 0       |
| 1 | B    | 無              | 0       |
| 2 | A    | "A"             | 1       |
| 3 | B    | "AB"            | 2       |
| 4 | C    | 無              | 0       |
| 5 | A    | "A"             | 1       |
| 6 | B    | "AB"            | 2       |
| 7 | A    | "ABA"           | 3       |
| 8 | B    | "ABAB"          | 4       |

### 匹配過程

當 `text[i] != pattern[j]` 時：
- 如果 `j != 0`，將 `j` 設為 `fail[j-1]`，繼續比較
- 如果 `j == 0`，將 `i` 加 1

這樣就不需要將模式串向右滑動一格重新開始，而是利用已經匹配的部分資訊。

### 時間複雜度

- **計算失敗函數**：O(m)，其中 m 是模式串長度
- **搜尋過程**：O(n)，其中 n 是主文字長度
- **總時間複雜度**：**O(n + m)**

相比朴素方法的 O(nm)，KMP 在處理大型文字時效率顯著提升。

### 空間複雜度

O(m)，用於儲存失敗函數表。

## 使用範例

```python
from kmp import kmp_search, compute_failure

text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"

# 計算失敗函數
fail = compute_failure(pattern)
print(f"失敗函數: {fail}")
# 輸出: [0, 0, 1, 2, 0, 1, 2, 3, 4]

# 搜尋所有匹配位置
matches = kmp_search(text, pattern)
print(f"匹配位置: {matches}")
# 輸出: [10]
```

## 參考資料

1. Knuth, D. E., Morris, J. H., & Pratt, V. R. (1977). *Fast pattern matching in strings*. SIAM Journal on Computing, 6(2), 323-350.
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 32.4)
3. [KMP Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/)
4. [Knuth-Morris-Pratt algorithm - Wikipedia](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
