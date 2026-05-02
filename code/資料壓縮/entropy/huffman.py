"""
霍夫曼編碼 (Huffman Coding)

由 David Huffman 在 1952 年提出，是一種最優前綴編碼演算法，基於字元出現頻率構建變長編碼樹，
出現頻率高的字元使用較短的編碼，頻率低的字元使用較長的編碼，使整體壓縮後的位元數最小。
"""

from typing import Dict, Tuple, Optional, List
import heapq


class HuffmanNode:
    """霍夫曼樹節點"""
    def __init__(self, freq: int, symbol: Optional[str] = None,
                 left: Optional['HuffmanNode'] = None, right: Optional['HuffmanNode'] = None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other: 'HuffmanNode') -> bool:
        """用於堆積比較，頻率低的節點優先"""
        return self.freq < other.freq


def build_huffman_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    """
    根據頻率表構建霍夫曼樹
    
    Args:
        freq_table: 字元到出現次數的映射
        
    Returns:
        霍夫曼樹的根節點
    """
    heap: List[HuffmanNode] = []
    # 將每個字元轉換為葉節點並加入最小堆
    for symbol, freq in freq_table.items():
        heapq.heappush(heap, HuffmanNode(freq, symbol))

    # 合併節點直到堆中只剩一個節點
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(node: HuffmanNode, prefix: str, codes: Dict[str, str]) -> None:
    """
    遞迴遍歷霍夫曼樹生成編碼表
    
    Args:
        node: 當前節點
        prefix: 當前累積的編碼前綴
        codes: 儲存字元到編碼的映射
    """
    if node.symbol is not None:
        # 葉節點，記錄編碼
        codes[node.symbol] = prefix if prefix else '0'
        return

    if node.left:
        generate_codes(node.left, prefix + '0', codes)
    if node.right:
        generate_codes(node.right, prefix + '1', codes)


def encode(data: str, codes: Dict[str, str]) -> Tuple[bytes, int]:
    """
    使用霍夫曼編碼壓縮資料
    
    Args:
        data: 要壓縮的原始字串
        codes: 字元到霍夫曼編碼的映射
        
    Returns:
        壓縮後的位元組資料，以及填充位數
    """
    # 將所有字元轉換為位元字串
    bitstring = ''.join(codes[char] for char in data)

    # 將位元字串轉換為位元組（不足8位補0）
    padding = (8 - len(bitstring) % 8) % 8
    bitstring += '0' * padding

    # 將每8位轉換為一個位元組
    encoded_bytes = bytearray()
    for i in range(0, len(bitstring), 8):
        encoded_bytes.append(int(bitstring[i:i+8], 2))

    return bytes(encoded_bytes), padding


def decode(encoded_bytes: bytes, tree: HuffmanNode, padding: int = 0, 
         data_length: int = None) -> str:
    """
    解碼霍夫曼壓縮的資料
    
    Args:
        encoded_bytes: 壓縮後的位元組資料
        tree: 霍夫曼樹根節點
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

    # 遍歷霍夫曼樹解碼
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
    # 示範：壓縮一段文字
    sample_text = "this is an example for huffman encoding"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    # 計算字元頻率
    freq_table = {}
    for char in sample_text:
        freq_table[char] = freq_table.get(char, 0) + 1

    # 構建霍夫曼樹和編碼表
    huffman_tree = build_huffman_tree(freq_table)
    codes = {}
    generate_codes(huffman_tree, '', codes)

    print(f"霍夫曼編碼表: {codes}\n")

    # 壓縮
    encoded_data, padding = encode(sample_text, codes)
    print(f"壓縮後位元組數: {len(encoded_data)}")
    print(f"填充位數: {padding}")
    print(f"壓縮率: {len(encoded_data)/len(sample_text)*100:.1f}%")

    # 解壓縮
    decoded_text = decode(encoded_data, huffman_tree, padding, len(sample_text))
    print(f"解壓後文字: {decoded_text}")
    print(f"解壓是否正確: {decoded_text == sample_text}")
