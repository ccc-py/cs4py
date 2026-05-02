"""
多層感知機與反向傳播 (Multilayer Perceptron & Backpropagation)

歷史背景：
- 1969 年 Minsky 和 Papert 指出單層感知機無法解決 XOR 問題
- 1974 年 Paul Werbos 首次提出反向傳播演算法
- 1986 年 Rumelhart, Hinton, Williams 發表論文推廣反向傳播
- 引發了第一次神經網路熱潮，是現代深度學習的基石

核心概念：
- 多層結構：輸入層 → 隱藏層 → 輸出層
- 非線性激活函數：Sigmoid, ReLU, Tanh
- 反向傳播：使用鏈式法則從輸出層向輸入層傳播誤差
- 梯度下降：根據誤差梯度更新權重
"""

from typing import List, Tuple, Optional, Callable
import math
import random


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))


def sigmoid_derivative(x: float) -> float:
    s = sigmoid(x)
    return s * (1.0 - s)


def relu(x: float) -> float:
    return max(0.0, x)


def relu_derivative(x: float) -> float:
    return 1.0 if x > 0 else 0.0


def tanh_act(x: float) -> float:
    return math.tanh(x)


def tanh_derivative(x: float) -> float:
    t = math.tanh(x)
    return 1.0 - t * t


class Layer:
    """神經網路層"""

    def __init__(self, n_inputs: int, n_outputs: int, activation: str = "sigmoid"):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        # Xavier 初始化
        limit = math.sqrt(6.0 / (n_inputs + n_outputs))
        self.weights = [
            [random.uniform(-limit, limit) for _ in range(n_inputs)]
            for _ in range(n_outputs)
        ]
        self.biases = [0.0] * n_outputs

        if activation == "sigmoid":
            self.act_fn = sigmoid
            self.act_deriv = sigmoid_derivative
        elif activation == "relu":
            self.act_fn = relu
            self.act_deriv = relu_derivative
        elif activation == "tanh":
            self.act_fn = tanh_act
            self.act_deriv = tanh_derivative
        else:
            self.act_fn = sigmoid
            self.act_deriv = sigmoid_derivative

        self.inputs: List[float] = []
        self.pre_activation: List[float] = []
        self.outputs: List[float] = []
        self.d_weights: List[List[float]] = []
        self.d_biases: List[float] = []
        self.d_inputs: List[float] = []

    def forward(self, inputs: List[float]) -> List[float]:
        self.inputs = inputs[:]
        self.outputs = []
        self.pre_activation = []

        for i in range(self.n_outputs):
            z = self.biases[i]
            for j in range(self.n_inputs):
                z += self.weights[i][j] * inputs[j]
            self.pre_activation.append(z)
            self.outputs.append(self.act_fn(z))

        return self.outputs

    def backward(self, d_outputs: List[float], lr: float) -> List[float]:
        self.d_inputs = [0.0] * self.n_inputs
        self.d_weights = [[0.0] * self.n_inputs for _ in range(self.n_outputs)]
        self.d_biases = [0.0] * self.n_outputs

        d_pre = [0.0] * self.n_outputs
        for i in range(self.n_outputs):
            d_pre[i] = d_outputs[i] * self.act_deriv(self.pre_activation[i])

        for i in range(self.n_outputs):
            self.d_biases[i] = d_pre[i]
            for j in range(self.n_inputs):
                self.d_weights[i][j] = d_pre[i] * self.inputs[j]
                self.d_inputs[j] += d_pre[i] * self.weights[i][j]

            # 更新權重
            self.biases[i] -= lr * self.d_biases[i]
            for j in range(self.n_inputs):
                self.weights[i][j] -= lr * self.d_weights[i][j]

        return self.d_inputs


class MLP:
    """多層感知機"""

    def __init__(self, layer_sizes: List[int], activations: Optional[List[str]] = None):
        """
        初始化 MLP

        參數：
            layer_sizes: 每層的神經元數量 [輸入, 隱藏1, 隱藏2, ..., 輸出]
            activations: 每層的激活函數 (最後一層通常為 sigmoid 或 linear)
        """
        self.layers = []
        if activations is None:
            activations = ["sigmoid"] * (len(layer_sizes) - 1)
            activations[-1] = "sigmoid"  # 輸出層預設 sigmoid

        for i in range(len(layer_sizes) - 1):
            act = activations[i] if i < len(activations) else "sigmoid"
            self.layers.append(Layer(layer_sizes[i], layer_sizes[i + 1], act))

    def forward(self, inputs: List[float]) -> List[float]:
        outputs = inputs
        for layer in self.layers:
            outputs = layer.forward(outputs)
        return outputs

    def backward(self, targets: List[float], lr: float) -> float:
        """反向傳播"""
        # 計算輸出層誤差（均方誤差梯度）
        output_layer = self.layers[-1]
        d_outputs = [
            2.0 * (output_layer.outputs[i] - targets[i]) / len(targets)
            for i in range(len(targets))
        ]

        # 從後向前傳播
        d = d_outputs
        for layer in reversed(self.layers):
            d = layer.backward(d, lr)

        # 計算損失
        loss = sum(
            (output_layer.outputs[i] - targets[i]) ** 2
            for i in range(len(targets))
        ) / len(targets)
        return loss

    def train_step(self, X: List[List[float]], y: List[List[float]], lr: float) -> float:
        """訓練一個 batch"""
        total_loss = 0.0
        for inputs, targets in zip(X, y):
            self.forward(inputs)
            total_loss += self.backward(targets, lr)
        return total_loss / len(X)

    def train(
        self,
        X: List[List[float]],
        y: List[List[float]],
        epochs: int = 1000,
        lr: float = 0.5,
        verbose: bool = False,
    ) -> List[float]:
        """完整訓練流程"""
        history = []
        for epoch in range(epochs):
            loss = self.train_step(X, y, lr)
            history.append(loss)
            if verbose and (epoch % 100 == 0 or epoch == epochs - 1):
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.6f}")
        return history

    def predict(self, X: List[List[float]]) -> List[List[float]]:
        return [self.forward(x) for x in X]


def demo_xor():
    """XOR 問題：單層感知機無法解決，MLP 可以"""
    print("=== XOR 問題 ===\n")

    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [[0], [1], [1], [0]]

    # 2 輸入 → 4 隱藏 → 1 輸出
    random.seed(42)
    mlp = MLP([2, 4, 1], activations=["sigmoid", "sigmoid"])

    history = mlp.train(X, y, epochs=1000, lr=0.5, verbose=True)

    print("\n預測結果：")
    predictions = mlp.predict(X)
    for inputs, pred, true in zip(X, predictions, y):
        p = round(pred[0], 4)
        print(f"  輸入 {inputs} -> {p:.4f} (期望 {true[0]}) {'✓' if round(p) == true[0] else '✗'}")


def demo_circle():
    """圓形分類問題"""
    print("\n=== 圓形分類 ===\n")

    random.seed(42)
    # 生成數據：在圓內為 1，圓外為 0
    X = []
    y = []
    for _ in range(20):
        x1 = random.uniform(-1, 1)
        x2 = random.uniform(-1, 1)
        label = 1 if x1**2 + x2**2 < 0.5 else 0
        X.append([x1, x2])
        y.append([label])

    mlp = MLP([2, 8, 1], activations=["tanh", "sigmoid"])
    history = mlp.train(X, y, epochs=500, lr=0.1, verbose=True)

    print("\n測試點：")
    test_points = [[0, 0], [0.8, 0.8], [-0.4, 0.4]]
    for point in test_points:
        pred = mlp.predict([point])[0][0]
        expected = 1 if point[0]**2 + point[1]**2 < 0.5 else 0
        print(f"  {point} -> {pred:.4f} (期望 {expected})")


def demo_history():
    """收斂曲線"""
    print("\n=== 收斂曲線 ===\n")

    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [[0], [1], [1], [0]]

    random.seed(42)
    mlp = MLP([2, 4, 1])
    history = mlp.train(X, y, epochs=200, lr=0.5, verbose=False)

    print(f"{'Epoch':>6} | {'Loss':>10} | 曲線")
    print("-" * 40)
    for i in range(0, len(history), 20):
        loss = history[i]
        bar = "█" * int(loss * 50)
        print(f"{i:>6} | {loss:>10.6f} | {bar}")


if __name__ == "__main__":
    demo_xor()
    demo_circle()
    demo_history()
