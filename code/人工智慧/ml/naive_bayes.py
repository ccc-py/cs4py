"""
樸素貝氏分類器 (Naive Bayes Classifier)

歷史背景：
- 基於托馬斯·貝葉斯 (Thomas Bayes, 1702-1761) 的貝葉斯定理
- 1950 年代由 R. A. Fisher 等人發展用於統計分類
- 1990 年代成為文字分類的主流方法，特別是垃圾郵件過濾
- 由於假設特徵條件獨立，計算效率高且效果良好
- 是生成式模型 (Generative Model) 的經典代表

核心概念：
- 貝葉斯定理：P(y|x) = P(x|y) * P(y) / P(x)
- 樸素假設：給定類別 y 時，所有特徵 x_i 互相獨立
- 因此 P(x|y) = Π P(x_i|y)
- 分類時選擇使後驗機率最大的類別
"""

from typing import List, Dict, Tuple, Any, Optional
import math
import re


class MultinomialNB:
    """多項式樸素貝氏分類器 - 適用於文字分類"""

    def __init__(self, alpha: float = 1.0):
        """
        初始化多項式樸素貝氏分類器

        參數：
            alpha: 拉普拉斯平滑參數 (Laplace smoothing)，預設 1.0
        """
        self.alpha = alpha
        self.classes: List[str] = []
        self.class_priors: Dict[str, float] = {}
        self.feature_probs: Dict[str, Dict[str, float]] = {}
        self.vocabulary: List[str] = []
        self.vocab_index: Dict[str, int] = {}

    def _tokenize(self, text: str) -> List[str]:
        """將文字轉為詞袋 (bag of words)"""
        # 簡單的英文分詞：轉小寫並取出字母數字字符
        words = re.findall(r'[a-z0-9]+', text.lower())
        return words

    def _build_vocabulary(self, documents: List[str]) -> None:
        """建立詞彙表"""
        vocab_set = set()
        for doc in documents:
            words = self._tokenize(doc)
            vocab_set.update(words)
        self.vocabulary = sorted(vocab_set)
        self.vocab_index = {word: i for i, word in enumerate(self.vocabulary)}

    def _document_to_counts(self, text: str) -> List[int]:
        """將文件轉為詞頻向量"""
        words = self._tokenize(text)
        counts = [0] * len(self.vocabulary)
        for word in words:
            if word in self.vocab_index:
                counts[self.vocab_index[word]] += 1
        return counts

    def fit(self, documents: List[str], labels: List[str]) -> None:
        """
        訓練分類器

        參數：
            documents: 文字文件列表
            labels: 對應的類別標籤
        """
        # 建立詞彙表
        self._build_vocabulary(documents)

        # 取得所有類別
        self.classes = sorted(set(labels))

        # 計算類別先驗機率 P(y)
        n_docs = len(documents)
        for cls in self.classes:
            count = sum(1 for label in labels if label == cls)
            self.class_priors[cls] = count / n_docs

        # 計算每個類別的特徵機率 P(word|class)
        vocab_size = len(self.vocabulary)
        alpha = self.alpha

        for cls in self.classes:
            # 取得該類別的所有文件
            class_docs = [doc for doc, label in zip(documents, labels) if label == cls]

            # 計算該類別中所有詞的總出現次數
            total_word_count = 0
            word_counts = [0] * vocab_size

            for doc in class_docs:
                counts = self._document_to_counts(doc)
                total_word_count += sum(counts)
                for i in range(vocab_size):
                    word_counts[i] += counts[i]

            # 使用拉普拉斯平滑計算機率
            # P(word_i | class) = (count(word_i) + alpha) / (total + alpha * vocab_size)
            self.feature_probs[cls] = {}
            denominator = total_word_count + alpha * vocab_size
            for i, word in enumerate(self.vocabulary):
                self.feature_probs[cls][word] = (word_counts[i] + alpha) / denominator

    def predict(self, document: str) -> str:
        """
        預測單一文件的類別

        返回：預測的類別
        """
        words = self._tokenize(document)
        best_class = None
        max_log_prob = float('-inf')

        for cls in self.classes:
            # 使用對數機率避免下溢
            log_prob = math.log(self.class_priors[cls])

            for word in words:
                if word in self.vocab_index:
                    prob = self.feature_probs[cls].get(word)
                    if prob is not None and prob > 0:
                        log_prob += math.log(prob)
                    else:
                        # 未登錄詞，使用平滑後的最小機率
                        vocab_size = len(self.vocabulary)
                        log_prob += math.log(self.alpha / (self.alpha * vocab_size))

            if log_prob > max_log_prob:
                max_log_prob = log_prob
                best_class = cls

        return best_class  # type: ignore

    def predict_proba(self, document: str) -> Dict[str, float]:
        """
        預測文件屬於各類別的機率（未正規化）

        返回：各類別的對數機率
        """
        words = self._tokenize(document)
        results = {}

        for cls in self.classes:
            log_prob = math.log(self.class_priors[cls])
            for word in words:
                if word in self.vocab_index:
                    prob = self.feature_probs[cls].get(word)
                    if prob is not None and prob > 0:
                        log_prob += math.log(prob)
            results[cls] = log_prob

        return results


class GaussianNB:
    """高斯樸素貝氏分類器 - 適用於連續特徵"""

    def __init__(self):
        """初始化高斯樸素貝氏分類器"""
        self.classes: List[str] = []
        self.class_priors: Dict[str, float] = {}
        self.means: Dict[str, List[float]] = {}
        self.variances: Dict[str, List[float]] = {}
        self.n_features: int = 0

    def fit(self, X: List[List[float]], y: List[str]) -> None:
        """
        訓練高斯樸素貝氏分類器

        參數：
            X: 特徵矩陣，每行為一個樣本
            y: 類別標籤
        """
        self.n_features = len(X[0])
        self.classes = sorted(set(y))

        n_samples = len(X)

        # 計算類別先驗機率
        for cls in self.classes:
            count = sum(1 for label in y if label == cls)
            self.class_priors[cls] = count / n_samples

        # 計算每個類別每個特徵的均值和方差
        for cls in self.classes:
            # 取得該類別的樣本
            class_samples = [X[i] for i in range(n_samples) if y[i] == cls]
            n_class = len(class_samples)

            # 初始化均值和方差
            means = [0.0] * self.n_features
            variances = [0.0] * self.n_features

            # 計算均值
            for sample in class_samples:
                for j in range(self.n_features):
                    means[j] += sample[j] / n_class

            # 計算方差
            for sample in class_samples:
                for j in range(self.n_features):
                    diff = sample[j] - means[j]
                    variances[j] += diff * diff / n_class

            # 避免方差為零（加入微小值以保持數值穩定）
            for j in range(self.n_features):
                if variances[j] == 0:
                    variances[j] = 1e-9

            self.means[cls] = means
            self.variances[cls] = variances

    def _gaussian_log_prob(self, x: float, mean: float, variance: float) -> float:
        """計算高斯分佈的對數機率密度"""
        # log N(x | μ, σ²) = -0.5 * log(2πσ²) - (x-μ)²/(2σ²)
        log_2pi = math.log(2 * math.pi)
        return -0.5 * (log_2pi + math.log(variance) + (x - mean) ** 2 / variance)

    def predict(self, x: List[float]) -> str:
        """
        預測單一樣本的類別

        返回：預測的類別
        """
        best_class = None
        max_log_prob = float('-inf')

        for cls in self.classes:
            # 先驗機率
            log_prob = math.log(self.class_priors[cls])

            # 加上各特徵的條件機率（假設獨立）
            for j in range(self.n_features):
                log_prob += self._gaussian_log_prob(
                    x[j], self.means[cls][j], self.variances[cls][j]
                )

            if log_prob > max_log_prob:
                max_log_prob = log_prob
                best_class = cls

        return best_class  # type: ignore

    def predict_batch(self, X: List[List[float]]) -> List[str]:
        """批量預測"""
        return [self.predict(x) for x in X]


def demo_spam_classification() -> None:
    """垃圾郵件分類示範"""
    print("=== 垃圾郵件分類示範 (Multinomial Naive Bayes) ===\n")

    # 訓練資料
    documents = [
        "buy now cheap viagra pills",
        "win money now claim your prize",
        "free offer click here to win",
        "limited time offer act now",
        "meeting scheduled for tomorrow",
        "please review the attached document",
        "let me know your thoughts on this",
        "the project report is ready",
    ]
    labels = ["spam", "spam", "spam", "spam", "ham", "ham", "ham", "ham"]

    # 訓練模型
    nb = MultinomialNB(alpha=1.0)
    nb.fit(documents, labels)

    # 測試
    test_docs = [
        "free money click here now",
        "meeting tomorrow review document",
        "buy cheap pills win prize",
    ]

    print("訓練完成！詞彙表大小:", len(nb.vocabulary))
    print("\n預測結果：")
    for doc in test_docs:
        pred = nb.predict(doc)
        proba = nb.predict_proba(doc)
        print(f"  文件: '{doc}'")
        print(f"  預測: {pred}")
        print(f"  機率: {proba}")
        print()


def demo_iris_classification() -> None:
    """使用合成鳶尾花資料示範高斯樸素貝氏"""
    print("=== 鳶尾花分類示範 (Gaussian Naive Bayes) ===\n")

    # 合成簡化的鳶尾花資料 (花萼長度, 花萼寬度)
    # setosa: 短而寬, versicolor: 中等, virginica: 長而窄
    X = [
        [5.1, 3.5], [4.9, 3.0], [4.7, 3.2], [4.6, 3.1], [5.0, 3.6],
        [5.4, 3.9], [4.6, 3.4], [5.0, 3.4], [4.4, 2.9], [4.9, 3.1],
        [7.0, 3.2], [6.4, 3.2], [6.9, 3.1], [5.5, 2.3], [6.5, 2.8],
        [7.7, 3.8], [6.0, 2.7], [6.1, 2.9], [6.7, 3.1], [6.3, 2.5],
        [6.3, 3.3], [5.8, 2.7], [7.1, 3.0], [6.3, 2.9], [6.5, 3.0],
        [7.6, 3.0], [7.3, 2.9], [6.7, 2.5], [7.2, 3.6], [6.5, 3.2],
    ]
    y = (
        ["setosa"] * 10
        + ["versicolor"] * 10
        + ["virginica"] * 10
    )

    # 訓練模型
    gnb = GaussianNB()
    gnb.fit(X, y)

    # 預測
    test_samples = [
        [5.0, 3.4],  # 應該是 setosa
        [6.5, 3.0],  # 應該是 versicolor 或 virginica
        [7.0, 2.8],  # 應該是 virginica
    ]

    print("類別先驗機率:")
    for cls, prior in gnb.class_priors.items():
        print(f"  {cls}: {prior:.3f}")

    print("\n預測結果：")
    for sample in test_samples:
        pred = gnb.predict(sample)
        print(f"  特徵 {sample} -> {pred}")


if __name__ == "__main__":
    demo_spam_classification()
    print("\n" + "=" * 50 + "\n")
    demo_iris_classification()
