# N-gram 語言模型

## 歷史背景

N-gram 模型是統計自然語言處理的奠基性方法之一，起源於 20 世紀中葉的資訊理論研究。Claude Shannon 在 1948 年提出馬可夫鏈可用於模擬語言，隨後在 1980-1990 年代，n-gram 模型成為語音識別、機器翻譯等任務的主流方法。Google 於 2006 年發布的 n-gram 語料庫（包含上兆個詞）更是推動了該領域的發展。

## 核心原理

N-gram 模型基於馬可夫假設：一個詞的出現只與其前面 n-1 個詞相關。

### 模型定義

- **Unigram (n=1)**：P(w₁, w₂, ..., wₘ) ≈ ∏ P(wᵢ)
- **Bigram (n=2)**：P(w₁, w₂, ..., wₘ) ≈ ∏ P(wᵢ | wᵢ₋₁)
- **Trigram (n=3)**：P(w₁, w₂, ..., wₘ) ≈ ∏ P(wᵢ | wᵢ₋₂, wᵢ₋₁)

### Laplace 平滑（加一平滑）

為解決未見過的 n-gram 機率為零的問題，將所有計數加一：

P(wᵢ | context) = (count(context, wᵢ) + 1) / (count(context) + |V|)

其中 |V| 為詞彙表大小。

## 使用範例

```python
from ngram import NgramModel

# 訓練語料
corpus = "I love Python programming I love coding Python is great".split()

# 訓練 Bigram 模型
bigram = NgramModel(2)
bigram.train(corpus)

# 查詢機率
prob = bigram.probability("Python", context=("I",))
print(f"P(Python|I) = {prob:.4f}")

# 生成文本
generated = bigram.generate(8, start=["I", "love"])
print("生成文本:", " ".join(generated))
```

## 參考資料

- Shannon, C. E. (1948). "A Mathematical Theory of Communication". Bell System Technical Journal.
- Jelinek, F. (1997). "Statistical Methods for Speech Recognition". MIT Press.
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) - Jurafsky & Martin
