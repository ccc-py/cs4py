# 朴素貝葉斯文本分類

## 歷史背景

朴素貝葉斯分類器基於貝葉斯定理，並假設特徵之間相互獨立（「朴素」的由來）。該方法在 1990 年代被廣泛應用於垃圾郵件過濾，成為早期文本分類的經典方法。儘管假設過於簡化，朴素貝葉斯在實踐中往往表現出色，且訓練速度快、易於實作。

## 核心原理

### 貝葉斯定理

P(c|d) = P(d|c) × P(c) / P(d)

對於文本分類，我們關注：
- P(c)：類別先驗機率
- P(d|c)：在類別 c 下出現文檔 d 的機率
- P(c|d)：給定文檔 d 屬於類別 c 的後驗機率

### TF-IDF 特徵

- **TF（詞頻）**：詞語在文檔中出現的次數，取 log 避免長文檔偏差
- **IDF（逆文檔頻率）**：log(N / df)，衡量詞語的區分能力
- **TF-IDF** = TF × IDF

### Laplace 平滑

處理未見過的詞語：將所有計數加一，避免機率為零。

## 使用範例

```python
from naive_bayes_text import NaiveBayesText

# 訓練數據
texts = ["buy now cheap", "hello how are you", "win money", "meeting tomorrow"]
labels = ["spam", "ham", "spam", "ham"]

# 訓練模型
nb = NaiveBayesText()
nb.train(texts, labels)

# 預測
pred, scores = nb.predict("free offer buy now")
print(f"預測類別: {pred}")
```

## 參考資料

- McCallum, A., & Nigam, K. (1998). "A Comparison of Event Models for Naive Bayes Text Classification". AAAI Workshop on Learning for Text Categorization.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). "Introduction to Information Retrieval". Cambridge University Press.
- [Scikit-learn: Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
