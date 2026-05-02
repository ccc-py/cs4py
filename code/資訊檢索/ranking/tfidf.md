# TF-IDF 權重 (TF-IDF Weighting)

## 歷史背景

TF-IDF（Term Frequency-Inverse Document Frequency）由 Karen Spärck Jones 在 1972 年提出，是資訊檢索領域最重要的加權方法之一。該方法基於兩個直覺：
1. 詞彙在文件中出現越多次，越能代表該文件（TF）
2. 詞彙在越多文件中出現，區分能力越低（IDF）

TF-IDF 至今仍是搜尋引擎和文件分類系統的基礎技術，也是許多現代方法（如 BM25）的靈感來源。

## 核心原理

### 詞頻 (Term Frequency, TF)

衡量詞彙在單一文件中的重要性：

- **原始詞頻**：`tf(t, d) = count(t, d)`
- **對數正規化**：`tf(t, d) = 1 + log(count(t, d))`
- **雙正規化**：`tf(t, d) = 0.5 + 0.5 * count(t, d) / max_count`

### 逆文件頻率 (Inverse Document Frequency, IDF)

衡量詞彙的罕見程度：

```
idf(t) = log(N / df(t))
```

其中 N 是總文件數，df(t) 是包含詞彙 t 的文件數。

**平滑 IDF**：
```
idf(t) = log((N + 1) / (df(t) + 1)) + 1
```

### TF-IDF 分數

```
tfidf(t, d) = tf(t, d) * idf(t)
```

### 文件排名

使用餘弦相似度計算查詢和文件的相似程度：

```
cos(q, d) = (q · d) / (||q|| * ||d||)
```

## 使用範例

```python
from ranking.tfidf import TfidfVectorizer

docs = ["the cat sat", "the dog ran", "cat and dog"]
vectorizer = TfidfVectorizer(use_log_tf=True)
vectorizer.fit(docs)
vectors = vectorizer.transform(docs)

# 排名
rankings = vectorizer.rank_documents("cat dog", docs)
for idx, score in rankings:
    print(f"文件 {idx}: {score:.4f}")
```

## 參考資料

- Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation*, 28(1), 11-21.
- Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
