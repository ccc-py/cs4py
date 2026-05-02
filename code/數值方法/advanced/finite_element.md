# 有限元素法 (Finite Element Method, FEM)

## 歷史背景

有限元素法的概念最早由 Courant 在 1943 年提出，他使用三角形元素和變分原理求解扭轉問題。但受限於計算能力，此方法未能實用化。

1960 年，Clough 和 Turner 在 their paper "Finite Element Analysis of Two-Dimensional Stress" 中首次使用「有限元素法」這個名稱，被視為現代 FEM 的起點。

1965 年，Zienkiewicz 和 Cheung 將 FEM 推廣到一般性的偏微分方程，使其成為工程領域的通用工具。

現今 FEM 廣泛應用於：
- 結構分析（橋梁、建築、飛機）
- 熱傳導分析
- 流體力學（CFD）
- 電磁場分析
- 生物醫學工程

## 核心原理

### 弱形式（Galerkin 方法）

將 Poisson 方程 $-u'' = f$ 乘上測試函數 $v$ 並積分：

$$\int_0^1 u' v' \, dx = \int_0^1 f v \, dx$$

使用分段線性基底函數 $\phi_i(x)$ 近似 $u \approx \sum u_j \phi_j$，得到：

$$\mathbf{K} \mathbf{u} = \mathbf{F}$$

其中 $K_{ij} = \int \phi_i' \phi_j' dx$，$F_i = \int f \phi_i dx$

### 線性基底函數

每個基底函數 $\phi_i$ 在節點 $i$ 處為 1，在相鄰節點處為 0：

```
φ_i(x) = (x - x_{i-1})/(x_i - x_{i-1})  當 x_{i-1} ≤ x ≤ x_i
φ_i(x) = (x_{i+1} - x)/(x_{i+1} - x_i)  當 x_i ≤ x ≤ x_{i+1}
φ_i(x) = 0                               其他
```

### 剛度矩陣組裝

對於均勻分割，剛度矩陣為三對角：

```
K = | 1  -1   0   0  ... |
    | -1   2  -1   0  ... |
    |  0  -1   2  -1  ... |
    |        ...        |
```

## 使用範例

```python
from finite_element import solve_poisson_1d
import math

# 求解 -u'' = 1, u(0) = u(1) = 0
f = lambda x: 1.0
nodes, u = solve_poisson_1d(f, 0.0, 1.0, 0.0, 0.0, num_elements=16)

# 求解 -u'' = sin(x), u(0) = u(π) = 0
f_sin = lambda x: math.sin(x)
nodes, u = solve_poisson_1d(f_sin, 0.0, math.pi, 0.0, 0.0, num_elements=20)
```

## 參考資料

- Hughes, T. J. R. *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis* (1987)
- Zienkiewicz, O. C. & Taylor, R. L. *The Finite Element Method* (第 7 版)
- Brenner, S. & Scott, R. *The Mathematical Theory of Finite Element Methods* (第 3 版)