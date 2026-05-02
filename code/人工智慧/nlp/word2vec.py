from typing import List, Dict, Tuple
import random
import math


class Word2Vec:
    """簡化版 Word2Vec（Skip-gram with Negative Sampling）。

    使用純 Python 實作詞嵌入訓練。
    """

    def __init__(self, vocab_size: int, embedding_dim: int):
        """初始化 Word2Vec 模型。

        Args:
            vocab_size: 詞彙表大小
            embedding_dim: 詞向量維度
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim

        # 初始化詞向量矩陣（輸入層到隱藏層）
        self.W1 = [[random.uniform(-0.01, 0.01) for _ in range(embedding_dim)]
                   for _ in range(vocab_size)]

        # 初始化輸出層權重（隱藏層到輸出層）
        self.W2 = [[random.uniform(-0.01, 0.01) for _ in range(vocab_size)]
                   for _ in range(embedding_dim)]

    def sigmoid(self, x: float) -> float:
        """Sigmoid 激活函數。"""
        if x < -100:
            return 0.0
        if x > 100:
            return 1.0
        return 1.0 / (1.0 + math.exp(-x))

    def train_skipgram(self, center_idx: int, context_idx: int,
                       neg_samples: List[int], learning_rate: float) -> None:
        """使用負採樣訓練一個樣本（Skip-gram）。

        Args:
            center_idx: 中心詞索引
            context_idx: 上下文詞索引（正樣本）
            neg_samples: 負樣本詞索引列表
            learning_rate: 學習率
        """
        # 前向傳播：取中心詞的詞向量
        h = self.W1[center_idx][:]  # 隱藏層輸出

        # 正樣本（目標詞）的梯度計算
        # 輸出層計算
        score_pos = sum(h[j] * self.W2[j][context_idx] for j in range(self.embedding_dim))
        p_pos = self.sigmoid(score_pos)

        # 正樣本梯度
        grad = (1 - p_pos) * learning_rate
        for j in range(self.embedding_dim):
            self.W2[j][context_idx] += grad * h[j]
            self.W1[center_idx][j] += grad * self.W2[j][context_idx]

        # 負樣本梯度計算
        for neg_idx in neg_samples:
            score_neg = sum(h[j] * self.W2[j][neg_idx] for j in range(self.embedding_dim))
            p_neg = self.sigmoid(score_neg)

            grad_neg = -p_neg * learning_rate  # 負樣本希望機率接近 0
            for j in range(self.embedding_dim):
                self.W2[j][neg_idx] += grad_neg * h[j]
                self.W1[center_idx][j] += grad_neg * self.W2[j][neg_idx]

    def fit(self, sentences: List[List[int]], window_size: int = 2,
           neg_samples_count: int = 5, learning_rate: float = 0.025,
           epochs: int = 10) -> None:
        """訓練 Word2Vec 模型。

        Args:
            sentences: 已轉換為索引的句子列表
            window_size: 上下文窗口大小
            neg_samples_count: 每個正樣本的負採樣數量
            learning_rate: 學習率
            epochs: 訓練輪數
        """
        vocab = list(range(self.vocab_size))

        for epoch in range(epochs):
            total_loss = 0
            for sentence in sentences:
                for i, center_word in enumerate(sentence):
                    # 取得上下文窗口內的詞
                    context_start = max(0, i - window_size)
                    context_end = min(len(sentence), i + window_size + 1)
                    context = [sentence[j] for j in range(context_start, context_end) if j != i]

                    for context_word in context:
                        # 負採樣
                        neg_samples = random.sample(
                            [w for w in vocab if w != context_word],
                            min(neg_samples_count, self.vocab_size - 1)
                        )
                        self.train_skipgram(center_word, context_word, neg_samples, learning_rate)
            print(f"Epoch {epoch + 1}/{epochs} 完成")

    def similarity(self, word_idx1: int, word_idx2: int) -> float:
        """計算兩個詞的餘弦相似度。

        Args:
            word_idx1: 第一個詞的索引
            word_idx2: 第二個詞的索引

        Returns:
            餘弦相似度（-1 到 1）
        """
        v1 = self.W1[word_idx1]
        v2 = self.W1[word_idx2]

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def get_vector(self, word_idx: int) -> List[float]:
        """取得詞向量。"""
        return self.W1[word_idx]


if __name__ == "__main__":
    # 小型語料庫示例
    corpus = [
        "king queen man woman",
        "king crown throne",
        "queen crown throne",
        "man woman child",
        "woman man king queen",
    ]

    # 建立詞彙表
    vocab = set()
    for sentence in corpus:
        vocab.update(sentence.split())
    word2idx = {w: i for i, w in enumerate(sorted(vocab))}
    idx2word = {i: w for w, i in word2idx.items()}
    vocab_size = len(word2idx)

    print("詞彙表:", word2idx)

    # 將語料轉換為索引
    sentences = [[word2idx[w] for w in s.split()] for s in corpus]

    # 訓練 Word2Vec
    model = Word2Vec(vocab_size, embedding_dim=10)
    model.fit(sentences, window_size=2, epochs=50, learning_rate=0.05)

    # 查詢相似度
    print("\n詞向量相似度:")
    for w1 in ["king", "queen", "man"]:
        for w2 in ["woman", "queen", "king"]:
            if w1 != w2:
                sim = model.similarity(word2idx[w1], word2idx[w2])
                print(f"  {w1} vs {w2}: {sim:.4f}")
