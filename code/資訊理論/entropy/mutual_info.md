# 資訊論 — 互資訊與相關度量 (Mutual Information)

## 歷史背景

互資訊由香農引入，用於量化兩個隨機變數之間的相互依賴程度。KL 散度（Kullback-Leibler divergence）由所羅門·庫爾貝克和理查德·萊布勒於 1951 年提出，用於衡量兩個機率分佈的差異。

## 核心原理

### 互資訊
互資訊衡量兩個變數共享的資訊量：

```
I(X;Y) = ΣΣ p(x,y) * log₂(p(x,y) / (p(x)*p(y)))
       = H(X) + H(Y) - H(X,Y)
```

性質：
- I(X;Y) ≥ 0，當 X, Y 獨立時等於 0
- I(X;Y) = I(Y;X)（對稱）
- I(X;Y) = H(X) - H(X|Y)

### KL 散度（相對熵）
```
D_KL(P||Q) = Σ p(x) * log₂(p(x)/q(x))
```

性質：
- D_KL(P||Q) ≥ 0，當 P=Q 時等於 0
- **非對稱**：D_KL(P||Q) ≠ D_KL(Q||P)
- 不是真正的距離度量（不滿足對稱性和三角不等式）

### 交叉熵
```
H(P,Q) = -Σ p(x) * log₂(q(x))
       = H(P) + D_KL(P||Q)
```

常用於機器學習的損失函數。

## 使用範例

```python
from mutual_info import mutual_information, kl_divergence, cross_entropy

# 互資訊
joint = [[0.5, 0.0], [0.0, 0.5]]
print(mutual_information(joint))  # 1.0 bits（完全相關）

# KL 散度
p = [0.5, 0.5]
q = [0.8, 0.2]
print(kl_divergence(p, q))  # > 0

# 交叉熵
print(cross_entropy(p, q))
```

## 參考資料

- Kullback, S., & Leibler, R. A. (1951). On Information and Sufficiency. Annals of Mathematical Statistics.
- Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory. Wiley.
