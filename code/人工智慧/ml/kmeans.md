# K-Means 分群演算法

## 歷史背景

K-Means 的核心概念最早由 Stuart Lloyd 於 1957 年在貝爾實驗室提出（稱為 Lloyd 演算法）。1967 年 James MacQueen 正式命名為 K-Means 並發表了收斂性分析。2006 年 David Arthur 和 Sergei Vassilvitskii 提出 K-Means++ 初始化方法，大幅改善了收斂速度和結果品質。

## 核心原理

### 演算法流程

1. **初始化**：選擇 k 個初始中心點
2. **分配**：將每個數據點分配到最近的中心點
3. **更新**：重新計算每個群集的中心點（均值）
4. **重複** 步驟 2-3 直到收斂（標籤不再改變或中心點移動小於閾值）

### K-Means++ 初始化

標準隨機初始化容易陷入局部最佳解。K-Means++ 改採概率選擇：
1. 隨機選擇第一個中心
2. 計算每個點到最近中心的距離 D(x)
3. 以 D(x)² 的概率選擇下一個中心
4. 重複直到選滿 k 個

### 評估指標

**WCSS（Within-Cluster Sum of Squares）**：
```
inertia = Σ ||x - μ_cluster||²
```

值越小表示群集越緊密。Elbow 方法透過繪製 k 對 inertia 的曲線來尋找最佳 k 值。

## 使用範例

```python
from ml.kmeans import kmeans

data = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]]
labels, centroids, inertia = kmeans(data, k=2, seed=42)

# 預測新數據點
from ml.kmeans import predict
cluster = predict([3, 4], centroids)
```

## 複雜度

- **時間**：O(n · k · d · i)，n 為數據點數，k 為群集數，d 為維度，i 為迭代次數
- **空間**：O(n · d + k · d)

## 限制

- 需要預先指定 k 值
- 對異常值敏感
- 只能發現凸形（球形）群集
- 結果依賴初始中心點

## 參考資料

- MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations.
- Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding.
