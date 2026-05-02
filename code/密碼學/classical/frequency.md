# 頻率分析 (Frequency Analysis)

## 歷史背景
9世紀阿拉伯學者肯迪（Al-Kindi）發明了頻率分析，用於破解替換密碼。他發現不同字母在文本中出現的頻率不同，通過匹配密文與明文頻率可破解密碼。

## 核心原理
頻率分析利用自然語言中字母出現的頻率分佈特性。例如，英文中字母E出現頻率最高（約12.7%），T次之（約9.1%）。通過計算密文字母頻率與英文標準頻率的匹配度（如卡方統計量），可推測替換規則。

## 使用範例
```python
from frequency import ENGLISH_FREQUENCIES, chi_squared, crack_caesar

# 查看英文頻率表
print(ENGLISH_FREQUENCIES[:5])  # A, B, C, D, E 的頻率

# 計算卡方統計量
observed = [0.0] * 26
observed[4] = 1.0  # 假設只有E出現
chi = chi_squared(observed, ENGLISH_FREQUENCIES)
print(f"Chi-squared: {chi}")

# 破解凱薩密碼
cipher = "KHOOR ZRUOG"
shift = crack_caesar(cipher)
print(f"Detected shift: {shift}")  # 3
```

## 參考資料
- [Frequency Analysis - Wikipedia](https://en.wikipedia.org/wiki/Frequency_analysis)
- Al-Kindi《破解加密信息的方法》
