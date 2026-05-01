# K-近鄰演算法 (K-Nearest Neighbors)

## 歷史背景

KNN 最早由 Evelyn Fix 和 Joseph Hodges 於 1951 年作為非參數統計方法提出。1967 年 Thomas Cover 和 Peter Hart 發表了系統性分析，證明了 KNN 的錯誤率上限不超過貝葉斯錯誤率的兩倍。KNN 是最早的機器學習演算法之一，至今仍在許多應用中表現出色。

## 核心原理

### 演算法

KNN 是一種「惰性學習」方法：訓練階段只儲存數據，預測時才進行計算。

1. 計算測試點與所有訓練點的距離
2. 選取 k 個最近的鄰居
3. 多數投票（或距離加權投票）決定類別

### 距離度量

| 距離 | 公式 | 適用場景 |
|------|------|---------|
| 歐幾里得 | √Σ(x_i - y_i)² | 連續數值特徵 |
| 曼哈頓 | Σ|x_i - y_i| | 高維稀疏數據 |
| 閔可夫斯基 | (Σ|x_i - y_i|^p)^(1/p) | 通用 |

### K 值選擇

- **k 太小**：模型複雜，易受雜訊影響（過擬合）
- **k 太大**：模型過於平滑，忽略局部結構（欠擬合）
- **經驗法則**：k ≈ √n（n 為訓練樣本數）

## 使用範例

```python
from ml.knn import KNNClassifier

X = [[1.0, 2.0], [5.0, 5.0], [1.0, 8.0]]
y = ["A", "B", "C"]

knn = KNNClassifier(k=3, weighted=True)
knn.fit(X, y)

# 預測
knn.predict_one([3.0, 4.0])  # 返回類別

# 獲取概率
knn.predict_proba([3.0, 4.0])  # 返回 {"A": 0.3, "B": 0.5, "C": 0.2}
```

## 複雜度

- **訓練**：O(1)，僅儲存數據
- **預測**：O(n × d)，n 為訓練樣本數，d 為特徵維度
- **空間**：O(n × d)，需儲存所有訓練數據

## 優缺點

| 優點 | 缺點 |
|------|------|
| 簡單易實現 | 預測速度慢 |
| 不需要訓練 | 需要大量記憶體 |
| 對數據分佈無假設 | 對不相關特徵敏感 |
| 天然支援多類別 | 需要特徵縮放 |

## 參考資料

- Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory.
- Fix, E., & Hodges, J. L. (1951). Discriminatory Analysis: Nonparametric Discrimination.
