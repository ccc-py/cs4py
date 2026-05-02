# 字元級 RNN 文本生成

## 歷史背景

循環神經網路（RNN）的概念最早可追溯至 1980 年代，但直到 2010 年代隨著深度學習興起才廣泛應用。Andrej Karpathy 於 2015 年發表的《The Unreasonable Effectiveness of Recurrent Neural Networks》展示了 RNN 在文本生成上的強大能力，引發了廣泛關注。RNN 能夠捕捉序列中的時間依賴關係，是早期序列建模的核心技術。

## 核心原理

### RNN 結構

RNN 的核心是一個循環結構，隱藏狀態會傳遞到下一個時間步：

h_t = tanh(W_xh · x_t + W_hh · h_{t-1} + b_h)
y_t = softmax(W_hy · h_t + b_y)

其中：
- x_t：當前時間步的輸入
- h_t：當前時間步的隱藏狀態
- y_t：當前時間步的輸出（預測的下一個字元）

### 訓練方法

- **BPTT（Backpropagation Through Time）**：將 RNN 展開為多層網路後進行反向傳播
- **損失函數**：交叉熵損失
- **文本生成**：利用訓練好的模型，每次取預測分佈中採樣的下一個字元

### 溫度參數

生成時可調整溫度參數控制隨機性：
- 溫度低 → 更確定性，偏向高機率字元
- 溫度高 → 更隨機，分佈更平坦

## 使用範例

```python
from rnn_nlp import CharRNN

# 準備數據
text = "hello world"
chars = sorted(set(text))
char2idx = {c: i for i, c in enumerate(chars)}
data = [char2idx[c] for c in text]

# 訓練 RNN
rnn = CharRNN(vocab_size=len(chars), hidden_size=20)
rnn.train(data, epochs=100, seq_len=8)

# 生成文本
generated = rnn.generate(start_idx=char2idx["h"], length=50)
result = "".join(chars[i] for i in generated)
print(f"生成文本: {result}")
```

## 參考資料

- Karpathy, A. (2015). "The Unreasonable Effectiveness of Recurrent Neural Networks". Blog post.
- Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). "Learning representations by back-propagating errors". Nature.
- [RNN 教程](http://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1/) - Denny Britz
