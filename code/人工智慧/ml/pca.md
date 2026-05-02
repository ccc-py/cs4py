# 主成分分析 (Principal Component Analysis, PCA)

## 歷史背景

主成分分析 (PCA) 的數學基礎最早由英國統計學家**卡爾·皮爾森 (Karl Pearson)** 於 1901 年提出，當時稱為「主軸定理」(Principal Axis Theorem)，他用於找出資料分佈的主要方向。

1933 年，美國統計學家**哈羅德·霍特林 (Harold Hotelling)** 將此方法推廣至多變量統計分析，正式命名為 Principal Component Analysis。霍特林還證明了 PCA 與因子分析 (Factor Analysis) 的關係。

現代機器學習中，PCA 是最廣泛使用的無監督降維技術，應用範圍包括：
- 資料壓縮（如影像壓縮）
- 資料視覺化（高維資料降至 2D/3D）
- 雜訊過濾（去除低變異成分）
- 特徵提取（作為預處理步驟）

## 核心原理

### 變異數與共變異數

給定一個資料矩陣 X (n 個樣本 × d 個特徵)，首先將資料中心化（減去均值）：

```
X_centered = X - μ
```

共變異數矩陣 C 描述了各特徵間的線性關係：

```
C = (1/(n-1)) × XᵀX
```

其中 Cᵢⱼ 表示第 i 個和第 j 個特徵的共變異數。

### 特徵分解 (Eigendecomposition)

PCA 的核心是對共變異數矩陣進行特徵分解：

```
C = V Λ Vᵀ
```

其中：
- **V**：特徵向量矩陣，每行是一個主成分方向
- **Λ**：對角矩陣，對角線元素為特徵值（變異數）

### 主成分

- **第一主成分**：特徵值最大的特徵向量方向，是資料變異最大的方向
- **第二主成分**：與第一主成分正交（不相關），剩餘變異最大的方向
- 以此類推...

### 降維

選取前 k 個主成分，將原始資料投影到這些方向上：

```
X_reduced = X_centered × V_k
```

其中 V_k 為前 k 個主成分組成的矩陣。

### 變異解釋比例

```
解釋比例_i = λ_i / Σ λ_j
```

累積解釋比例表示保留了多少原始資訊。

### 冪迭代法 (Power Iteration)

本實作使用冪迭代法求特徵向量，而非直接使用 SVD：
1. 隨機初始化向量 v
2. 反覆計算 v = Cv / ||Cv||
3. 收斂後的 v 即為最大特徵值對應的特徵向量
4. 使用 deflation 移除該方向，繼續求下一個主成分

## 使用範例

### 2D 到 1D 降維

```python
from ml.pca import PCA

# 2D 資料（沿對角線分佈）
X = [
    [1.0, 1.1],
    [2.0, 2.1],
    [3.0, 2.9],
    [4.0, 4.2],
]

# 擬合 PCA
pca = PCA(n_components=1)
X_reduced = pca.fit_transform(X)

print(f"主成分方向: {pca.components_[0]}")
print(f"降維後: {X_reduced}")
```

### 查看變異解釋比例

```python
pca = PCA(n_components=2)
pca.fit(X)

ratio = pca.explained_variance_ratio()
print(f"PC1 解釋: {ratio[0]:.2%}")
print(f"PC2 解釋: {ratio[1]:.2%}")
```

### 3D 到 2D 降維

```python
# 3D 資料
X_3d = [
    [1.0, 2.0, 1.5],
    [2.0, 3.0, 2.5],
    # ...
]

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_3d)
```

## 複雜度

使用冪迭代法實作的 PCA：

- **訓練時間**：O(n_components × (d² × iterations + n × d))
  - n: 樣本數, d: 特徵數, iterations: 冪迭代次數
- **轉換時間**：O(n × d × n_components)
- **空間**：O(n × d + d²)

與 SVD 方法比較：
- SVD: O(min(n×d², d×n²))
- 冪迭代: 適合大型稀疏矩陣，可增量計算

## 優缺點

### 優點
- 無監督學習，不需要標籤
- 降維同時保留最大變異
- 去除特徵間的相關性
- 可用於資料壓縮和視覺化

### 缺點
- 僅能捕捉線性關係（非線性需使用 Kernel PCA）
- 對資料縮放敏感（建議先標準化）
- 主成分的解釋性可能不如原始特徵
- 對異常值敏感（可用 Robust PCA 改進）

## 參考資料

1. Pearson, K. (1901). "On Lines and Planes of Closest Fit to Systems of Points in Space"
2. Hotelling, H. (1933). "Analysis of a complex of statistical variables into principal components"
3. Jolliffe, I. T. (2002). "Principal Component Analysis" (2nd Edition)
4. Bishop, C. M. (2006). "Pattern Recognition and Machine Learning" - Chapter 12
5. 維基百科: https://en.wikipedia.org/wiki/Principal_component_analysis
