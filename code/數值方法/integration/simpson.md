# 辛普森法則（Simpson's Rule）

## 歷史背景

辛普森法則由英國數學家托馬斯·辛普森（Thomas Simpson）於 1743 年提出，但這個方法的核心思想其實早在 17 世紀就由牛頓和萊布尼茨的追隨者們使用。辛普森將其系統化並推廣，因此以其名字命名。

這個方法本質上是用二次多項式（拋物線）來近似被積函數，比線性近似（梯形法則）更精確。在數值積分的發展史上，Simpson 法則是「牛頓-柯特斯公式」（Newton-Cotes formulas）家族中最重要的一員，其精度與計算複雜度達到了很好的平衡。

## 核心原理

### 公式推導

將區間 $[a, b]$ 分割為 $n$（$n$ 為偶數）個子區間，每兩個相鄰子區間組成一組，用穿過三點的二次多項式來近似：

$$
\int_a^b f(x) dx \approx \frac{h}{3} \left[ f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \cdots + 2f(x_{n-2}) + 4f(x_{n-1}) + f(x_n) \right]
$$

其中 $h = \frac{b-a}{n}$，係數模式為：$1, 4, 2, 4, 2, \ldots, 4, 1$。

### 誤差分析

辛普森法則的誤差為：

$$
E_S = -\frac{(b-a)^5}{180n^4} f^{(4)}(\xi), \quad \xi \in [a, b]
$$

誤差與 $n^4$ 成反比，即**四次收斂**。每次將 $n$ 加倍，誤差減為約 1/16。

### 精確性

Simpson 法則對於**三次及以下的多項式是精確的**（因為四次導數為零）。這使得它在許多實際應用中非常有效。

## 使用範例

```python
from code.數值方法.integration.simpson import simpson
import math

# ∫₀¹ x² dx = 1/3
result = simpson(lambda x: x**2, 0.0, 1.0, n=10)
print(f"近似值: {result}")

# ∫₀^π sin(x) dx = 2
result = simpson(math.sin, 0.0, math.pi, n=10)
print(f"近似值: {result}")
```

## 優缺點

### 優點
- **高精度**：四次收斂，遠優於梯形法則
- **對多項式精確**：三次以下多項式可精確積分
- **計算效率高**：達到給定精度所需的函數評估次數少

### 缺點
- **要求 n 為偶數**：區間數必須是偶數
- **要求四次可微**：對於四次導數很大的函數，誤差可能較大
- **不適合奇異點**：若被積函數有奇異點，效果會變差

## 與梯形法則比較

| 特性 | 梯形法則 | Simpson 法則 |
|------|---------|------------|
| 收斂階 | $O(h^2)$ | $O(h^4)$ |
| 所需區間數 | 多 | 少 |
| 對多項式精確性 | 一次以下 | 三次以下 |
| 實作複雜度 | 簡單 | 稍複雜 |

## 參考資料

1. [Simpson's Rule - Wikipedia](https://en.wikipedia.org/wiki/Simpson%27s_rule)
2. Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis* (9th ed.). Cengage Learning.
3. Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.
