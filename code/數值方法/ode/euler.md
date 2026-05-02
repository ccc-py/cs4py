# 尤拉方法（Euler's Method）

## 歷史背景

尤拉方法以瑞士數學家萊昂哈德·尤拉（Leonhard Euler）命名，他在 18 世紀提出了這個求解常微分方程（ODE）的最基本數值方法。雖然尤拉在許多數學領域都有開創性貢獻，但這個方法因其簡單性而成為數值分析入門教材的標準內容。

在現代科學計算中，尤拉方法因精度不足（一階方法）而很少直接用於實際問題。然而，它是理解更複雜方法（如龍格-庫塔法）的重要基礎，也是現代自適應步長算法（如 Runge-Kutta-Fehlberg）的組成部分。

## 核心原理

### 微分方程離散化

考慮一階常微分方程：

$$
\frac{dy}{dx} = f(x, y), \quad y(x_0) = y_0
$$

利用前向差分近似導數：

$$
y'(x_n) \approx \frac{y(x_{n+1}) - y(x_n)}{h}
$$

代入微分方程：

$$
\frac{y_{n+1} - y_n}{h} = f(x_n, y_n)
$$

得到尤拉法的迭代公式：

$$
y_{n+1} = y_n + h \cdot f(x_n, y_n)
$$

### 幾何直觀

從點 $(x_n, y_n)$ 出發，沿著切線方向（斜率為 $f(x_n, y_n)$）走一個步長 $h$，得到下一個點 $(x_{n+1}, y_{n+1})$。

### 誤差分析

尤拉法是一階方法，局部截斷誤差為 $O(h^2)$，全局誤差為 $O(h)$。每次將步長減半，誤差約減半。

## 使用範例

```python
from code.數值方法.ode.euler import euler

# 指數增長：dy/dx = y, y(0) = 1
f = lambda x, y: y
x_vals, y_vals = euler(f, 0.0, 1.0, h=0.1, steps=10)

for x, y in zip(x_vals, y_vals):
    print(f"x={x:.1f}, y={y:.6f}")
```

## 優缺點

### 優點
- **極簡單**：容易理解和實作
- **計算量小**：每步只需一次函數評估
- **數值穩定**：對於某些問題（如剛性方程）隱式尤拉法穩定性更好

### 缺點
- **精度低**：一階方法，誤差大
- **需要小步長**：為達到高精度需要大量步數
- **不適合剛性方程**：顯式尤拉法對剛性方程可能不穩定

## 與 RK4 比較

| 特性 | 尤拉法 | RK4 |
|------|--------|-----|
| 階數 | 1 | 4 |
| 每步函數評估次數 | 1 | 4 |
| 全局誤差 | $O(h)$ | $O(h^4)$ |
| 適用場景 | 教學、簡單問題 | 實際應用 |

## 參考資料

1. [Euler Method - Wikipedia](https://en.wikipedia.org/wiki/Euler_method)
2. Butcher, J. C. (2008). *Numerical Methods for Ordinary Differential Equations* (2nd ed.). Wiley.
3. Hairer, E., Nørsett, S. P., & Wanner, G. (1993). *Solving Ordinary Differential Equations I: Nonstiff Problems* (2nd ed.). Springer.
