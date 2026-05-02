# 有限差分法 (Finite Difference Method)

## 歷史背景

有限差分法的根源可追溯至 17 世紀，牛頓和萊布尼茲發展微積分時就已經使用差商近似導數的概念。然而，作為系統性求解偏微分方程的數值方法，有限差分法在 20 世紀隨著電子計算機的發明而迅速發展。

1950 年代，Richtmyer 和 Lax 等人建立了有限差分法的理論基礎。各種數值格式陸續被提出：

- **顯式格式**：直接計算，簡單但有穩定性限制
- **隱式格式**：需要求解線性系統，但無條件穩定
- **Crank-Nicolson 格式**：二階精度且無條件穩定

這些方法廣泛應用於：
- 熱傳導與擴散問題
- 流體力學（Navier-Stokes 方程）
- 金融工程（Black-Scholes 方程）
- 電磁場計算

## 核心原理

### 差分近似

將連續定義域離散化為有限個格點，用差商近似導數：

```
前向差分：f'(x) ≈ (f(x+h) - f(x)) / h        — O(h)
後向差分：f'(x) ≈ (f(x) - f(x-h)) / h        — O(h)
中央差分：f'(x) ≈ (f(x+h) - f(x-h)) / (2h)  — O(h²)
```

二階導數：
```
f''(x) ≈ (f(x+h) - 2f(x) + f(x-h)) / h²     — O(h²)
```

### 熱傳導方程

一維熱傳導方程：
$$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$$

離散化後（顯式格式）：
$$u_i^{n+1} = u_i^n + r(u_{i+1}^n - 2u_i^n + u_{i-1}^n)$$

其中 $r = \alpha \Delta t / \Delta x^2$

### 穩定性條件

顯式格式的 CFL 條件：$r \leq 0.5$
隱式格式：無條件穩定

## 使用範例

```python
from finite_difference import (
    forward_difference, backward_difference, central_difference,
    solve_heat_equation, solve_heat_implicit
)
import math

# 導數近似
f = math.sin
x = 1.0
h = 0.001
approx = central_difference(f, x, h)  # 近似 cos(1.0)

# 熱傳導方程
u0 = [100 if 20 <= i <= 30 else 0 for i in range(50)]
u_result = solve_heat_equation(u0, alpha=0.01, dx=0.1, dt=0.001, nt=100)
```

## 參考資料

- Press, W. H., et al. *Numerical Recipes: The Art of Scientific Computing* (第 3 版)
- Richtmyer, R. D. & Morton, K. W. *Difference Methods for Initial-Value Problems* (1967)
- Stoer, J. & Bulirsch, R. *Introduction to Numerical Analysis* (第 3 版)