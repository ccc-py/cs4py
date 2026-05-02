# 牛頓法（Newton's Method / Newton-Raphson）

## 歷史背景

牛頓法由艾薩克·牛頓（Isaac Newton）於 1669 年在《分析學》（De analysi per aequationes numero terminorum infinitas）中提出，最初用於求解多項式的實根。後來約瑟夫·拉弗森（Joseph Raphson）在 1690 年獨立提出了類似的簡化形式，因此常稱為牛頓-拉弗森法（Newton-Raphson method）。

這個方法在當時並未立即受到重視，直到 19 世紀才被廣泛應用於工程計算。如今，牛頓法及其變體是數值分析中最重要的求根演算法之一，廣泛應用於優化、機器學習（如邏輯回歸的參數估計）等領域。

## 核心原理

### 幾何直觀

牛頓法的核心思想是：在當前猜測值 $x_n$ 處，用函數的切線來近似原函數，然後取切線與 x 軸的交點作為下一個猜測值 $x_{n+1}$。

### 迭代公式

給定當前點 $x_n$，切線方程為：

$$
y = f(x_n) + f'(x_n)(x - x_n)
$$

令 $y = 0$，解出：

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

### 收斂性

若 $f(x)$ 在根 $r$ 附近二次可微，且 $f'(r) \neq 0$，則牛頓法具有**二次收斂**速度：

$$
|x_{n+1} - r| \leq C |x_n - r|^2
$$

這意味著每次迭代，有效位數約翻倍。

### 注意事項

1. **需要導數**：必須知道或能計算 $f'(x)$
2. **初始值敏感**：初始猜測值需足夠接近根，否則可能發散
3. **導數為零**：若 $f'(x_n) = 0$，則迭代無法繼續

## 使用範例

```python
from code.數值方法.root_finding.newton import newton

# 求 sqrt(2)，即解 x² - 2 = 0
f = lambda x: x**2 - 2
f_prime = lambda x: 2 * x
root, iters, history = newton(f, 1.5, f_prime, tol=1e-12)
print(f"sqrt(2) ≈ {root}, 迭代次數: {iters}")

# 使用數值微分（不提供導數函數）
root, iters, _ = newton(f, 1.5, tol=1e-10)
print(f"使用數值微分: {root}")
```

## 優缺點

### 優點
- **收斂速度快**：二次收斂，遠快於二分法
- **高精度**：少量迭代即可達到極高精度
- **可推廣**：可擴展至多元函數（牛頓法求解非線性方程組）

### 缺點
- **需要導數**：若無法解析求導，數值微分會增加計算量
- **初始值敏感**：初始猜測不佳可能導致發散
- **不保證收斂**：相較於二分法，牛頓法沒有全局收斂保證

## 參考資料

1. [Newton's Method - Wikipedia](https://en.wikipedia.org/wiki/Newton%27s_method)
2. Ypma, T. J. (1995). "Historical development of the Newton-Raphson method". *SIAM Review*, 37(4), 531-551.
3. Kelley, C. T. (2003). *Solving Nonlinear Equations with Newton's Method*. SIAM.
