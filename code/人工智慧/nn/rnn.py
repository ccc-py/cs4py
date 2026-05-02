"""
遞迴神經網路 (Recurrent Neural Network, RNN & LSTM)

歷史背景：
- 1986 年：Elman 提出 Simple RNN，引入隱藏狀態傳遞時間信息
- 1997 年：Hochreiter & Schmidhuber 提出 LSTM，解決 RNN 梯度消失/爆炸問題
- 2014 年：Cho 等人提出 GRU，簡化 LSTM 結構
- 應用：語言模型、機器翻譯、語音識別、時間序列預測
- 2017 年後：Transformer 架構逐漸取代 RNN 在 NLP 的主導地位，但 RNN 仍是理解序列模型的基礎

核心概念：
- 隱藏狀態 (Hidden State)：攜帶過去時間步的信息
- 參數共享：同一組權重用於所有時間步
- BPTT (Backpropagation Through Time)：將 RNN 展開為前饋網路進行訓練
- LSTM 門控機制：遺忘門、輸入門、輸出門控制信息流
"""

from typing import List, Tuple, Optional
import math
import random


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))


def tanh(x: float) -> float:
    return math.tanh(x)


class RNNCell:
    """基本 RNN 單元"""

    def __init__(self, n_in: int, n_hidden: int):
        self.n_in = n_in
        self.n_hidden = n_hidden
        limit = math.sqrt(1.0 / n_hidden)
        self.Wx = [[random.uniform(-limit, limit) for _ in range(n_in)] for _ in range(n_hidden)]
        self.Wh = [[random.uniform(-limit, limit) for _ in range(n_hidden)] for _ in range(n_hidden)]
        self.bias = [0.0] * n_hidden

        self.h_prev = [0.0] * n_hidden
        self.x = None

    def forward(self, x: List[float], h_prev: Optional[List[float]] = None) -> Tuple[List[float], List[float]]:
        if h_prev:
            self.h_prev = h_prev
        else:
            self.h_prev = [0.0] * self.n_hidden

        self.x = x
        h_new = []
        for i in range(self.n_hidden):
            val = self.bias[i]
            for j in range(self.n_in):
                val += self.Wx[i][j] * x[j]
            for j in range(self.n_hidden):
                val += self.Wh[i][j] * self.h_prev[j]
            h_new.append(tanh(val))
        return h_new, self.h_prev

    def step_backward(self, d_h: List[float], x: List[float], h_prev: List[float]) -> Tuple[List[float], List[float], List[float]]:
        # d_tanh = d_h * (1 - h^2)
        d_tanh = [d_h[i] * (1.0 - h_new**2) for i, h_new in enumerate(self.h_new_cache)]
        # d_bias = d_tanh
        # d_Wx = d_tanh * x.T
        # d_Wh = d_tanh * h_prev.T
        # d_x = Wx.T * d_tanh
        # d_h_prev = Wh.T * d_tanh
        # ... (Simplified for brevity, full implementation needed for training)
        pass


class LSTMCell:
    """LSTM 單元"""

    def __init__(self, n_in: int, n_hidden: int):
        self.n_in = n_in
        self.n_hidden = n_hidden
        limit = math.sqrt(1.0 / n_hidden)

        # Input, Forget, Output, Candidate gates
        self.Wx = [[random.uniform(-limit, limit) for _ in range(n_in)] for _ in range(4 * n_hidden)]
        self.Wh = [[random.uniform(-limit, limit) for _ in range(n_hidden)] for _ in range(4 * n_hidden)]
        self.bias = [0.0] * (4 * n_hidden)

        self.cache = {}

    def forward(self, x: List[float], h_prev: List[float], c_prev: List[float]) -> Tuple[List[float], List[float], List[float]]:
        n = self.n_hidden
        # Compute gates
        gates = [0.0] * (4 * n)
        for i in range(4 * n):
            val = self.bias[i]
            for j in range(self.n_in):
                val += self.Wx[i][j] * x[j]
            for j in range(n):
                val += self.Wh[i][j] * h_prev[j]
            gates[i] = val

        # Split gates
        f = [sigmoid(gates[i]) for i in range(n)]
        i_gate = [sigmoid(gates[i + n]) for i in range(n)]
        c_tilde = [tanh(gates[i + 2 * n]) for i in range(n)]
        o = [sigmoid(gates[i + 3 * n]) for i in range(n)]

        c_new = [f[k] * c_prev[k] + i_gate[k] * c_tilde[k] for k in range(n)]
        h_new = [o[k] * tanh(c_new[k]) for k in range(n)]

        self.cache = {'x': x, 'h_prev': h_prev, 'c_prev': c_prev,
                      'f': f, 'i_gate': i_gate, 'c_tilde': c_tilde, 'o': o,
                      'c_new': c_new, 'h_new': h_new}
        return h_new, c_new, h_prev

    def backward(self, d_h: List[float], d_c: Optional[List[float]] = None, lr: float = 0.01) -> Tuple[List[float], List[float]]:
        # Full LSTM backward is complex; this is a placeholder structure.
        # For educational code, we focus on forward and simple tasks.
        return [0.0] * self.n_in, [0.0] * self.n_hidden


class RNN:
    """多層 RNN/LSTM"""

    def __init__(self, n_in: int, n_hidden: int, n_layers: int = 1, cell_type: str = 'lstm'):
        self.n_in = n_in
        self.n_hidden = n_hidden
        self.layers = []
        if cell_type == 'lstm':
            self.layers.append(LSTMCell(n_in, n_hidden))
            for _ in range(n_layers - 1):
                self.layers.append(LSTMCell(n_hidden, n_hidden))
        else:
            self.layers.append(RNNCell(n_in, n_hidden))
            for _ in range(n_layers - 1):
                self.layers.append(RNNCell(n_hidden, n_hidden))

    def forward(self, sequence: List[List[float]], h0: Optional[List[float]] = None) -> List[List[float]]:
        h = [h0] if h0 else [[0.0]*self.n_hidden] * len(self.layers)
        c = [[0.0]*self.n_hidden] * len(self.layers)
        outputs = []

        for x in sequence:
            h_next = []
            c_next = []
            for i, layer in enumerate(self.layers):
                inp = x if i == 0 else h[i-1]
                if isinstance(layer, LSTMCell):
                    h_out, c_out, _ = layer.forward(inp, h[i], c[i])
                    h_next.append(h_out)
                    c_next.append(c_out)
                else:
                    h_out, _ = layer.forward(inp, h[i])
                    h_next.append(h_out)
                    c_next.append([0.0]*self.n_hidden)
            h = h_next
            c = c_next
            outputs.append(h[-1])
        return outputs


def demo_sequence():
    """序列預測演示"""
    print("=== 序列預測 (學習正弦波) ===\n")

    # 生成正弦波序列
    seq = []
    for i in range(20):
        seq.append([math.sin(i * 0.5)])

    # 訓練目標：預測下一個點
    rnn = RNN(n_in=1, n_hidden=4, cell_type='lstm')
    lr = 0.01

    print("初始預測 (前 5 個):")
    preds = rnn.forward(seq)
    for i in range(min(5, len(seq))):
        print(f"  真實: {seq[i][0]:.3f}, 預測: {preds[i][0]:.3f}")


def demo_parity():
    """奇偶校驗序列分類"""
    print("\n=== 奇偶校驗分類 ===\n")
    print("任務：判斷二進制序列中 1 的數量是奇數還是偶數")

    # 序列: [0, 1, 1, 0, 1] -> 3 個 1 -> 奇數
    seq = [[0], [1], [1], [0], [1]]
    print(f"序列: {[x[0] for x in seq]}")

    rnn = RNN(n_in=1, n_hidden=4, cell_type='lstm')
    outputs = rnn.forward(seq)
    print(f"最終隱藏狀態: {[round(x, 3) for x in outputs[-1]]}")


if __name__ == "__main__":
    demo_sequence()
    demo_parity()
