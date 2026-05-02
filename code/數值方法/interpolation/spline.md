# 三次樣條插值（Cubic Spline Interpolation）

## 歷史背景

樣條（Spline）一詞源自造船業，指一種柔軟的彈性細條，工匠將其壓過一系列點來繪製光艕曲線。數學上的樣條插值由伊薩克·舍恩貝格（Isaac Schoenberg）在 1946 年正式提出。

三次樣條因其在計算機輔助設計（CAD）、電腦圖學和數值分析中廣泛應用而成為最重要的插值方法之一。它能夠生成視覺上光艕的曲線，同時避免了高次多項式插值的龍格現象。

## 核心原理

### 基本思想

將插值區間 $[x_0, x_n]$ 分割為 $n$ 個子區間 $[x_{i-1}, x_i]$，在每個子區間上使用三次多項式：

$$
S_i(x) = a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3
$$

### 連續性條件

為了保證曲線光艕，樣條在內部節點處滿足：

1. **函數值連續**：$S_i(x_i) = y_i = S_{i+1}(x_i)$
2. **一階導數連續**：$S_i'(x_i) = S_{i+1}'(x_i)$（C¹ 連續）
3. **二階導數連續**：$S_i''(x_i) = S_{i+1}''(x_i)$（C² 連續）

### 自然樣條（Natural Spline）

自然樣條的邊界條件為：

$$
S''(x_0) = S''(x_n) = 0
$$

這使得曲線在端點處呈直線延伸（二階導數為零）。

### 求解方法

通過連續性條件，可以得到關於二階導數 $M_i = S_i''(x_i)$ 的三對角線性方程組：

$$
h_{i-1}M_{i-1} + 2(h_{i-1}+h_i)M_i + h_iM_{i+1} = 6\left(\frac{y_{i+1}-y_i}{h_i} - \frac{y_i-y_{i-1}}{h_{i-1}}\right)
$$

使用 **Thomas 算法**（特種高斯消去法），可以在 $O(n)$ 時間內求解。

## 使用範例

```python
from code.數值方法.interpolation.spline import cubic_spline

# 插值點
points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)]

# 構造自然樣條
s = cubic_spline(points, boundary="natural")

# 評估樣條
print(f"s(0.5) = {s(0.5)}")
print(f"s(1.5) = {s(1.5)}")
print(f"s(2.5) = {s(2.5)}")
```

## 優缺點

### 優點
- **光艕性好**：C² 連續，視覺上非常光艕
- **避免龍格現象**：分段低次，無邊緣震盪
- **計算效率高**：三對角矩陣可 $O(n)$ 求解
- **數值穩定**：相較於高次拉格朗日插值穩定得多

### 缺點
- **實作複雜**：需要求解三對角方程組
- **需要所有點**：增加一個點需要重新計算整個樣條
- **邊界條件敏感**：不同的邊界條件會影響結果

## 與拉格朗日插值比較

| 特性 | 拉格朗日插值 | 三次樣條 |
|------|------------|---------|
| 多項式次數 | $n$ 次（高次） | 3 次（分段低次） |
| 連續性 | $C^0$（僅函數值） | $C^2$（函數、一階、二階導數） |
| 龍格現象 | 有 | 無 |
| 計算複雜度 | $O(n^2)$ 每點 | $O(n)$ 預處理 |

## 參考資料

1. [Spline (Mathematics) - Wikipedia](https://en.wikipedia.org/wiki/Spline_(mathematics))
2. Schoenberg, I. J. (1946). "Contributions to the problem of approximation of equidistant data by analytic functions". *Quarterly of Applied Mathematics*, 4(2), 45-99.
3. de Boor, C. (2001). *A Practical Guide to Splines* (Revised ed.). Springer.
