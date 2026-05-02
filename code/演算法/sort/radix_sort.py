"""
基數排序 (Radix Sort)

歷史背景：
- 由 Herman Hollerith 於 1887 年為美國人口普查設計
- 最早用於打孔卡片排序機
- 是一種非比較排序演算法，基於數字的位數進行排序
- 屬於穩定排序，時間複雜度與資料規模和位數有關

原理：
- LSD (Least Significant Digit)：從最低位開始排序
- 使用計數排序或桶排序作為子程序
"""

from typing import List, Optional
import random


def counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """
    根據某一位進行計數排序

    Args:
        arr: 要排序的陣列
        exp: 位數指數（1: 個位, 10: 十位, 100: 百位...）

    Returns:
        按該位排序後的陣列
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # 十進制，基數為 10

    # 統計每個數字出現次數
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    # 將計數轉換為位置
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 從後往前建構輸出（保持穩定性）
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    return output


def radix_sort_lsd(arr: List[int]) -> List[int]:
    """
    LSD 基數排序（從最低位開始）

    原理：
    1. 從最低位（個位）開始，對每一位進行穩定排序
    2. 使用計數排序作為子程序
    3. 重複直到最高位

    時間複雜度：O(d * (n + b))，其中 d 是最大數的位數，b 是基數（10）
    空間複雜度：O(n + b)
    穩定：是
    非比較排序：是

    Args:
        arr: 要排序的整數陣列（非負整數）

    Returns:
        排序後的陣列
    """
    if not arr:
        return []

    # 找出最大值以確定位數
    max_val = max(arr)
    if max_val == 0:
        return arr[:]

    # 對每一位進行計數排序
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr


def radix_sort_lsd_inplace(arr: List[int]) -> None:
    """
    原地版本的 LSD 基數排序

    直接修改輸入陣列
    """
    if not arr:
        return

    max_val = max(arr)
    if max_val == 0:
        return

    exp = 1
    while max_val // exp > 0:
        arr[:] = counting_sort_by_digit(arr, exp)
        exp *= 10


def radix_sort_msd(
    arr: List[int],
    exp: Optional[int] = None,
    start: int = 0,
    end: Optional[int] = None
) -> List[int]:
    """
    MSD 基數排序（從最高位開始）

    原理：
    1. 從最高位開始排序
    2. 使用遞迴處理每個桶內的元素
    3. 只在必要時才處理低位

    時間複雜度：O(d * (n + b))
    空間複雜度：O(n)（遞迴呼叫堆疊）

    Args:
        arr: 要排序的整數陣列
        exp: 當前處理的位數
        start: 起始索引
        end: 結束索引

    Returns:
        排序後的陣列
    """
    if end is None:
        end = len(arr)

    if end - start <= 1:
        return arr

    if exp is None:
        max_val = max(arr)
        if max_val == 0:
            return arr[:]
        exp = 1
        while max_val // (exp * 10) > 0:
            exp *= 10

    if exp == 0:
        return arr

    # 建立 10 個桶
    buckets = [[] for _ in range(10)]

    # 分配到桶中
    for i in range(start, end):
        digit = (arr[i] // exp) % 10
        buckets[digit].append(arr[i])

    # 將桶合併回原陣列
    idx = start
    for bucket in buckets:
        if bucket:
            arr[start:start + len(bucket)] = bucket
            start += len(bucket)

    # 對每個非空桶進行遞迴排序（使用下一個低位）
    start = idx
    for bucket in buckets:
        if len(bucket) > 1:
            # 計算這個桶在 arr 中的範圍
            bucket_start = start
            start += len(bucket)
            radix_sort_msd(arr, exp // 10, bucket_start, start)

    return arr


def radix_sort_string(arr: List[str], max_len: Optional[int] = None) -> List[str]:
    """
    字串的基數排序（LSD）

    原理：
    從最右邊字元開始，對每個位置進行穩定排序
    較短字串會在左側補空字元

    時間複雜度：O(L * n)，其中 L 是最長字串長度
    穩定：是

    Args:
        arr: 要排序的字串陣列
        max_len: 最大字串長度（可選）

    Returns:
        排序後的字串陣列
    """
    if not arr:
        return []

    if max_len is None:
        max_len = max(len(s) for s in arr)

    # 從最右邊字元開始往左排序
    for pos in range(max_len - 1, -1, -1):
        # 使用計數排序對該位置字元排序
        buckets = [[] for _ in range(27)]  # 26 個字母 + 空字元

        for s in arr:
            if pos < len(s):
                char_idx = ord(s[pos]) - ord('a') + 1
            else:
                char_idx = 0  # 空字元排在前面
            buckets[char_idx].append(s)

        arr = []
        for bucket in buckets:
            arr.extend(bucket)

    return arr


if __name__ == "__main__":
    print("=== LSD 基數排序測試 ===\n")

    test_cases = [
        [170, 45, 75, 90, 802, 24, 2, 66],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [0, 0, 0, 1, 1, 2, 2],
        [random.randint(0, 9999) for _ in range(20)],
    ]

    for i, arr in enumerate(test_cases):
        original = arr[:]
        sorted_arr = radix_sort_lsd(arr)
        print(f"測試案例 {i+1}:")
        print(f"  輸入：{original}")
        print(f"  輸出：{sorted_arr}")
        print(f"  是否排序正確：{sorted_arr == sorted(original)}")
        print()

    print("=== 原地 LSD 基數排序測試 ===\n")

    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"排序前：{arr}")
    radix_sort_lsd_inplace(arr)
    print(f"排序後：{arr}")

    print("\n=== MSD 基數排序測試 ===\n")

    arr_msd = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"排序前：{arr_msd}")
    radix_sort_msd(arr_msd)
    print(f"排序後：{arr_msd}")
    print(f"是否排序正確：{arr_msd == sorted([170, 45, 75, 90, 802, 24, 2, 66])}")

    print("\n=== 字串基數排序測試 ===\n")

    words = ["cat", "bat", "rat", "apple", "bear", "ant", "dog"]
    print(f"排序前：{words}")
    sorted_words = radix_sort_string(words)
    print(f"排序後：{sorted_words}")

    print("\n=== 效能測試 ===\n")

    import time

    for n in [100, 1000, 5000, 10000]:
        arr = [random.randint(0, 100000) for _ in range(n)]

        # 基數排序
        start = time.time()
        radix_sort_lsd(arr[:])
        t_radix = time.time() - start

        # 內建排序（Timsort）作為比較
        start = time.time()
        sorted(arr[:])
        t_builtin = time.time() - start

        print(f"n={n}:")
        print(f"  基數排序: {t_radix:.6f} 秒")
        print(f"  內建排序: {t_builtin:.6f} 秒")
        print(f"  比例: {t_radix/t_builtin:.2f}x")
        print()
