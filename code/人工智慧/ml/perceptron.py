"""
感知機 (Perceptron)

歷史背景：
- 1957 年由 Frank Rosenblatt 在康乃爾大學發明
- 第一個可從資料中學習的人工神經網路模型
- 1969 年 Minsky 和 Papert 在《Perceptrons》中指出其無法解決 XOR 問題
- 導致第一次 AI 寒冬，但也促使多層網路和反向傳播的發展
- 是現代深度學習的基礎構成單元

核心概念：
- 輸入向量 x 與權重 w 的線性組合加上偏置 b
- 輸出：y = sign(w · x + b)
- 使用感知機學習規則更新權重：w = w + η * (y_true - y_pred) * x
- 在線性可分數據上保證收斂
"""

from typing import List, Tuple, Optional
import random


class Perceptron:
    """單層感知機"""

    def __init__(self, n_inputs: int, learning_rate: float = 0.1):
        """
        初始化感知機

        參數：
            n_inputs: 輸入特徵數量
            learning_rate: 學習率 η
        """
        self.n_inputs = n_inputs
        self.lr = learning_rate
        # 初始化權重為小的隨機值
        self.weights = [random.uniform(-0.1, 0.1) for _ in range(n_inputs)]
        self.bias = 0.0
        self.errors: List[int] = []

    def activate(self, weighted_sum: float) -> int:
        """階躍激活函數"""
        return 1 if weighted_sum >= 0 else 0

    def predict(self, inputs: List[float]) -> int:
        """預測單一輸入"""
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias
        return self.activate(weighted_sum)

    def predict_batch(self, inputs: List[List[float]]) -> List[int]:
        """批量預測"""
        return [self.predict(x) for x in inputs]

    def train_step(self, inputs: List[float], expected: int) -> int:
        """
        單步訓練

        返回：預測錯誤數（0 或 1）
        """
        predicted = self.predict(inputs)
        error = expected - predicted

        if error != 0:
            for i in range(self.n_inputs):
                self.weights[i] += self.lr * error * inputs[i]
            self.bias += self.lr * error

        return abs(error)

    def train(
        self,
        data: List[Tuple[List[float], int]],
        epochs: int = 100,
        verbose: bool = False,
    ) -> bool:
        """
        在整個訓練集上訓練感知機

        參數：
            data: 訓練數據 [(輸入, 標籤), ...]
            epochs: 最大訓練回合數
            verbose: 是否打印訓練進度

        返回：是否在最大回合數內收斂
        """
        self.errors = []

        for epoch in range(epochs):
            epoch_errors = 0
            for inputs, expected in data:
                epoch_errors += self.train_step(inputs, expected)

            self.errors.append(epoch_errors)

            if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch + 1}/{epochs}, 錯誤數：{epoch_errors}")

            if epoch_errors == 0:
                if verbose:
                    print(f"在 epoch {epoch + 1} 收斂")
                return True

        return False

    def get_weights(self) -> Tuple[List[float], float]:
        """返回權重和偏置"""
        return self.weights[:], self.bias


def demo_and_gate():
    """AND 閘演示 - 線性可分"""
    print("=== AND 閘 (線性可分) ===\n")

    data = [
        ([0, 0], 0),
        ([0, 1], 0),
        ([1, 0], 0),
        ([1, 1], 1),
    ]

    perceptron = Perceptron(n_inputs=2, learning_rate=0.1)
    random.seed(42)
    converged = perceptron.train(data, epochs=100, verbose=True)

    print(f"\n收斂：{'是' if converged else '否'}")
    print("\n最終預測：")
    for inputs, expected in data:
        pred = perceptron.predict(inputs)
        print(f"  輸入 {inputs} -> 預測 {pred}, 期望 {expected}, {'✓' if pred == expected else '✗'}")


def demo_or_gate():
    """OR 閘演示 - 線性可分"""
    print("\n=== OR 閘 (線性可分) ===\n")

    data = [
        ([0, 0], 0),
        ([0, 1], 1),
        ([1, 0], 1),
        ([1, 1], 1),
    ]

    perceptron = Perceptron(n_inputs=2, learning_rate=0.1)
    random.seed(42)
    converged = perceptron.train(data, epochs=100, verbose=True)

    print(f"\n收斂：{'是' if converged else '否'}")
    print("\n最終預測：")
    for inputs, expected in data:
        pred = perceptron.predict(inputs)
        print(f"  輸入 {inputs} -> 預測 {pred}, 期望 {expected}, {'✓' if pred == expected else '✗'}")


def demo_xor_gate():
    """XOR 閘演示 - 非線性可分（感知機無法解決）"""
    print("\n=== XOR 閘 (非線性可分) ===\n")

    data = [
        ([0, 0], 0),
        ([0, 1], 1),
        ([1, 0], 1),
        ([1, 1], 0),
    ]

    perceptron = Perceptron(n_inputs=2, learning_rate=0.1)
    random.seed(42)
    converged = perceptron.train(data, epochs=100, verbose=True)

    print(f"\n收斂：{'是' if converged else '否'}（XOR 是非線性可分問題）")
    print("\n最終預測（會出錯）：")
    for inputs, expected in data:
        pred = perceptron.predict(inputs)
        print(f"  輸入 {inputs} -> 預測 {pred}, 期望 {expected}, {'✓' if pred == expected else '✗'}")


def demo_2d_classification():
    """2D 點分類演示"""
    print("\n=== 2D 點分類 ===\n")

    # 生成線性可分的二維數據
    random.seed(42)
    data = []
    for _ in range(20):
        x, y = random.uniform(-5, 5), random.uniform(-5, 5)
        label = 1 if y > x + 1 else 0
        data.append(([x, y], label))

    perceptron = Perceptron(n_inputs=2, learning_rate=0.01)
    converged = perceptron.train(data, epochs=50, verbose=True)

    print(f"\n收斂：{'是' if converged else '否'}")

    # 測試幾個點
    test_points = [([1.0, 3.0], 1), ([4.0, 2.0], 0), ([0.0, 2.0], 1)]
    print("\n測試點：")
    for point, expected in test_points:
        pred = perceptron.predict(point)
        print(f"  點 {point} -> 預測 {pred}, 期望 {expected}")


def demo_error_history():
    """訓練錯誤歷史展示"""
    print("\n=== 訓練收斂曲線 ===\n")

    data = [
        ([0, 0], 0),
        ([0, 1], 0),
        ([1, 0], 0),
        ([1, 1], 1),
    ]

    perceptron = Perceptron(n_inputs=2, learning_rate=0.1)
    random.seed(42)
    perceptron.train(data, epochs=20, verbose=False)

    for i, err in enumerate(perceptron.errors):
        bar = "█" * err
        print(f"Epoch {i + 1:2d}: {bar} ({err} errors)")


if __name__ == "__main__":
    demo_and_gate()
    demo_or_gate()
    demo_xor_gate()
    demo_2d_classification()
    demo_error_history()
