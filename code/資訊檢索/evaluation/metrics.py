"""
資訊檢索評估指標實作

包含 Precision, Recall, F1-score, MAP, NDCG 等指標。
"""

from typing import List, Dict, Tuple
import math


def precision_at_k(retrieved: List[int], relevant: set, k: int) -> float:
    """
    計算 Precision@K
    
    Precision@K = (前 K 個結果中相關文件數) / K
    
    Args:
        retrieved: 排名後的檢索結果（文件 ID 列表）
        relevant: 相關文件集合
        k: 考慮前 k 個結果
        
    Returns:
        Precision@K 值
    """
    if k == 0:
        return 0.0
    
    retrieved_k = retrieved[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant)
    
    return relevant_count / k


def recall_at_k(retrieved: List[int], relevant: set, k: int) -> float:
    """
    計算 Recall@K
    
    Recall@K = (前 K 個結果中相關文件數) / (總相關文件數)
    
    Args:
        retrieved: 排名後的檢索結果
        relevant: 相關文件集合
        k: 考慮前 k 個結果
        
    Returns:
        Recall@K 值
    """
    if len(relevant) == 0:
        return 0.0
    
    retrieved_k = retrieved[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant)
    
    return relevant_count / len(relevant)


def f1_score(precision: float, recall: float) -> float:
    """
    計算 F1-score
    
    F1 = 2 * (P * R) / (P + R)
    
    Args:
        precision: 精確率
        recall: 召回率
        
    Returns:
        F1-score
    """
    if precision + recall == 0:
        return 0.0
    
    return 2.0 * precision * recall / (precision + recall)


def average_precision(retrieved: List[int], relevant: set) -> float:
    """
    計算 Average Precision (AP)
    
    AP = Σ (P@k * rel_k) / (相關文件總數)
    其中 rel_k = 1 如果第 k 個結果相關，否則 0
    
    Args:
        retrieved: 排名後的檢索結果
        relevant: 相關文件集合
        
    Returns:
        Average Precision 值
    """
    if len(relevant) == 0:
        return 0.0
    
    precision_sum = 0.0
    relevant_found = 0
    
    for k, doc in enumerate(retrieved, 1):
        if doc in relevant:
            relevant_found += 1
            precision_at_k_val = precision_at_k(retrieved, relevant, k)
            precision_sum += precision_at_k_val
    
    if relevant_found == 0:
        return 0.0
    
    return precision_sum / len(relevant)


def mean_average_precision(queries_results: List[Tuple[List[int], set]]) -> float:
    """
    計算 Mean Average Precision (MAP)
    
    MAP = Σ AP_i / (查詢數)
    
    Args:
        queries_results: 每個查詢的 (檢索結果, 相關文件集合) 列表
        
    Returns:
        MAP 值
    """
    if len(queries_results) == 0:
        return 0.0
    
    ap_sum = sum(average_precision(retrieved, relevant) 
                 for retrieved, relevant in queries_results)
    
    return ap_sum / len(queries_results)


def ndcg_at_k(retrieved: List[int], relevance_scores: Dict[int, float], k: int) -> float:
    """
    計算 Normalized Discounted Cumulative Gain (NDCG@K)
    
    DCG@K = Σ (2^rel_i - 1) / log2(i + 1)
    NDCG@K = DCG@K / IDCG@K
    
    Args:
        retrieved: 排名後的檢索結果
        relevance_scores: 文件 ID -> 相關性分數的字典
        k: 考慮前 k 個結果
        
    Returns:
        NDCG@K 值
    """
    if k == 0:
        return 0.0
    
    retrieved_k = retrieved[:k]
    
    # 計算 DCG
    dcg = 0.0
    for i, doc in enumerate(retrieved_k, 1):
        rel = relevance_scores.get(doc, 0.0)
        dcg += (2.0 ** rel - 1.0) / math.log2(i + 1)
    
    # 計算 IDCG（理想 DCG）
    # 將所有相關性分數排序，取前 k 個
    all_scores = sorted(relevance_scores.values(), reverse=True)
    ideal_scores = all_scores[:k]
    
    idcg = 0.0
    for i, rel in enumerate(ideal_scores, 1):
        idcg += (2.0 ** rel - 1.0) / math.log2(i + 1)
    
    if idcg == 0:
        return 0.0
    
    return dcg / idcg


def precision_recall_curve(retrieved: List[int], relevant: set) -> Tuple[List[float], List[float]]:
    """
    計算 Precision-Recall 曲線上的點
    
    Args:
        retrieved: 排名後的檢索結果
        relevant: 相關文件集合
        
    Returns:
        (precision_values, recall_values) 列表
    """
    precisions = []
    recalls = []
    
    for k in range(1, len(retrieved) + 1):
        p = precision_at_k(retrieved, relevant, k)
        r = recall_at_k(retrieved, relevant, k)
        precisions.append(p)
        recalls.append(r)
    
    return precisions, recalls


if __name__ == "__main__":
    # 示範用法
    print("=== 資訊檢索評估指標示範 ===\n")
    
    # 模擬一次檢索
    retrieved = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    relevant = {1, 3, 5, 7, 9}  # 實際相關的文件
    
    print("1. 基本指標:")
    for k in [5, 10]:
        p = precision_at_k(retrieved, relevant, k)
        r = recall_at_k(retrieved, relevant, k)
        f1 = f1_score(p, r)
        print(f"  @{k}: P={p:.4f}, R={r:.4f}, F1={f1:.4f}")
    
    print("\n2. Average Precision:")
    ap = average_precision(retrieved, relevant)
    print(f"  AP = {ap:.4f}")
    
    print("\n3. MAP (多個查詢):")
    queries_results = [
        ([1, 2, 3, 4, 5], {1, 3, 5}),
        ([2, 4, 6, 8, 10], {2, 6}),
        ([1, 3, 5, 7, 9], {1, 3, 5, 7, 9})
    ]
    map_score = mean_average_precision(queries_results)
    print(f"  MAP = {map_score:.4f}")
    
    print("\n4. NDCG:")
    relevance_scores = {1: 3.0, 3: 2.0, 5: 3.0, 7: 1.0, 9: 2.0}
    for k in [5, 10]:
        ndcg = ndcg_at_k(retrieved, relevance_scores, k)
        print(f"  NDCG@{k} = {ndcg:.4f}")
    
    print("\n5. Precision-Recall 曲線 (前 5 個點):")
    precisions, recalls = precision_recall_curve(retrieved[:5], relevant)
    for i, (p, r) in enumerate(zip(precisions, recalls), 1):
        print(f"  @{i}: P={p:.4f}, R={r:.4f}")
