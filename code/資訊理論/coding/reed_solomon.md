# 資訊論 — 里德-所羅門碼 (Reed-Solomon Code)

## 歷史背景

里德-所羅門碼由 Irving S. Reed 和 Gustave Solomon 於 1960 年提出，是一種非二進位循環碼。RS 碼廣泛應用於 QR 碼、CD、DVD、衛星通訊、深空通訊等領域。

## 核心原理

### 伽羅瓦域 GF(2^8)
RS 碼運算在 GF(256) 上進行，每個符號為 8 位元。使用本原多項式：

```
p(x) = x^8 + x^4 + x^3 + x^2 + 1 (十六進位 0x11D)
```

### RS(n,k) 碼
- n: 碼字長度（255 for GF(256)）
- k: 資料長度
- 可修正錯誤數：t = (n-k)/2

### 生成多項式
```
g(x) = (x - α^0)(x - α^1)...(x - α^(n-k-1))
```

### 編碼過程
1. 訊息多項式 m(x)（k 個符號）
2. 計算 r(x) = m(x) * x^(n-k) mod g(x)
3. 碼字：c(x) = m(x) * x^(n-k) + r(x)

### 特性
- 最大距離可分離（MDS）碼：最小距離 d = n - k + 1
- 系統性編碼：前 k 個符號為原始資料

## 使用範例

```python
from reed_solomon import ReedSolomon

# 建立 RS(255, 251) 碼（可修正 2 個錯誤）
rs = ReedSolomon(n=255, k=251)

# 編碼
data = [0x01, 0x02, 0x03, ...]
encoded = rs.encode(data)

# 解碼（含錯誤修正）
decoded, success = rs.decode(received)
```

## 參考資料

- Reed, I. S., & Solomon, G. (1960). Polynomial Codes Over Certain Finite Fields. Journal of the SIAM.
- Bose, R. C., & Ray-Chaudhuri, D. K. (1960). On A Class of Error Correcting Binary Group Codes.
