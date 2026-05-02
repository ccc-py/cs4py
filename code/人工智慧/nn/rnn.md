# 遞迴神經網路 (Recurrent Neural Network)

## 歷史背景

1986 年 Jeffrey Elman 提出 Simple RNN，引入隱藏狀態來處理序列數據。然而，RNN 面臨嚴重的梯度消失/爆炸問題，難以學習長期依賴。1997 年 Hochreiter 和 Schmidhuber 提出 LSTM (Long Short-Term Memory)，透過門控機制解決了這一問題。2014 年 Cho 等人提出更簡潔的 GRU。儘管 2017 年後 Transformer 架構在 NLP 領域占據主導，RNN 仍是理解序列模型的重要基礎。

## 核心原理

### Simple RNN

每個時間步的隱藏狀態由當前輸入和前一時間步的隱藏狀態決定：

```
h_t = tanh(Wx * x_t + Wh * h_{t-1} + b)
```

### LSTM (Long Short-Term Memory)

LSTM 引入細胞狀態 (Cell State) 和三個門控：

1. **遺忘門 (Forget Gate)**：決定遺忘多少過去信息
   ```
   f_t = σ(Wf * [h_{t-1}, x_t] + bf)
   ```
2. **輸入門 (Input Gate)**：決定更新多少新信息
   ```
   i_t = σ(Wi * [h_{t-1}, x_t] + bi)
   c̃_t = tanh(Wc * [h_{t-1}, x_t] + bc)
   ```
3. **輸出門 (Output Gate)**：決定輸出多少信息
   ```
   o_t = σ(Wo * [h_{t-1}, x_t] + bo)
   h_t = o_t * tanh(c_t)
   ```

細胞狀態更新：`c_t = f_t * c_{t-1} + i_t * c̃_t`

### BPTT (Backpropagation Through Time)

將 RNN 沿時間展開為前饋網路，然後應用標準反向傳播。

## 使用範例

```python
from nn.rnn import RNN, LSTMCell

# 建立 LSTM
rnn = RNN(n_in=1, n_hidden=4, cell_type='lstm')

# 處理序列
sequence = [[0.1], [0.2], [0.3], [0.4]]
outputs = rnn.forward(sequence)

# 最後一個時間步的輸出包含整個序列的信息
print(f"最終隱藏狀態: {outputs[-1]}")
```

## RNN vs LSTM vs Transformer

| 特性 | RNN | LSTM | Transformer |
|------|-----|------|-------------|
| 長期依賴 | 弱 | 強 | 極強 |
| 訓練速度 | 慢 (序列依賴) | 慢 | 快 (並行) |
| 參數量 | 少 | 多 | 多 |
| 位置信息 | 隱式 | 隱式 | 位置編碼 |

## 參考資料

- Elman, J. L. (1990). Finding structure in time.
- Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory.
- Cho, K., et al. (2014). Learning phrase representations using RNN encoder-decoder.
