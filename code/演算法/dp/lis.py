"""
最長遞增子序列 (Longest Increasing Subsequence, LIS)

歷史背景：
- 最長遞增子序列是經典的動態規劃問題
- O(n log n) 的解法基於 patience sorting（耐心排序）的概念
- 應用於股票分析、生物資訊學、版本控制等領域

定義：
- 給定一個序列，找出最長的子序列（不要求連續），使得子序列嚴格遞增
"""

from typing import List, Tuple, Optional
import bisect


def lis_dp(nums: List[int]) -> int:
    """
    O(n²) 動態規劃解法

    原理：
    dp[i] = 以 nums[i] 結尾的最長遞增子序列長度
    對於每個 i，檢查所有 j < i，如果 nums[j] < nums[i]，則 dp[i] = max(dp[i], dp[j] + 1)

    時間複雜度：O(n²)
    空間複雜度：O(n)

    Args:
        nums: 輸入序列

    Returns:
        LIS 的長度
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # 每個元素至少可以自成序列

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_dp_with_reconstruction(nums: List[int]) -> Tuple[int, List[int]]:
    """
    O(n²) DP 並重建 LIS

    Returns:
        (LIS 長度, LIS 序列)
    """
    if not nums:
        return 0, []

    n = len(nums)
    dp = [1] * n
    prev = [-1] * n  # 記錄前驅索引

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # 找到 LIS 的結尾索引
    max_len = max(dp)
    end_idx = dp.index(max_len)

    # 重建序列
    lis = []
    idx = end_idx
    while idx != -1:
        lis.append(nums[idx])
        idx = prev[idx]
    lis.reverse()

    return max_len, lis


def lis_patience_sorting(nums: List[int]) -> int:
    """
    O(n log n) 解法：Patience Sorting（耐心排序）

    原理：
    維護一個陣列 tails，其中 tails[i] = 長度為 i+1 的遞增子序列的最小結尾元素
    對於每個 num，使用二分搜尋找到插入位置：
    - 如果 num 比所有 tails 都大，追加到尾部
    - 否則，替換第一個大於等於 num 的元素

    時間複雜度：O(n log n)
    空間複雜度：O(n)

    Args:
        nums: 輸入序列

    Returns:
        LIS 的長度
    """
    if not nums:
        return 0

    tails = []

    for num in nums:
        # 二分搜尋：找到第一個 >= num 的位置
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num

    return len(tails)


def lis_with_reconstruction_nlogn(nums: List[int]) -> Tuple[int, List[int]]:
    """
    O(n log n) 解法並重建 LIS

    使用 parent 陣列記錄每個元素的前驅，用於重建
    """
    if not nums:
        return 0, []

    n = len(nums)
    tails = []  # 儲存索引而非值
    tails_val = []  # 儲存值，用於二分搜尋
    parent = [-1] * n

    for i, num in enumerate(nums):
        idx = bisect.bisect_left(tails_val, num)
        if idx == len(tails):
            tails.append(i)
            tails_val.append(num)
        else:
            tails[idx] = i
            tails_val[idx] = num

        if idx > 0:
            parent[i] = tails[idx - 1]

    # 重建 LIS
    lis = []
    idx = tails[-1] if tails else -1
    while idx != -1:
        lis.append(nums[idx])
        idx = parent[idx]
    lis.reverse()

    return len(tails), lis


if __name__ == "__main__":
    print("=== 最長遞增子序列 (LIS) 測試 ===\n")

    # 測試 1：基本範例
    print("1. 基本範例：")
    test_cases = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7],
        [1],
        [],
        [2, 1, 5, 3, 6, 4, 8, 9],
    ]

    for nums in test_cases:
        dp_len = lis_dp(nums)
        nlogn_len = lis_patience_sorting(nums)
        print(f"  輸入：{nums}")
        print(f"  O(n²) DP: {dp_len}, O(n log n): {nlogn_len}")
    print()

    # 測試 2：重建 LIS
    print("2. 重建 LIS 序列：")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    length, sequence = lis_dp_with_reconstruction(nums)
    print(f"  輸入：{nums}")
    print(f"  LIS 長度：{length}")
    print(f"  LIS 序列：{sequence}")
    print()

    # 測試 3：O(n log n) 重建
    print("3. O(n log n) 重建：")
    length2, sequence2 = lis_with_reconstruction_nlogn(nums)
    print(f"  輸入：{nums}")
    print(f"  LIS 長度：{length2}")
    print(f"  LIS 序列：{sequence2}")
    print()

    # 測試 4：比較效能
    print("4. 效能比較：")
    import time
    large_nums = list(range(500, 0, -1))  # 反序，LIS 長度為 1

    start = time.time()
    len1 = lis_dp(large_nums)
    t1 = time.time() - start

    start = time.time()
    len2 = lis_patience_sorting(large_nums)
    t2 = time.time() - start

    print(f"  陣列大小：{len(large_nums)}")
    print(f"  O(n²) DP: {t1:.6f} 秒，長度 = {len1}")
    print(f"  O(n log n): {t2:.6f} 秒，長度 = {len2}")
    print(f"  結果相同：{len1 == len2}")
