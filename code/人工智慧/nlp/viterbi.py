from typing import List, Dict, Tuple


def viterbi(
    observations: List[str],
    states: List[str],
    start_prob: Dict[str, float],
    trans_prob: Dict[Tuple[str, str], float],
    emit_prob: Dict[Tuple[str, str], float]
) -> List[str]:
    """執行 Viterbi 演算法，尋找 HMM 中最可能的狀態序列。

    Args:
        observations: 觀測序列
        states: 所有可能的狀態列表
        start_prob: 初始狀態機率，鍵為狀態，值為機率
        trans_prob: 狀態轉移機率，鍵為 (前一狀態, 當前狀態)
        emit_prob: 發射機率，鍵為 (狀態, 觀測值)

    Returns:
        最可能的狀態序列
    """
    T = len(observations)
    viterbi_table = [{} for _ in range(T)]
    backpointer = [{} for _ in range(T)]

    # 初始化第一步
    for state in states:
        viterbi_table[0][state] = start_prob.get(state, 0) * emit_prob.get((state, observations[0]), 0)
        backpointer[0][state] = None

    # 遞推計算後續步驟
    for t in range(1, T):
        for curr_state in states:
            max_prob = -1
            prev_state_best = None
            for prev_state in states:
                prob = (viterbi_table[t-1][prev_state] *
                        trans_prob.get((prev_state, curr_state), 0) *
                        emit_prob.get((curr_state, observations[t]), 0))
                if prob > max_prob:
                    max_prob = prob
                    prev_state_best = prev_state
            viterbi_table[t][curr_state] = max_prob
            backpointer[t][curr_state] = prev_state_best

    # 回溯找到最佳路徑
    last_state = max(viterbi_table[T-1], key=lambda k: viterbi_table[T-1][k])
    best_path = [last_state]
    for t in range(T-1, 0, -1):
        best_path.insert(0, backpointer[t][best_path[0]])

    return best_path


if __name__ == "__main__":
    # 簡單 HMM 示例：詞性標註
    states = ["NOUN", "VERB", "ADJ"]
    observations = ["I", "love", "Python", "programming"]

    # 初始機率
    start_prob = {"NOUN": 0.3, "VERB": 0.5, "ADJ": 0.2}

    # 狀態轉移機率
    trans_prob = {
        ("NOUN", "VERB"): 0.4, ("NOUN", "NOUN"): 0.3, ("NOUN", "ADJ"): 0.3,
        ("VERB", "NOUN"): 0.6, ("VERB", "VERB"): 0.2, ("VERB", "ADJ"): 0.2,
        ("ADJ", "NOUN"): 0.7, ("ADJ", "VERB"): 0.2, ("ADJ", "ADJ"): 0.1,
    }

    # 發射機率
    emit_prob = {
        ("NOUN", "I"): 0.1, ("NOUN", "love"): 0.1, ("NOUN", "Python"): 0.6, ("NOUN", "programming"): 0.2,
        ("VERB", "I"): 0.1, ("VERB", "love"): 0.7, ("VERB", "Python"): 0.1, ("VERB", "programming"): 0.1,
        ("ADJ", "I"): 0.1, ("ADJ", "love"): 0.2, ("ADJ", "Python"): 0.3, ("ADJ", "programming"): 0.4,
    }

    best_path = viterbi(observations, states, start_prob, trans_prob, emit_prob)
    print("觀測序列:", observations)
    print("最可能的狀態序列（詞性）:", best_path)
