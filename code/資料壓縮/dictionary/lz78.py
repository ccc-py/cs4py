"""
LZ78 壓縮演算法

由 Abraham Lempel 和 Jacob Ziv 在 1978 年提出，是 LZ77 的改進版本。
LZ78 使用顯式的字典（通常實作為前綴樹/Trie），
將資料壓縮為 (字典索引, 新字元) 的二元組。
"""

from typing import List, Dict, Tuple


def encode(data: str) -> List[Tuple[int, str]]:
    """
    LZ78 編碼
    
    Args:
        data: 要壓縮的字串
        
    Returns:
        壓縮後的 (索引, 字元) 二元組列表
    """
    dictionary: Dict[str, int] = {}
    next_index = 1
    result = []
    i = 0

    while i < len(data):
        j = i
        current = ""
        # 找到最長的前綴匹配
        while j < len(data) and current + data[j] in dictionary:
            current = current + data[j]
            j += 1

        if j < len(data):
            # 找到了一個新的字串
            idx = dictionary.get(current, 0)
            char = data[j]
            result.append((idx, char))
            dictionary[current + char] = next_index
            next_index += 1
            i = j + 1
        else:
            # 到達結尾
            if current:
                result.append((dictionary.get(current, 0), ''))
            break

    return result


def decode(tokens: List[Tuple[int, str]]) -> str:
    """
    LZ78 解壓縮
    
    Args:
        tokens: 壓縮後的 (索引, 字元) 二元組列表
        
    Returns:
        解壓後的原始字串
    """
    dictionary: Dict[int, str] = {0: ""}
    next_index = 1
    result = []

    for index, char in tokens:
        prefix = dictionary.get(index, "")
        entry = prefix + char
        result.append(entry)
        dictionary[next_index] = entry
        next_index += 1

    return ''.join(result)


def tokens_to_string(tokens: List[Tuple[int, str]]) -> str:
    """
    將 tokens 轉換為可讀字串（用於除錯）
    
    Args:
        tokens: 壓縮後的二元組列表
        
    Returns:
        可讀的字串表示
    """
    parts = []
    for index, char in tokens:
        if char:
            parts.append(f"({index},'{char}')")
        else:
            parts.append(f"({index},'')")
    return ' '.join(parts)


if __name__ == "__main__":
    # 示範 LZ78 壓縮
    sample_text = "TOBEORNOTTOBEORTOBEORNOT"
    print(f"原始文字: {sample_text}")
    print(f"原始長度: {len(sample_text)} 字元\n")

    # 壓縮
    tokens = encode(sample_text)
    print(f"壓縮後 tokens: {tokens}")
    print(f"Tokens 字串表示: {tokens_to_string(tokens)}")
    print(f"Token 數量: {len(tokens)}\n")

    # 計算壓縮後大小
    estimated_size = len(tokens) * (12 + 8) / 8  # 位元組
    print(f"估計壓縮後大小: {estimated_size:.1f} 位元組")
    print(f"原始大小: {len(sample_text)} 位元組")
    print(f"壓縮率: {estimated_size/len(sample_text)*100:.1f}%\n")

    # 解壓縮
    decoded = decode(tokens)
    print(f"解壓後文字: {decoded}")
    print(f"解壓是否正確: {decoded == sample_text}")

    # 另一個例子
    print("\n" + "="*50 + "\n")
    sample2 = "ABABABAB"
    print(f"測試文字: {sample2}")
    tokens2 = encode(sample2)
    print(f"壓縮 tokens: {tokens_to_string(tokens2)}")
    decoded2 = decode(tokens2)
    print(f"解壓是否正確: {decoded2 == sample2}")

    # 展示字典的建立
    print("\n字典建立過程:")
    test = "ABA"
    print(f"輸入: {test}")
    tokens = encode(test)
    print(f"輸出: {tokens}")
    print("解碼驗證:", decode(tokens) == test)
