# 資訊檢索評估指標 (Evaluation Metrics)

## 歷史背景

資訊檢索系統的評估始於 1960 年代美國國防部對檔案檢索系統的需求。Cranfield 實驗（1957-1968）首次建立了標準化的評估框架，提出使用 Precision 和 Recall 作為核心指標。

後來發展的重要指標包括：
- **MAP**（1990年代）：考慮排名品質
- **NDCG**（1999年由 Jarvelin 和 Kekalainen 提出）：考慮相關性程度

這些指標至今仍是學術研究和工業應用的標準。

## 核心原理

### Precision 和 Recall

```
Precision = 相關文件數 / 檢索到的文件數
Recall = 相關文件數 / 所有相關文件數
```

### F1-score

調和平均數，平衡 P 和 R：
```
F1 = 2 * (P * R) / (P + R)
```

### Average Precision (AP)

考慮排名的 Precision，每當檢索到相關文件時計算 P@k：
```
AP = Σ (P@k * rel_k) / (相關文件數)
```

### Mean Average Precision (MAP)

多個查詢的 AP 平均值。

### NDCG (Normalized Discounted Cumulative Gain)

考慮相關性程度（不僅是二元相關）和排名位置：
```
DCG@K = Σ (2^rel_i - 1) / log2(i + 1)
NDCG@K = DCG@K / IDCG@K
```

IDCG 是理想排序下的 DCG。

## 使用範例

```python
from evaluation.metrics import precision_at_k, recall_at_k, mean_average_precision

retrieved = [1, 2, 3, 4, 5]
relevant = {1, 3, 5}

p = precision_at_k(retrieved, relevant, k=5)
r = recall_at_k(retrieved, relevant, k=5)
print(f"P@5={p:.4f}, R@5={r:.4f}")
```

## 參考資料

- Cranfield, C. W. (1969). *Report on the Cranfield tests*. Aslib Proceedings.
- Jarvelin, K., & Kekalainen, J. (2002). Cumulated gain-based evaluation of IR techniques. *ACM Transactions on Information Systems*, 20(4), 422-446.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
