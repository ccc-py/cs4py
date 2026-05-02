from typing import List, Dict, Tuple
import math


class NaiveBayesText:
    """基於 TF-IDF 特徵的多元朴素貝葉斯分類器。

    用於文本分類任務，如垃圾郵件檢測。
    """

    def __init__(self):
        """初始化分類器。"""
        self.classes: List[str] = []
        self.class_prior: Dict[str, float] = {}
        self.word_probs: Dict[str, Dict[str, float]] = {}
        self.vocab: set = set()
        self.idf: Dict[str, float] = {}
        self.doc_count: int = 0

    def _tokenize(self, text: str) -> List[str]:
        """簡單分詞（按空格分割並轉小寫）。"""
        return text.lower().split()

    def _compute_idf(self, docs: List[List[str]]) -> None:
        """計算每個詞的 IDF 值。"""
        self.doc_count = len(docs)
        doc_freq: Dict[str, int] = {}
        for doc in docs:
            unique_words = set(doc)
            for word in unique_words:
                doc_freq[word] = doc_freq.get(word, 0) + 1
        self.idf = {word: math.log(self.doc_count / (freq + 1)) for word, freq in doc_freq.items()}

    def _compute_tfidf(self, tokens: List[str]) -> Dict[str, float]:
        """計算單個文檔的 TF-IDF 向量。"""
        tf: Dict[str, int] = {}
        for word in tokens:
            tf[word] = tf.get(word, 0) + 1

        tfidf: Dict[str, float] = {}
        for word, count in tf.items():
            tfidf[word] = (1 + math.log(count)) * self.idf.get(word, 0)
        return tfidf

    def train(self, texts: List[str], labels: List[str]) -> None:
        """訓練朴素貝葉斯分類器。

        Args:
            texts: 訓練文本列表
            labels: 對應的類別標籤
        """
        # 分詞與建立詞彙表
        tokenized_docs = [self._tokenize(text) for text in texts]
        self.vocab = set()
        for doc in tokenized_docs:
            self.vocab.update(doc)

        # 計算 IDF
        self._compute_idf(tokenized_docs)

        # 按類別分組計算詞頻
        class_docs: Dict[str, List[List[str]]] = {}
        for doc, label in zip(tokenized_docs, labels):
            if label not in class_docs:
                class_docs[label] = []
            class_docs[label].append(doc)

        # 計算類別先驗機率與詞條件機率
        total_docs = len(texts)
        vocab_size = len(self.vocab)

        for label, docs in class_docs.items():
            self.classes.append(label)
            self.class_prior[label] = len(docs) / total_docs

            # 統計該類別所有文檔的詞頻（TF-IDF 加權）
            word_tfidf_sum: Dict[str, float] = {}
            total_tfidf = 0.0
            for doc in docs:
                tfidf = self._compute_tfidf(doc)
                for word, val in tfidf.items():
                    word_tfidf_sum[word] = word_tfidf_sum.get(word, 0) + val
                    total_tfidf += val

            # Laplace 平滑
            self.word_probs[label] = {}
            for word in self.vocab:
                count = word_tfidf_sum.get(word, 0)
                self.word_probs[label][word] = (count + 1) / (total_tfidf + vocab_size)

    def predict(self, text: str) -> Tuple[str, Dict[str, float]]:
        """預測文本類別。

        Args:
            text: 待分類文本

        Returns:
            (預測類別, 各類別的後驗機率對數)
        """
        tokens = self._tokenize(text)
        tfidf = self._compute_tfidf(tokens)

        best_class = None
        best_score = float('-inf')
        scores = {}

        for label in self.classes:
            # 對數機率避免下溢
            score = math.log(self.class_prior.get(label, 1e-10))
            for word, val in tfidf.items():
                if word in self.vocab:
                    prob = self.word_probs[label].get(word, 1e-10)
                    score += val * math.log(prob)
            scores[label] = score
            if score > best_score:
                best_score = score
                best_class = label

        return best_class, scores


if __name__ == "__main__":
    # 垃圾郵件分類示例
    texts = [
        "buy now cheap viagra",
        "hello how are you",
        "win money click here",
        "meeting scheduled for tomorrow",
        "free offer limited time",
        "let us discuss the project",
    ]
    labels = ["spam", "ham", "spam", "ham", "spam", "ham"]

    nb = NaiveBayesText()
    nb.train(texts, labels)

    test_texts = [
        "free viagra buy now",
        "hello how are you doing",
        "meeting with team tomorrow",
    ]

    print("垃圾郵件分類測試:")
    for text in test_texts:
        pred, scores = nb.predict(text)
        print(f"  文本: '{text}'")
        print(f"  預測: {pred}, 分數: {scores}")
