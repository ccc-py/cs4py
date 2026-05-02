from typing import List, Dict, Tuple
import random
import math


class CharRNN:
    """字元級 RNN，用於文本生成。

    包含輸入層、隱藏層和輸出層，使用簡化的 BPTT（隨時間反向傳播）。
    """

    def __init__(self, vocab_size: int, hidden_size: int, learning_rate: float = 0.1):
        """初始化 RNN。

        Args:
            vocab_size: 字元詞彙表大小
            hidden_size: 隱藏層維度
            learning_rate: 學習率
        """
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.lr = learning_rate

        # 權重矩陣
        scale = 0.01
        self.W_xh = [[random.uniform(-scale, scale) for _ in range(hidden_size)]
                     for _ in range(vocab_size)]  # 輸入到隱藏層
        self.W_hh = [[random.uniform(-scale, scale) for _ in range(hidden_size)]
                     for _ in range(hidden_size)]  # 隱藏層到隱藏層
        self.W_hy = [[random.uniform(-scale, scale) for _ in range(vocab_size)]
                     for _ in range(hidden_size)]  # 隱藏層到輸出層

        self.b_h = [0.0] * hidden_size  # 隱藏層偏置
        self.b_y = [0.0] * vocab_size   # 輸出層偏置

    def _tanh(self, x: float) -> float:
        """Tanh 激活函數。"""
        if x < -100:
            return -1.0
        if x > 100:
            return 1.0
        e_pos = math.exp(x)
        e_neg = math.exp(-x)
        return (e_pos - e_neg) / (e_pos + e_neg)

    def _tanh_derivative(self, x: float) -> float:
        """Tanh 的導數。"""
        return 1 - x * x

    def _softmax(self, x: List[float]) -> List[float]:
        """Softmax 函數。"""
        max_x = max(x)
        exp_x = [math.exp(v - max_x) for v in x]
        sum_exp = sum(exp_x)
        return [v / sum_exp for v in exp_x]

    def forward(self, inputs: List[int]) -> Tuple[List[List[float]], List[List[float]]]:
        """前向傳播。

        Args:
            inputs: 輸入字元索引序列

        Returns:
            (隱藏狀態序列, 輸出機率序列)
        """
        seq_len = len(inputs)
        hidden_states = [[0.0] * self.hidden_size for _ in range(seq_len + 1)]
        outputs = [[0.0] * self.vocab_size for _ in range(seq_len)]

        for t in range(seq_len):
            x = inputs[t]
            h_prev = hidden_states[t]

            # 隱藏狀態：h_t = tanh(W_xh[x] + W_hh * h_{t-1} + b_h)
            h_new = [0.0] * self.hidden_size
            for i in range(self.hidden_size):
                val = 0.0
                # W_xh[x][i]
                val += self.W_xh[x][i]
                # W_hh * h_prev
                for j in range(self.hidden_size):
                    val += self.W_hh[j][i] * h_prev[j]
                val += self.b_h[i]
                h_new[i] = self._tanh(val)
            hidden_states[t + 1] = h_new

            # 輸出：y_t = softmax(W_hy * h_t + b_y)
            y = [0.0] * self.vocab_size
            for i in range(self.vocab_size):
                for j in range(self.hidden_size):
                    y[i] += self.W_hy[j][i] * h_new[j]
                y[i] += self.b_y[i]
            outputs[t] = self._softmax(y)

        return hidden_states, outputs

    def train_step(self, inputs: List[int], targets: List[int]) -> float:
        """執行一個訓練步驟（簡化版 BPTT）。

        Args:
            inputs: 輸入序列
            targets: 目標序列（通常是 inputs 向右偏移一位）

        Returns:
            損失值
        """
        seq_len = len(inputs)
        hidden_states, outputs = self.forward(inputs)

        # 計算交叉熵損失
        loss = 0.0
        for t in range(seq_len):
            target = targets[t]
            pred = outputs[t][target]
            loss -= math.log(pred + 1e-10)

        # 簡化版梯度更新（實際上應實作完整的 BPTT）
        # 這裡使用隨機梯度更新的簡化版本
        for t in range(seq_len):
            target = targets[t]
            for i in range(self.hidden_size):
                for j in range(self.vocab_size):
                    if j == target:
                        error = 1 - outputs[t][j]
                    else:
                        error = -outputs[t][j]
                    self.W_hy[i][j] += self.lr * error * hidden_states[t + 1][i]

        return loss / seq_len

    def train(self, data: List[int], epochs: int = 100, seq_len: int = 10) -> None:
        """訓練 RNN。

        Args:
            data: 訓練數據（字元索引序列）
            epochs: 訓練輪數
            seq_len: 每個訓練序列的長度
        """
        n = len(data)
        for epoch in range(epochs):
            total_loss = 0.0
            for i in range(0, n - seq_len, seq_len):
                inputs = data[i:i + seq_len]
                targets = data[i + 1:i + seq_len + 1]
                loss = self.train_step(inputs, targets)
                total_loss += loss
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")

    def generate(self, start_idx: int, length: int, temperature: float = 1.0) -> List[int]:
        """生成文本。

        Args:
            start_idx: 起始字元索引
            length: 生成長度
            temperature: 溫度參數（越高越隨機）

        Returns:
            生成的字元索引序列
        """
        result = [start_idx]
        hidden = [0.0] * self.hidden_size

        for _ in range(length - 1):
            x = result[-1]

            # 更新隱藏狀態
            h_new = [0.0] * self.hidden_size
            for i in range(self.hidden_size):
                val = self.W_xh[x][i]
                for j in range(self.hidden_size):
                    val += self.W_hh[j][i] * hidden[j]
                val += self.b_h[i]
                h_new[i] = self._tanh(val)

            # 計算輸出機率
            y = [0.0] * self.vocab_size
            for i in range(self.vocab_size):
                for j in range(self.hidden_size):
                    y[i] += self.W_hy[j][i] * h_new[j]
                y[i] += self.b_y[i]

            # 溫度調整
            if temperature != 1.0:
                y = [v / temperature for v in y]
            probs = self._softmax(y)

            # 採樣下一個字元
            next_idx = random.choices(range(self.vocab_size), weights=probs)[0]
            result.append(next_idx)
            hidden = h_new

        return result


if __name__ == "__main__":
    # 簡單訓練語料
    text = "hello world hello python hello code"
    chars = sorted(set(text))
    char2idx = {c: i for i, c in enumerate(chars)}
    idx2char = {i: c for c, i in char2idx.items()}
    data = [char2idx[c] for c in text]

    print("訓練文本:", text)
    print("詞彙表:", chars)

    # 訓練 RNN
    rnn = CharRNN(vocab_size=len(chars), hidden_size=20, learning_rate=0.1)
    rnn.train(data, epochs=50, seq_len=8)

    # 生成文本
    start = char2idx["h"]
    generated = rnn.generate(start, length=30)
    generated_text = "".join(idx2char[i] for i in generated)
    print(f"\n生成文本（起始 'h'）: {generated_text}")
