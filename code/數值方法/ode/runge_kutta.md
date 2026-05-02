# 龍格-庫塔法（Runge-Kutta Methods）

## 歷史背景

龍格-庫塔法由德國數學家卡爾·龍格（Carl Runge）和馬丁·庫塔（Martin Kutta）在 19 世紀末至 20 世紀初發展。龍格在 1895 年提出了最早的版本，庫塔在 1901 年將其推廣至四階方法。

四階龍格-庫塔法（RK4）因其優異的精度與計算成本比而成為工程界最常用的 ODE 求解器。從 NASA 的阿波羅計畫到現代氣候模型，RK4 被廣泛應用於各種科學和工程領域。現代的自適應步長求解器（如 MATLAB 的 ode45）也是基於龍格-庫塔法的變體。

## 核心原理

### RK4 公式

對於 ODE $dy/dx = f(x, y)$，RK4 的迭代公式為：

$$
\begin{align}
k_1 &= h \cdot f(x_n, y_n) \\
k_2 &= h \cdot f(x_n + \frac{h}{2}, y_n + \frac{k_1}{2}) \\
k_3 &= h \cdot f(x_n + \frac{h}{2}, y_n + \frac{k_2}{2}) \\
k_4 &= h \cdot f(x_n + h, y_n + k_3) \\
y_{n+1} &= y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)
\end{align}
$$

### 幾何直觀

RK4 通過計算四個不同點的斜率（區間左端、兩次中點、右端），然後取加權平均。這相當於在區間內對斜率進行了 Simpson 積分式的加權。

### 精度分析

RK4 是四階方法：
- 局部截斷誤差：$O(h^5)$
- 全局誤差：$O(h^4)$

每次將步長減半，誤差約減為 1/16。

### 與尤拉法的比較

| 特性 | 尤拉法 | RK4 |
|------|--------|-----|
| 斜率計算次數 | 1 | 4 |
| 階數 | 1 | 4 |
| 全局誤差 | $O(h)$ | $O(h^4)$ |
| 相對計算量 | 1x | ~4x |
| 相對精度 | 低 | 高 |

對於相同的精度要求，RK4 可以使用更大的步長，總體計算量通常更少。

## 使用範例

```python
from code.數值方法.ode.runge_kutta import runge_kutta_4

# 指數增長：dy/dx = y, y(0) = 1
f = lambda x, y: y
x_vals, y_vals = runge_kutta_4(f, 0.0, 1.0, h=0.1, steps=10)

for x, y in zip(x_vals, y_vals):
    print(f"x={x:.1f}, y={y:.6f}")

# 邏輯方程
f = lambda t, y: y * (1 - y / 10.0)
t_vals, y_vals = runge_kutta_4(f, 0.0, 1.0, h=0.1, steps=50)
```

## 優缺點

### 優點
- **高精度**：四階精度，誤差小
- **無需計算導數**：不像牛頓法需要導數資訊
- **數值穩定**：對於非剛性問題穩定性良好
- **廣泛適用**：適用於大多數非剛性 ODE

### 缺點
- **計算量較大**：每步需要 4 次函數評估
- **不適合剛性方程**：對於剛性問題可能不穩定（需使用隱式方法）
- **無內建誤差估計**：標準 RK4 無法自動調整步長（需使用 RK45 等變體）

## 參考資料

1. [Runge-Kutta Methods - Wikipedia](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)
2. Butcher, J. C. (2008). *Numerical Methods for Ordinary Differential Equations* (2nd ed.). Wiley.
3. Hairer, E., Nørsett, S. P., & Wanner, G. (1993). *Solving Ordinary Differential Equations I: Nonstiff Problems* (2nd ed.). Springer.
