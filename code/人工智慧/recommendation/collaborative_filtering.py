"""用戶基協同過濾推薦算法實作"""

from typing import Dict, List, Tuple
import math


def cosine_similarity(u: Dict[int, float], v: Dict[int, float]) -> float:
    """計算兩個用戶的餘弦相似度

    Args:
        u: 用戶u的評分向量，鍵為物品ID，值為評分
        v: 用戶v的評分向量，鍵為物品ID，值為評分

    Returns:
        餘弦相似度，範圍[-1, 1]
    """
    common_items = set(u.keys()) & set(v.keys())
    if not common_items:
        return 0.0
    dot_product = sum(u[item] * v[item] for item in common_items)
    norm_u = math.sqrt(sum(rating ** 2 for rating in u.values()))
    norm_v = math.sqrt(sum(rating ** 2 for rating in v.values()))
    if norm_u == 0 or norm_v == 0:
        return 0.0
    return dot_product / (norm_u * norm_v)


def pearson_correlation(u: Dict[int, float], v: Dict[int, float]) -> float:
    """計算兩個用戶的皮爾森相關係數

    Args:
        u: 用戶u的評分向量
        v: 用戶v的評分向量

    Returns:
        皮爾森相關係數，範圍[-1, 1]
    """
    common_items = set(u.keys()) & set(v.keys())
    if len(common_items) < 2:
        return 0.0
    u_mean = sum(u[item] for item in common_items) / len(common_items)
    v_mean = sum(v[item] for item in common_items) / len(common_items)
    cov = sum((u[item] - u_mean) * (v[item] - v_mean) for item in common_items)
    std_u = math.sqrt(sum((u[item] - u_mean) ** 2 for item in common_items))
    std_v = math.sqrt(sum((v[item] - v_mean) ** 2 for item in common_items))
    if std_u == 0 or std_v == 0:
        return 0.0
    return cov / (std_u * std_v)


def predict_rating(user_id: int, item_id: int, ratings: Dict[int, Dict[int, float]],
                   similarity_func=cosine_similarity, k: int = 3) -> float:
    """預測用戶對未評分物品的評分

    Args:
        user_id: 目標用戶ID
        item_id: 目標物品ID
        ratings: 所有用戶的評分數據，結構為{user_id: {item_id: rating}}
        similarity_func: 相似度計算函數，默認為餘弦相似度
        k: 選取最相似的前k個用戶

    Returns:
        預測評分，若無法預測則返回0.0
    """
    if user_id not in ratings:
        return 0.0
    target_ratings = ratings[user_id]
    similarities = []
    for other_id, other_ratings in ratings.items():
        if other_id == user_id:
            continue
        if item_id not in other_ratings:
            continue
        sim = similarity_func(target_ratings, other_ratings)
        if sim > 0:
            similarities.append((sim, other_ratings[item_id]))
    if not similarities:
        return 0.0
    similarities.sort(reverse=True, key=lambda x: x[0])
    top_k = similarities[:k]
    numerator = sum(sim * rating for sim, rating in top_k)
    denominator = sum(sim for sim, _ in top_k)
    return numerator / denominator if denominator != 0 else 0.0


def top_n_recommendations(user_id: int, ratings: Dict[int, Dict[int, float]],
                         n: int = 5, similarity_func=cosine_similarity, k: int = 3) -> List[int]:
    """生成用戶的Top-N推薦列表

    Args:
        user_id: 目標用戶ID
        ratings: 所有用戶的評分數據
        n: 推薦數量
        similarity_func: 相似度計算函數
        k: 預測評分時使用的相似用戶數量

    Returns:
        推薦物品ID列表，按預測評分降序排列
    """
    if user_id not in ratings:
        return []
    target_ratings = ratings[user_id]
    all_items = set()
    for user_ratings in ratings.values():
        all_items.update(user_ratings.keys())
    unrated_items = all_items - set(target_ratings.keys())
    item_scores = []
    for item_id in unrated_items:
        pred = predict_rating(user_id, item_id, ratings, similarity_func, k)
        if pred > 0:
            item_scores.append((pred, item_id))
    item_scores.sort(reverse=True, key=lambda x: x[0])
    return [item_id for _, item_id in item_scores[:n]]


if __name__ == "__main__":
    # 示例用戶-物品評分矩陣
    ratings = {
        1: {101: 5, 102: 3, 103: 4, 104: 2},
        2: {101: 4, 102: 5, 103: 3, 105: 4},
        3: {101: 2, 102: 4, 104: 5, 105: 3},
        4: {102: 2, 103: 5, 104: 4, 105: 5}
    }
    print("協同過濾演示")
    print("用戶1的Top-3推薦（餘弦相似度）:", top_n_recommendations(1, ratings, n=3))
    print("用戶1對物品105的預測評分（餘弦相似度）:", predict_rating(1, 105, ratings))
    print("用戶1的Top-3推薦（皮爾森相關）:", top_n_recommendations(1, ratings, n=3, similarity_func=pearson_correlation))
    print("用戶1對物品105的預測評分（皮爾森相關）:", predict_rating(1, 105, ratings, similarity_func=pearson_correlation))
