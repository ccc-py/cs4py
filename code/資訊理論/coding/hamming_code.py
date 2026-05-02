"""
資訊理論 - 海明碼 (Hamming Code)

實作 (7,4) 海明碼的編碼、錯誤檢測與修正。
"""

from typing import List, Tuple


def encode_hamming_7_4(data_bits: List[int]) -> List[int]:
    """
    編碼 4 位元資料為 7 位元海明碼
    
    位置：1,2,4 為同位位元，3,5,6,7 為資料位元
    
    Args:
        data_bits: 4 位元資料 [d1, d2, d3, d4]
        
    Returns:
        7 位元編碼 [p1, p2, d1, p3, d2, d3, d4]
    """
    d = data_bits
    # 計算同位位元
    p1 = d[0] ^ d[1] ^ d[3]  # 位置 1,3,5,7
    p2 = d[0] ^ d[2] ^ d[3]  # 位置 2,3,6,7
    p3 = d[1] ^ d[2] ^ d[3]  # 位置 4,5,6,7
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]


def calculate_syndrome(received: List[int]) -> int:
    """
    計算症候群 (syndrome) 用於錯誤定位
    
    Args:
        received: 接收到的 7 位元
        
    Returns:
        錯誤位置 (0 表示無錯誤，1-7 表示該位置錯誤)
    """
    p1, p2, d1, p3, d2, d3, d4 = received
    
    # 重新計算同位位元
    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s3 = p3 ^ d2 ^ d3 ^ d4
    
    # 症候群指示錯誤位置 (二進位 s3 s2 s1)
    return (s3 << 2) | (s2 << 1) | s1


def decode_hamming_7_4(received: List[int]) -> Tuple[List[int], bool]:
    """
    解碼 7 位元海明碼，修正單一錯誤
    
    Args:
        received: 接收到的 7 位元
        
    Returns:
        (4 位元資料, 是否修正了錯誤)
    """
    syndrome = calculate_syndrome(received)
    corrected = received.copy()
    error_corrected = False
    
    if syndrome != 0:
        # 位置從 1 開始，需要轉換為 0-indexed
        pos = syndrome - 1
        corrected[pos] ^= 1  # 翻轉錯誤位元
        error_corrected = True
    
    # 提取資料位元（位置 3,5,6,7，0-indexed 為 2,4,5,6）
    data = [corrected[2], corrected[4], corrected[5], corrected[6]]
    return data, error_corrected


def introduce_error(codeword: List[int], position: int) -> List[int]:
    """
    在指定位置引入錯誤（用於測試）
    
    Args:
        codeword: 原始碼字
        position: 錯誤位置 (1-7)
        
    Returns:
        包含錯誤的碼字
    """
    corrupted = codeword.copy()
    corrupted[position - 1] ^= 1
    return corrupted


if __name__ == "__main__":
    # 示範：編碼
    print("=== 海明碼 (7,4) 示範 ===")
    data = [1, 0, 1, 1]
    encoded = encode_hamming_7_4(data)
    print(f"原始資料: {data}")
    print(f"編碼結果: {encoded}")
    
    # 示範：無錯誤解碼
    decoded, corrected = decode_hamming_7_4(encoded)
    print(f"\n解碼結果: {decoded}, 修正: {corrected}")
    
    # 示範：單一錯誤修正
    print("\n=== 錯誤修正示範 ===")
    for pos in range(1, 8):
        corrupted = introduce_error(encoded, pos)
        decoded, corrected = decode_hamming_7_4(corrupted)
        print(f"錯誤位置 {pos}: {corrupted} → 解碼: {decoded}, 修正: {corrected}")
    
    # 示範：雙重錯誤（無法修正）
    print("\n=== 雙重錯誤（無法修正）===")
    corrupted = introduce_error(encoded, 1)
    corrupted = introduce_error(corrupted, 3)
    decoded, corrected = decode_hamming_7_4(corrupted)
    print(f"雙重錯誤: {corrupted}")
    print(f"解碼結果: {decoded} (可能錯誤)")
