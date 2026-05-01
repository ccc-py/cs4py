# 感知機 (Perceptron)

## 歷史背景

感知機由 Frank Rosenblatt 於 1957 年在康乃爾大學航空實驗室發明，是第一個人工神經網路模型，能夠從資料中學習。1962 年 Rosenblatt 出版《Principles of Neurodynamics》詳細描述此模型。

然而，1969 年 Marvin Minsky 和 Seymour Papert 在《Perceptrons》一書中證明感知機無法解決 XOR 等線性不可分問題。此結果導致第一次 AI 寒冬，但也間接推動了多層網路和反向傳播演算法的發展。

## 核心原理

### 數學模型

```
輸出 y = sign(w · x + b)
```

其中：
- **w**：權重向量
- **x**：輸入向量
- **b**：偏置（bias）
- **sign**：階躍函數，≥ 0 輸出 1，否則輸出 0

### 學習規則

```
w = w + η * (y_true - y_pred) * x
b = b + η * (y_true - y_pred)
```

其中 η 為學習率。

### 收斂定理

若訓練資料線性可分，感知機學習規則保證在有限步數內收斂。對於非線性可分問題（如 XOR），感知機會持續振盪無法收斂。

## 使用範例

```python
from ml.perceptron import Perceptron

# 訓練 AND 閘
data = [
    ([0, 0], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([1, 1], 1),
]

perceptron = Perceptron(n_inputs=2, learning_rate=0.1)
perceptron.train(data, epochs=100)

# 預測
print(perceptron.predict([1, 1]))  # 輸出 1
```

## 複雜度

- **時間**：O(n · d · E)，n 為特徵數，d 為資料筆數，E 為收斂所需 epoch 數
- **空間**：O(n)，僅需儲存權重和偏置

## 限制與延伸

感知機無法解決非線性可分問題。後續發展包括：
- 多層感知機（MLP）
- 反向傳播演算法
- 核方法（Kernel Methods）
- 支援向量機（SVM）

## 參考資料

- Rosenblatt, F. (1958). The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain. Psychological Review.
- Minsky, M., & Papert, S. (1969). Perceptrons: An Introduction to Computational Geometry.
