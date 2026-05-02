# 蒙地卡羅積分 (Monte Carlo Integration)

## 歷史背景

蒙地卡羅方法以摩納哥的賭場城市「蒙地卡羅」命名，由 Stanislaw Ulam、John von Neumann 和 Nicholas Metropolis 在 1940 年代於洛斯阿拉莫斯國家實驗室開發。最初用於核武器研發中的中子擴散問題。

Ulam 在 1946 年意識到可以通過隨機抽樣來解決複雜的積分問題，這與他在賭博中觀察到的機率現象相似。此方法後來成為計算物理和金融工程中的重要工具。

## 核心原理

### 基本蒙地卡羅積分

對於一維積分 $\int_a^b f(x) dx$，利用期望值：

$$
\int_a^b f(x) dx = (b-a) \cdot \mathbb{E}[f(X)] \approx \frac{b-a}{N} \sum_{i=1}^N f(X_i)
$$

其中 $X_i \sim \text{Uniform}(a, b)$ 是均勻分佈的隨機變數。

### 誤差分析

蒙地卡羅積分的誤差為 $O(1/\sqrt{N})$，與維度無關。這使得它在高維積分問題中比傳統數值方法（如梯形法則、辛普森法則）更具優勢。

### 變異數縮減技術

1. **分層抽樣 (Stratified Sampling)**: 將積分區域分成多個子區域，每個區域獨立抽樣，減少估計的變異數。

2. **重要性抽樣 (Importance Sampling)**: 使用提議分佈 $g(x)$ 代替均勻分佈：
   $$
   \int f(x) dx = \int \frac{f(x)}{g(x)} g(x) dx
   $$
   選擇與 $f(x)$ 形狀相似的 $g(x)$ 可以降低變異數。

## 使用範例

```python
from monte_carlo.integration import monte_carlo_integration, stratified_sampling

# 定義被積函數 f(x) = x^2
def f(x: float) -> float:
    return x ** 2

# 蒙地卡羅估計 ∫_0^1 x^2 dx = 1/3
result = monte_carlo_integration(f, 0, 1, n_samples=10000)
print(f"估計值: {result:.6f}")  # 約 0.333

# 使用分層抽樣減少變異數
result_strat = stratified_sampling(f, 0, 1, n_samples=10000, n_strata=10)
print(f"分層抽樣: {result_strat:.6f}")
```

## 與傳統方法比較

| 方法 | 收斂速度 | 高維度表現 | 實作難度 |
|------|----------|------------|----------|
| 梯形法則 | O(1/N²) | 維度災難 | 簡單 |
| 辛普森法則 | O(1/N⁴) | 維度災難 | 中等 |
| 蒙地卡羅 | O(1/√N) | 優秀 | 簡單 |
| 準蒙地卡羅 | O(1/N) | 優秀 | 中等 |

## 參考資料

1. Metropolis, N., & Ulam, S. (1949). The Monte Carlo Method. *Journal of the American Statistical Association*, 44(247), 335-341.
2. Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer.
3. Kroese, D. P., Taimre, T., & Botev, Z. I. (2011). *Handbook of Monte Carlo Methods*. Wiley.
