# Word2Vec（Skip-gram）

## 歷史背景

Word2Vec 由 Google 的 Tomas Mikolov 等人於 2013 年提出，革命性地將詞語映射為稠密向量（word embeddings），使得語義相近的詞在向量空間中距離相近。Word2Vec 包含兩種架構：Continuous Bag of Words (CBOW) 和 Skip-gram。該模型的出現標誌著 NLP 從稀疏表示（如 one-hot、TF-IDF）進入到稠密向量表示的新時代。

## 核心原理

### Skip-gram 模型

Skip-gram 的目標是給定中心詞，預測其上下文詞。模型包含兩層：
1. **輸入層到隱藏層**：查詢詞向量矩陣 W1
2. **隱藏層到輸出層**：經過 W2 矩陣計算後使用 sigmoid 輸出

### 負採樣（Negative Sampling）

原始 Skip-gram 需要對整個詞彙表做 softmax，計算量巨大。負採樣的改進：
- 對每個正樣本（中心詞-上下文詞對），隨機採樣 K 個負樣本
- 將多分類問題轉化為二分類問題（正樣本 vs 負樣本）
- 大幅減少計算量

### 詞向量相似度

使用餘弦相似度衡量詞向量之間的語義相似度：

sim(v₁, v₂) = (v₁·v₂) / (||v₁|| × ||v₂||)

## 使用範例

```python
from word2vec import Word2Vec

# 建立詞彙表
corpus = ["king queen man woman"]
vocab = set(" ".join(corpus).split())
word2idx = {w: i for i, w in enumerate(sorted(vocab))}
sentences = [[word2idx[w] for w in s.split()] for s in corpus]

# 訓練模型
model = Word2Vec(vocab_size=len(vocab), embedding_dim=10)
model.fit(sentences, window_size=2, epochs=50)

# 查詢相似度
sim = model.similarity(word2idx["king"], word2idx["queen"])
print(f"king vs queen 相似度: {sim:.4f}")
```

## 參考資料

- Mikolov, T., et al. (2013). "Efficient Estimation of Word Representations in Vector Space". arXiv:1301.3781.
- Mikolov, T., et al. (2013). "Distributed Representations of Words and Phrases and their Compositionality". NIPS.
- [Word2Vec 官方教程](https://code.google.com/archive/p/word2vec/)
