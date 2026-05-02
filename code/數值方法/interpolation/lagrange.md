# 拉格朗日插值（Lagrange Interpolation）

## 歷史背景

拉格朗日插值以義大利-法國數學家約瑟夫·路易斯·拉格朗日（Joseph-Louis Lagrange）命名，他在 1795 年系統化了這個方法。然而，這個想法最早可追溯到 18 世紀初，由愛德蒙·哈雷（Edmond Halley，哈雷彗星的發現者）和艾薩克·牛頓（Isaac Newton）獨立發展。

在現代數值分析中，拉格朗日插值因為龍格現象（Runge's phenomenon）而不常用於高次插值。但它作為多項式插值的理論基礎，在數值分析教科書中始終佔有重要地位。實際應用中，分段低次插值（如樣條插值）更受青睞。

## 核心原理

### 插值問題

給定 $n+1$ 個點 $(x_0, y_0), (x_1, y_1), \ldots, (x_n, y_n)$，其中 $x_i$ 互不相同，要找到一個次數不超過 $n$ 的多項式 $P_n(x)$，使得 $P_n(x_i) = y_i$ 對所有 $i$ 成立。

### 拉格朗日基函數

拉格朗日插值的核心是構造 $n+1$ 個基函數 $L_j(x)$，滿足：

$$
L_j(x_i) = \delta_{ij} = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \neq j \end{cases}
$$

基函數的表達式為：

$$
L_j(x) = \prod_{\substack{i=0 \\ i \neq j}}^n \frac{x - x_i}{x_j - x_i}
$$

### 插值多項式

有了基函數，插值多項式可以寫為：

$$
P_n(x) = \sum_{j=0}^n y_j \cdot L_j(x)
$$

### 龍格現象

當使用等距點進行高次插值時，在區間邊緣會出現劇烈震盪，這就是**龍格現象**。以龍格函數 $f(x) = \frac{1}{1 + 25x^2}$ 為例，即使增加插值點，邊緣的誤差也不會減小，反而可能增大。

## 使用範例

```python
from code.數值方法.interpolation.lagrange import lagrange_interpolation

# 插值點
points = [(0.0, 1.0), (1.0, 3.0), (2.0, 7.0)]
p = lagrange_interpolation(points)

# 評估插值多項式
print(f"p(0) = {p(0)}")  # 應為 1.0
print(f"p(1) = {p(1)}")  # 應為 3.0
print(f"p(2) = {p(2)}")  # 應為 7.0
```

## 優缺點

### 優點
- **概念簡單**：公式直觀，易於理解和推導
- **無需求解線性方程組**：直接構造多項式
- **適合理論分析**：基函數的性質清晰

### 缺點
- **數值不穩定**：高次插值會出現龍格現象
- **不適合增點**：增加一個點，所有基函數都要重新計算
- **計算效率低**：每個點的評估需要 $O(n^2)$ 時間

## 與其他插值方法比較

| 方法 | 適用場景 | 計算複雜度 | 數值穩定性 |
|------|---------|-----------|-----------|
| 拉格朗日插值 | 理論教學、低次插值 | $O(n^2)$ 每點 | 差 |
| 牛頓插值 | 需頻繁增點 | $O(n^2)$ 預處理 | 中等 |
| 樣條插值 | 實際應用、平滑曲線 | $O(n)$ 預處理 | 好 |

## 參考資料

1. [Lagrange Polynomial - Wikipedia](https://en.wikipedia.org/wiki/Lagrange_polynomial)
2. Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis* (9th ed.). Cengage Learning.
3. Runge, C. (1901). "Über empirische Funktionen und die Interpolation zwischen äquidistanten Ordinaten". *Zeitschrift für Mathematik und Physik*, 46, 224-243.
