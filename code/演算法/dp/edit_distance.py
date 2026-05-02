"""
編輯距離 (Edit Distance / Levenshtein Distance)

歷史背景：
- 編輯距離由 Vladimir Levenshtein 於 1965 年提出，也稱為 Levenshtein 距離
- 用於測量兩個字串之間的差異程度
- 廣泛應用於拼字檢查、DNA 序列比對、自然語言處理等領域

定義：
- 將字串 str1 轉換為 str2 所需的最少操作次數
- 允許的操作：插入、刪除、替換（每個操作成本為 1）
"""

from typing import List, Tuple, Optional


def edit_distance_dp(str1: str, str2: str) -> int:
    """
    使用動態規劃計算編輯距離（完整 DP 表）

    原理：
    dp[i][j] = str1[0:i] 轉換為 str2[0:j] 的最小操作次數

    遞推式：
    - 若 str1[i-1] == str2[j-1]：dp[i][j] = dp[i-1][j-1]
    - 否則：dp[i][j] = 1 + min(
          dp[i-1][j],    # 刪除 str1[i-1]
          dp[i][j-1],    # 插入 str2[j-1]
          dp[i-1][j-1]   # 替換 str1[i-1] 為 str2[j-1]
      )

    時間複雜度：O(m * n)
    空間複雜度：O(m * n)

    Args:
        str1: 源字串
        str2: 目標字串

    Returns:
        編輯距離
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化：空字串轉換
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 填表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # 刪除
                    dp[i][j - 1],    # 插入
                    dp[i - 1][j - 1]  # 替換
                )

    return dp[m][n]


def edit_distance_optimized(str1: str, str2: str) -> int:
    """
    空間優化的編輯距離（只保留兩行）

    原理：
    - 每次只需要前一行和當前行
    - 空間複雜度從 O(m*n) 降到 O(min(m, n))

    時間複雜度：O(m * n)
    空間複雜度：O(min(m, n))
    """
    # 確保 str1 是較短的字串，節省空間
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    m, n = len(str1), len(str2)
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr

    return prev[n]


def reconstruct_operations(str1: str, str2: str) -> Tuple[int, List[str]]:
    """
    重建編輯操作序列

    Returns:
        (編輯距離, 操作序列)
        操作格式：('delete', i), ('insert', j), ('replace', i, j), ('keep', i, j)
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                )

    # 反向重建操作
    operations = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i - 1] == str2[j - 1]:
            operations.append(('keep', i - 1, j - 1))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(('replace', i - 1, j - 1))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(('delete', i - 1))
            i -= 1
        else:
            operations.append(('insert', j - 1))
            j -= 1

    operations.reverse()
    return dp[m][n], operations


def visualize_alignment(str1: str, str2: str, operations: List[str]) -> None:
    """視覺化對齊結果"""
    s1_aligned = []
    s2_aligned = []

    for op in operations:
        if op[0] == 'keep':
            s1_aligned.append(str1[op[1]])
            s2_aligned.append(str2[op[2]])
        elif op[0] == 'replace':
            s1_aligned.append(str1[op[1]])
            s2_aligned.append(str2[op[2]])
        elif op[0] == 'delete':
            s1_aligned.append(str1[op[1]])
            s2_aligned.append('-')
        elif op[0] == 'insert':
            s1_aligned.append('-')
            s2_aligned.append(str2[op[1]])

    print(f"  字串1: {''.join(s1_aligned)}")
    print(f"  字串2: {''.join(s2_aligned)}")


if __name__ == "__main__":
    print("=== 編輯距離 (Edit Distance) 測試 ===\n")

    # 測試 1：基本範例
    print("1. 基本範例：")
    test_cases = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("book", "back"),
        ("", "abc"),
        ("abc", "abc"),
    ]

    for s1, s2 in test_cases:
        dist = edit_distance_dp(s1, s2)
        dist_opt = edit_distance_optimized(s1, s2)
        print(f"  '{s1}' -> '{s2}': 距離 = {dist} (優化版: {dist_opt})")
    print()

    # 測試 2：重建操作
    print("2. 重建編輯操作：")
    s1, s2 = "kitten", "sitting"
    dist, ops = reconstruct_operations(s1, s2)
    print(f"  '{s1}' -> '{s2}'")
    print(f"  編輯距離：{dist}")
    print(f"  操作序列：")
    for op in ops:
        print(f"    {op}")
    print("  對齊結果：")
    visualize_alignment(s1, s2, ops)
    print()

    # 測試 3：空字串
    print("3. 空字串測試：")
    print(f"  '' -> 'abc': {edit_distance_dp('', 'abc')}")
    print(f"  'abc' -> '': {edit_distance_dp('abc', '')}")
    print(f"  '' -> '': {edit_distance_dp('', '')}")
    print()

    # 測試 4：效能比較
    print("4. 效能比較（長字串）：")
    import time
    s1 = "a" * 100
    s2 = "b" * 100

    start = time.time()
    d1 = edit_distance_dp(s1, s2)
    t1 = time.time() - start

    start = time.time()
    d2 = edit_distance_optimized(s1, s2)
    t2 = time.time() - start

    print(f"  字串長度：{len(s1)}")
    print(f"  完整 DP 表：{t1:.6f} 秒")
    print(f"  空間優化：{t2:.6f} 秒")
    print(f"  結果相同：{d1 == d2}")
