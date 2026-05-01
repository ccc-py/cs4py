# 決策樹 (Decision Tree)

## 歷史背景

決策樹的發展可追溯至 1970 年代。J. Ross Quinlan 於 1979 年提出 ID3 演算法，使用資訊增益作為分割標準。1986 年他改進為 C4.5，增加了對連續特徵和缺失值的處理。與此同時，Breiman、Friedman、Olshen 和 Stone 於 1984 年提出 CART（Classification and Regression Trees），使用基尼不純度作為分割標準，成為現代實現的主流方法。

## 核心原理

### 分割標準

**基尼不純度（Gini Impurity）**：
```
Gini(S) = 1 - Σ p_i²
```
p_i 為第 i 類在集合 S 中的比例。值越小表示越純淨。

**基尼增益**：
```
Gain = Gini(parent) - Σ (|S_j| / |S|) · Gini(S_j)
```

### 建構流程

1. 計算當前節點的不純度
2. 對每個特徵的每個可能閾值計算分割後的基尼增益
3. 選擇增益最大的特徵和閾值
4. 遞迴對子節點重複，直到終止條件滿足

### 終止條件

- 所有樣本屬於同一類別
- 達到最大深度
- 節點樣本數少於最小分割數
- 基尼增益小於閾值

## 使用範例

```python
from ml.decision_tree import DecisionTree

X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]

tree = DecisionTree(max_depth=3)
tree.fit(X, y)

# 預測
tree.predict([[0, 1], [1, 1]])  # 返回 [1, 0]

# 查看樹結構
print(tree.print_tree())
```

## 複雜度

- **訓練**：O(n · d · log n)，n 為樣本數，d 為特徵數
- **預測**：O(depth)，通常 depth ≈ log n
- **空間**：O(n)，儲存樹結構

## 優缺點

| 優點 | 缺點 |
|------|------|
| 易於理解和解釋 | 容易過擬合 |
| 不需要特徵縮放 | 對數據變化敏感 |
| 處理數值和類別特徵 | 不穩定（小變化導致不同樹） |
| 不需要假設數據分佈 | 偏向特徵值多的特徵 |

## 參考資料

- Quinlan, J. R. (1986). Induction of decision trees. Machine Learning.
- Breiman, L., et al. (1984). Classification and Regression Trees.
