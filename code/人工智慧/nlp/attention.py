from typing import List, Dict, Optional, Tuple
import math


def scaled_dot_product_attention(
    query: List[List[float]],
    key: List[List[float]],
    value: List[List[float]],
    mask: Optional[List[List[float]]] = None
) -> Tuple[List[List[float]], List[List[float]]]:
    """計算縮放點積注意力（Scaled Dot-Product Attention）。

    Attention(Q, K, V) = softmax(QK^T / √d_k) V

    Args:
        query: 查詢矩陣，形狀 [seq_len, d_k]
        key: 鍵矩陣，形狀 [seq_len, d_k]
        value: 值矩陣，形狀 [seq_len, d_v]（此處簡化為 d_v = d_k）
        mask: 可選的遮罩矩陣，形狀 [seq_len, seq_len]，1 表示保留，0 表示遮蔽

    Returns:
        (輸出矩陣, 注意力權重矩陣)
    """
    seq_len = len(query)
    d_k = len(query[0])

    # 計算 QK^T
    scores = [[0.0] * seq_len for _ in range(seq_len)]
    for i in range(seq_len):
        for j in range(seq_len):
            dot = sum(query[i][k] * key[j][k] for k in range(d_k))
            scores[i][j] = dot / math.sqrt(d_k)

    # 應用遮罩（如果有）
    if mask:
        for i in range(seq_len):
            for j in range(seq_len):
                if mask[i][j] == 0:
                    scores[i][j] = float('-inf')

    # Softmax
    attn_weights = [[0.0] * seq_len for _ in range(seq_len)]
    for i in range(seq_len):
        # 數值穩定性：減去最大值
        max_score = max(scores[i])
        exp_scores = [math.exp(s - max_score) for s in scores[i]]
        sum_exp = sum(exp_scores)
        for j in range(seq_len):
            attn_weights[i][j] = exp_scores[j] / sum_exp

    # 加權求和 V
    output = [[0.0] * d_k for _ in range(seq_len)]
    for i in range(seq_len):
        for j in range(seq_len):
            weight = attn_weights[i][j]
            for k in range(d_k):
                output[i][k] += weight * value[j][k]

    return output, attn_weights


class MultiHeadAttention:
    """多頭注意力機制的簡化實作。"""

    def __init__(self, d_model: int, num_heads: int):
        """初始化多頭注意力。

        Args:
            d_model: 模型維度
            num_heads: 注意力頭數量
        """
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        if self.d_k * num_heads != d_model:
            raise ValueError("d_model 必須能被 num_heads 整除")

        # 簡化：不實作實際的權重矩陣，僅展示概念
        self.W_q = [[1.0] * d_model for _ in range(d_model)]  # 簡化為單位矩陣
        self.W_k = [[1.0] * d_model for _ in range(d_model)]
        self.W_v = [[1.0] * d_model for _ in range(d_model)]
        self.W_o = [[1.0] * d_model for _ in range(d_model)]

    def forward(self, x: List[List[float]]) -> List[List[float]]:
        """前向傳播（簡化版，僅展示概念）。"""
        seq_len = len(x)
        d_model = self.d_model

        # 概念上：將輸入投影到 Q, K, V，分割為多頭，分別計算注意力，最後拼接
        # 這裡簡化為直接返回輸入
        output = [[0.0] * d_model for _ in range(seq_len)]
        for i in range(seq_len):
            for j in range(d_model):
                output[i][j] = x[i][j]

        return output


if __name__ == "__main__":
    # 玩具序列示例
    # 假設有 3 個 token，每個 token 用 4 維向量表示
    seq = [
        [1.0, 0.0, 0.0, 0.0],  # token 1
        [0.0, 1.0, 0.0, 0.0],  # token 2
        [0.0, 0.0, 1.0, 0.0],  # token 3
    ]

    print("輸入序列（3 個 token，4 維）:")
    for i, token in enumerate(seq):
        print(f"  token {i+1}: {token}")

    # 計算自注意力（Q=K=V=seq）
    output, attn_weights = scaled_dot_product_attention(seq, seq, seq)

    print("\n注意力權重矩陣:")
    for row in attn_weights:
        print(f"  {[f'{w:.3f}' for w in row]}")

    print("\n注意力輸出:")
    for i, token in enumerate(output):
        print(f"  token {i+1}: {[f'{v:.3f}' for v in token]}")
