# 資訊論 — 海明碼 (Hamming Code)

## 歷史背景

海明碼由理查德·海明（Richard Hamming）於 1950 年發明，是早期錯誤修正碼的代表。海明在貝爾實驗室工作時，為了解決電腦記憶體中的錯誤問題而設計了此編碼。

## 核心原理

### (7,4) 海明碼
將 4 位元資料編碼為 7 位元碼字，可檢測並修正單一錯誤。

### 編碼結構
位置 1, 2, 4 為同位位元（parity bits），其餘為資料位元：

```
位置:  1   2   3   4   5   6   7
內容:  p1  p2  d1  p3  d2  d3  d4
```

### 同位位元計算
```
p1 = d1 ⊕ d2 ⊕ d4  (涵蓋位置 1,3,5,7)
p2 = d1 ⊕ d3 ⊕ d4  (涵蓋位置 2,3,6,7)
p3 = d2 ⊕ d3 ⊕ d4  (涵蓋位置 4,5,6,7)
```

### 症候群解碼
接收到碼字後，重新計算同位檢查：
- s1, s2, s3 組成症候群
- 若症候群 = 0，無錯誤
- 否則症候群的值就是錯誤位置

## 使用範例

```python
from hamming_code import encode_hamming_7_4, decode_hamming_7_4

# 編碼
data = [1, 0, 1, 1]
encoded = encode_hamming_7_4(data)
print(encoded)  # [0, 1, 1, 0, 0, 1, 1]

# 解碼（含錯誤修正）
decoded, corrected = decode_hamming_7_4(encoded)
print(decoded)  # [1, 0, 1, 1]
```

## 參考資料

- Hamming, R. W. (1950). Error Detecting and Error Correcting Codes. Bell System Technical Journal.
- Lin, S., & Costello, D. J. (2004). Error Control Coding. Prentice Hall.
