# 割線法（Secant Method）

## 歷史背景

割線法是由牛頓法衍生而來的求根方法，最早可追溯到 17 世紀。相較於牛頓法需要計算導數，割線法僅需函數值，利用兩個前序點來近似導數。這個方法在實際應用中非常受歡迎，因為許多情況下導數難以計算或不存在解析形式。

「割線」一詞來自幾何學中的割線（secant line），即通過曲線上兩點的直線。割線法的幾何意義就是用這條割線與 x 軸的交點來逼近根。

## 核心原理

### 從牛頓法到割線法

牛頓法的迭代公式為：

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

當 $f'(x)$ 難以計算時，可以用差商近似導數：

$$
f'(x_n) \approx \frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}}
$$

代入牛頓法公式，得到割線法的迭代公式：

$$
x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}
$$

### 收斂性

割線法的收斂階為：

$$
p = \frac{1 + \sqrt{5}}{2} \approx 1.618
$$

即黃金比例。這是**超線性收斂**（superlinear convergence），收斂速度介於線性收斂（二分法）和二次收斂（牛頓法）之間。

### 收斂條件

若 $f(x)$ 在根附近足夠光滑，且初始值 $x_0, x_1$ 足夠接近根，則割線法收斂。

## 使用範例

```python
from code.數值方法.root_finding.secant import secant

# 求 sqrt(2)，即解 x² - 2 = 0
f = lambda x: x**2 - 2
root, iters, history = secant(f, 1.0, 2.0, tol=1e-12)
print(f"sqrt(2) ≈ {root}, 迭代次數: {iters}")

# 求解 x³ - x - 1 = 0
f = lambda x: x**3 - x - 1
root, iters, _ = secant(f, 1.0, 2.0, tol=1e-10)
print(f"根 ≈ {root}, f(root) = {f(root)}")
```

## 優缺點

### 優點
- **無需導數**：不需要計算或近似導數函數
- **收斂速度快**：超線性收斂，優於二分法
- **每步計算量小**：只需計算函數值，不需導數

### 缺點
- **需要兩個初始點**：比牛頓法多一個初始猜測
- **不保證收斂**：沒有像二分法那樣的全局收斂保證
- **收斂速度仍慢於牛頓法**：雖然差異不大

## 三種方法比較

| 方法 | 收斂速度 | 需要導數 | 初始條件 | 保證收斂 |
|------|---------|---------|---------|---------|
| 二分法 | 線性 | 否 | 區間 [a,b] 且 f(a)f(b)<0 | 是 |
| 割線法 | 超線性 (~1.618) | 否 | 兩個初始點 | 否 |
| 牛頓法 | 二次 | 是 | 一個初始點 | 否 |

## 參考資料

1. [Secant Method - Wikipedia](https://en.wikipedia.org/wiki/Secant_method)
2. Ostrowski, A. M. (1966). *Solution of Equations and Systems of Equations*. Academic Press.
3. Traub, J. F. (1964). *Iterative Methods for the Solution of Equations*. Prentice-Hall.
