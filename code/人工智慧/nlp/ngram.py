from typing import List, Dict, Tuple
import random


class NgramModel:
    """N-gram 語言模型，支援 unigram、bigram、trigram。

    使用 Laplace 平滑（加一平滑）處理未見過的 n-gram。
    """

    def __init__(self, n: int):
        """初始化 N-gram 模型。

        Args:
            n: n-gram 的階數（1=unigram, 2=bigram, 3=trigram）
        """
        self.n = n
        self.ngram_counts: Dict[Tuple[str, ...], Dict[str, int]] = {}
        self.context_totals: Dict[Tuple[str, ...], int] = {}
        self.vocab: set = set()

    def train(self, tokens: List[str]) -> None:
        """訓練 N-gram 模型，統計 n-gram 出現次數。

        Args:
            tokens: 訓練語料（分詞後的 token 列表）
        """
        self.vocab = set(tokens)
        for i in range(len(tokens) - self.n + 1):
            if self.n == 1:
                context = ()
                word = tokens[i]
            else:
                context = tuple(tokens[i:i + self.n - 1])
                word = tokens[i + self.n - 1]

            if context not in self.ngram_counts:
                self.ngram_counts[context] = {}
            self.ngram_counts[context][word] = self.ngram_counts[context].get(word, 0) + 1
            self.context_totals[context] = self.context_totals.get(context, 0) + 1

    def probability(self, word: str, context: Tuple[str, ...] = ()) -> float:
        """計算給定上下文下某個詞的機率（Laplace 平滑）。

        Args:
            word: 目標詞
            context: 上下文（n-1 個詞）

        Returns:
            該詞的機率
        """
        vocab_size = len(self.vocab)
        if self.n == 1:
            context = ()

        count = self.ngram_counts.get(context, {}).get(word, 0)
        total = self.context_totals.get(context, 0)
        return (count + 1) / (total + vocab_size)

    def generate(self, length: int, start: List[str] = None) -> List[str]:
        """根據模型生成文本。

        Args:
            length: 要生成的文本長度
            start: 起始詞序列（長度需 ≥ n-1）

        Returns:
            生成的詞列表
        """
        if self.n == 1:
            return self._generate_unigram(length)

        if start is None:
            context = random.choice(list(self.ngram_counts.keys()))
            generated = list(context)
        else:
            if len(start) < self.n - 1:
                raise ValueError(f"起始序列長度需 ≥ {self.n - 1}")
            context = tuple(start[:self.n - 1])
            generated = list(start)

        while len(generated) < length:
            candidates = list(self.ngram_counts.get(context, {}).keys())
            if not candidates:
                break
            probs = [self.probability(w, context) for w in candidates]
            next_word = random.choices(candidates, weights=probs)[0]
            generated.append(next_word)
            context = tuple(generated[-(self.n - 1):])

        return generated[:length]

    def _generate_unigram(self, length: int) -> List[str]:
        """生成 unigram 文本。"""
        candidates = list(self.ngram_counts.get((), {}).keys())
        if not candidates:
            return []
        probs = [self.probability(w, ()) for w in candidates]
        return random.choices(candidates, weights=probs, k=length)


if __name__ == "__main__":
    # 訓練語料
    corpus = "I love Python programming I love coding Python is great".split()
    print("訓練語料:", corpus)

    # Unigram 模型
    unigram = NgramModel(1)
    unigram.train(corpus)
    print("\nUnigram 生成（10 個詞）:", unigram.generate(10))

    # Bigram 模型
    bigram = NgramModel(2)
    bigram.train(corpus)
    print("Bigram 生成（起始 'I love'）:", bigram.generate(8, start=["I", "love"]))

    # Trigram 模型
    trigram = NgramModel(3)
    trigram.train(corpus)
    print("Trigram 生成（起始 'I love Python'）:", trigram.generate(6, start=["I", "love", "Python"]))
