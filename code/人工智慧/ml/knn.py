"""
K-近鄰演算法 (K-Nearest Neighbors, KNN)

歷史背景：
- 1951 年由 Evelyn Fix 和 Joseph Hodges 作為非參數方法首次提出
- 1967 年由 Thomas Cover 和 Peter Hart 進行系統性分析
- 是最簡單的機器學習演算法之一，屬於「惰性學習」（lazy learning）
- 不需要訓練階段，預測時才計算
- 廣泛應用於推薦系統、文字分類、異常檢測

核心概念：
- 將新數據點分類為其 k 個最近鄰居中最常見的類別
- 距離度量：歐幾里得、曼哈頓、閔可夫斯基等
- 權重方式：均勻投票或距離倒數加權
- k 值選擇：k 太小易過擬合，k 太平易忽略局部結構
"""

from typing import List, Tuple, Dict, Optional, Any
import math
from collections import Counter


def euclidean_distance(a: List[float], b: List[float]) -> float:
    """歐幾里得距離"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def manhattan_distance(a: List[float], b: List[float]) -> float:
    """曼哈頓距離"""
    return sum(abs(x - y) for x, y in zip(a, b))


def minkowski_distance(a: List[float], b: List[float], p: float = 2) -> float:
    """閔可夫斯基距離（p=1 為曼哈頓，p=2 為歐幾里得）"""
    return sum(abs(x - y) ** p for x, y in zip(a, b)) ** (1 / p)


class KNNClassifier:
    """K-近鄰分類器"""

    def __init__(
        self,
        k: int = 3,
        distance_func: str = "euclidean",
        weighted: bool = True,
    ):
        """
        初始化 KNN 分類器

        參數：
            k: 鄰居數量
            distance_func: 距離度量方式（euclidean/manhattan/minkowski）
            weighted: 是否使用距離倒數加權投票
        """
        self.k = k
        self.weighted = weighted
        self.X_train: List[List[float]] = []
        self.y_train: List[Any] = []

        if distance_func == "euclidean":
            self.distance_func = euclidean_distance
        elif distance_func == "manhattan":
            self.distance_func = manhattan_distance
        elif distance_func == "minkowski":
            self.distance_func = lambda a, b: minkowski_distance(a, b, p=3)
        else:
            self.distance_func = euclidean_distance

    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """儲存訓練數據（KNN 無需實際訓練）"""
        self.X_train = X
        self.y_train = y

    def predict(self, X: List[List[float]]) -> List[Any]:
        """批量預測"""
        return [self.predict_one(x) for x in X]

    def predict_one(self, x: List[float]) -> Any:
        """預測單一數據點"""
        # 計算與所有訓練點的距離
        distances = []
        for i, train_x in enumerate(self.X_train):
            dist = self.distance_func(x, train_x)
            distances.append((dist, self.y_train[i]))

        # 取 k 個最近鄰居
        distances.sort(key=lambda d: d[0])
        neighbors = distances[:self.k]

        # 投票
        if self.weighted:
            return self._weighted_vote(neighbors)
        else:
            return self._majority_vote(neighbors)

    def predict_proba(self, x: List[float]) -> Dict[Any, float]:
        """
        預測類別概率（基於鄰居比例）
        返回：{類別: 概率}
        """
        distances = []
        for i, train_x in enumerate(self.X_train):
            dist = self.distance_func(x, train_x)
            distances.append((dist, self.y_train[i]))

        distances.sort(key=lambda d: d[0])
        neighbors = distances[:self.k]

        if self.weighted:
            weights: Dict[Any, float] = Counter()
            for dist, label in neighbors:
                weight = 1.0 / (dist + 1e-10)
                weights[label] += weight

            total = sum(weights.values())
            return {label: w / total for label, w in weights.items()}
        else:
            labels = [label for _, label in neighbors]
            counts = Counter(labels)
            total = sum(counts.values())
            return {label: c / total for label, c in counts.items()}

    def accuracy(self, X: List[List[float]], y: List[Any]) -> float:
        """計算分類準確率"""
        predictions = self.predict(X)
        correct = sum(1 for pred, true in zip(predictions, y) if pred == true)
        return correct / len(y) if y else 0.0

    def find_knn(self, x: List[float], k: Optional[int] = None) -> List[Tuple[float, Any]]:
        """返回 k 個最近鄰居的（距離, 標籤）"""
        k = k or self.k
        distances = []
        for i, train_x in enumerate(self.X_train):
            dist = self.distance_func(x, train_x)
            distances.append((dist, self.y_train[i]))
        distances.sort(key=lambda d: d[0])
        return distances[:k]

    def _majority_vote(self, neighbors: List[Tuple[float, Any]]) -> Any:
        """多數投票"""
        labels = [label for _, label in neighbors]
        return Counter(labels).most_common(1)[0][0]

    def _weighted_vote(self, neighbors: List[Tuple[float, Any]]) -> Any:
        """距離倒數加權投票"""
        weights: Dict[Any, float] = Counter()
        for dist, label in neighbors:
            weight = 1.0 / (dist + 1e-10)
            weights[label] += weight
        return weights.most_common(1)[0][0]


def leave_one_out_cv(
    X: List[List[float]],
    y: List[Any],
    k_values: List[int],
    distance_func: str = "euclidean",
) -> List[Tuple[int, float]]:
    """
    Leave-One-Out 交叉驗證找最佳 k

    返回：[(k, accuracy), ...]
    """
    results = []

    for k in k_values:
        correct = 0
        for i in range(len(X)):
            # 留一個點作測試
            test_x = [X[i]]
            test_y = [y[i]]
            train_x = X[:i] + X[i + 1:]
            train_y = y[:i] + y[i + 1:]

            knn = KNNClassifier(k=k, distance_func=distance_func)
            knn.fit(train_x, train_y)

            if knn.predict(test_x)[0] == test_y[0]:
                correct += 1

        accuracy = correct / len(X) if X else 0.0
        results.append((k, accuracy))

    return results


def demo_simple():
    """簡單 2D 分類演示"""
    print("=== KNN 簡單分類 ===\n")

    # 訓練數據：三類點
    X = [
        [1.0, 2.0], [1.5, 1.8], [1.2, 2.2],  # 類別 A
        [5.0, 5.0], [5.5, 4.8], [4.8, 5.2],  # 類別 B
        [1.0, 8.0], [1.5, 7.5], [0.8, 8.2],  # 類別 C
    ]
    y = ["A", "A", "A", "B", "B", "B", "C", "C", "C"]

    knn = KNNClassifier(k=3)
    knn.fit(X, y)

    # 測試點
    test_points = [
        [1.3, 2.0],   # 應為 A
        [5.2, 5.0],   # 應為 B
        [1.2, 8.0],   # 應為 C
        [3.0, 5.0],   # 中間區域
    ]

    print("測試結果：")
    for point in test_points:
        pred = knn.predict_one(point)
        proba = knn.predict_proba(point)
        neighbors = knn.find_knn(point, k=3)
        print(f"  點 {point} -> {pred}")
        print(f"    概率：{ {k: round(v, 3) for k, v in proba.items()} }")
        print(f"    鄰居：{[(round(d, 2), l) for d, l in neighbors]}")


def demo_iris():
    """簡化版鳶尾花分類"""
    print("\n=== 鳶尾花分類（簡化） ===\n")

    # 簡化鳶尾花數據：[萼片長, 萼片寬, 花瓣長, 花瓣寬]
    X = [
        [5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [4.7, 3.2, 1.3, 0.2],
        [5.0, 3.6, 1.4, 0.2], [5.4, 3.9, 1.7, 0.4],                   # setosa
        [6.0, 3.0, 4.5, 1.5], [5.9, 2.8, 4.2, 1.5], [5.7, 2.9, 4.3, 1.3],
        [6.2, 2.9, 4.5, 1.5], [5.5, 2.4, 3.8, 1.1],                   # versicolor
        [7.0, 3.2, 5.5, 2.0], [6.8, 3.0, 5.5, 2.1], [7.2, 3.6, 6.1, 2.5],
        [6.9, 3.2, 5.7, 2.3], [7.1, 3.0, 5.9, 2.1],                   # virginica
    ]
    y = (
        ["setosa"] * 5
        + ["versicolor"] * 5
        + ["virginica"] * 5
    )

    # Leave-one-out 交叉驗證
    for k in [1, 3, 5, 7]:
        knn = KNNClassifier(k=k, weighted=True)
        knn.fit(X, y)
        acc = knn.accuracy(X, y)
        print(f"k={k}: 訓練準確率 = {acc:.1%}")

    # 預測新花
    print("\n預測新花：")
    new_flowers = [
        [5.0, 3.5, 1.3, 0.3],   # 像 setosa
        [5.8, 2.7, 4.1, 1.3],   # 像 versicolor
        [7.0, 3.2, 5.8, 2.2],   # 像 virginica
    ]

    knn = KNNClassifier(k=3)
    knn.fit(X, y)

    for flower in new_flowers:
        pred = knn.predict_one(flower)
        proba = knn.predict_proba(flower)
        print(f"  {flower} -> {pred} ({proba})")


def demo_distance_comparison():
    """距離度量比較"""
    print("\n=== 距離度量比較 ===\n")

    X = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    y = ["A", "B", "A"]

    test = [3, 4, 5]

    for dist_name, dist_func in [
        ("歐幾里得", euclidean_distance),
        ("曼哈頓", manhattan_distance),
        ("閔可夫斯基(p=3)", lambda a, b: minkowski_distance(a, b, p=3)),
    ]:
        knn = KNNClassifier(k=2, distance_func=dist_name if dist_name != "閔可夫斯基(p=3)" else "minkowski")
        knn.fit(X, y)

        neighbors = knn.find_knn(test, k=3)
        print(f"{dist_name}：")
        for d, l in neighbors:
            print(f"  距離={d:.2f}, 類別={l}")
        print()


def demo_k_selection():
    """K 值選擇演示"""
    print("\n=== K 值選擇（交叉驗證） ===\n")

    X = [
        [1.0, 2.0], [1.5, 1.8], [1.2, 2.2],
        [5.0, 5.0], [5.5, 4.8], [4.8, 5.2],
    ]
    y = ["A", "A", "A", "B", "B", "B"]

    results = leave_one_out_cv(X, y, k_values=[1, 2, 3, 5])

    for k, acc in results:
        bar = "█" * int(acc * 20)
        print(f"k={k:>2}: 準確率 = {acc:.1%}  {bar}")


if __name__ == "__main__":
    demo_simple()
    demo_iris()
    demo_distance_comparison()
    demo_k_selection()
