# 資訊論 — 熵 (Entropy)

## 歷史背景

香農熵由克勞德·香農（Claude Shannon）於 1948 年在《通訊的數學理論》中提出，奠定了資訊論的基礎。熵量化了隨機變數的不確定性，成為資訊論中最核心的概念。

## 核心原理

### 香農熵
對於離散隨機變數 X，其熵定義為：

```
H(X) = -Σ p(x) * log₂(p(x))
```

單位為位元（bits），使用以 2 為底的對數。

### 聯合熵
兩個隨機變數 X, Y 的聯合熵：

```
H(X,Y) = -ΣΣ p(x,y) * log₂(p(x,y))
```

### 條件熵
給定 Y 時 X 的條件熵：

```
H(X|Y) = Σ p(y) * H(X|Y=y)
       = H(X,Y) - H(Y)
```

### 重要關係
- H(X,Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)
- H(X|Y) ≤ H(X)（條件熵不大於邊際熵）
- 當 X, Y 獨立時，H(X|Y) = H(X)

## 使用範例

```python
from entropy import shannon_entropy, joint_entropy, conditional_entropy

# 計算硬幣熵
fair_coin = [0.5, 0.5]
print(shannon_entropy(fair_coin))  # 1.0 bits

# 聯合與條件熵
joint = [[0.25, 0.25], [0.25, 0.25]]
print(joint_entropy(joint))              # 2.0 bits
print(conditional_entropy(joint, 'Y'))  # 1.0 bits
```

## 參考資料

- Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.
- Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory. Wiley.
