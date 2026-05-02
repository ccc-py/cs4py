"""推薦系統評估指標實作"""

from typing import List, Dict, Tuple


def precision_at_k(recommended: List[int], relevant: List[int], k: int) -> float:
    """計算Precision@K

    Precision@K 衡量推薦的前K個物品中有多少是相關的。

    Args:
        recommended: 推薦物品列表（按順序）
        relevant: 相關物品列表（ground truth）
        k: 考慮的前K個推薦

    Returns:
        Precision@K 值
    """
    if k <= 0:
        return 0.0
    top_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for item in top_k if item in relevant_set)
    return hits / min(k, len(recommended))


def recall_at_k(recommended: List[int], relevant: List[int], k: int) -> float:
    """計算Recall@K

    Recall@K 衡量相關物品中有多少出現在前K個推薦中。

    Args:
        recommended: 推薦物品列表（按順序）
        relevant: 相關物品列表（ground truth）
        k: 考慮的前K個推薦

    Returns:
        Recall@K 值
    """
    if not relevant:
        return 0.0
    top_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for item in top_k if item in relevant_set)
    return hits / len(relevant)


def average_precision(recommended: List[int], relevant: List[int]) -> float:
    """計算Average Precision (AP)

    對每個相關物品被檢索到的位置計算精度，然後取平均。

    Args:
        recommended: 推薦物品列表（按順序）
        relevant: 相關物品列表（ground truth）

    Returns:
        AP 值
    """
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    hits = 0
    sum_precision = 0.0
    for i, item in enumerate(recommended):
        if item in relevant_set:
            hits += 1
            sum_precision += hits / (i + 1)
    return sum_precision / len(relevant)


def mean_average_precision(recommended_lists: List[List[int]], relevant_lists: List[List[int]]) -> float:
    """計算Mean Average Precision (MAP)

    多個查詢的Average Precision的平均值。

    Args:
        recommended_lists: 每個查詢的推薦物品列表
        relevant_lists: 每個查詢的相關物品列表

    Returns:
        MAP 值
    """
    if not recommended_lists:
        return 0.0
    aps = [average_precision(rec, rel) for rec, rel in zip(recommended_lists, relevant_lists)]
    return sum(aps) / len(aps)


def dcg_at_k(recommended: List[int], relevant_scores: Dict[int, float], k: int) -> float:
    """計算Discounted Cumulative Gain (DCG) at K

    Args:
        recommended: 推薦物品列表（按順序）
        relevant_scores: 相關物品及其相關性分數
        k: 考慮的前K個推薦

    Returns:
        DCG@K 值
    """
    top_k = recommended[:k]
    dcg = 0.0
    for i, item in enumerate(top_k):
        score = relevant_scores.get(item, 0.0)
        if score > 0:
            dcg += score / math.log2(i + 2)
    return dcg


def idcg_at_k(relevant_scores: Dict[int, float], k: int) -> float:
    """計算Ideal DCG at K

    將相關性分數降序排列後計算的理想DCG。

    Args:
        relevant_scores: 相關物品及其相關性分數
        k: 考慮的前K個

    Returns:
        IDCG@K 值
    """
    sorted_scores = sorted(relevant_scores.values(), reverse=True)
    idcg = 0.0
    for i, score in enumerate(sorted_scores[:k]):
        idcg += score / math.log2(i + 2)
    return idcg


def ndcg_at_k(recommended: List[int], relevant_scores: Dict[int, float], k: int) -> float:
    """計算Normalized DCG (NDCG) at K

    Args:
        recommended: 推薦物品列表（按順序）
        relevant_scores: 相關物品及其相關性分數
        k: 考慮的前K個推薦

    Returns:
        NDCG@K 值
    """
    dcg = dcg_at_k(recommended, relevant_scores, k)
    idcg = idcg_at_k(relevant_scores, k)
    return dcg / idcg if idcg > 0 else 0.0


def evaluate_recommendations(recommended: List[int], relevant: List[int],
                            relevant_scores: Dict[int, float] = None,
                            ks: List[int] = [5, 10]) -> Dict[str, float]:
    """綜合評估推薦結果

    Args:
        recommended: 推薦物品列表
        relevant: 相關物品列表
        relevant_scores: 相關物品分數（用於NDCG）
        ks: 要計算的K值列表

    Returns:
        評估指標字典
    """
    if relevant_scores is None:
        relevant_scores = {item: 1.0 for item in relevant}
    results = {}
    for k in ks:
        results[f"Precision@{k}"] = precision_at_k(recommended, relevant, k)
        results[f"Recall@{k}"] = recall_at_k(recommended, relevant, k)
        results[f"NDCG@{k}"] = ndcg_at_k(recommended, relevant_scores, k)
    results["MAP"] = average_precision(recommended, relevant)
    return results


if __name__ == "__main__":
    import math
    print("推薦系統評估指標演示")
    recommended = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    relevant = [101, 103, 105, 107, 109]
    relevant_scores = {101: 3.0, 103: 2.0, 105: 3.0, 107: 1.0, 109: 2.0}
    print(f"推薦列表: {recommended[:10]}")
    print(f"相關物品: {relevant}")
    print(f"\n評估結果:")
    metrics = evaluate_recommendations(recommended, relevant, relevant_scores, ks=[3, 5, 10])
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")
    print(f"\nAP: {average_precision(recommended, relevant):.4f}")
    print(f"MAP (多個用戶):")
    rec_lists = [
        [101, 102, 103, 104, 105],
        [201, 202, 203, 204, 205]
    ]
    rel_lists = [
        [101, 103, 105],
        [202, 205]
    ]
    print(f"  {mean_average_precision(rec_lists, rel_lists):.4f}")
