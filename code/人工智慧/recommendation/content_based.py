"""內容基推薦算法實作"""

from typing import Dict, List, Tuple
import math


def compute_tfidf(documents: List[str]) -> Tuple[List[Dict[str, float]], Dict[str, float]]:
    """計算文檔集合的TF-IDF特徵

    Args:
        documents: 文檔列表，每個文檔為一個字符串

    Returns:
        (TF-IDF特徵列表, 詞彙到索引的映射)
    """
    doc_count = len(documents)
    word_doc_freq = {}
    doc_word_freqs = []
    for doc in documents:
        words = doc.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
            word_doc_freq[word] = word_doc_freq.get(word, 0) + 1
        doc_word_freqs.append(word_freq)
    vocab = sorted(word_doc_freq.keys())
    vocab_index = {word: i for i, word in enumerate(vocab)}
    tfidf_features = []
    for word_freq in doc_word_freqs:
        features = {}
        max_freq = max(word_freq.values()) if word_freq else 1
        for word, freq in word_freq.items():
            tf = freq / max_freq
            idf = math.log(doc_count / (word_doc_freq[word] + 1))
            features[word] = tf * idf
        tfidf_features.append(features)
    return tfidf_features, vocab_index


def cosine_similarity_vec(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """計算兩個向量的餘弦相似度

    Args:
        vec1: 第一個向量，鍵為特徵名，值為權重
        vec2: 第二個向量

    Returns:
        餘弦相似度
    """
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    dot = sum(vec1[k] * vec2[k] for k in common)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def build_user_profile(liked_items: List[int], item_features: List[Dict[str, float]]) -> Dict[str, float]:
    """根據用戶喜歡的物品構建用戶畫像

    Args:
        liked_items: 用戶喜歡的物品索引列表
        item_features: 所有物品的特徵列表

    Returns:
        用戶畫像向量
    """
    profile = {}
    for item_idx in liked_items:
        features = item_features[item_idx]
        for word, weight in features.items():
            profile[word] = profile.get(word, 0.0) + weight
    if liked_items:
        for word in profile:
            profile[word] /= len(liked_items)
    return profile


def recommend_items(user_profile: Dict[str, float], item_features: List[Dict[str, float]],
                    item_ids: List[int], liked_items: List[int], n: int = 5) -> List[int]:
    """根據用戶畫像推薦物品

    Args:
        user_profile: 用戶畫像向量
        item_features: 所有物品的特徵列表
        item_ids: 物品ID列表，與item_features對應
        liked_items: 用戶已喜歡的物品索引（排除）
        n: 推薦數量

    Returns:
        推薦物品ID列表，按相似度降序排列
    """
    scores = []
    for idx, features in enumerate(item_features):
        if idx in liked_items:
            continue
        sim = cosine_similarity_vec(user_profile, features)
        if sim > 0:
            scores.append((sim, item_ids[idx]))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [item_id for _, item_id in scores[:n]]


if __name__ == "__main__":
    # 示例物品描述
    items = [
        "action adventure hero save world",
        "romance love story couple happy ending",
        "action combat fight battle warrior",
        "comedy funny joke laugh entertainment",
        "romance drama emotional relationship",
        "adventure exploration discover treasure map"
    ]
    item_ids = [101, 102, 103, 104, 105, 106]
    print("內容基推薦演示")
    features, vocab = compute_tfidf(items)
    print(f"詞彙表大小: {len(vocab)}")
    liked_indices = [0, 2]
    profile = build_user_profile(liked_indices, features)
    print(f"用戶畫像關鍵詞: {list(profile.keys())[:5]}")
    recommendations = recommend_items(profile, features, item_ids, liked_indices, n=3)
    print(f"推薦物品ID: {recommendations}")
    print("\n物品相似度:")
    for i in range(len(items)):
        if i not in liked_indices:
            sim = cosine_similarity_vec(profile, features[i])
            print(f"  與物品{item_ids[i]}的相似度: {sim:.3f}")
