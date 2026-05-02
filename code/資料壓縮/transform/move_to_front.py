"""
Move-to-Front (MTF) 編碼

一種簡單的資料轉換演算法，將輸入資料流轉換為較小的整數值。
MTF 通常與 BWT 配合使用：BWT 使相同字元聚集，MTF 將這些聚集的字元轉為 0 或小的正整數，
然後再用 RLE 或霍夫曼編碼進一步壓縮。
"""

from typing import List, Dict


def encode(data: List[int]) -> List[int]:
    """
    MTF 編碼
    
    Args:
        data: 輸入的整數列表（如字元的 ASCII 值）
        
    Returns:
        MTF 編碼後的整數列表
    """
    # 初始化列表：通常包含所有可能的符號（0-255）
    mtf_list = list(range(256))

    result = []

    for value in data:
        # 找到值在列表中的位置
        index = mtf_list.index(value)

        # 輸出索引
        result.append(index)

        # 將該值移到列表最前面
        del mtf_list[index]
        mtf_list.insert(0, value)

    return result


def decode(encoded: List[int]) -> List[int]:
    """
    MTF 解碼
    
    Args:
        encoded: MTF 編碼後的整數列表
        
    Returns:
        解壓後的原始整數列表
    """
    # 初始化相同的列表
    mtf_list = list(range(256))

    result = []

    for index in encoded:
        # 根據索引取值
        value = mtf_list[index]
        result.append(value)

        # 將該值移到列表最前面
        del mtf_list[index]
        mtf_list.insert(0, value)

    return result


def encode_string(text: str) -> List[int]:
    """
    MTF 編碼字串（便捷函數）
    
    Args:
        text: 輸入字串
        
    Returns:
        MTF 編碼後的整數列表
    """
    return encode([ord(c) for c in text])


def decode_string(encoded: List[int]) -> str:
    """
    MTF 解碼為字串（便捷函數）
    
    Args:
        encoded: MTF 編碼後的整數列表
        
    Returns:
        解壓後的原始字串
    """
    return ''.join(chr(c) for c in decode(encoded))


def count_small_values(encoded: List[int], threshold: int = 10) -> float:
    """
    計算小值（0-9）的比例，這顯示了 MTF 的效果
    
    Args:
        encoded: MTF 編碼後的列表
        threshold: 小值的閾值
        
    Returns:
        小值的比例
    """
    if not encoded:
        return 0.0
    small_count = sum(1 for v in encoded if v < threshold)
    return small_count / len(encoded)


if __name__ == "__main__":
    # 示範 MTF 編碼
    sample_text = "banana"
    print(f"原始文字: {sample_text}")
    print(f"原始 ASCII: {[ord(c) for c in sample_text]}\n")

    # MTF 編碼
    encoded = encode_string(sample_text)
    print(f"MTF 編碼結果: {encoded}")
    print(f"小值比例: {count_small_values(encoded)*100:.1f}%\n")

    # MTF 解碼
    decoded = decode_string(encoded)
    print(f"MTF 解碼結果: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}\n")

    # 展示 MTF 如何處理 BWT 的輸出
    print("="*50)
    print("\nBWT + MTF 效果示範:")

    # 來自 BWT 的輸出（重複字元聚集）
    bwt_output = "ard$rcaaabb"
    print(f"BWT 輸出: {bwt_output}")

    # MTF 編碼
    mtf_result = encode_string(bwt_output)
    print(f"MTF 編碼: {mtf_result}")
    print(f"小值比例: {count_small_values(mtf_result)*100:.1f}%")

    # 解碼驗證
    mtf_decoded = decode_string(mtf_result)
    print(f"MTF 解碼: {mtf_decoded}")
    print(f"驗證正確: {mtf_decoded == bwt_output}")

    # 完整的壓縮流程示範
    print("\n" + "="*50)
    print("\n完整壓縮流程: BWT -> MTF -> RLE")
    from code.資料壓縮.transform.burrows_wheeler import bwt_encode
    from code.資料壓縮.transform.run_length import encode_binary

    text = "abracadabra"
    print(f"原始文字: {text}")

    # BWT
    bwt_result, bwt_index = bwt_encode(text)
    print(f"\n1. BWT 結果: {bwt_result}")

    # MTF
    mtf_result = encode_string(bwt_result)
    print(f"2. MTF 結果: {mtf_result}")

    # RLE（只壓縮連續的 0）
    rle_result = encode_binary(mtf_result, threshold=3)
    print(f"3. RLE 結果: {rle_result}")

    # 計算壓縮效果
    original_bits = len(text) * 8
    # 簡單估算 MTF+RLE 後的位元數
    rle_bits = sum(
        v.bit_length() if isinstance(v, int) else 8 + v[1] * 4
        for v in rle_result
    )
    print(f"\n原始: {original_bits} 位元")
    print(f"壓縮後約: {rle_bits} 位元")
    print(f"壓縮率: {rle_bits/original_bits*100:.1f}%")
