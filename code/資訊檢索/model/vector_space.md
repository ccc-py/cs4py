# 向量空間模型 (Vector Space Model)

## 歷史背景

向量空間模型由 Gerard Salton 在 1970 年代提出，是資訊檢索領域最具影響力的模型之一。該模型將文件和查詢表示為高維空間中的向量，使用餘弦相似度衡量相關性。

Salton 的 SMART 系統首次大規模應用了此模型，證明了數學方法在文件檢索中的有效性。向量空間模型為後來的機器學習方法（如 LSI、Word2Vec）奠定了基礎。

## 核心原理

### 文件表示

每個詞彙對應一個維度，文件表示為向量：
```
D = (w1, w2, ..., wn)
```
其中 wi 是詞彙 i 的權重（TF 或 TF-IDF）。

### 餘弦相似度

衡量兩個向量的夾角餘弦值：
```
cos(θ) = (q · d) / (||q|| * ||d||)
```

相似度範圍 [-1, 1]，在資訊檢索中通常為正值。

### 權重計算

- **原始詞頻**：`w(t, d) = count(t, d)`
- **TF-IDF**：`w(t, d) = tf(t, d) * idf(t)`

### 文件排名

計算查詢向量與所有文件向量的餘弦相似度，按分數降序排列。

## 使用範例

```python
from model.vector_space import VectorSpaceModel

docs = ["the cat sat", "the dog ran", "cat and dog"]
vsm = VectorSpaceModel(use_tfidf=True)
vsm.fit(docs)

results = vsm.query("cat dog")
for idx, score in results:
    print(f"文件 {idx}: 相似度 {score:.4f}")
```

## 參考資料

- Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM*, 18(11), 613-620.
- Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
