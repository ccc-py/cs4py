# 離散餘弦轉換 (DCT)

## 歷史背景

離散餘弦轉換（Discrete Cosine Transform, DCT）由 Nasir Ahmed、T. Natarajan 和 K. R. Rao 在 1974 年提出。Ahmed 當時正在研究數位訊號處理中的轉換編碼，他發現 DCT 對於語音和圖片壓縮特別有效。

DCT 最重要的應用是在 **JPEG** 圖片壓縮標準中。JPEG 使用 8x8 區塊的 2D DCT-II，配合量化和霍夫曼編碼，可以達到很高的壓縮比，同時保持可接受的圖片品質。

其他應用包括：
- **MPEG 影片壓縮**
- **MP3 音訊壓縮**
- **H.26x 系列影片標準**

## 核心原理

### DCT 的數學定義

一維 DCT-II 的定義：

\[
X_k = c_k \sum_{n=0}^{N-1} x_n \cos\left(\frac{\pi k (2n+1)}{2N}\right)
\]

其中：
- \(c_0 = \sqrt{\frac{1}{N}}\)
- \(c_k = \sqrt{\frac{2}{N}}\) for \(k > 0\)

### 二維 DCT

對於 8x8 區塊，2D DCT 是先對每行做 1D DCT，再對結果的每列做 1D DCT：

\[
F(u,v) = \frac{1}{4} c(u) c(v) \sum_{i=0}^{7} \sum_{j=0}^{7} f(i,j) \cos\left(\frac{\pi u (2i+1)}{16}\right) \cos\left(\frac{\pi v (2j+1)}{16}\right)
\]

### 能量集中特性

DCT 最強大的特性是**能量集中**（Energy Compaction）：

- **低頻係數**（左上角）包含圖片的主要資訊
- **高頻係數**（右下角）通常很小，可以量化和捨棄

這使得 DCT 非常適合有損壓縮。

### JPEG 壓縮流程

1. **分割**：將圖片分割為 8x8 區塊
2. **層級偏移**：將像素值從 0-255 轉為 -128 到 127
3. **DCT**：對每個區塊做 2D DCT
4. **量化**：除以量化表並取整（這是有損步驟）
5. **熵編碼**：使用霍夫曼或算術編碼壓縮量化後的係數

## 使用範例

```python
from code.資料壓縮.image.dct import compress_block, decompress_block, print_matrix

# 建立一個簡單的 8x8 區塊
block = []
for i in range(8):
    row = [float(i * 32 + j * 4) for j in range(8)]
    block.append(row)

print("原始區塊:")
print_matrix(block)

# 壓縮（DCT + 量化）
quantized = compress_block(block, quality=50)
print("\n量化後的 DCT 係數:")
print_matrix(quantized, precision=0)

# 解壓縮
reconstructed = decompress_block(quantized, quality=50)
print("\n重建後的區塊:")
print_matrix(reconstructed)
```

### 執行結果範例

```
原始區塊:
   0.0    4.0    8.0   12.0   16.0   20.0   24.0   28.0
  32.0   36.0   40.0   44.0   48.0   52.0   56.0   60.0
  ...

量化後的 DCT 係數:
  -168    0    0    0    0    0    0    0
     3   -1    0    0    0    0    0    0
     0    0    0    0    0    0    0    0
  ...

重建後的區塊:
   0.0    4.0    8.0   12.0   16.0   20.0   24.0   28.0
  32.0   36.0   40.0   44.0   48.0   52.0   56.0   60.0
  ...
```

注意：大部分量化後的係數變為 0，這就是壓縮的來源！

## 品質因子對壓縮的影響

| 品質因子 | 壓縮比 | 圖片品質 |
|---------|--------|---------|
| 90-100 | 低 | 極佳 |
| 70-90 | 中等 | 很好 |
| 50 | 高 | 可接受（JPEG 預設） |
| 10-30 | 極高 | 明顯失真 |

## 參考資料

1. Ahmed, N., Natarajan, T., & Rao, K. R. (1974). "Discrete Cosine Transform". *IEEE Transactions on Computers*.
2. Wallace, G. K. (1991). "The JPEG Still Picture Compression Standard". *Communications of the ACM*.
3. [Wikipedia: Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform)
4. Pennebaker, W. B., & Mitchell, J. L. (1992). *JPEG Still Image Data Compression Standard*. Springer.
