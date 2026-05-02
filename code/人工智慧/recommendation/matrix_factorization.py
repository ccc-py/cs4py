"""矩陣分解推薦算法實作（基於SVD的潛在因子模型）"""

from typing import Dict, List, Tuple
import math
import random


def initialize_factors(num_users: int, num_items: int, num_factors: int) -> Tuple[List[List[float]], List[List[float]]]:
    """初始化用戶和物品的潛在因子矩陣

    Args:
        num_users: 用戶數量
        num_items: 物品數量
        num_factors: 潛在因子維度

    Returns:
        (用戶因子矩陣, 物品因子矩陣)
    """
    random.seed(42)
    user_factors = [[random.gauss(0, 0.1) for _ in range(num_factors)] for _ in range(num_users)]
    item_factors = [[random.gauss(0, 0.1) for _ in range(num_factors)] for _ in range(num_items)]
    return user_factors, item_factors


def predict(user_factors: List[float], item_factors: List[float]) -> float:
    """計算用戶因子與物品因子的內積預測評分

    Args:
        user_factors: 用戶的潛在因子向量
        item_factors: 物品的潛在因子向量

    Returns:
        預測評分
    """
    return sum(u * i for u, i in zip(user_factors, item_factors))


def train_sgd(ratings: Dict[int, Dict[int, float]], num_factors: int = 10,
              learning_rate: float = 0.01, regularization: float = 0.02,
              num_epochs: int = 20) -> Tuple[List[List[float]], List[List[float]]]:
    """使用隨機梯度下降訓練矩陣分解模型

    Args:
        ratings: 評分數據，結構為{user_id: {item_id: rating}}
        num_factors: 潛在因子維度
        learning_rate: 學習率
        regularization: 正則化參數
        num_epochs: 訓練輪數

    Returns:
        (用戶因子矩陣, 物品因子矩陣)
    """
    users = sorted(ratings.keys())
    items = set()
    for user_ratings in ratings.values():
        items.update(user_ratings.keys())
    items = sorted(items)
    user_index = {u: i for i, u in enumerate(users)}
    item_index = {i: idx for idx, i in enumerate(items)}
    num_users, num_items = len(users), len(items)
    user_factors, item_factors = initialize_factors(num_users, num_items, num_factors)
    training_data = []
    for user_id, user_ratings in ratings.items():
        for item_id, rating in user_ratings.items():
            training_data.append((user_index[user_id], item_index[item_id], rating))
    random.seed(42)
    for epoch in range(num_epochs):
        random.shuffle(training_data)
        total_error = 0.0
        for u_idx, i_idx, rating in training_data:
            pred = predict(user_factors[u_idx], item_factors[i_idx])
            error = rating - pred
            total_error += error ** 2
            for f in range(num_factors):
                user_grad = error * item_factors[i_idx][f] - regularization * user_factors[u_idx][f]
                item_grad = error * user_factors[u_idx][f] - regularization * item_factors[i_idx][f]
                user_factors[u_idx][f] += learning_rate * user_grad
                item_factors[i_idx][f] += learning_rate * item_grad
        rmse = math.sqrt(total_error / len(training_data))
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch + 1}/{num_epochs}, RMSE: {rmse:.4f}")
    return user_factors, item_factors


def predict_rating_mf(user_id: int, item_id: int,
                      user_factors: List[List[float]], item_factors: List[List[float]],
                      user_index: Dict[int, int], item_index: Dict[int, int]) -> float:
    """使用訓練好的矩陣分解模型預測評分

    Args:
        user_id: 用戶ID
        item_id: 物品ID
        user_factors: 用戶因子矩陣
        item_factors: 物品因子矩陣
        user_index: 用戶ID到索引的映射
        item_index: 物品ID到索引的映射

    Returns:
        預測評分
    """
    if user_id not in user_index or item_id not in item_index:
        return 0.0
    u_idx = user_index[user_id]
    i_idx = item_index[item_id]
    return predict(user_factors[u_idx], item_factors[i_idx])


def top_n_recommendations_mf(user_id: int, ratings: Dict[int, Dict[int, float]],
                             user_factors: List[List[float]], item_factors: List[List[float]],
                             user_index: Dict[int, int], item_index: Dict[int, int],
                             n: int = 5) -> List[int]:
    """使用矩陣分解模型生成Top-N推薦

    Args:
        user_id: 目標用戶ID
        ratings: 原始評分數據
        user_factors: 用戶因子矩陣
        item_factors: 物品因子矩陣
        user_index: 用戶ID到索引的映射
        item_index: 物品ID到索引的映射
        n: 推薦數量

    Returns:
        推薦物品ID列表
    """
    if user_id not in ratings:
        return []
    target_ratings = ratings[user_id]
    u_idx = user_index[user_id]
    item_scores = []
    for item_id, i_idx in item_index.items():
        if item_id in target_ratings:
            continue
        score = predict(user_factors[u_idx], item_factors[i_idx])
        item_scores.append((score, item_id))
    item_scores.sort(reverse=True, key=lambda x: x[0])
    return [item_id for _, item_id in item_scores[:n]]


if __name__ == "__main__":
    # 示例評分數據
    ratings = {
        1: {101: 5, 102: 3, 103: 4, 104: 2},
        2: {101: 4, 102: 5, 103: 3, 105: 4},
        3: {101: 2, 102: 4, 104: 5, 105: 3},
        4: {102: 2, 103: 5, 104: 4, 105: 5}
    }
    print("矩陣分解推薦演示")
    users = sorted(ratings.keys())
    items = set()
    for user_ratings in ratings.values():
        items.update(user_ratings.keys())
    items = sorted(items)
    user_index = {u: i for i, u in enumerate(users)}
    item_index = {i: idx for idx, i in enumerate(items)}
    user_factors, item_factors = train_sgd(ratings, num_factors=5, num_epochs=20)
    print("\n預測評分:")
    for user_id in [1, 2]:
        for item_id in [105, 106]:
            if item_id not in ratings.get(user_id, {}):
                pred = predict_rating_mf(user_id, item_id, user_factors, item_factors, user_index, item_index)
                print(f"  用戶{user_id}對物品{item_id}的預測評分: {pred:.2f}")
    print("\nTop-3推薦:")
    for user_id in [1, 2]:
        recs = top_n_recommendations_mf(user_id, ratings, user_factors, item_factors, user_index, item_index, n=3)
        print(f"  用戶{user_id}的Top-3推薦: {recs}")
