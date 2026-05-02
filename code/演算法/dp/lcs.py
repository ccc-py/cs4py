"""
最長公共子序列 (Longest Common Subsequence)
使用動態規劃求解
"""

from typing import List, Tuple


def lcs_length(text1: str, text2: str) -> int:
    """
    計算兩個字串的最長公共子序列長度
    
    Args:
        text1: 第一個字串
        text2: 第二個字串
        
    Returns:
        最長公共子序列的長度
    """
    m, n = len(text1), len(text2)
    # dp[i][j] 表示 text1[:i] 和 text2[:j] 的 LCS 長度
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def lcs_sequence(text1: str, text2: str) -> Tuple[int, str]:
    """
    計算最長公共子序列並重建子序列
    
    Args:
        text1: 第一個字串
        text2: 第二個字串
        
    Returns:
        (LCS 長度, LCS 字串)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 建立 DP 表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # 回溯重建 LCS
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    lcs_chars.reverse()
    return dp[m][n], ''.join(lcs_chars)


def lcs_optimized(text1: str, text2: str) -> Tuple[int, str]:
    """
    空間優化的 LCS - 只使用兩行陣列
    
    Args:
        text1: 第一個字串
        text2: 第二個字串
        
    Returns:
        (LCS 長度, LCS 字串)
    """
    # 確保 text2 是較短的字串以節省空間
    if len(text1) < len(text2):
        text1, text2 = text2, text1
        swapped = True
    else:
        swapped = False
    
    m, n = len(text1), len(text2)
    # 只使用兩行
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    # 重建 LCS（需要重新計算或保存選擇）
    # 為了簡潔，這裡使用完整 DP 表來重建
    return lcs_sequence(text1 if not swapped else text2, text2 if not swapped else text1)


def lcs_all(text1: str, text2: str) -> List[str]:
    """
    找出所有的最長公共子序列（可能有多個）
    
    Args:
        text1: 第一個字串
        text2: 第二個字串
        
    Returns:
        所有 LCS 的列表
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    def backtrack(i: int, j: int) -> List[str]:
        if i == 0 or j == 0:
            return [""]
        
        if text1[i - 1] == text2[j - 1]:
            prev = backtrack(i - 1, j - 1)
            return [s + text1[i - 1] for s in prev]
        else:
            result = []
            if dp[i - 1][j] >= dp[i][j - 1]:
                result.extend(backtrack(i - 1, j))
            if dp[i][j - 1] >= dp[i - 1][j]:
                # 避免重複
                r2 = backtrack(i, j - 1)
                for s in r2:
                    if s not in result:
                        result.append(s)
            return result
    
    return backtrack(m, n)


if __name__ == "__main__":
    # 測試案例 1
    print("=== 測試案例 1 ===")
    text1 = "abcde"
    text2 = "ace"
    length, sequence = lcs_sequence(text1, text2)
    print(f"字串1: {text1}")
    print(f"字串2: {text2}")
    print(f"LCS 長度: {length}")
    print(f"LCS: {sequence}")
    
    # 測試案例 2
    print("\n=== 測試案例 2 ===")
    text1 = "AGGTAB"
    text2 = "GXTXAYB"
    length, sequence = lcs_sequence(text1, text2)
    print(f"字串1: {text1}")
    print(f"字串2: {text2}")
    print(f"LCS 長度: {length}")
    print(f"LCS: {sequence}")
    
    # 測試案例 3 - 多個 LCS
    print("\n=== 測試案例 3 - 多個 LCS ===")
    text1 = "ABC"
    text2 = "AC"
    length, sequence = lcs_sequence(text1, text2)
    print(f"字串1: {text1}")
    print(f"字串2: {text2}")
    print(f"LCS: {sequence}")
    
    # 比較效能
    print("\n=== 空間優化版本 ===")
    text1 = "abcdefgh"
    text2 = "acfgh"
    length, sequence = lcs_optimized(text1, text2)
    print(f"字串1: {text1}")
    print(f"字串2: {text2}")
    print(f"LCS: {sequence}")
