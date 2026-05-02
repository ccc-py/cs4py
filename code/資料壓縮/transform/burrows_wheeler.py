"""
Burrows-Wheeler 轉換 (BWT)

由 Michael Burrows 和 David Wheeler 在 1994 年提出。
BWT 是一種可逆的資料轉換，將輸入字串重新排列，
使得相似的字元聚集在一起，從而提高後續壓縮（如 RLE、MTF）的效果。
BWT 是 bzip2 壓縮工具的核心演算法之一。
"""

from typing import List, Tuple


def bwt_encode(data: str) -> Tuple[str, int]:
    """
    BWT 編碼：對字串進行循環旋轉並排序

    Args:
        data: 要轉換的原始字串（會自動添加終止符）

    Returns:
        (轉換後的字串, 原始字串所在的行索引)
    """
    # 添加終止符（通常是最小的字元）
    data = data + '$'

    # 生成所有循環旋轉
    rotations = []
    for i in range(len(data)):
        rotation = data[i:] + data[:i]
        rotations.append(rotation)

    # 按字典序排序
    rotations.sort()

    # 取出每行的最後一個字元，組成輸出
    encoded = ''.join(row[-1] for row in rotations)

    # 找到原始字串所在的行
    original_index = rotations.index(data)

    return encoded, original_index


def bwt_decode(encoded: str, index: int) -> str:
    """
    BWT 解碼（使用排序恢復法）
    
    Args:
        encoded: BWT 轉換後的字串
        index: 原始字串所在的行索引
        
    Returns:
        解壓後的原始字串（不含終止符）
    """
    n = len(encoded)

    # L 是最後一列，F 是第一列（排序後）
    L = list(encoded)
    F = sorted(L)

    # 建立 next 陣列：next[i] = F[i] 在 L 中對應的位置
    # 由於有重複字元，需要追蹤每個字元已經用了幾次
    next_array = [0] * n
    char_count = {}

    for i, char in enumerate(F):
        if char not in char_count:
            char_count[char] = 0
        # 找到 L 中第 char_count[char] 個 char 的位置
        count = 0
        for j, c in enumerate(L):
            if c == char:
                if count == char_count[char]:
                    next_array[i] = j
                    break
                count += 1
        char_count[char] += 1

    # 重建字串：從 '$' 的位置開始，跟隨 next 陣列
    # 注意：這會從原始字串的結尾開始重建
    result = []
    pos = L.index('$')  # 找到 '$' 在 L 中的位置
    for _ in range(n - 1):  # -1 是因為有終止符
        pos = next_array[pos]
        result.append(L[pos])

    return ''.join(result)


def bwt_with_mtf_rle(data: str) -> Tuple[str, int, List[int]]:
    """
    BWT + MTF + RLE 完整流程（bzip2 的簡化版）

    Args:
        data: 原始字串

    Returns:
        (BWT 結果, BWT 索引, MTF+RLE 編碼結果)
    """
    # 從同一目錄導入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from move_to_front import encode as mtf_encode
    from run_length import encode_binary

    # BWT
    bwt_result, index = bwt_encode(data)

    # MTF（將字元轉為 ASCII 值）
    chars = [ord(c) for c in bwt_result]
    mtf_result = mtf_encode(chars)

    # RLE
    rle_result = encode_binary(mtf_result, threshold=3)

    return bwt_result, index, rle_result


if __name__ == "__main__":
    # 示範 BWT
    sample_text = "banana"
    print(f"原始文字: {sample_text}\n")

    # BWT 編碼
    encoded, index = bwt_encode(sample_text)
    print(f"BWT 編碼結果: {encoded}")
    print(f"原始字串索引: {index}\n")

    # BWT 解碼
    decoded = bwt_decode(encoded, index)
    print(f"BWT 解碼結果: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}\n")

    # 展示 BWT 如何讓相同字元聚集
    print("="*50)
    text2 = "mississippi"
    print(f"\n原始文字: {text2}")
    encoded2, index2 = bwt_encode(text2)
    print(f"BWT 結果: {encoded2}")
    print(f"注意 'i' 和 's' 的聚集效果")

    # 完整流程：BWT + MTF + RLE
    print("\n" + "="*50)
    print("\nBWT + MTF + RLE 完整流程示範:")
    text3 = "abracadabra"
    print(f"原始文字: {text3}")

    bwt_result, bwt_idx, compressed = bwt_with_mtf_rle(text3)
    print(f"BWT 結果: {bwt_result}")
    print(f"MTF+RLE 壓縮結果: {compressed}")

    # 計算壓縮效果
    original_size = len(text3) * 8  # 位元
    compressed_bits = sum(
        c if isinstance(c, int) and not isinstance(c, tuple) else 8 + c[1] * 4
        for c in compressed
    )
    print(f"\n原始大小: {original_size} 位元")
    print(f"壓縮後約: {compressed_bits} 位元")
    print(f"壓縮率: {compressed_bits/original_size*100:.1f}%")
