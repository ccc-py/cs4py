# 資訊論 — 率失真理論 (Rate-Distortion Theory)

## 歷史背景

率失真理論由克勞德·香農於 1948 年提出，後由 Toby Berger 等人發展完善。該理論探討了有損壓縮的理論極限：給定可接受的失真程度，最小需要多少位元來表示資料。

## 核心原理

### 率失真函數 R(D)
R(D) 定義為在平均失真不超過 D 的情況下，所需的最小速率：

```
R(D) = min_{Q: E[d(X,Y)] ≤ D} I(X;Y)
```

其中：
- D: 可接受的失真程度
- d(x,y): 失真度量
- I(X;Y): 互資訊

### 二元對稱源
對於 Bernoulli(p) 源，使用 Hamming 失真：

```
R(D) = H₂(p) - H₂(D),  0 ≤ D ≤ min(p, 1-p)
R(D) = 0,              D ≥ min(p, 1-p)
```

其中 H₂(p) 是二元熵函數。

### Blahut-Arimoto 演算法
求解率失真問題的迭代演算法：
1. 初始化轉移機率 Q(Y|X)
2. 重複直到收斂：
   - 計算輔助量 c(y,x) = exp(-β·d(x,y))
   - 更新 Q(Y|X) 和邊際 Q(Y)

### 重要意義
- 當 D=0：R(0) = H(X)（無損壓縮極限）
- 當 D 增加：R(D) 減少（允許失真可提升壓縮率）
- 實際編碼器（如 JPEG, MP3）試圖接近 R(D)

## 使用範例

```python
from rate_distortion import rate_distortion_function, lossy_compression_demo

# 計算率失真函數
p = 0.5
rd = rate_distortion_function(p, 0.5)
for d, r in rd[:5]:
    print(f"D={d:.2f}, R(D)={r:.4f}")

# 示範
lossy_compression_demo()
```

## 參考資料

- Shannon, C. E. (1948). A Mathematical Theory of Communication.
- Berger, T. (1971). Rate Distortion Theory: A Mathematical Basis for Data Compression.
- Blahut, R. E. (1972). Computation of Channel Capacity and Rate-Distortion Functions.
