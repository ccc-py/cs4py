# Burrows-Wheeler 轉換 (BWT)

## 歷史背景

Burrows-Wheeler 轉換由 Michael Burrows 和 David Wheeler 在 1994 年發表於 DEC 系統研究中心的技術報告中。雖然這個轉換本身不進行壓縮，但它能將輸入資料重新排列，使得：

1. **相似的字元聚集在一起**（形成 runs）
2. **提高後續壓縮演算法的效果**（如 RLE、MTF）

BWT 是 **bzip2** 壓縮工具的核心演算法，與 Move-to-Front (MTF) 和 RLE 配合使用，可以達到非常好的壓縮效果。

## 核心原理

### BWT 的步驟

以 "banana" 為例：

1. **添加終止符**：`banana$`（終止符是最小的字元）
2. **生成所有循環旋轉**：
   ```
   banana$
   anana$b
   nana$ba
   ana$ban
   na$bana
   a$banan
   $banana
   ```
3. **按字典序排序**：
   ```
   $banana   ← 原始字串在這行
   a$banan
   ana$ban
   anana$b
   banana$
   na$bana
   nana$ba
   ```
4. **取出每行最後一個字元**：`annb$aa`

輸出：`annb$aa`，以及原始字串的索引 `0`。

### BWT 的可逆性

BWT 是可逆的，這意味著可以從 `annb$aa` 和索引 `0` 恢復原始字串。解碼過程使用**排序恢復法**：

1. 將編碼結果作為第一列
2. 排序得到第二列
3. 重複上述步驟，建立完整的矩陣
4. 根據索引找到原始字串

### 為什麼 BWT 有助於壓縮？

BWT 不壓縮資料，但它讓資料**更容易被壓縮**：

- 原始：`abracadabra`
- BWT 後：`ard$rcaaabb`（注意多個 `a` 和 `b` 聚集在一起）
- 後續使用 MTF 和 RLE 可以進一步壓縮

## 使用範例

```python
from code.資料壓縮.transform.burrows_wheeler import bwt_encode, bwt_decode

# 原始資料
text = "banana"

# BWT 編碼
encoded, index = bwt_encode(text)
print(f"BWT 結果: {encoded}")
print(f"索引: {index}")

# BWT 解碼
decoded = bwt_decode(encoded, index)
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 執行結果範例

```
BWT 結果: annb$aa
索引: 0
解壓後: banana
驗證正確: True
```

## BWT + MTF + RLE 流程

這是 bzip2 的簡化版壓縮流程：

```python
from code.資料壓縮.transform.burrows_wheeler import bwt_with_mtf_rle

# 原始資料
text = "abracadabra"

# 完整流程
bwt_result, bwt_idx, compressed = bwt_with_mtf_rle(text)
print(f"BWT: {bwt_result}")
print(f"壓縮結果: {compressed}")
```

## 參考資料

1. Burrows, M., & Wheeler, D. J. (1994). "A Block-sorting Lossless Data Compression Algorithm". *DEC Systems Research Center*.
2. [Wikipedia: Burrows-Wheeler transform](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform)
3. Manber, U., & Myers, G. (1993). "Suffix Arrays: A New Method for On-Line String Searches". *SIAM Journal on Computing*.
4. [BWT Tutorial](https://www.cs.princeton.edu/courses/archive/fall14/cos226/assignments/burrows.html)
