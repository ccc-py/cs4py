"""
算術編碼 (Arithmetic Coding)

算術編碼是一種比霍夫曼編碼更接近熵界的無損壓縮演算法。
不同於霍夫曼將每個符號映射到整數位元的編碼，算術編碼將整個訊息映射到 [0, 1) 區間內的一個小數。
"""

from typing import Dict, List, Tuple
from fractions import Fraction
from collections import Counter
import math


def build_probability_table(data: str) -> Dict[str, Tuple[Fraction, Fraction]]:
    """
    根據輸入資料建立機率表，返回每個符號的機率區間
    
    Args:
        data: 輸入字串
        
    Returns:
        字典，key 為符號，value 為 (區間起點, 區間終點) 的 Fraction 元組
    """
    freq = Counter(data)
    total = len(data)

    prob_table = {}
    cumulative = Fraction(0, 1)

    for symbol in sorted(freq.keys()):
        prob = Fraction(freq[symbol], total)
        prob_table[symbol] = (cumulative, cumulative + prob)
        cumulative += prob

    return prob_table


def encode(data: str, prob_table: Dict[str, Tuple[Fraction, Fraction]]) -> str:
    """
    算術編碼：將整個訊息編碼為一個位元字串
    
    Args:
        data: 要編碼的字串
        prob_table: 機率表
        
    Returns:
        位元字串
    """
    low = Fraction(0, 1)
    high = Fraction(1, 1)
    bits = []

    for symbol in data:
        range_width = high - low
        symbol_low, symbol_high = prob_table[symbol]
        new_low = low + range_width * symbol_low
        new_high = low + range_width * symbol_high
        low, high = new_low, new_high

        # 當區間完全在小於 0.5 或大於等於 0.5 時，可以輸出位元
        while True:
            if high <= Fraction(1, 2):
                bits.append('0')
                low *= 2
                high *= 2
            elif low >= Fraction(1, 2):
                bits.append('1')
                low = (low - Fraction(1, 2)) * 2
                high = (high - Fraction(1, 2)) * 2
            else:
                break

    # 輸出最後一位（區間內任一值）
    bits.append('1' if low >= Fraction(1, 2) else '0')

    return ''.join(bits)


def decode(bits: str, prob_table: Dict[str, Tuple[Fraction, Fraction]], 
           data_length: int) -> str:
    """
    解碼算術編碼
    
    Args:
        bits: 位元字串
        prob_table: 機率表
        data_length: 原始資料長度
        
    Returns:
        解碼後的字串
    """
    # 將位元字串轉換為 [0, 1) 中的一個值
    value = Fraction(0, 1)
    for bit in bits:
        value = (value * 2 + (1 if bit == '1' else 0)) / 2 ** len(bits)

    # 解碼每個符號
    low = Fraction(0, 1)
    high = Fraction(1, 1)
    result = []

    for _ in range(data_length):
        range_width = high - low
        for symbol, (sym_low, sym_high) in prob_table.items():
            sym_start = low + range_width * sym_low
            sym_end = low + range_width * sym_high
            if sym_start <= value < sym_end:
                result.append(symbol)
                low, high = sym_start, sym_end
                break

    return ''.join(result)


if __name__ == "__main__":
    # 示範算術編碼
    sample_text = "abracadabra"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    # 建立機率表
    prob_table = build_probability_table(sample_text)
    print(f"機率表: {prob_table}\n")

    # 編碼
    bits = encode(sample_text, prob_table)
    print(f"編碼位元字串: {bits}")
    print(f"編碼位元數: {len(bits)}")
    print(f"原始位元數（8位元/字元）: {len(sample_text) * 8}")
    print(f"壓縮率: {len(bits)/(len(sample_text)*8)*100:.1f}%\n")

    # 解碼
    decoded = decode(bits, prob_table, len(sample_text))
    print(f"解壓後文字: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}")

    # 比較算術編碼與霍夫曼編碼的壓縮率
    print("\n" + "="*50)
    print("與霍夫曼編碼比較:")
    freq = Counter(sample_text)
    huffman_bits = 0
    for char, count in freq.items():
        huffman_bits += count * (-math.log2(freq[char]/len(sample_text)))
    print(f"霍夫曼估計位元數: {huffman_bits:.1f}")
    print(f"算術編碼位元數: {len(bits)}")
    print(f"算術編碼更接近熵界: {len(bits) <= huffman_bits}")
