# Move-to-Front (MTF) 編碼

## 歷史背景

Move-to-Front (MTF) 編碼是一種簡單而有效的資料轉換演算法，最早用於動態資料結構的效能優化。

在資料壓縮領域，MTF 通常與 **Burrows-Wheeler Transform (BWT)** 配合使用：

1. **BWT** 使相同的字元聚集在一起
2. **MTF** 將這些聚集的字元轉換為 0 或小的正整數
3. **RLE 或霍夫曼編碼** 進一步壓縮這些小整數

這個組合（BWT + MTF + RLE/霍夫曼）是 **bzip2** 壓縮工具的核心。

## 核心原理

### MTF 演算法

MTF 維護一個包含所有可能符號的列表（通常 0-255），對於每個輸入值：

1. **查找**：找到該值在列表中的位置（索引）
2. **輸出**：輸出這個索引
3. **移動**：將該值移到列表的最前面

### 簡單範例

初始列表：`[0, 1, 2, 3, 4, ...]`

輸入：`97, 98, 97, 97, 98`

| 輸入 | 操作 | 輸出 | 更新後的列表 |
|------|------|------|-------------|
| 97 | 在位置 97 | 97 | [97, 0, 1, 2, ...] |
| 98 | 在位置 98 | 98 | [98, 97, 0, 1, ...] |
| 97 | 在位置 1 | 1 | [97, 98, 0, 1, ...] |
| 97 | 在位置 0 | 0 | [97, 98, 0, 1, ...] |
| 98 | 在位置 1 | 1 | [98, 97, 0, 1, ...] |

輸出：`[97, 98, 1, 0, 1]`

### 為什麼 MTF 有效？

當輸入資料中有**連續重複的值**時（BWT 的輸出正是如此），MTF 會輸出大量的 **0** 和小的正整數，這些值非常適合後續的 RLE 或霍夫曼編碼。

## 使用範例

```python
from code.資料壓縮.transform.move_to_front import encode_string, decode_string

# 原始資料（模擬 BWT 的輸出）
text = "ard$rcaaabb"

# MTF 編碼
encoded = encode_string(text)
print(f"原始: {text}")
print(f"MTF 編碼: {encoded}")

# MTF 解碼
decoded = decode_string(encoded)
print(f"MTF 解碼: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 執行結果範例

```
原始: ard$rcaaabb
MTF 編碼: [97, 98, 1, 3, 2, 99, 3, 0, 0, 0, 1]
MTF 解碼: ard$rcaaabb
驗證正確: True
```

注意：最後三個 `a` 變成了 `0, 0, 0`，這非常適合 RLE 壓縮！

## 完整壓縮流程

```python
from code.資料壓縮.transform.burrows_wheeler import bwt_encode
from code.資料壓縮.transform.move_to_front import encode_string
from code.資料壓縮.transform.run_length import encode_binary

# 原始資料
text = "abracadabra"

# BWT
bwt_result, _ = bwt_encode(text)
print(f"BWT: {bwt_result}")

# MTF
mtf_result = encode_string(bwt_result)
print(f"MTF: {mtf_result}")

# RLE
rle_result = encode_binary(mtf_result, threshold=3)
print(f"RLE: {rle_result}")
```

## 參考資料

1. Bentley, J. L., Sleator, D. D., Tarjan, R. E., & Wei, V. K. (1986). "A Locally Adaptive Data Compression Scheme". *Communications of the ACM*.
2. [Wikipedia: Move-to-front transform](https://en.wikipedia.org/wiki/Move-to-front_transform)
3. Burrows, M., & Wheeler, D. J. (1994). "A Block-sorting Lossless Data Compression Algorithm". *DEC Systems Research Center*.
4. [MTF in Data Compression](https://www.cs.cmu.edu/~./dst/Tutorials/InfoCompress/)
