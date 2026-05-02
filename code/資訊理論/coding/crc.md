# 資訊論 — 循環冗餘檢查 (CRC)

## 歷史背景

循環冗餘檢查（CRC）由 W. Wesley Peterson 於 1961 年提出，是一種基於多項式除法的錯誤檢測碼。CRC 廣泛應用於網路協定（乙太網、Wi-Fi）、儲存裝置（硬碟、光碟）等領域。

## 核心原理

### 多項式表示
將資料視為係數在多項式 GF(2) 上的表示：

```
資料 110101 → 多項式 x^5 + x^4 + x^2 + 1
```

### CRC 計算
1. 資料左移 r 位（r = 多項式階數）
2. 除以生成多項式 g(x)
3. 餘數即為 CRC 碼

### 常見標準
| 名稱 | 多項式 (十六進位) | 用途 |
|------|-------------------|------|
| CRC-8 | 0x07 | 簡單檢查 |
| CRC-16-CCITT | 0x1021 | XMODEM, Bluetooth |
| CRC-32 | 0x04C11DB7 | Ethernet, ZIP, PNG |

### 錯誤檢測能力
- 可檢測所有單一錯誤
- 可檢測所有雙重錯誤（適當選擇多項式）
- 可檢測所有奇數個錯誤
- 可檢測所有 ≤ r 位元的突發錯誤

## 使用範例

```python
from crc import crc8, crc32, verify_crc

# CRC-8
data = [0x01, 0x02, 0x03]
crc = crc8(data)
print(f"CRC-8: 0x{crc:02X}")

# 驗證
is_valid = verify_crc(data, crc, 0x07, 8)
print(f"驗證: {is_valid}")
```

## 參考資料

- Peterson, W. W., & Brown, D. T. (1961). Cyclic Codes for Error Detection. Proceedings of the IRE.
- Koopman, P., & Chakravarty, T. (2004). Cyclic Redundancy Code (CRC) Polynomial Selection For Embedded Networks.
