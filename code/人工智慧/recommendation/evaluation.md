# 推薦系統評估指標 (Recommendation Evaluation Metrics)

## 歷史背景

隨著推薦系統的發展，如何評估推薦結果的質量成為一個重要課題。早期的推薦系統主要使用準確率（Accuracy）來評估，但研究人員很快發現，推薦系統的目標不僅是預測準確，更重要的是推薦有用的物品給用戶。

因此，信息檢索領域的多種評估指標被引入推薦系統，包括 Precision、Recall、MAP、NDCG 等。這些指標能夠更好地反映推薦系統在實際應用中的效果。

## 核心原理

### 1. Precision@K 和 Recall@K

**Precision@K**：推薦的前K個物品中有多少比例是相關的。
$$\text{Precision}@K = \frac{|\text{推薦的前K個} \cap \text{相關物品}|}{\min(K, |\text{推薦列表}|)}$$

**Recall@K**：相關物品中有多少比例出現在前K個推薦中。
$$\text{Recall}@K = \frac{|\text{推薦的前K個} \cap \text{相關物品}|}{|\text{相關物品}|}$$

### 2. Mean Average Precision (MAP)

**Average Precision (AP)**：對每個相關物品被檢索到的位置計算精度，然後取平均。
$$\text{AP} = \frac{1}{|\text{相關物品}|} \sum_{k=1}^{n} P(k) \cdot \text{rel}(k)$$
其中 $P(k)$ 是前k個結果的精度，$\text{rel}(k)$ 表示第k個結果是否相關。

**MAP**：多個查詢的AP的平均值。

### 3. NDCG (Normalized Discounted Cumulative Gain)

**DCG (Discounted Cumulative Gain)**：考慮推薦順序的累積增益，位置越靠前權重越大。
$$\text{DCG}@K = \sum_{i=1}^{K} \frac{\text{rel}_i}{\log_2(i+1)}$$

**IDCG (Ideal DCG)**：理想情況下的DCG，即相關性分數降序排列。

**NDCG**：標準化後的DCG。
$$\text{NDCG}@K = \frac{\text{DCG}@K}{\text{IDCG}@K}$$

## 使用範例

```python
from evaluation import precision_at_k, recall_at_k, ndcg_at_k, mean_average_precision

# 推薦結果和ground truth
recommended = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
relevant = [101, 103, 105, 107, 109]

# Precision@K 和 Recall@K
print(f"Precision@5: {precision_at_k(recommended, relevant, 5):.3f}")
print(f"Recall@5: {recall_at_k(recommended, relevant, 5):.3f}")

# NDCG@K（需要相關性分數）
relevant_scores = {101: 3.0, 103: 2.0, 105: 3.0, 107: 1.0, 109: 2.0}
print(f"NDCG@5: {ndcg_at_k(recommended, relevant_scores, 5):.3f}")

# MAP（多個用戶）
rec_lists = [
    [101, 102, 103, 104, 105],
    [201, 202, 203, 204, 205]
]
rel_lists = [
    [101, 103, 105],
    [202, 205]
]
print(f"MAP: {mean_average_precision(rec_lists, rel_lists):.3f}")

# 綜合評估
from evaluation import evaluate_recommendations
metrics = evaluate_recommendations(recommended, relevant, relevant_scores, ks=[5, 10])
for name, value in metrics.items():
    print(f"{name}: {value:.4f}")
```

## 參考資料

1. Herlocker, J. L., Konstan, J. A., Terveen, L. G., & Riedl, J. T. (2004). Evaluating collaborative filtering recommender systems. *ACM Transactions on Information Systems*, 22(1), 5-53.
2. Cremonesi, P., Koren, Y., & Turrin, R. (2010). Performance of recommender algorithms on top-n recommendation tasks. *RecSys*, 39-46.
3. Jarvelin, K., & Kekalainen, J. (2002). Cumulated gain-based evaluation of IR techniques. *ACM TOIS*, 20(4), 422-446.
