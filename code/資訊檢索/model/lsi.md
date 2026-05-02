# 潛在語意索引 (Latent Semantic Indexing, LSI)

## 歷史背景

LSI 由 Scott Deerwester、Susan Dumais 等人在 1988 年提出，結合了資訊檢索和線性代數中的奇異值分解（SVD）技術。LSI 解決了詞彙不匹配問題（synonymy and polysemy），即相同概念可能用不同詞彙表達。

LSI 是資訊檢索領域首次將線性代數應用於語意分析的嘗試，為後來的潛在狄利克雷分配（LDA）和神經網路方法（Word2Vec、BERT）奠定了基礎。

## 核心原理

### 詞彙-文件矩陣

建立矩陣 A（m x n）：
- m：詞彙數量
- n：文件數量
- A[i][j]：詞彙 i 在文件 j 中的頻率

### 奇異值分解 (SVD)

將矩陣分解為：
```
A ≈ U * Σ * V^T
```

其中：
- U：詞彙-概念矩陣（m x k）
- Σ：奇異值對角矩陣（k x k）
- V^T：概念-文件矩陣（k x n）

### 降維

保留最大的 k 個奇異值，過濾雜訊，發現潛在語意結構。

### 查詢映射

將查詢向量投影到潛在語意空間：
```
q_lsi = U^T * q
```

然後計算與文件的餘弦相似度。

## 使用範例

```python
from model.lsi import LSI

docs = ["the car is fast", "the automobile is quick", "doctor works in hospital"]
lsi = LSI(n_components=2)
lsi.fit(docs)

results = lsi.query("fast vehicle")
for idx, score in results:
    print(f"文件 {idx}: {score:.4f}")
```

## 參考資料

- Deerwester, S., Dumais, S. T., Furnas, G. W., Landauer, T. K., & Harshman, R. (1990). Indexing by latent semantic analysis. *Journal of the American Society for Information Science*, 41(6), 391-407.
- Landauer, T. K., Foltz, P. W., & Laham, D. (1998). An introduction to latent semantic analysis. *Discourse Processes*, 25(2-3), 259-284.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
