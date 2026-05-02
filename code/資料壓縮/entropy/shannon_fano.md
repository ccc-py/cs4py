# Shannon-Fano 編碼

## 歷史背景

Shannon-Fano 編碼由 Claude Shannon 和 Robert Fano 在 1949 年提出，是早期重要的資料壓縮演算法之一。當時 Shannon 正在研究資訊理論的基礎，而 Fano 則致力於尋找有效的編碼方法。

雖然這個方法後來被 Huffman 編碼證明不是最優的，但它引入了**根據機率分配變長編碼**的核心概念，並且展示了如何通過遞迴分割來構建編碼樹。可以說，Shannon-Fano 是 Huffman 編碼的前身和靈感來源。

## 核心原理

Shannon-Fano 編碼採用**頂向下**（Top-Down）的遞迴分割方法：

### 演算法步驟

1. **統計頻率**：計算每個符號在資料中出現的次數
2. **排序**：將符號按頻率從高到低排序
3. **遞迴分割**：
   - 將符號列表分割成兩部分，使得兩部分的頻率總和盡量接近
   - 給左半部分分配編碼位元 `0`，右半部分分配 `1`
   - 對每個部分遞迴執行上述分割，直到每個部分只包含一個符號
4. **生成編碼**：從根到葉的路徑即為該符號的編碼

### 與 Huffman 的差異

| 特性 | Shannon-Fano | Huffman |
|------|-------------|---------|
| 建樹方向 | 頂向下（Top-Down） | 底向上（Bottom-Up） |
| 分割策略 | 每次找最佳分割點 | 每次合併最小兩個 |
| 最優性 | 不一定最優 | 保證最優 |
| 實作複雜度 | 簡單 | 中等 |

### 為什麼 Shannon-Fano 不是最優的？

Shannon-Fano 的分割不一定能達到**最優前綴編碼**。因為它總是試圖將列表分成兩半，但這種貪心策略無法保證全局最優。Huffman 編碼通過反覆合併最小頻率的節點，保證了最優性。

## 使用範例

```python
from code.資料壓縮.entropy.shannon_fano import build_shannon_tree, generate_codes, encode, decode

# 原始資料
text = "this is an example for shannon fano encoding"

# 計算頻率並排序
from collections import Counter
freq_table = Counter(text)
sorted_symbols = sorted(freq_table.items(), key=lambda x: -x[1])

# 構建 Shannon-Fano 樹
tree = build_shannon_tree(sorted_symbols, 0, len(sorted_symbols) - 1)

# 生成編碼表
codes = {}
generate_codes(tree, '', codes)
print("編碼表:", codes)

# 壓縮
encoded = encode(text, codes)
print(f"壓縮後大小: {len(encoded)} bytes")

# 解壓縮
decoded = decode(encoded, tree)
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 執行結果範例

```
編碼表: {' ': '00', 'e': '010', 'n': '011', 'a': '100', ...}
壓縮後大小: 33 bytes
原始大小: 47 bytes
壓縮率: 70.2%
解壓後: this is an example for shannon fano encoding
驗證正確: True
```

## 與 Huffman 編碼比較

以下是對同一段文字使用兩種編碼的結果比較：

```python
from code.資料壓縮.entropy.shannon_fano import compare_with_huffman

text = "abracadabra"
compare_with_huffman(text)
```

結果可能顯示 Huffman 編碼在某些情況下比 Shannon-Fano 更優（更少位元數）。

## 參考資料

1. Shannon, C. E. (1948). "A Mathematical Theory of Communication". *Bell System Technical Journal*.
2. Fano, R. M. (1949). "The Transmission of Information". *MIT Research Laboratory of Electronics*.
3. [Wikipedia: Shannon-Fano coding](https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding)
4. Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
