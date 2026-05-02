from typing import List, Dict, Tuple
import math


def count_ngrams(tokens: List[str], n: int) -> Dict[Tuple[str, ...], int]:
    """計算 n-gram 出現次數。

    Args:
        tokens: 分詞後的 token 列表
        n: n-gram 的階數

    Returns:
        n-gram 計數字典
    """
    ngrams = {}
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])
        ngrams[ngram] = ngrams.get(ngram, 0) + 1
    return ngrams


def modified_precision(candidate: List[str], references: List[List[str]], n: int) -> float:
    """計算修正後的 n-gram 精確率。

    使用多個參考譯文中的最大匹配次數作為分母的修正。

    Args:
        candidate: 候選翻譯（分詞後）
        references: 參考翻譯列表（每個已分詞）
        n: n-gram 的階數

    Returns:
        修正後的 n-gram 精確率
    """
    candidate_ngrams = count_ngrams(candidate, n)
    if not candidate_ngrams:
        return 0.0

    # 對每個 n-gram，取所有參考譯文中的最大出現次數
    max_ref_counts = {}
    for ref in references:
        ref_ngrams = count_ngrams(ref, n)
        for ngram, count in ref_ngrams.items():
            max_ref_counts[ngram] = max(max_ref_counts.get(ngram, 0), count)

    # 計算修正後的匹配數
    clipped_count = 0
    for ngram, count in candidate_ngrams.items():
        clipped_count += min(count, max_ref_counts.get(ngram, 0))

    total_count = sum(candidate_ngrams.values())
    return clipped_count / total_count if total_count > 0 else 0.0


def brevity_penalty(candidate_len: int, reference_lens: List[int]) -> float:
    """計算簡潔度懲罰（Brevity Penalty）。

    Args:
        candidate_len: 候選翻譯長度
        reference_lens: 各參考翻譯的長度列表

    Returns:
        簡潔度懲罰值
    """
    # 選擇與候選長度最接近的參考長度
    closest_ref_len = min(reference_lens, key=lambda ref_len: abs(ref_len - candidate_len))

    if candidate_len > closest_ref_len:
        return 1.0
    else:
        return math.exp(1 - closest_ref_len / candidate_len)


def bleu_score(candidate: str, references: List[str],
               max_n: int = 4, weights: List[float] = None) -> float:
    """計算 BLEU 分數。

    BLEU = BP × exp(Σ w_n × log p_n)

    Args:
        candidate: 候選翻譯（字串）
        references: 參考翻譯列表（字串列表）
        max_n: 最大的 n-gram 階數（通常為 4）
        weights: 各 n-gram 的權重（預設為均權）

    Returns:
        BLEU 分數（0 到 100）
    """
    # 簡單分詞（按空格分割）
    candidate_tokens = candidate.lower().split()
    references_tokens = [ref.lower().split() for ref in references]

    if weights is None:
        weights = [1.0 / max_n] * max_n

    # 計算各階 n-gram 的精確率
    precisions = []
    for n in range(1, max_n + 1):
        p = modified_precision(candidate_tokens, references_tokens, n)
        precisions.append(p)

    # 如果有任何精確率為 0，需要特殊處理（避免 log(0)）
    log_precisions = []
    for p in precisions:
        if p == 0:
            log_precisions.append(float('-inf'))
        else:
            log_precisions.append(math.log(p))

    # 幾何平均
    if float('-inf') in log_precisions:
        geo_mean = 0.0
    else:
        weighted_log_sum = sum(w * lp for w, lp in zip(weights, log_precisions))
        geo_mean = math.exp(weighted_log_sum)

    # 簡潔度懲罰
    bp = brevity_penalty(len(candidate_tokens),
                         [len(ref) for ref in references_tokens])

    bleu = bp * geo_mean
    return bleu * 100  # 轉為 0-100 分數


def bleu_detail(candidate: str, references: List[str], max_n: int = 4) -> Dict:
    """回傳 BLEU 計算的詳細資訊。

    Returns:
        包含各項指標的字典
    """
    candidate_tokens = candidate.lower().split()
    references_tokens = [ref.lower().split() for ref in references]

    result = {
        "candidate_length": len(candidate_tokens),
        "reference_lengths": [len(ref) for ref in references_tokens],
        "ngram_precisions": {},
        "brevity_penalty": 0.0,
        "bleu_score": 0.0,
    }

    precisions = []
    for n in range(1, max_n + 1):
        p = modified_precision(candidate_tokens, references_tokens, n)
        result["ngram_precisions"][f"{n}-gram"] = p
        precisions.append(p)

    # 計算 BLEU
    log_sum = 0.0
    for p in precisions:
        if p > 0:
            log_sum += math.log(p) / max_n
        else:
            log_sum = float('-inf')
            break

    if log_sum != float('-inf'):
        bp = brevity_penalty(len(candidate_tokens),
                             [len(ref) for ref in references_tokens])
        result["brevity_penalty"] = bp
        result["bleu_score"] = bp * math.exp(log_sum) * 100

    return result


if __name__ == "__main__":
    # 機器翻譯評估示例
    candidate = "the cat is on the mat"
    references = [
        "the cat is on the mat",
        "there is a cat on the mat",
    ]

    print("候選翻譯:", candidate)
    print("參考翻譯:", references)

    bleu = bleu_score(candidate, references)
    print(f"\nBLEU-4 分數: {bleu:.2f}")

    # 詳細資訊
    detail = bleu_detail(candidate, references)
    print("\n詳細資訊:")
    print(f"  候選長度: {detail['candidate_length']}")
    print(f"  參考長度: {detail['reference_lengths']}")
    print(f"  簡潔度懲罰: {detail['brevity_penalty']:.4f}")
    for ngram, prec in detail['ngram_precisions'].items():
        print(f"  {ngram} 精確率: {prec:.4f}")

    # 比較不同翻譯品質
    print("\n比較不同翻譯:")
    candidates = [
        "the cat on mat",
        "the cat is on the mat",
        "cat mat on the",
    ]
    for cand in candidates:
        score = bleu_score(cand, references)
        print(f"  '{cand}' -> BLEU: {score:.2f}")
