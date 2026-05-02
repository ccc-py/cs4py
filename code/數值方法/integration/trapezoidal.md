# 梯形法則（Trapezoidal Rule）

## 歷史背景

梯形法則是數值積分中最古老、最直觀的方法之一。其概念可追溯到古希臘時期——將曲邊梯形分割為多個小梯形來近似面積。在牛頓-萊布尼茨公式（微積分基本定理）出現之前，這種幾何近似是計算積分的主要方法。

現代數值分析中，梯形法則常以「複合梯形法則」（Composite Trapezoidal Rule）的形式出現，即將區間 $[a, b]$ 分割為 $n$ 個子區間，分別應用梯形公式再求和。這種方法雖然簡單，但在許多實際應用中（如數值求解微分方程）扮演重要角色。

## 核心原理

### 公式推導

對於單個區間 $[x_i, x_{i+1}]$，梯形面積為：

$$
\int_{x_i}^{x_{i+1}} f(x) dx \approx \frac{h}{2} [f(x_i) + f(x_{i+1})]
$$

其中 $h = x_{i+1} - x_i$。

將整個區間 $[a, b]$ 分割為 $n$ 等份，得到複合梯形法則：

$$
\int_a^b f(x) dx \approx \frac{h}{2} \left[ f(a) + 2\sum_{i=1}^{n-1} f(x_i) + f(b) \right]
$$

其中 $h = \frac{b-a}{n}$，$x_i = a + ih$。

### 誤差分析

梯形法則的誤差為：

$$
E_T = -\frac{(b-a)^3}{12n^2} f''(\xi), \quad \xi \in [a, b]
$$

誤差與 $n^2$ 成反比，即**線性收斂**（每次將 $n$ 加倍，誤差減為約 1/4）。

### Richardson 外推

利用梯形法則的誤差結構，可以通過 Richardson 外推提高精度：

$$
I_{\text{extrapolated}} = \frac{4I_{2n} - I_n}{3}
$$

這給出了 $O(h^4)$ 精度的結果，相當於 Simpson 法則。

## 使用範例

```python
from code.數值方法.integration.trapezoidal import trapezoidal
import math

# ∫₀¹ x² dx = 1/3
result = trapezoidal(lambda x: x**2, 0.0, 1.0, n=100)
print(f"近似值: {result}")

# ∫₀^π sin(x) dx = 2
result = trapezoidal(math.sin, 0.0, math.pi, n=1000)
print(f"近似值: {result}")
```

## 優缺點

### 優點
- **簡單直觀**：容易理解和實作
- **穩健性好**：對於平滑函數效果穩定
- **可自適應**：容易實作自適應版本（根據局部誤差調整步長）

### 缺點
- **收斂速度慢**：線性收斂，需要較多區間分割
- **精度有限**：對於給定的 $n$，精度不如 Simpson 法則
- **要求函數二階可微**：否則誤差估計不準確

## 參考資料

1. [Trapezoidal Rule - Wikipedia](https://en.wikipedia.org/wiki/Trapezoidal_rule)
2. Atkinson, K. E. (2008). *An Introduction to Numerical Analysis* (2nd ed.). Wiley.
3. Stoer, J., & Bulirsch, R. (2002). *Introduction to Numerical Analysis* (3rd ed.). Springer.
