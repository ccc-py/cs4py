"""
LZ77 滑動視窗壓縮演算法

由 Abraham Lempel 和 Jacob Ziv 在 1977 年提出，是第一個實用的字典式壓縮演算法。
LZ77 使用滑動視窗來尋找重複的資料片段，並用 (偏移量, 長度, 下一字元) 三元組來表示匹配。
"""

from typing import List, Tuple, Optional


def find_longest_match(data: str, pos: int, window_start: int,
                       lookahead_size: int) -> Tuple[int, int, Optional[str]]:
    """
    在滑動視窗中尋找最長匹配
    
    Args:
        data: 輸入字串
        pos: 當前位置
        window_start: 搜尋視窗起始位置
        lookahead_size: 前瞻視窗大小
        
    Returns:
        (偏移量, 匹配長度, 下一個字元) 三元組
    """
    search_window = data[window_start:pos]
    lookahead_end = min(pos + lookahead_size, len(data))
    lookahead = data[pos:lookahead_end]

    best_offset = 0
    best_length = 0

    # 在搜尋視窗中尋找最長匹配
    for i in range(len(search_window)):
        match_length = 0
        # 計算從位置 i 開始能匹配多長
        while (match_length < len(lookahead) and
               i + match_length < len(search_window) and
               search_window[i + match_length] == lookahead[match_length]):
            match_length += 1

        if match_length > best_length:
            best_length = match_length
            best_offset = len(search_window) - i

    # 如果沒有匹配，返回當前字元
    if best_length == 0:
        return (0, 0, data[pos] if pos < len(data) else None)

    # 返回匹配資訊和下一個字元
    next_char = data[pos + best_length] if pos + best_length < len(data) else None
    return (best_offset, best_length, next_char)


def encode(data: str, window_size: int = 20, lookahead_size: int = 15) -> List[Tuple[int, int, Optional[str]]]:
    """
    LZ77 編碼
    
    Args:
        data: 要壓縮的字串
        window_size: 搜尋視窗大小
        lookahead_size: 前瞻視窗大小
        
    Returns:
        壓縮後的三元組列表
    """
    tokens = []
    pos = 0

    while pos < len(data):
        window_start = max(0, pos - window_size)
        offset, length, next_char = find_longest_match(
            data, pos, window_start, lookahead_size
        )

        if length > 0:
            tokens.append((offset, length, next_char))
            pos += length + (1 if next_char is not None else 0)
        else:
            # 無匹配，輸出字面量
            tokens.append((0, 0, data[pos]))
            pos += 1

    return tokens


def decode(tokens: List[Tuple[int, int, Optional[str]]]) -> str:
    """
    LZ77 解碼
    
    Args:
        tokens: 壓縮後的三元組列表
        
    Returns:
        解壓後的原始字串
    """
    result = []

    for offset, length, next_char in tokens:
        if offset == 0 and length == 0:
            # 字面量
            if next_char is not None:
                result.append(next_char)
        else:
            # 從已解碼的資料中複製
            start = len(result) - offset
            for i in range(length):
                result.append(result[start + i])
            if next_char is not None:
                result.append(next_char)

    return ''.join(result)


def tokens_to_string(tokens: List[Tuple[int, int, Optional[str]]]) -> str:
    """
    將 tokens 轉換為可讀字串（用於除錯）
    
    Args:
        tokens: 壓縮後的三元組列表
        
    Returns:
        可讀的字串表示
    """
    parts = []
    for offset, length, next_char in tokens:
        if offset == 0 and length == 0:
            parts.append(f"'{next_char}'")
        else:
            parts.append(f"({offset},{length},{next_char})")
    return ' '.join(parts)


if __name__ == "__main__":
    # 示範 LZ77 壓縮
    sample_text = "abracadabra abracadabra"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    # 壓縮
    tokens = encode(sample_text, window_size=20, lookahead_size=15)
    print(f"壓縮後 tokens: {tokens}")
    print(f"Tokens 數量: {len(tokens)}")
    print(f"Tokens 字串表示: {tokens_to_string(tokens)}\n")

    # 計算壓縮後的近似大小（假設每個 token 用 2 位元組表示）
    estimated_size = len(tokens) * 2
    print(f"估計壓縮後大小: {estimated_size} 位元組")
    print(f"壓縮率: {estimated_size/len(sample_text)*100:.1f}%\n")

    # 解壓縮
    decoded = decode(tokens)
    print(f"解壓後文字: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}")

    # 另一個例子：重複性高的資料
    print("\n" + "="*50 + "\n")
    sample2 = "ABCABCABCABCABC"
    print(f"重複性高的文字: {sample2}")
    tokens2 = encode(sample2)
    print(f"壓縮後 tokens: {tokens_to_string(tokens2)}")
    decoded2 = decode(tokens2)
    print(f"解壓是否正確: {decoded2 == sample2}")
