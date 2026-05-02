# 霍夫曼編碼 (Huffman Coding)

## 歷史背景

霍夫曼編碼由 David A. Huffman 於 1952 年在麻省理工學院就讀博士期間提出。當時他的教授 Robert Fano 給學生們一個作業：找出最有效的二進制編碼方法。Huffman 在嘗試多種方法後，創造了這個基於貪心算法的編碼方式，並證明了它是最優的前綴編碼。

有趣的是，Huffman 當時並不知道他的方法會成為日後數據壓縮的基石。如今，霍夫曼編碼被廣泛應用於各種壓縮標準中，包括 DEFLATE（ZIP、gzip）、JPEG、MP3 等。

## 核心原理

霍夫曼編碼是一種**最優前綴編碼**（Optimal Prefix Code），其核心思想是：
- **高頻字元用短編碼，低頻字元用長編碼**
- **前綴特性**：任何字元的編碼都不是其他字元編碼的前綴，這確保了解碼的唯一性

### 演算法步驟

1. **統計頻率**：掃描資料，統計每個符號出現的次數
2. **構建最小堆**：將每個符號及其頻率作為葉節點放入最小堆
3. **合併節點**：
   - 從堆中取出兩個頻率最小的節點
   - 創建一個新節點，其頻率為兩者之和，左右子節點分別為這兩個節點
   - 將新節點放回堆中
   - 重複直到堆中只有一個節點（根節點）
4. **生成編碼**：從根節點出發，左邊分支記為 0，右邊分支記為 1，到達葉節點時的路徑即為該符號的編碼

### 數學性質

對於給定的符號集和頻率分佈，霍夫曼編碼能產生**最小期望碼長**的編碼方案。期望碼長為：

\[
E(L) = \sum_{i=1}^{n} p_i \cdot l_i
\]

其中 \(p_i\) 是符號 i 的頻率，\(l_i\) 是其編碼長度。霍夫曼編碼使得 \(E(L)\) 達到最小。

## 使用範例

```python
from code.資料壓縮.entropy.huffman import build_huffman_tree, generate_codes, encode, decode

# 原始資料
text = "this is an example for huffman encoding"

# 計算頻率
freq_table = {}
for char in text:
    freq_table[char] = freq_table.get(char, 0) + 1

# 構建霍夫曼樹
tree = build_huffman_tree(freq_table)

# 生成編碼表
codes = {}
generate_codes(tree, '', codes)
print("編碼表:", codes)

# 壓縮
encoded, _ = encode(text, codes)
print(f"壓縮後大小: {len(encoded)} bytes")
print(f"原始大小: {len(text)} bytes")

# 解壓縮
decoded = decode(encoded, tree)
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 執行結果範例

```
編碼表: {' ': '00', 'a': '010', 'c': '0110', 'd': '0111', ...}
壓縮後大小: 32 bytes
原始大小: 39 bytes
壓縮率: 82.1%
解壓後: this is an example for huffman encoding
驗證正確: True
```

## 與其他編碼比較

| 特性 | 霍夫曼編碼 | Shannon-Fano | 算術編碼 |
|------|-----------|--------------|---------|
| 最優性 | 最優（整數位元） | 不一定最優 | 更接近熵界 |
| 複雜度 | O(n log n) | O(n log n) | 較高 |
| 實作難度 | 中等 | 簡單 | 複雜 |
| 前綴特性 | 有 | 有 | 不需要 |

## 參考資料

1. Huffman, D. A. (1952). "A Method for the Construction of Minimum-Redundancy Codes". *Proceedings of the IRE*.
2. [Wikipedia: Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)
3. Sayood, K. (2017). *Introduction to Data Compression* (5th ed.). Morgan Kaufmann.
4. [Greedy Algorithms - Huffman Coding](https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/)
