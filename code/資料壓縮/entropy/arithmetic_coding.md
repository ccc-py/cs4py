# 算術編碼 (Arithmetic Coding)

## 歷史背景

算術編碼的概念最早由 Peter Elias 在 1960 年代初期提出（未發表）。後來，Jorma Rissanen 和 Glen Langdon 在 1970 年代末至 1980 年代初發展了實用的算術編碼演算法。

與霍夫曼編碼不同，算術編碼不是為每個符號分配一個整數位元的編碼，而是將**整個訊息**編碼為 [0, 1) 區間內的一個小數。這使得算術編碼能夠達到更接近熵界（Entropy Bound）的壓縮效果。

如今，算術編碼被應用於 JPEG 2000、H.264/AVC 等現代壓縮標準中。

## 核心原理

### 熵與編碼效率

對於一個資訊來源，其熵（Entropy）定義為：

\[
H(X) = -\sum_{i=1}^{n} p_i \log_2 p_i
\]

其中 \(p_i\) 是符號 i 出現的機率。熵代表了理論上可達到的最小平均編碼長度。

### 算術編碼的思想

不同於霍夫曼編碼為每個符號分配獨立的位元串，算術編碼：

1. **將整個訊息映射到一個區間**：初始區間為 [0, 1)
2. **逐步縮小區間**：每讀入一個符號，根據其機率區間縮小當前區間
3. **輸出區間內的任意值**：最後區間內的任何值都可以代表整個訊息

### 演算法步驟

假設有四個符號 A, B, C, D，機率分別為 0.4, 0.3, 0.2, 0.1：

| 符號 | 機率 | 區間 |
|------|------|------|
| A | 0.4 | [0, 0.4) |
| B | 0.3 | [0.4, 0.7) |
| C | 0.2 | [0.7, 0.9) |
| D | 0.1 | [0.9, 1.0) |

編碼 "BAC"：
1. 初始區間 [0, 1)
2. 讀入 B → 新區間 [0.4, 0.7)，寬度 0.3
3. 讀入 A → 新區間 [0.4, 0.4 + 0.3×0.4) = [0.4, 0.52)
4. 讀入 C → 新區間 [0.4 + 0.12×0.7, 0.4 + 0.12×0.9) = [0.484, 0.508)

最後輸出此區間內的任意值，如 0.5。

## 使用範例

```python
from code.資料壓縮.entropy.arithmetic_coding import (
    build_probability_table, encode_to_bits, decode_from_bits
)

# 原始資料
text = "abracadabra"

# 建立機率表
prob_table = build_probability_table(text)
print("機率表:", prob_table)

# 編碼
bits = encode_to_bits(text, prob_table)
print(f"編碼位元: {bits}")
print(f"位元數: {len(bits)}")

# 解碼
decoded = decode_from_bits(bits, prob_table, len(text))
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 執行結果範例

```
機率表: {'a': (Fraction(0, 1), Fraction(5, 11)), 'b': (Fraction(5, 11), Fraction(7, 11)), ...}
編碼位元: 001010101001
位元數: 12
解壓後: abracadabra
驗證正確: True
```

## 算術編碼 vs 霍夫曼編碼

| 特性 | 算術編碼 | 霍夫曼編碼 |
|------|---------|-----------|
| 編碼單位 | 整個訊息 | 單個符號 |
| 壓縮效率 | 更接近熵界 | 受整數位元限制 |
| 實作複雜度 | 較高 | 中等 |
| 專利問題 | 曾受專利保護 | 免費使用 |

## 參考資料

1. Rissanen, J., & Langdon, G. G. (1979). "Arithmetic coding". *IBM Journal of Research and Development*.
2. Witten, I. H., Neal, R. M., & Cleary, J. G. (1987). "Arithmetic Coding for Data Compression". *Communications of the ACM*.
3. [Wikipedia: Arithmetic coding](https://en.wikipedia.org/wiki/Arithmetic_coding)
4. Sayood, K. (2017). *Introduction to Data Compression* (5th ed.). Morgan Kaufmann.
