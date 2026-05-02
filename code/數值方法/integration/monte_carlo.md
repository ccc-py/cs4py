# 蒙地卡羅積分（Monte Carlo Integration）

## 歷史背景

蒙地卡羅方法得名於摩納哥的蒙地卡羅賭場，由斯坦尼斯瓦夫·烏拉姆（Stanisław Ulam）、約翰·馮·諾伊曼（John von Neumann）和尼古拉斯·梅特羅波利斯（Nicholas Metropolis）等人在 1940 年代末期於洛斯阿拉莫斯國家實驗室（Los Alamos National Laboratory）發展。當時的目的是為氫彈研製中的中子擴散問題進行數值模擬。

這個方法的核心思想是利用大數定律：通過大量隨機抽樣來估計積分值。隨著現代計算機的發展，蒙地卡羅方法已成為物理、金融、工程等領域中處理高維積分和複雜隨機系統的標準工具。

## 核心原理

### 一維積分

對於一維積分 $\int_a^b f(x) dx$，可以將其視為函數在區間上的平均值乘以區間長度：

$$
\int_a^b f(x) dx = (b - a) \cdot \mathbb{E}[f(X)], \quad X \sim \text{Uniform}(a, b)
$$

通過隨機抽樣 $X_1, X_2, \ldots, X_N \sim \text{Uniform}(a, b)$，用樣本均值估計：

$$
\hat{I} = \frac{b - a}{N} \sum_{i=1}^N f(X_i)
$$

### 高維積分

對於 $d$ 維積分：

$$
\int_{a_1}^{b_1} \cdots \int_{a_d}^{b_d} f(\mathbf{x}) d\mathbf{x} = V \cdot \mathbb{E}[f(\mathbf{X})]
$$

其中 $V = \prod_{i=1}^d (b_i - a_i)$ 是超矩形的體積。

### 誤差分析

蒙地卡羅積分的誤差（標準差）為：

$$
\text{StdErr} = \frac{V \cdot \sigma}{\sqrt{N}}
$$

其中 $\sigma^2$ 是 $f(X)$ 的方差。注意誤差與 $N^{-1/2}$ 成正比，與維度 $d$ **無關**！這是蒙地卡羅方法在高維情況下相較於確定性方法（如梯形法則、Simpson 法則）的最大優勢。

### 收斂速度

蒙地卡羅積分具有**平方根收斂**（$O(N^{-1/2})$），這比確定性方法的收斂速度慢。但是，確定性方法的複雜度會隨維度指數增長，而蒙地卡羅方法不會。

## 使用範例

```python
from code.數值方法.integration.monte_carlo import monte_carlo_1d, estimate_pi
import math

# ∫₀¹ e^x dx
result, error = monte_carlo_1d(math.exp, 0.0, 1.0, N=10000)
print(f"估值: {result}, 標準誤差: {error}")

# 估計 π
pi_est, pi_err = estimate_pi(N=100000)
print(f"π 估值: {pi_est}, 誤差: {abs(pi_est - math.pi)}")
```

## 優缺點

### 優點
- **維度無關**：收斂速度不隨維度增加而變慢
- **適用於複雜區域**：不需要規則的積分區域
- **容易實作**：邏輯簡單，只需要隨機數生成器

### 缺點
- **收斂速度慢**：只有 $O(N^{-1/2})$ 的收斂速度
- **誤差隨機**：結果每次運行都不同，有統計誤差
- **需要大量樣本**：為達到高精度，需要非常多的抽樣點

## 與確定性方法比較

| 特性 | 蒙地卡羅 | 梯形/Simpson |
|------|---------|-------------|
| 收斂速度 | $O(N^{-1/2})$ | $O(N^{-p})$ ($p=2$ 或 $4$) |
| 維度影響 | 無 | 指數增長 |
| 適用維度 | 任意 | 低維（1-3 維） |
| 實作難度 | 簡單 | 中等 |

## 參考資料

1. [Monte Carlo Integration - Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_integration)
2. Kroese, D. P., et al. (2011). *Handbook of Monte Carlo Methods*. Wiley.
3. Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods* (2nd ed.). Springer.
