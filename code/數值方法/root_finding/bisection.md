# 二分法（Bisection Method）

## 歷史背景

二分法是目前已知最古老的數值求根方法之一，其概念可追溯至古希臘時期。西元三世紀，希臘數學家張丘建（Zhang Qiujian）在其著作《張丘建算經》中已隱含二分搜尋的概念。現代數值分析中，二分法因其簡單性與可靠性，常被作為介紹數值求根的第一個演算法。

牛頓在 1669 年提出更高效的牛頓法後，二分法依然保有其地位——作為一個保證收斂的「兜底」方法，常在混合演算法中先用二分法將根鎖定在足夠小的區間內，再切換至牛頓法加速收斂。

## 核心原理

### 中間值定理（Intermediate Value Theorem）

若函數 $f(x)$ 在閉區間 $[a, b]$ 上連續，且 $f(a)$ 與 $f(b)$ 異號（即 $f(a) \cdot f(b) < 0$），則區間內至少存在一點 $c \in (a, b)$ 使得 $f(c) = 0$。

### 演算法步驟

1. 給定初始區間 $[a, b]$，確認 $f(a) \cdot f(b) < 0$
2. 計算中點 $c = \frac{a + b}{2}$
3. 計算 $f(c)$
4. 若 $|f(c)| < \text{tol}$ 或區間寬度 $b - a < \text{tol}$，停止並回傳 $c$
5. 否則，若 $f(a) \cdot f(c) < 0$，令 $b = c$；否則令 $a = c$
6. 重複步驟 2-5，直到滿足停止條件

### 收斂性

二分法的收斂速度為**線性收斂**，誤差上界為：

$$
|x_n - r| \leq \frac{b - a}{2^{n+1}}
$$

其中 $n$ 為迭代次數。每次迭代誤差約減半，與初始區間寬度無關。

## 使用範例

```python
from code.數值方法.root_finding.bisection import bisection

# 求 sqrt(2)，即解 x² - 2 = 0
f = lambda x: x**2 - 2
root, iters, history = bisection(f, 1.0, 2.0, tol=1e-10)
print(f"sqrt(2) ≈ {root}, 迭代次數: {iters}")

# 求解 x³ - x - 1 = 0
f = lambda x: x**3 - x - 1
root, iters, _ = bisection(f, 1.0, 2.0, tol=1e-10)
print(f"根 ≈ {root}, f(root) = {f(root)}")
```

## 優缺點

### 優點
- **保證收斂**：只要初始區間滿足異號條件且函數連續
- **實作簡單**：邏輯直觀，不易出錯
- **穩健性高**：不依賴導數，對函數性質要求低

### 缺點
- **收斂速度慢**：線性收斂，需要較多迭代
- **需要初始區間**：必須事先知道根所在的區間
- **僅適用一維**：無法直接推廣至高維問題

## 參考資料

1. [Bisection Method - Wikipedia](https://en.wikipedia.org/wiki/Bisection_method)
2. Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis* (9th ed.). Cengage Learning.
3. Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.
