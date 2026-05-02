# 資訊論 — 二元通道 (Binary Channels)

## 歷史背景

二元通道是數位通訊最基本的模型。二元對稱通道（BSC）和二元擦除通道（BEC）是兩個經典的通道模型，廣泛用於分析通訊系統的性能。

## 核心原理

### 二元對稱通道 (BSC)
BSC 以機率 p 翻轉位元，以機率 1-p 正確傳輸：

```
輸入 0 → 輸出 0 (機率 1-p), 輸出 1 (機率 p)
輸入 1 → 輸出 1 (機率 1-p), 輸出 0 (機率 p)
```

容量：C = 1 - H₂(p)

### 二元擦除通道 (BEC)
BEC 以機率 p 擦除位元（輸出標記為擦除），以機率 1-p 正確傳輸：

```
輸入 0 → 輸出 0 (機率 1-p), 擦除 (機率 p)
輸入 1 → 輸出 1 (機率 1-p), 擦除 (機率 p)
```

容量：C = 1 - p

### 錯誤率分析
對於 BSC，錯誤率等於翻轉機率 p。對於 BEC，擦除率等於 p，但擦除可以被檢測到（與錯誤不同）。

## 使用範例

```python
from binary_channel import BinarySymmetricChannel, BinaryErasureChannel

# BSC 模擬
bsc = BinarySymmetricChannel(0.1)
print(bsc.transmit_sequence([1,0,1,1]))  # 可能有翻轉

# BEC 模擬
bec = BinaryErasureChannel(0.2)
print(bec.transmit_sequence([1,0,1,1]))  # -1 表示擦除
```

## 參考資料

- Shannon, C. E. (1948). A Mathematical Theory of Communication.
- Richardson, T., & Urbanke, R. (2008). Modern Coding Theory. Cambridge University Press.
