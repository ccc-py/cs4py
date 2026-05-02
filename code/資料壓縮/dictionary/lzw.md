# LZW 壓縮演算法

## 歷史背景

LZW（Lempel-Ziv-Welch）演算法由 Terry Welch 在 1984 年發表，是 LZ78 演算法的改進版本。LZW 最重要的貢獻在於：

1. **不需要傳送字典**：壓縮端和解壓縮端可以同步地建立完全相同的字典
2. **單遍掃描**：只需要掃描輸入資料一次
3. **廣泛應用**：被用於 GIF 圖片格式、Unix 的 `compress` 指令、TIFF 格式等

LZW 的專利問題曾經引發爭議，但專利已於 2003 年到期，現在可以自由使用。

## 核心原理

### 字典的建立

LZW 使用一個動態增長的字典，初始時字典包含所有可能的單一字元（通常 0-255 對應 ASCII 字元）。

### 壓縮過程

以 "TOBEORNOTTOBEORTOBEORNOT" 為例：

1. 初始字典：0='T', 1='O', 2='B', 3='E', 4='R', 5='N', ...
2. 讀取 'T'，在字典中，繼續
3. 讀取 'O'，'TO' 不在字典中，輸出 'T' 的碼字 0，將 'TO' 加入字典（索引 256）
4. 依此類推...

### 解壓縮過程

解壓縮端使用相同的演算法來重建字典：

1. 讀取第一個碼字，直接輸出對應的字元
2. 對於後續的碼字：
   - 如果碼字在字典中，輸出對應的字串
   - 如果碼字不在字典中（特殊情況），則是前一個字串加上其第一個字元
   - 將前一個碼字對應的字串 + 新字串的第一個字元加入字典

### 特殊情況處理

當壓縮端輸出一個剛加入字典的碼字時，解壓縮端還沒有這個碼字。例如：
- 壓縮端：遇到 "ABAB"，輸出 A, B, 然後 "AB" 的碼字
- 解壓縮端：需要能夠推導出這個新碼字的內容

## 使用範例

```python
from code.資料壓縮.dictionary.lzw import encode, decode

# 原始資料
text = "TOBEORNOTTOBEORTOBEORNOT"

# 壓縮
codes = encode(text)
print("壓縮碼字:", codes)
print(f"碼字數量: {len(codes)}")
print(f"原始長度: {len(text)} 字元")

# 解壓縮
decoded = decode(codes)
print(f"解壓後: {decoded}")
print(f"驗證正確: {decoded == text}")
```

### 執行結果範例

```
壓縮碼字: [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 261, 263, 260]
碼字數量: 14
原始長度: 24 字元
解壓後: TOBEORNOTTOBEORTOBEORNOT
驗證正確: True
```

注意：碼字 256 代表 "TO"，258 代表 "BEOR" 等，這些是在壓縮過程中動態加入字典的。

## 與其他 LZ 演算法比較

| 特性 | LZ77 | LZ78 | LZW |
|------|------|------|-----|
| 字典結構 | 滑動視窗 | 顯式字典 | 顯式字典 |
| 字典傳送 | 不需要 | 需要 | 不需要 |
| 壓縮速度 | 較慢（搜尋） | 快 | 快 |
| 記憶體使用 | 低 | 高 | 高 |

## 參考資料

1. Welch, T. A. (1984). "A Technique for High-Performance Data Compression". *Computer*.
2. [Wikipedia: LZW](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch)
3. Nelson, M., & Gailly, J. L. (1996). *The Data Compression Book* (2nd ed.). M&T Books.
4. [GIF 格式中的 LZW](https://www.w3.org/Graphics/GIF/spec-gif89a.txt)
