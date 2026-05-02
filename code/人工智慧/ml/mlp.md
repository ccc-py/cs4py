# 多層感知機與反向傳播 (MLP & Backpropagation)

## 歷史背景

1969 年 Minsky 和 Papert 在《Perceptrons》中指出單層感知機無法解決 XOR 問題，導致神經網路研究進入第一次寒冬。1974 年 Paul Werbos 在其博士論文中首次提出反向傳播演算法，但當時未受重視。1986 年 Rumelhart, Hinton 和 Williams 在《Nature》上發表論文，系統性地展示了反向傳播如何訓練多層神經網路，引發了第二次神經網路熱潮，並成為現代深度學習的基石。

## 核心原理

### 前向傳播

數據從輸入層流向輸出層：
```
z = W · x + b
a = σ(z)  （激活函數）
```

### 激活函數

| 函數 | 公式 | 特性 |
|------|------|------|
| Sigmoid | 1/(1+e⁻ˣ) | 輸出 [0,1]，易梯度消失 |
| Tanh | (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | 輸出 [-1,1]，零中心化 |
| ReLU | max(0,x) | 解決梯度消失，現代主流 |

### 反向傳播

使用鏈式法則計算梯度：
```
∂Loss/∂W = ∂Loss/∂a · ∂a/∂z · ∂z/∂W
```

誤差從輸出層向輸入層逐層傳播：
1. 計算輸出層誤差
2. 對每個隱藏層，計算該層誤差並更新權重
3. 使用梯度下降更新參數：W = W - η · ∂Loss/∂W

### XOR 問題

| x1 | x2 | 輸出 |
|----|----|------|
| 0  | 0  | 0    |
| 0  | 1  | 1    |
| 1  | 0  | 1    |
| 1  | 1  | 0    |

XOR 是非線性可分問題，單層感知機無法解決，但加入一個隱藏層即可完美分類。

## 使用範例

```python
from ml.mlp import MLP

X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [[0], [1], [1], [0]]

mlp = MLP([2, 4, 1])  # 2輸入 → 4隱藏 → 1輸出
mlp.train(X, y, epochs=1000, lr=0.5)

# 預測
mlp.predict([[0, 1]])  # => [[0.95]]
```

## 複雜度

- **訓練**：O(E × N × Σ(n_i · n_{i+1}))，E 為 epochs，N 為樣本數，n_i 為每層神經元數
- **預測**：O(Σ(n_i · n_{i+1}))

## 參考資料

- Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. Nature.
- Werbos, P. J. (1974). Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences.
