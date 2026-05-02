# 線性迴歸 (Linear Regression)

## 歷史背景

線性迴歸是統計學和機器學習中最基礎的迴歸方法。其數學基礎——最小平方法 (Method of Least Squares)——最早由法國數學家**勒讓德 (Adrien-Marie Legendre)** 於 1805 年在《Nouvelles méthodes pour la détermination des orbites des comètes》中提出。

同年（1809 年），德國數學家**高斯 (Carl Friedrich Gauss)** 在《Theoria Motus Corporum Coelestium》中獨立發展了相同的方法，並聲稱他早在 1795 年就已發明。高斯將此方法應用於天文學，成功預測了穀神星 (Ceres) 的軌道位置，這是當時數學史上的重大成就。

梯度下降法 (Gradient Descent) 則由法國數學家 **Augustin-Louis Cauchy** 於 1847 年提出，用於解決數值最佳化問題。現代深度學習中，梯度下降及其變體（SGD、Adam 等）是神經網路訓練的核心。

## 核心原理

### 線性模型

線性迴歸假設目標變數 y 與特徵 x 成線性關係：

```
y = w₀ + w₁x₁ + w₂x₂ + ... + wₙxₙ + ε
  = w · x + b + ε
```

其中：
- **w**：權重向量 (weights)
- **b**：偏置 (bias/intercept)
- **ε**：誤差項，通常假設服從常態分佈

### 損失函數：均方誤差 (MSE)

```
MSE = (1/N) Σ (y_pred⁽ⁱ⁾ - y⁽ⁱ⁾)²
    = (1/N) ||Xw - y||²
```

### 正規方程 (Normal Equation)

對 MSE 求導並設為零，得到解析解：

```
w = (XᵀX)⁻¹ Xᵀ y
```

這個方法不需要迭代，直接計算出最優解。但當特徵數量很大時，矩陣求逆的計算成本為 O(n³)，效率較差。

### 梯度下降 (Gradient Descent)

迭代更新參數：

```
w = w - η × ∇L(w)
```

其中梯度為：
```
∂L/∂w_j = (2/N) Σ (y_pred - y_true) × x_j
∂L/∂b   = (2/N) Σ (y_pred - y_true)
```

η 為學習率 (learning rate)。

### 決定係數 R²

衡量模型擬合程度的指標：

```
R² = 1 - SS_res / SS_tot
```

其中 SS_res 為殘差平方和，SS_tot 為總平方和。R² 越接近 1 表示擬合越好。

## 使用範例

### 簡單線性迴歸

```python
from ml.linear_regression import LinearRegression

# 資料：y = 2x + 1
X = [[1], [2], [3], [4], [5]]
y = [3, 5, 7, 9, 11]

# 使用正規方程
model = LinearRegression(fit_intercept=True)
model.fit_normal_equation(X, y)

print(f"權重: {model.weights[0]:.2f}")  # 約 2.00
print(f"偏置: {model.bias:.2f}")        # 約 1.00

# 預測
print(model.predict([[6]]))  # 輸出約 [13.0]
```

### 梯度下降

```python
from ml.linear_regression import LinearRegression

model = LinearRegression(fit_intercept=True)
model.fit_gradient_descent(
    X, y,
    learning_rate=0.01,
    epochs=2000,
    verbose=True
)
```

### 多元線性迴歸

```python
# 三個特徵：y = 1.5x₁ - 0.8x₂ + 2.0x₃ + 3.0
X = [
    [1.0, 2.0, 3.0],
    [2.0, 3.0, 4.0],
    # ...
]
y = [7.9, 11.4, ...]

model = LinearRegression(fit_intercept=True)
model.fit_normal_equation(X, y)
print(f"R² = {model.score(X, y):.4f}")
```

## 複雜度

### 正規方程
- **訓練時間**：O(n³ + n²d + nd²)，n 為樣本數，d 為特徵數
- **預測時間**：O(d)
- **空間**：O(nd + d²)

### 梯度下降
- **訓練時間**：O(epochs × n × d)
- **預測時間**：O(d)
- **空間**：O(nd)

## 優缺點

### 優點
- 簡單易懂，解釋性強
- 訓練和預測速度快
- 不需要太多調參
- 當特徵數不多時，正規方程給出精確解

### 缺點
- 假設特徵與目標成線性關係
- 對異常值敏感（MSE 會放大異常值的影響）
- 特徵間共線性 (collinearity) 會導致不穩定
- 正規方程在大特徵數時計算昂貴

## 參考資料

1. Legendre, A. M. (1805). "Nouvelles méthodes pour la détermination des orbites des comètes"
2. Gauss, C. F. (1809). "Theoria Motus Corporum Coelestium"
3. Cauchy, A. L. (1847). "Méthode générale pour la résolution des systèmes d'équations simultanées"
4. Hastie, T. et al. (2009). "The Elements of Statistical Learning" - Chapter 3
5. 維基百科: https://en.wikipedia.org/wiki/Linear_regression
