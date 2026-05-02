"""
LZW 壓縮演算法

由 Abraham Lempel、Jacob Ziv 和 Terry Welch 在 1984 年提出。
LZW 是 LZ78 的改進版本，最大的特點是**不需要傳送字典**，
因為壓縮端和解壓縮端可以同步地建立相同的字典。
LZW 曾被廣泛用於 GIF 圖片和 Unix compress 指令。
"""

from typing import List, Dict, Tuple


def encode(data: str) -> List[int]:
    """
    LZW 編碼
    
    Args:
        data: 要壓縮的字串
        
    Returns:
        壓縮後的碼字列表（整數列表）
    """
    # 初始化字典：每個單一字元對應一個碼字
    dictionary: Dict[str, int] = {}
    for i in range(256):
        dictionary[chr(i)] = i

    result = []
    current = ""

    for char in data:
        combined = current + char
        if combined in dictionary:
            current = combined
        else:
            # 輸出當前字串的碼字
            result.append(dictionary[current])
            # 將新字串加入字典
            dictionary[combined] = len(dictionary)
            current = char

    # 輸出最後一個
    if current:
        result.append(dictionary[current])

    return result


def decode(codes: List[int]) -> str:
    """
    LZW 解壓縮
    
    Args:
        codes: 壓縮後的碼字列表
        
    Returns:
        解壓後的原始字串
    """
    # 初始化字典（與壓縮端相同）
    dictionary: Dict[int, str] = {}
    for i in range(256):
        dictionary[i] = chr(i)

    result = []
    previous_code = codes[0]
    result.append(dictionary[previous_code])

    for code in codes[1:]:
        if code in dictionary:
            # 碼字在字典中
            entry = dictionary[code]
        elif code == len(dictionary):
            # 特殊情況：碼字正好是下一個字典索引
            entry = dictionary[previous_code] + dictionary[previous_code][0]
        else:
            raise ValueError(f"錯誤的碼字: {code}")

        result.append(entry)

        # 將新字串加入字典
        dictionary[len(dictionary)] = dictionary[previous_code] + entry[0]
        previous_code = code

    return ''.join(result)


def codes_to_hex(codes: List[int]) -> str:
    """
    將碼字轉換為十六進制字串（用於顯示）
    
    Args:
        codes: 碼字列表
        
    Returns:
        十六進制字串
    """
    return ' '.join(f'{c:04x}' for c in codes)


def calculate_compression_ratio(original: str, codes: List[int]) -> float:
    """
    計算壓縮率
    
    Args:
        original: 原始字串
        codes: 碼字列表
        
    Returns:
        壓縮率（百分比）
    """
    # 假設每個碼字用 16 位元（2 位元組）表示
    compressed_bits = len(codes) * 16
    original_bits = len(original) * 8
    return compressed_bits / original_bits * 100


if __name__ == "__main__":
    # 示範 LZW 壓縮
    sample_text = "TOBEORNOTTOBEORTOBEORNOT"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    # 壓縮
    codes = encode(sample_text)
    print(f"壓縮後碼字: {codes}")
    print(f"碼字數量: {len(codes)}")
    print(f"碼字 (hex): {codes_to_hex(codes)}\n")

    # 計算壓縮率
    ratio = calculate_compression_ratio(sample_text, codes)
    print(f"原始位元數: {len(sample_text) * 8}")
    print(f"壓縮後位元數: {len(codes) * 16}")
    print(f"壓縮率: {ratio:.1f}%\n")

    # 解壓縮
    decoded = decode(codes)
    print(f"解壓後文字: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}")

    # 另一個範例：重複性高的資料
    print("\n" + "="*50 + "\n")
    sample2 = "ABABABABABABABAB"
    print(f"重複性高的文字: {sample2}")
    codes2 = encode(sample2)
    print(f"壓縮後碼字: {codes2}")
    print(f"碼字數量: {len(codes2)} (原始: {len(sample2)} 字元)")
    decoded2 = decode(codes2)
    print(f"解壓是否正確: {decoded2 == sample2}")

    # 展示字典的動態建立
    print("\n字典建立過程:")
    test = "ABA"
    print(f"輸入: {test}")
    codes = encode(test)
    print(f"輸出碼字: {codes}")
    print("解碼驗證:", decode(codes) == test)
