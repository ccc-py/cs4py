"""
Shannon-Fano 編碼

由 Claude Shannon 和 Robert Fano 在 1949 年提出，是一種早期的資料壓縮演算法。
雖然不是最優編碼，但其簡單的頂向下分割方法為後來的霍夫曼編碼奠定了基礎。
"""

from typing import Dict, List, Tuple
import heapq


class ShannonNode:
    """Shannon-Fano 樹節點"""
    def __init__(self, symbol: str = None, left: 'ShannonNode' = None,
                 right: 'ShannonNode' = None, freq: int = 0):
        self.symbol = symbol
        self.left = left
        self.right = right
        self.freq = freq


def build_shannon_tree(symbols: List[Tuple[str, int]], start: int, end: int) -> ShannonNode:
    """
    遞迴構建 Shannon-Fano 樹（頂向下分割）
    
    Args:
        symbols: 已按頻率排序的 (符號, 頻率) 列表
        start: 當前區段的起始索引
        end: 當前區段的結束索引
        
    Returns:
        樹節點
    """
    if start == end:
        return ShannonNode(symbol=symbols[start][0], freq=symbols[start][1])

    if start > end:
        return None

    total_freq = sum(freq for _, freq in symbols[start:end+1])
    half_freq = total_freq / 2

    left_freq = 0
    split_point = start
    for i in range(start, end + 1):
        if left_freq + symbols[i][1] > half_freq:
            break
        left_freq += symbols[i][1]
        split_point = i

    if split_point >= end:
        split_point = end - 1

    left = build_shannon_tree(symbols, start, split_point) if start <= split_point else None
    right = build_shannon_tree(symbols, split_point + 1, end) if split_point + 1 <= end else None

    return ShannonNode(left=left, right=right, freq=total_freq)


def generate_codes(node: ShannonNode, prefix: str, codes: Dict[str, str]) -> None:
    """
    遞迴遍歷樹生成編碼表
    
    Args:
        node: 當前節點
        prefix: 當前累積的編碼前綴
        codes: 儲存符號到編碼的映射
    """
    if node is None:
        return

    if node.symbol is not None:
        codes[node.symbol] = prefix if prefix else '0'
        return

    if node.left:
        generate_codes(node.left, prefix + '0', codes)
    if node.right:
        generate_codes(node.right, prefix + '1', codes)


def encode(data: str, codes: Dict[str, str]) -> Tuple[bytes, int]:
    """
    使用 Shannon-Fano 編碼壓縮資料
    
    Args:
        data: 要壓縮的原始字串
        codes: 符號到編碼的映射
        
    Returns:
        壓縮後的位元組資料，以及填充位數
    """
    bitstring = ''.join(codes[char] for char in data)

    # 補齊到 8 的倍數
    padding = (8 - len(bitstring) % 8) % 8
    bitstring += '0' * padding

    # 轉換為位元組
    encoded_bytes = bytearray()
    for i in range(0, len(bitstring), 8):
        encoded_bytes.append(int(bitstring[i:i+8], 2))

    return bytes(encoded_bytes), padding


def decode(encoded_bytes: bytes, tree: ShannonNode, padding: int = 0,
         data_length: int = None) -> str:
    """
    解碼 Shannon-Fano 壓縮的資料
    
    Args:
        encoded_bytes: 壓縮後的位元組資料
        tree: Shannon-Fano 樹根節點
        padding: 填充位數
        data_length: 原始資料長度（用於正確解碼）
        
    Returns:
        解壓後的原始字串
    """
    # 將位元組轉換回位元字串
    bitstring = ''.join(format(byte, '08b') for byte in encoded_bytes)
    
    # 移除填充位
    if padding > 0:
        bitstring = bitstring[:-padding]

    # 遍歷樹解碼
    result = []
    node = tree
    
    if data_length is not None:
        # 已知原始長度，解碼指定數量的字元
        decoded_count = 0
        for bit in bitstring:
            node = node.left if bit == '0' else node.right
            if node.symbol is not None:
                result.append(node.symbol)
                node = tree
                decoded_count += 1
                if decoded_count >= data_length:
                    break
    else:
        # 未知長度，解碼直到位元字串結束
        for bit in bitstring:
            node = node.left if bit == '0' else node.right
            if node.symbol is not None:
                result.append(node.symbol)
                node = tree

    return ''.join(result)


if __name__ == "__main__":
    # 示範 Shannon-Fano 編碼
    sample_text = "this is an example for shannon fano encoding"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    from collections import Counter
    freq_table = Counter(sample_text)
    sorted_symbols = sorted(freq_table.items(), key=lambda x: -x[1])

    print(f"符號頻率: {sorted_symbols}\n")

    sf_tree = build_shannon_tree(sorted_symbols, 0, len(sorted_symbols) - 1)
    codes = {}
    generate_codes(sf_tree, '', codes)

    print(f"Shannon-Fano 編碼表: {codes}\n")

    # 壓縮
    encoded, padding = encode(sample_text, codes)
    print(f"壓縮後位元組數: {len(encoded)}")
    print(f"填充位數: {padding}")
    print(f"壓縮率: {len(encoded)/len(sample_text)*100:.1f}%")

    # 解壓縮
    decoded = decode(encoded, sf_tree, padding, len(sample_text))
    print(f"解壓後文字: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}")
