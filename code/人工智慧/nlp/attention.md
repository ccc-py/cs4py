# 注意力機制（Attention Mechanism）

## 歷史背景

注意力機制最早由 Dzmitry Bahdanau 等人於 2014 年在機器翻譯中引入，用於解決 Seq2Seq 模型的資訊瓶頸問題。隨後 Vaswani 等人在 2017 年提出的 Transformer 架構完全基於注意力機制，摒棄了 RNN/CNN，成為現代 NLP（如 BERT、GPT）的基石。

## 核心原理

### 縮放點積注意力（Scaled Dot-Product Attention）

Attention(Q, K, V) = softmax(QK^T / √d_k) V

1. **查詢（Query）、鍵（Key）、值（Value）**：將輸入投影到三個空間
2. **計算相似度**：Q 與 K 的點積衡量相關性
3. **縮放**：除以 √d_k 避免點積過大導致梯度消失
4. **Softmax**：轉換為注意力權重（總和為 1）
5. **加權求和**：用權重對 V 進行加權

### 為什麼要縮放？

當 d_k 很大時，點積結果可能很大，導致 softmax 進入梯度極小的區域。除以 √d_k 可以緩解此問題。

### 多頭注意力（Multi-Head Attention）

將 Q、K、V 分成多組（頭），每組獨立計算注意力，最後拼接並投影：

MultiHead(Q,K,V) = Concat(head₁, ..., head_h) W^O

其中 head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)

## 使用範例

```python
from attention import scaled_dot_product_attention

# 玩具序列：3 個 token，每個 4 維
seq = [
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
]

output, attn_weights = scaled_dot_product_attention(seq, seq, seq)
print("注意力權重:")
for row in attn_weights:
    print([f"{w:.3f}" for w in row])
```

## 參考資料

- Bahdanau, D., Cho, K., & Bengio, Y. (2014). "Neural Machine Translation by Jointly Learning to Align and Translate". ICLR.
- Vaswani, A., et al. (2017). "Attention is All You Need". NIPS.
- [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/) - Jay Alammar
