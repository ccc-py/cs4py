# 行程長度編碼 (Run-Length Encoding, RLE)

## 歷史背景

行程長度編碼（RLE）是最古老的資料壓縮方法之一，其概念非常直觀：將連續重複的資料用「數值 + 次數」的方式表示。

RLE 最早被應用於：
- **圖片壓縮**：BMP、TIFF、PCX 等格式使用 RLE
- **傳真機**：Modified Huffman Coding（基於 RLE）
- **簡單資料壓縮**：適合處理有大量連續相同值

雖然 RLE 的壓縮率有限，但其**簡單、快速、無損**的特性，使其在特定場景下仍然很有用。

## 核心原理

### 基本概念

RLE 的核心思想是：
- 如果資料中有連續 N 個相同的值 V
- 將其編碼為 `(V, N)` 或 `V N`

例如：
- "AAAAABBB" → "A5B3"（5個A，3個B）
- [1,1,1,1,0,0,0,0] → [(1,4), (0,4)]

### 適用場景

RLE 對以下資料壓縮效果很好：
- **圖片**：大量連續的相同像素（如背景）
- **文件**：有大量連續的空白或相同字元
- **感測器資料**：連續採樣值相同

對於隨機資料，RLE 可能會**導致資料變大**（因為需要額外儲存次數）。

## 使用範例

### 字串壓縮

```python
from code.資料壓縮.transform.run_length import encode, decode

# 原始資料
text = "AAAAABBBBCCCCCCDDDDEEEE"

# 壓縮
encoded = encode(text)
print(f"壓縮後: {encoded}")
print(f"原始長度: {len(text)}")
print(f"壓縮後長度: {len(encoded)}")

# 解壓縮
decoded = decode(encoded)
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 二進制資料壓縮

```python
from code.資料壓縮.transform.run_length import encode_binary, decode_binary

# 二進制資料（如黑白圖片）
data = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0]

# 壓縮（threshold=3 表示至少連續 3 個才壓縮）
encoded = encode_binary(data, threshold=3)
print(f"壓縮後: {encoded}")

# 解壓縮
decoded = decode_binary(encoded)
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == data}")
```

### 簡單圖片壓縮

```python
from code.資料壓縮.transform.run_length import encode_image, decode_image

# 4x4 灰階圖片（0=黑，255=白）
image = [
    255, 255, 255, 255,
    255, 0, 0, 255,
    255, 0, 0, 255,
    255, 255, 255, 255
]

# 壓縮（每行獨立編碼）
encoded = encode_image(image, width=4)
print(f"壓縮後: {encoded}")

# 解壓縮
decoded = decode_image(encoded, width=4)
print(f"驗證正確: {decoded == image}")
```

## 壓縮效果比較

| 資料類型 | 原始大小 | 壓縮後大小 | 壓縮率 |
|---------|---------|-----------|--------|
| "AAAAABBBB" (8字元) | 8 | 4 | 50% |
| [1]*100 (100位元組) | 100 | 5 | 5% |
| 隨機資料 (100位元組) | 100 | ~200 | 200% (變大!) |

## 參考資料

1. Robinson, A. H., & Cherry, C. (1967). "Results of a prototype television bandwidth compression scheme". *Proceedings of the IEEE*.
2. [Wikipedia: Run-length encoding](https://en.wikipedia.org/wiki/Run-length_encoding)
3. Salomon, D. (2004). *Data Compression: The Complete Reference* (3rd ed.). Springer.
4. [RLE in Image Compression](https://www.cs.cmu.edu/~./dst/Tutorials/ImageCompression/RLE/rle.html)
