"""
後綴陣列實作

使用 O(n log² n) 或 O(n log n) 演算法建構後綴陣列，並用二分搜尋進行模式比對。
"""

from typing import List, Tuple, Dict
import operator


def build_suffix_array(text: str) -> List[int]:
    """
    建構後綴陣列
    
    使用 O(n log² n) 的排序方法：
    1. 為每個後綴建立 (起始位置, 第一個字符) 的元組
    2. 依據前 2^k 個字符排序，逐步倍增 k
    
    Args:
        text: 輸入文字
        
    Returns:
        後綴陣列，每個元素是後綴的起始位置
    """
    n = len(text)
    if n == 0:
        return []
    
    # 初始化：依據第一個字符排序
    suffixes = [(i, text[i]) for i in range(n)]
    suffixes.sort(key=lambda x: x[1])
    
    # rank[i] = 後綴 i 的當前排名（從 0 開始）
    rank = [0] * n
    for i, (pos, _) in enumerate(suffixes):
        rank[pos] = i
    
    # 倍增排序
    k = 1
    while k < n:
        # 依據 (rank[i], rank[i+k]) 排序
        suffixes = [(i, rank[i], rank[i + k] if i + k < n else -1)
                    for i in range(n)]
        suffixes.sort(key=operator.itemgetter(1, 2))
        
        # 重新分配排名
        new_rank = [0] * n
        new_rank[suffixes[0][0]] = 0
        for i in range(1, n):
            prev = suffixes[i - 1]
            curr = suffixes[i]
            if curr[1] != prev[1] or curr[2] != prev[2]:
                new_rank[curr[0]] = new_rank[prev[0]] + 1
            else:
                new_rank[curr[0]] = new_rank[prev[0]]
        
        rank = new_rank
        k *= 2
        
        # 如果所有排名都不同，提前結束
        if rank[suffixes[-1][0]] == n - 1:
            break
    
    return [pos for pos, _, _ in suffixes]


def build_lcp_array(text: str, suffix_array: List[int]) -> List[int]:
    """
    建構最長公共前綴陣列 (LCP Array)
    
    LCP[i] = suffix_array[i] 和 suffix_array[i-1] 的最長公共前綴長度
    
    Args:
        text: 原始文字
        suffix_array: 後綴陣列
        
    Returns:
        LCP 陣列
    """
    n = len(suffix_array)
    if n == 0:
        return []
    
    # 計算逆映射：inverse[i] = 後綴 i 在 suffix_array 中的位置
    inverse = [0] * n
    for i, pos in enumerate(suffix_array):
        inverse[pos] = i
    
    lcp = [0] * n
    h = 0  # 當前 LCP 長度
    
    for i in range(n):
        if inverse[i] == 0:
            h = 0
            continue
        
        j = suffix_array[inverse[i] - 1]  # 前一個後綴的起始位置
        
        # 計算 LCP
        while i + h < n and j + h < n and text[i + h] == text[j + h]:
            h += 1
        
        lcp[inverse[i]] = h
        
        if h > 0:
            h -= 1
    
    return lcp


def search_pattern(text: str, pattern: str, suffix_array: List[int]) -> List[int]:
    """
    在後綴陣列中搜尋模式
    
    使用二分搜尋找到第一個和最後一個匹配的位置，
    時間複雜度 O(m log n)，m 為模式長度。
    
    Args:
        text: 原始文字
        pattern: 要搜尋的模式
        suffix_array: 後綴陣列
        
    Returns:
        所有匹配的位置列表
    """
    n = len(suffix_array)
    m = len(pattern)
    
    if m == 0 or n == 0:
        return []
    
    # 找到第一個匹配的位置（下界）
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        pos = suffix_array[mid]
        suffix = text[pos:pos + m]
        if suffix < pattern:
            left = mid + 1
        else:
            right = mid
    
    first = left
    
    # 找到最後一個匹配的位置（上界）
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        pos = suffix_array[mid]
        suffix = text[pos:pos + m]
        if suffix <= pattern:
            left = mid + 1
        else:
            right = mid
    
    last = left
    
    # 收集所有匹配位置
    matches = []
    for i in range(first, last):
        pos = suffix_array[i]
        if text[pos:pos + m] == pattern:
            matches.append(pos)
    
    return matches


if __name__ == "__main__":
    # 示範用法
    print("=== 後綴陣列示範 ===\n")
    
    text = "banana$"
    print(f"文字: {text}")
    
    # 建構後綴陣列
    sa = build_suffix_array(text)
    print(f"\n1. 後綴陣列: {sa}")
    
    # 顯示所有後綴（依字典序排序）
    print("\n2. 排序後的後綴:")
    for i, pos in enumerate(sa):
        print(f"   位置 {pos}: {text[pos:]}")
    
    # 搜尋模式
    patterns = ["ana", "ban", "na", "x"]
    print("\n3. 模式搜尋:")
    for pattern in patterns:
        matches = search_pattern(text, pattern, sa)
        print(f"   模式 '{pattern}': 匹配位置 {matches}")
    
    # 測試較長文字
    print("\n4. 較長文字測試:")
    long_text = "mississippi"
    sa2 = build_suffix_array(long_text)
    print(f"   文字: {long_text}")
    print(f"   後綴陣列: {sa2}")
    matches = search_pattern(long_text, "ssi", sa2)
    print(f"   搜尋 'ssi': {matches}")
