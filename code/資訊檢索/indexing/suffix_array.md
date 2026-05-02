# 後綴陣列 (Suffix Array)

## 歷史背景

後綴陣列由 Manber 和 Myers 於 1990 年提出，作為後綴樹（Suffix Tree）的空間效率替代方案。後綴樹雖然操作更快（O(n)），但實作複雜且空間開銷大。後綴陣列僅需 O(n) 空間，且能支援相同的字串操作。

後綴陣列廣泛應用於：
- 基因序列比對（BLAST 工具）
- 文字壓縮（Burrows-Wheeler 轉換的基礎）
- 重複子串偵測
- 全文搜尋系統

## 核心原理

### 後綴陣列定義

對於長度為 n 的字串，其後綴陣列是一個排列 `SA[0..n-1]`，使得：
```
text[SA[0]:] < text[SA[1]:] < ... < text[SA[n-1]:]
```
即所有後綴按字典序排序後的起始位置。

### 建構演算法

本實作使用 **倍增演算法（Doubling Algorithm）**：
1. 初始依據第一個字符排序
2. 第 k 輪依據前 2^k 個字符排序
3. 使用上一輪的排名作為鍵值進行排序
4. 時間複雜度：O(n log² n)

更優化的演算法（如 SA-IS）可達到 O(n)。

### 模式搜尋

利用後綴陣列的排序特性，使用二分搜尋：
- 找到第一個匹配位置（下界）
- 找到最後一個匹配位置（上界）
- 時間複雜度：O(m log n)，m 為模式長度

## 使用範例

```python
from indexing.suffix_array import build_suffix_array, search_pattern

text = "banana"
sa = build_suffix_array(text)
print(sa)  # [5, 3, 1, 0, 4, 2] (取決於實作)

matches = search_pattern(text, "ana", sa)
print(matches)  # [1, 3]
```

## 參考資料

- Manber, U., & Myers, G. (1990). Suffix arrays: a new method for on-line string searches. *SIAM Journal on Computing*, 22(5), 935-948.
- Kärkkäinen, J., & Sanders, P. (2003). Simple linear work suffix array construction. *ICALP*, 943-955.
- Nong, G., Zhang, S., & Chan, W. H. (2009). Linear suffix array construction by almost pure induced-sorting. *DCC*, 193-202.
