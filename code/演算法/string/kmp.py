"""
KMP (Knuth-Morris-Pratt) 字串匹配演算法

使用失敗函數（前綴表）來避免重複比較，達到 O(n+m) 的時間複雜度。
"""

from typing import List, Optional


def compute_failure(pattern: str) -> List[int]:
    """
    計算 KMP 的失敗函數（π 表 / 前綴表）

    失敗函數 fail[i] 表示 pattern[0:i+1] 中，最長的「相等前綴後綴」長度。
    當 pattern[i] 不匹配時，可以將模式串向右滑動到 fail[i-1] 的位置繼續匹配。

    參數:
        pattern: 要匹配的模式字串

    回傳:
        失敗函數表（長度為 len(pattern)）
    """
    m: int = len(pattern)
    fail: List[int] = [0] * m
    length: int = 0  # 當前最長相等前綴後綴的長度
    i: int = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            fail[i] = length
            i += 1
        else:
            if length != 0:
                # 回退到上一個可能的長度
                length = fail[length - 1]
            else:
                fail[i] = 0
                i += 1

    return fail


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    KMP 搜尋演算法：在 text 中找出所有 pattern 出現的起始位置

    參數:
        text: 主文字
        pattern: 要搜尋的模式字串

    回傳:
        所有匹配位置的起始索引列表
    """
    if not pattern:
        return []

    n: int = len(text)
    m: int = len(pattern)
    fail: List[int] = compute_failure(pattern)
    result: List[int] = []

    i: int = 0  # text 的索引
    j: int = 0  # pattern 的索引

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # 找到一個匹配
            result.append(i - j)
            j = fail[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = fail[j - 1]
            else:
                i += 1

    return result


def kmp_first_match(text: str, pattern: str) -> Optional[int]:
    """
    找出第一個匹配位置，找不到則回傳 None

    參數:
        text: 主文字
        pattern: 要搜尋的模式字串

    回傳:
        第一個匹配的起始索引，或 None
    """
    matches: List[int] = kmp_search(text, pattern)
    return matches[0] if matches else None


if __name__ == "__main__":
    # 示範 KMP 演算法
    text: str = "ABABDABACDABABCABAB"
    pattern: str = "ABABCABAB"

    print("KMP 字串匹配演算法示範")
    print(f"文字: {text}")
    print(f"模式: {pattern}")
    print()

    # 計算失敗函數
    fail: List[int] = compute_failure(pattern)
    print(f"失敗函數 (π 表): {fail}")
    print()

    # 搜尋所有匹配
    matches: List[int] = kmp_search(text, pattern)
    print(f"找到 {len(matches)} 個匹配:")
    for pos in matches:
        print(f"  位置 {pos}: {text[pos:pos+len(pattern)]}")
    print()

    # 測試空模式
    print(f"空模式搜尋: {kmp_search(text, '')}")
    print()

    # 測試無匹配
    print(f"無匹配結果: {kmp_search(text, 'XYZ')}")
    print()

    # 測試第一個匹配
    first: Optional[int] = kmp_first_match(text, pattern)
    print(f"第一個匹配位置: {first}")
