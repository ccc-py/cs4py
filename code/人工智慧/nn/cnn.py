"""
卷積神經網路 (Convolutional Neural Network, CNN)

歷史背景：
- 1980 年代：Kunihiko Fukushima 提出 Neocognitron，啟發了 CNN
- 1989 年：Yann LeCun 應用反向傳播到卷積層，提出 LeNet
- 1998 年：LeNet-5 成功應用於郵政編碼手寫數字識別
- 2012 年：AlexNet 在 ImageNet 競賽中大幅超越傳統方法，引發深度學習熱潮
- 2015 年：ResNet 引入殘差連接，解決深層網路退化問題

核心概念：
- 卷積層 (Conv2D)：使用濾核在圖像上滑動，提取局部特徵
- 池化層 (Pooling)：下採樣，減少參數量，增加平移不變性
- 權值共享：同一濾核在全圖使用，大幅減少參數
- 局部感受野：每個神經元只連接輸入的局部區域

本實作包含：
- Conv2D, MaxPool2D, Flatten, Linear 層
- 純 Python 實現卷積正向/反向傳播
- 使用 SGD 訓練小型圖像分類任務
"""

from typing import List, Tuple, Optional
import math
import random


def conv2d_forward(input_3d: List[List[List[float]]], kernel_3d: List[List[List[float]]],
                   stride: int = 1, padding: int = 0) -> List[List[List[float]]]:
    """
    2D 卷積正向傳播
    input_3d: [C_in, H, W]
    kernel_3d: [C_out, C_in, K, K]
    返回: [C_out, H_out, W_out]
    """
    c_in, h_in, w_in = len(input_3d), len(input_3d[0]), len(input_3d[0][0])
    c_out = len(kernel_3d)
    k_size = len(kernel_3d[0][0])

    h_out = (h_in + 2 * padding - k_size) // stride + 1
    w_out = (w_in + 2 * padding - k_size) // stride + 1

    # Padding
    if padding > 0:
        padded = [[[0.0] * (w_in + 2 * padding) for _ in range(h_in + 2 * padding)] for _ in range(c_in)]
        for c in range(c_in):
            for r in range(h_in):
                for cc in range(w_in):
                    padded[c][r + padding][cc + padding] = input_3d[c][r][cc]
    else:
        padded = input_3d

    output = [[[0.0] * w_out for _ in range(h_out)] for _ in range(c_out)]

    for co in range(c_out):
        for ci in range(c_in):
            for r in range(h_out):
                for c in range(w_out):
                    r_start = r * stride
                    c_start = c * stride
                    sum_val = 0.0
                    for kr in range(k_size):
                        for kc in range(k_size):
                            sum_val += padded[ci][r_start + kr][c_start + kc] * kernel_3d[co][ci][kr][kc]
                    output[co][r][c] += sum_val

    return output


def relu_forward(x: List) -> List:
    if isinstance(x, list):
        return [relu_forward(v) for v in x]
    return max(0.0, x)


def max_pool2d_forward(input_3d: List[List[List[float]]], k_size: int = 2,
                       stride: int = 2) -> Tuple[List[List[List[float]]], List[List[List[List[Tuple[int, int]]]]]]:
    """Max Pooling 正向傳播，返回輸出和最大值位置"""
    c_in = len(input_3d)
    h_in = len(input_3d[0])
    w_in = len(input_3d[0][0])

    h_out = (h_in - k_size) // stride + 1
    w_out = (w_in - k_size) // stride + 1

    output = [[[0.0] * w_out for _ in range(h_out)] for _ in range(c_in)]
    indices = [[[[ (0,0) ] * w_out for _ in range(h_out)] for _ in range(c_in)]] # Simplified structure needed

    # Correct indices structure
    indices = []

    for c in range(c_in):
        c_indices = []
        for r in range(h_out):
            r_indices = []
            for cc in range(w_out):
                r_start = r * stride
                c_start = cc * stride
                max_val = -float('inf')
                max_pos = (0, 0)
                for kr in range(k_size):
                    for kc in range(k_size):
                        val = input_3d[c][r_start + kr][c_start + kc]
                        if val > max_val:
                            max_val = val
                            max_pos = (kr, kc)
                output[c][r][cc] = max_val
                r_indices.append(max_pos)
            c_indices.append(r_indices)
        indices.append(c_indices)

    return output, indices


class ConvLayer:
    def __init__(self, c_in: int, c_out: int, k_size: int = 3, stride: int = 1, padding: int = 0):
        self.c_in = c_in
        self.c_out = c_out
        self.k_size = k_size
        self.stride = stride
        self.padding = padding

        # He initialization
        limit = math.sqrt(2.0 / (c_in * k_size * k_size))
        self.weights = [[[
            [random.uniform(-limit, limit) for _ in range(k_size)]
            for _ in range(k_size)]
            for _ in range(c_in)]
            for _ in range(c_out)]

        self.bias = [0.0] * c_out
        self.input = None
        self.d_weights = None
        self.d_bias = None
        self.unpadded_input = None

    def forward(self, x: List[List[List[float]]]) -> List[List[List[float]]]:
        self.input = x
        out = conv2d_forward(x, self.weights, self.stride, self.padding)
        for co in range(self.c_out):
            for r in range(len(out[co])):
                for c in range(len(out[co][0])):
                    out[co][r][c] += self.bias[co]
        return out

    def backward(self, d_out: List[List[List[float]]], lr: float) -> List[List[List[float]]]:
        # Compute d_weights and d_bias
        self.d_weights = [[[
            [0.0] * self.k_size for _ in range(self.k_size)]
            for _ in range(self.c_in)] for _ in range(self.c_out)]

        self.d_bias = [0.0] * self.c_out

        # Update weights
        padded = self.input
        if self.padding > 0:
            h_in, w_in = len(self.input[0]), len(self.input[0][0])
            padded = [[[0.0] * (w_in + 2 * self.padding) for _ in range(h_in + 2 * self.padding)] for _ in range(self.c_in)]
            for c in range(self.c_in):
                for r in range(h_in):
                    for cc in range(w_in):
                        padded[c][r + self.padding][cc + self.padding] = self.input[c][r][cc]

        h_out, w_out = len(d_out[0]), len(d_out[0][0])

        for co in range(self.c_out):
            for ci in range(self.c_in):
                for r in range(h_out):
                    for c in range(w_out):
                        r_start = r * self.stride
                        c_start = c * self.stride
                        grad = d_out[co][r][c]
                        self.d_bias[co] += grad
                        for kr in range(self.k_size):
                            for kc in range(self.k_size):
                                self.d_weights[co][ci][kr][kc] += grad * padded[ci][r_start + kr][c_start + kc]

        # Compute d_input
        d_input = [[[0.0] * len(self.input[0][0]) for _ in range(len(self.input[0]))] for _ in range(self.c_in)]
        # This is complex for general padding/stride. Simplified version for padding=0, stride=1 is easier.
        # For educational code, we'll focus on the forward path correctness and simple backward.
        # To keep code size reasonable, we implement full backward.
        
        for co in range(self.c_out):
            for r in range(h_out):
                for c in range(w_out):
                    r_start = r * self.stride
                    c_start = c * self.stride
                    grad = d_out[co][r][c]
                    for ci in range(self.c_in):
                        for kr in range(self.k_size):
                            for kc in range(self.k_size):
                                rr = r_start + kr - self.padding
                                cc = c_start + kc - self.padding
                                if 0 <= rr < len(d_input[0]) and 0 <= cc < len(d_input[0][0]):
                                    d_input[ci][rr][cc] += grad * self.weights[co][ci][kr][kc]

        # Update weights
        for co in range(self.c_out):
            self.bias[co] -= lr * self.d_bias[co]
            for ci in range(self.c_in):
                for kr in range(self.k_size):
                    for kc in range(self.k_size):
                        self.weights[co][ci][kr][kc] -= lr * self.d_weights[co][ci][kr][kc]

        return d_input


class LinearLayer:
    def __init__(self, n_in: int, n_out: int):
        limit = math.sqrt(2.0 / n_in)
        self.weights = [[random.uniform(-limit, limit) for _ in range(n_in)] for _ in range(n_out)]
        self.bias = [0.0] * n_out
        self.n_in = n_in
        self.n_out = n_out
        self.input = None
        self.d_weights = None
        self.d_bias = None

    def forward(self, x: List[float]) -> List[float]:
        self.input = x
        out = []
        for i in range(self.n_out):
            val = self.bias[i]
            for j in range(self.n_in):
                val += self.weights[i][j] * x[j]
            out.append(val)
        return out

    def backward(self, d_out: List[float], lr: float) -> List[float]:
        d_input = [0.0] * self.n_in
        self.d_weights = [[0.0] * self.n_in for _ in range(self.n_out)]
        self.d_bias = [0.0] * self.n_out

        for i in range(self.n_out):
            self.d_bias[i] = d_out[i]
            for j in range(self.n_in):
                self.d_weights[i][j] = d_out[i] * self.input[j]
                d_input[j] += d_out[i] * self.weights[i][j]

        for i in range(self.n_out):
            self.bias[i] -= lr * self.d_bias[i]
            for j in range(self.n_in):
                self.weights[i][j] -= lr * self.d_weights[i][j]

        return d_input


class Flatten:
    def __init__(self): self.shape = None
    def forward(self, x): self.shape = self._get_shape(x); return flatten(x)
    def _get_shape(self, x):
        if not isinstance(x, list): return []
        return [len(x)] + self._get_shape(x[0])
    def backward(self, d, lr=None): return self._reshape(d, self.shape)
    def _reshape(self, flat, shape):
        if not shape: return flat[0]
        k = 1
        for s in shape[1:]: k *= s
        return [self._reshape(flat[i*k:(i+1)*k], shape[1:]) for i in range(shape[0])]

class CNN:
    def __init__(self):
        self.layers = []
        self.pool_indices = []

    def add(self, layer):
        self.layers.append(layer)

    def forward(self, x: List[List[List[float]]]) -> List[float]:
        out = x
        for layer in self.layers:
            if isinstance(layer, MaxPoolLayer):
                out, indices = layer.forward(out)
                self.pool_indices.append(indices)
            else:
                out = layer.forward(out)
        return out

    def backward(self, d_out, lr):
        d = d_out
        self.pool_indices.reverse()
        for layer in reversed(self.layers):
            if isinstance(layer, MaxPoolLayer):
                indices = self.pool_indices.pop(0)
                d = layer.backward(d, indices)
            elif isinstance(layer, ReLULayer):
                d = layer.backward(d)
            else:
                d = layer.backward(d, lr)
        self.pool_indices.reverse()


class MaxPoolLayer:
    def __init__(self, k_size=2, stride=2):
        self.k_size = k_size
        self.stride = stride

    def forward(self, x):
        self.input = x
        return max_pool2d_forward(x, self.k_size, self.stride)

    def backward(self, d_out, indices):
        c = len(indices)
        h_in = len(self.input[0])
        w_in = len(self.input[0][0])
        d_in = [[[0.0]*w_in for _ in range(h_in)] for _ in range(c)]

        for ci in range(c):
            h_out = len(d_out[ci])
            w_out = len(d_out[ci][0])
            for r in range(h_out):
                for cc in range(w_out):
                    kr, kc = indices[ci][r][cc]
                    r_start = r * self.stride
                    c_start = cc * self.stride
                    d_in[ci][r_start + kr][c_start + kc] += d_out[ci][r][cc]
        return d_in


class ReLULayer:
    def __init__(self): pass
    def forward(self, x):
        self.mask = relu_forward(x)
        self.input = x # Not needed for mask logic, but good practice
        # Actually mask should be x > 0
        self.mask = [[[1.0 if v > 0 else 0.0 for v in row] for row in plane] for plane in x]
        return relu_forward(x)

    def backward(self, d):
        out = [[[0.0]*len(d[0][0]) for _ in range(len(d[0]))] for _ in range(len(d))]
        for c in range(len(d)):
            for r in range(len(d[c])):
                for cc in range(len(d[c][0])):
                    out[c][r][cc] = d[c][r][cc] * self.mask[c][r][cc]
        return out


class Softmax:
    @staticmethod
    def forward(x: List[float]) -> List[float]:
        max_val = max(x)
        exps = [math.exp(v - max_val) for v in x]
        total = sum(exps)
        return [e / total for e in exps]

    @staticmethod
    def loss(probs: List[float], target: int) -> Tuple[float, List[float]]:
        loss = -math.log(max(probs[target], 1e-7))
        d = probs[:]
        d[target] -= 1.0
        return loss, d


def flatten(x: List) -> List[float]:
    res = []
    if isinstance(x, list):
        for v in x:
            res.extend(flatten(v))
    else:
        res.append(x)
    return res


def demo_simple():
    """演示 CNN 基本操作"""
    print("=== CNN 基本操作 ===\n")

    # 輸入: 1 channel, 4x4
    img = [[[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]]]

    # 濾核: 1 output, 1 input, 3x3 (Sobel-like)
    kernel = [[[[1, 0, -1],
                [2, 0, -2],
                [1, 0, -1]]]]

    out = conv2d_forward(img, kernel, stride=1, padding=0)
    print("卷積輸出 (2x2):")
    for row in out[0]:
        print(f"  {row}")

    pooled, _ = max_pool2d_forward(out, k_size=2, stride=2)
    print("\n池化輸出 (1x1):")
    print(f"  {pooled[0][0]}")


def demo_training():
    """演示 CNN 訓練"""
    print("\n=== CNN 微型訓練 (2x2 圖像分類) ===\n")
    random.seed(42)

    # 數據集: 4 張 2x2 圖像，2 類
    # 類 0: [[0,0],[0,0]] 附近
    # 類 1: [[1,1],[1,1]] 附近
    X = [
        [[[0.1, 0.2], [0.1, 0.2]]],  # 類 0
        [[[0.9, 0.8], [0.9, 0.8]]],  # 類 1
        [[[0.2, 0.1], [0.2, 0.1]]],  # 類 0
        [[[0.8, 0.9], [0.8, 0.9]]],  # 類 1
    ]
    y = [0, 1, 0, 1]

    # 建立網路
    # Conv -> ReLU -> Flatten -> Linear
    net = CNN()
    # Padding=0, stride=1 on 2x2 with 2x2 kernel -> 1x1 output
    net.layers.append(ConvLayer(c_in=1, c_out=2, k_size=2, stride=1, padding=0))
    net.layers.append(ReLULayer())
    net.layers.append(Flatten())
    # Output shape: [2, 1, 1] -> flattened size 2
    net.layers.append(LinearLayer(n_in=2, n_out=2))

    lr = 0.1
    epochs = 200

    for epoch in range(epochs):
        total_loss = 0
        for img, target in zip(X, y):
            # Forward
            out = net.forward(img)
            # Flatten (already flat from Linear)
            probs = Softmax.forward(out)
            loss, d_loss = Softmax.loss(probs, target)
            total_loss += loss

            # Backward
            net.backward(d_loss, lr)

        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")

    print("\n預測結果:")
    for img, target in zip(X, y):
        out = net.forward(img)
        probs = Softmax.forward(out)
        pred = probs.index(max(probs))
        print(f"  輸入 {img[0][0]} -> 預測 {pred} (期望 {target}) {'✓' if pred == target else '✗'}")


if __name__ == "__main__":
    demo_simple()
    demo_training()
