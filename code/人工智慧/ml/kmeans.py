"""
K-Means 分群演算法 (K-Means Clustering)

歷史背景：
- 1957 年由 Stuart Lloyd 在貝爾實驗室提出（Lloyd 演算法）
- 1967 年由 James MacQueen 正式命名為 K-Means
- 是最經典且廣泛使用的分群演算法
- 應用於資料壓縮、影像分割、市場區隔、異常檢測等

核心概念：
- 將數據分為 k 個群集，每個數據點屬於最近的群集中心
- 迭代優化：分配 → 更新中心 → 重複直到收斂
- 目標：最小化群集內平方和（WCSS / inertia）
"""

from typing import List, Tuple, Optional
import math
import random


def euclidean_distance(a: List[float], b: List[float]) -> float:
    """計算兩點之間的歐幾里得距離"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def kmeans(
    data: List[List[float]],
    k: int,
    max_iters: int = 100,
    tolerance: float = 1e-4,
    seed: Optional[int] = None,
) -> Tuple[List[int], List[List[float]], float]:
    """
    K-Means 分群演算法

    參數：
        data: 數據點列表，每個點為特徵向量
        k: 分群數量
        max_iters: 最大迭代次數
        tolerance: 收斂容忍值（中心點移動小於此值則停止）
        seed: 隨機種子

    返回：
        (labels, centroids, inertia)
        - labels: 每個數據點的群集標籤
        - centroids: 最終群集中心點
        - inertia: 群集內平方和
    """
    if seed is not None:
        random.seed(seed)

    n = len(data)
    dim = len(data[0]) if n > 0 else 0

    # 隨機選擇初始中心點（K-Means++ 初始化）
    centroids = _kmeans_plus_plus_init(data, k, dim)

    labels = [0] * n

    for iteration in range(max_iters):
        # 步驟 1：分配每個點到最近的中心
        new_labels = []
        for point in data:
            distances = [euclidean_distance(point, c) for c in centroids]
            new_labels.append(distances.index(min(distances)))

        # 檢查是否收斂
        if new_labels == labels and iteration > 0:
            break
        labels = new_labels

        # 步驟 2：更新中心點
        old_centroids = [c[:] for c in centroids]
        centroids = _update_centroids(data, labels, k, dim)

        # 檢查中心點移動是否小於容忍值
        max_shift = max(
            euclidean_distance(old, new)
            for old, new in zip(old_centroids, centroids)
        )
        if max_shift < tolerance:
            break

    # 計算 inertia（WCSS）
    inertia = sum(
        euclidean_distance(point, centroids[label]) ** 2
        for point, label in zip(data, labels)
    )

    return labels, centroids, inertia


def _kmeans_plus_plus_init(
    data: List[List[float]],
    k: int,
    dim: int,
) -> List[List[float]]:
    """K-Means++ 初始化：讓初始中心點分散開"""
    n = len(data)
    centroids = [data[random.randint(0, n - 1)][:]]

    for _ in range(1, k):
        # 計算每個點到最近中心的距離平方
        distances = []
        for point in data:
            min_dist = min(
                euclidean_distance(point, c) ** 2 for c in centroids
            )
            distances.append(min_dist)

        # 依概率選擇下一個中心（距離越遠越可能被選中）
        total = sum(distances)
        if total == 0:
            break

        r = random.uniform(0, total)
        cumulative = 0.0
        for i, d in enumerate(distances):
            cumulative += d
            if cumulative >= r:
                centroids.append(data[i][:])
                break
        else:
            centroids.append(data[-1][:])

    return centroids


def _update_centroids(
    data: List[List[float]],
    labels: List[int],
    k: int,
    dim: int,
) -> List[List[float]]:
    """計算每個群集的新中心點"""
    new_centroids = []

    for cluster_id in range(k):
        members = [data[i] for i in range(len(data)) if labels[i] == cluster_id]

        if not members:
            # 空群集：保留原位置或隨機選一個點
            new_centroids.append([0.0] * dim)
            continue

        centroid = []
        for d in range(dim):
            centroid.append(sum(m[d] for m in members) / len(members))
        new_centroids.append(centroid)

    return new_centroids


def predict(
    point: List[float],
    centroids: List[List[float]],
) -> int:
    """預測新數據點屬於哪個群集"""
    distances = [euclidean_distance(point, c) for c in centroids]
    return distances.index(min(distances))


def print_clusters(
    data: List[List[float]],
    labels: List[int],
    centroids: List[List[float]],
) -> str:
    """以字串形式打印分群結果"""
    clusters: dict = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(data[i])

    lines = []
    for cluster_id, members in sorted(clusters.items()):
        center = centroids[cluster_id]
        lines.append(f"群集 {cluster_id}（中心：{[round(c, 2) for c in center]}，{len(members)} 個點）：")
        for m in members:
            lines.append(f"  {m}")

    return "\n".join(lines)


def demo_1d():
    """一維數據分群演示"""
    print("=== K-Means 一維分群 ===\n")

    data = [[x] for x in [1, 2, 3, 10, 11, 12, 20, 21, 22]]

    labels, centroids, inertia = kmeans(data, k=3, seed=42)

    print(f"分群結果（inertia={inertia:.2f}）：")
    print(print_clusters(data, labels, centroids))


def demo_2d():
    """二維數據分群演示"""
    print("\n=== K-Means 二維分群 ===\n")

    random.seed(42)
    # 生成三個自然群集
    data = []
    for cx, cy in [(2, 2), (8, 8), (2, 8)]:
        for _ in range(5):
            x = cx + random.gauss(0, 0.5)
            y = cy + random.gauss(0, 0.5)
            data.append([round(x, 2), round(y, 2)])

    labels, centroids, inertia = kmeans(data, k=3, seed=42)

    print(f"分群結果（inertia={inertia:.2f}）：")
    print(print_clusters(data, labels, centroids))


def demo_elbow():
    """Elbow 方法找最佳 k 值"""
    print("\n=== Elbow 方法 ===\n")

    random.seed(42)
    data = []
    for cx, cy in [(2, 2), (8, 8), (2, 8)]:
        for _ in range(5):
            data.append([cx + random.gauss(0, 0.5), cy + random.gauss(0, 0.5)])

    print("k 值 | inertia")
    print("-" * 20)
    for k in range(1, 7):
        _, _, inertia = kmeans(data, k=k, seed=42, max_iters=50)
        bar = "█" * int(inertia / 5)
        print(f"  {k}  | {inertia:8.2f} {bar}")


def demo_image_colors():
    """簡單色彩分群演示"""
    print("\n=== 色彩分群（RGB 空間） ===\n")

    # 模擬圖片中的像素顏色
    colors = [
        [255, 0, 0], [250, 10, 5], [245, 5, 10],    # 紅色系
        [0, 255, 0], [5, 250, 10], [10, 245, 5],    # 綠色系
        [0, 0, 255], [5, 10, 250], [10, 5, 245],    # 藍色系
        [128, 128, 128], [120, 130, 125],           # 灰色系
    ]

    labels, centroids, _ = kmeans(colors, k=4, seed=42)

    print(f"分群結果：")
    print(print_clusters(colors, labels, centroids))

    print("\n壓縮後的調色盤：")
    for i, c in enumerate(centroids):
        print(f"  色彩 {i}: RGB({[int(round(x)) for x in c]})")


if __name__ == "__main__":
    demo_1d()
    demo_2d()
    demo_elbow()
    demo_image_colors()
