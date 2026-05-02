# 資訊論 — 通道容量 (Channel Capacity)

## 歷史背景

香農第二定理（有雜訊通道編碼定理）於 1948 年提出，證明了在雜訊通道上可以實現可靠通訊，只要傳輸速率低於通道容量。這是資訊論最重要的定理之一。

## 核心原理

### 通道容量定義
通道容量是通道能可靠傳輸的最大資訊速率：

```
C = max_{p(x)} I(X;Y)
```

其中 I(X;Y) 是輸入 X 和輸出 Y 的互資訊。

### 二元對稱通道 (BSC)
BSC 參數為錯誤機率 p：

```
C = 1 - H₂(p) = 1 + p·log₂(p) + (1-p)·log₂(1-p)
```

當 p=0 或 p=1 時，C=1；當 p=0.5 時，C=0（最差情況）。

### 二元擦除通道 (BEC)
BEC 參數為擦除機率 p：

```
C = 1 - p
```

### 香農第二定理
對於任意速率 R < C，存在編碼方案使得錯誤機率任意小。對於 R > C，錯誤機率有正的下界。

## 使用範例

```python
from channel_capacity import channel_capacity_bsc, dmc_capacity

# BSC 容量
print(channel_capacity_bsc(0.1))  # ~0.531 bits/symbol

# DMC 容量（Blahut-Arimoto 演算法）
w = [[0.9, 0.2], [0.1, 0.8]]
print(dmc_capacity(w))  # 約 0.583 bits/symbol
```

## 參考資料

- Shannon, C. E. (1948). A Mathematical Theory of Communication.
- Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory. Wiley.
- Blahut, R. E. (1972). Computation of Channel Capacity and Rate-Distortion Functions.
