"""
決策樹 (Decision Tree)

歷史背景：
- 1970 年代由 J. Ross Quinlan 發展 ID3 演算法
- 1986 年 Quinlan 提出 C4.5，改進處理連續特徵
- 1984 年 Breiman 等人提出 CART（分類與迴歸樹）
- 是機器學習中最易於解釋的模型之一
- 是隨機森林、梯度提升樹等集成方法的基礎

核心概念：
- 遞迴選擇最佳特徵分割數據，直到純度足夠或達到深度限制
- ID3 使用資訊增益（Information Gain）
- C4.5 使用資訊增益比（Gain Ratio）
- CART 使用基尼不純度（Gini Impurity）
"""

from typing import List, Tuple, Dict, Optional, Any
import math
from collections import Counter


class DecisionNode:
    """決策樹節點"""

    def __init__(
        self,
        feature_idx: Optional[int] = None,
        threshold: Optional[float] = None,
        value: Optional[Any] = None,
        left: Optional['DecisionNode'] = None,
        right: Optional['DecisionNode'] = None,
    ):
        self.feature_idx = feature_idx  # 用於分割的特徵索引
        self.threshold = threshold      # 分割閾值
        self.value = value              # 葉節點的預測值
        self.left = left                # 左子樹（<= threshold）
        self.right = right              # 右子樹（> threshold）

    def is_leaf(self) -> bool:
        return self.value is not None


class DecisionTree:
    """
    基於 CART 演算法的決策樹（使用基尼不純度）

    支援分類任務，處理連續和離散特徵。
    """

    def __init__(
        self,
        max_depth: Optional[int] = None,
        min_samples_split: int = 2,
        min_impurity_decrease: float = 0.0,
    ):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_impurity_decrease = min_impurity_decrease
        self.root: Optional[DecisionNode] = None

    def fit(self, X: List[List[float]], y: List[Any]) -> None:
        """訓練決策樹"""
        self.root = self._build_tree(X, y, depth=0)

    def predict(self, X: List[List[float]]) -> List[Any]:
        """批量預測"""
        return [self._predict_one(x, self.root) for x in X]

    def predict_one(self, x: List[float]) -> Any:
        """預測單一數據點"""
        return self._predict_one(x, self.root)

    def print_tree(self) -> str:
        """以字串形式打印決策樹"""
        if self.root is None:
            return "樹尚未訓練"
        return self._print_node(self.root, indent=0)

    def _predict_one(self, x: List[float], node: Optional[DecisionNode]) -> Any:
        """遞迴預測單一數據點"""
        if node is None or node.is_leaf():
            return node.value if node else None

        if x[node.feature_idx] <= node.threshold:
            return self._predict_one(x, node.left)
        else:
            return self._predict_one(x, node.right)

    def _build_tree(
        self,
        X: List[List[float]],
        y: List[Any],
        depth: int,
    ) -> DecisionNode:
        """遞迴建立決策樹"""
        n_samples = len(y)
        n_classes = len(set(y))

        # 終止條件：達到最大深度、樣本數不足、或已純淨
        if (
            n_classes == 1
            or n_samples < self.min_samples_split
            or (self.max_depth is not None and depth >= self.max_depth)
        ):
            return DecisionNode(value=self._most_common(y))

        # 尋找最佳分割
        best_feature, best_threshold, best_gain = self._best_split(X, y)

        if best_feature is None or best_gain < self.min_impurity_decrease:
            return DecisionNode(value=self._most_common(y))

        # 分割數據
        left_X, left_y, right_X, right_y = self._split_data(
            X, y, best_feature, best_threshold
        )

        if not left_y or not right_y:
            return DecisionNode(value=self._most_common(y))

        # 遞迴建立子樹
        left_child = self._build_tree(left_X, left_y, depth + 1)
        right_child = self._build_tree(right_X, right_y, depth + 1)

        return DecisionNode(
            feature_idx=best_feature,
            threshold=best_threshold,
            left=left_child,
            right=right_child,
        )

    def _best_split(
        self,
        X: List[List[float]],
        y: List[Any],
    ) -> Tuple[Optional[int], Optional[float], float]:
        """
        尋找最佳分割（基尼不純度）

        返回：(最佳特徵索引, 最佳閾值, 基尼增益)
        """
        best_feature = None
        best_threshold = None
        best_gain = 0.0

        parent_gini = self._gini(y)
        n_samples = len(y)

        n_features = len(X[0]) if X else 0

        for feature_idx in range(n_features):
            # 收集該特徵的所有可能閾值（相鄰不同類別值的中點）
            values = sorted(set(x[feature_idx] for x in X))

            if len(values) <= 1:
                continue

            thresholds = [
                (values[i] + values[i + 1]) / 2 for i in range(len(values) - 1)
            ]

            for threshold in thresholds:
                left_y = [
                    y[i] for i in range(n_samples)
                    if X[i][feature_idx] <= threshold
                ]
                right_y = [
                    y[i] for i in range(n_samples)
                    if X[i][feature_idx] > threshold
                ]

                if not left_y or not right_y:
                    continue

                # 計算基尼增益
                left_weight = len(left_y) / n_samples
                right_weight = len(right_y) / n_samples
                child_gini = (
                    left_weight * self._gini(left_y)
                    + right_weight * self._gini(right_y)
                )
                gain = parent_gini - child_gini

                if gain > best_gain or (best_feature is None and gain >= 0):
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _split_data(
        self,
        X: List[List[float]],
        y: List[Any],
        feature_idx: int,
        threshold: float,
    ) -> Tuple[List[List[float]], List[Any], List[List[float]], List[Any]]:
        """依特徵和閾值分割數據"""
        left_X, left_y = [], []
        right_X, right_y = [], []

        for i in range(len(X)):
            if X[i][feature_idx] <= threshold:
                left_X.append(X[i])
                left_y.append(y[i])
            else:
                right_X.append(X[i])
                right_y.append(y[i])

        return left_X, left_y, right_X, right_y

    @staticmethod
    def _gini(y: List[Any]) -> float:
        """計算基尼不純度"""
        if not y:
            return 0.0
        counts = Counter(y)
        n = len(y)
        return 1.0 - sum((count / n) ** 2 for count in counts.values())

    @staticmethod
    def _most_common(y: List[Any]) -> Any:
        """返回最常出現的類別"""
        return Counter(y).most_common(1)[0][0]

    def _print_node(self, node: DecisionNode, indent: int) -> str:
        """遞迴打印決策樹"""
        lines = []

        if node.is_leaf():
            lines.append("  " * indent + f"→ 預測: {node.value}")
        else:
            lines.append("  " * indent + f"特徵[{node.feature_idx}] <= {node.threshold:.2f}?")
            lines.append("  " * (indent + 1) + "是:")
            lines.append(self._print_node(node.left, indent + 2))
            lines.append("  " * (indent + 1) + "否:")
            lines.append(self._print_node(node.right, indent + 2))

        return "\n".join(lines)


def demo_xor():
    """XOR 問題演示"""
    print("=== XOR 問題 ===\n")

    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ]
    y = [0, 1, 1, 0]

    tree = DecisionTree(max_depth=3)
    tree.fit(X, y)

    predictions = tree.predict(X)
    print("預測結果：")
    for x, pred, true in zip(X, predictions, y):
        print(f"  {x} -> {pred}（期望 {true}）{'✓' if pred == true else '✗'}")

    print(f"\n決策樹：\n{tree.print_tree()}")


def demo_iris_like():
    """類鳶尾花分類演示"""
    print("\n=== 類鳶尾花分類 ===\n")

    # 模擬簡化版鳶尾花數據：[萼片長度, 花瓣長度]
    X = [
        [5.1, 1.4], [4.9, 1.3], [4.7, 1.5], [5.0, 1.4],  # setosa
        [6.0, 4.0], [5.9, 3.8], [6.2, 4.1], [5.8, 3.9],  # versicolor
        [7.0, 5.5], [6.8, 5.3], [7.2, 5.7], [6.9, 5.1],  # virginica
    ]
    y = (
        ["setosa"] * 4
        + ["versicolor"] * 4
        + ["virginica"] * 4
    )

    tree = DecisionTree(max_depth=3)
    tree.fit(X, y)

    print("分類結果：")
    for x, pred, true in zip(X, tree.predict(X), y):
        print(f"  {x} -> {pred}{'✓' if pred == true else '✗'}")

    print(f"\n決策樹：\n{tree.print_tree()}")


def demo_decision_boundary():
    """決策邊界展示"""
    print("\n=== 2D 分類與決策邊界 ===\n")

    X = [
        [1, 2], [2, 1], [1, 1], [2, 2],       # 類別 A（左下）
        [8, 8], [9, 8], [8, 9], [9, 9],       # 類別 B（右上）
        [1, 8], [2, 9], [1, 9], [2, 8],       # 類別 C（左上）
    ]
    y = ["A"] * 4 + ["B"] * 4 + ["C"] * 4

    tree = DecisionTree(max_depth=3)
    tree.fit(X, y)

    # 測試一些點
    test_points = [
        [1.5, 1.5],  # 應為 A
        [8.5, 8.5],  # 應為 B
        [1.5, 8.5],  # 應為 C
        [5, 5],      # 中間區域
    ]

    print("測試點分類：")
    for point in test_points:
        pred = tree.predict_one(point)
        print(f"  {point} -> {pred}")

    print(f"\n決策樹：\n{tree.print_tree()}")


if __name__ == "__main__":
    demo_xor()
    demo_iris_like()
    demo_decision_boundary()
