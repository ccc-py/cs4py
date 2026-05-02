"""
計數排序 (Counting Sort)

歷史背景：
- 計數排序由 Harold H. Seward 於 1954 年提出
- 是一種非比較排序演算法（不依賴元素間的比較）
- 利用整數鍵值的範圍，通過計數來確定每個元素的位置
- 可以達到 O(n + k) 的線性時間複雜度，其中 k 是鍵值範圍

特性：
- 非比較排序
- 穩定排序
- 適合整數排序，且鍵值範圍不太大
- 是基數排序（Radix Sort）的基礎
"""

from typing import List, Optional, Dict
import sys


def counting_sort(arr: List[int], max_val: Optional[int] = None) -> List[int]:
    """
    標準計數排序

    原理：
    1. 找出陣列中的最大值（或使用給定的 max_val）
    2. 建立計數陣列 count，大小為 max_val + 1
    3. 遍歷輸入陣列，統計每個值的出現次數
    4. 將計數陣列轉換為累積計數（prefix sum）
    5. 從後往前遍歷原陣列，根據累積計數將元素放入正確位置

    時間複雜度：O(n + k)，k 是數值範圍
    空間複雜度：O(k)
    穩定：是

    Args:
        arr: 待排序的非負整數陣列
        max_val: 可選，指定最大值（如果不提供則自動計算）

    Returns:
        排序後的陣列
    """
    if not arr:
        return []

    if max_val is None:
        max_val = max(arr)

    # 初始化計數陣列
    count = [0] * (max_val + 1)

    # 統計每個值的出現次數
    for num in arr:
        count[num] += 1

    # 轉換為累積計數（每個值的最後位置）
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # 建立結果陣列
    result = [0] * len(arr)

    # 從後往前遍歷（保持穩定性）
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        count[num] -= 1
        result[count[num]] = num

    return result


def counting_sort_range(arr: List[int], min_val: Optional[int] = None,
                        max_val: Optional[int] = None) -> List[int]:
    """
    處理負數的計數排序

    原理：
    - 找出最小值和最大值
    - 將值偏移，使最小值對應到索引 0

    時間複雜度：O(n + k)
    空間複雜度：O(k)

    Args:
        arr: 待排序的整數陣列（可包含負數）
        min_val: 可選，指定最小值
        max_val: 可選，指定最大值

    Returns:
        排序後的陣列
    """
    if not arr:
        return []

    if min_val is None:
        min_val = min(arr)
    if max_val is None:
        max_val = max(arr)

    range_size = max_val - min_val + 1
    count = [0] * range_size

    # 統計次數（偏移 min_val）
    for num in arr:
        count[num - min_val] += 1

    # 累積計數
    for i in range(1, range_size):
        count[i] += count[i - 1]

    # 建立結果
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        idx = num - min_val
        count[idx] -= 1
        result[count[idx]] = num

    return result


def stability_demo() -> None:
    """展示計數排序的穩定性"""
    # 使用元組 (值, 原始索引) 來觀察順序
    arr = [(5, 'a'), (2, 'b'), (5, 'c'), (2, 'd'), (1, 'e')]
    # 只按第一個元素排序
    values = [x[0] for x in arr]
    sorted_values = counting_sort(values)

    print("原始順序（值, 標記）：", arr)
    print("排序後的值：", sorted_values)
    print("注意：值相同的元素，原始順序 'a' 在 'c' 前，'b' 在 'd' 前")


def radix_sort_with_counting(arr: List[int], max_digits: int = 10) -> List[int]:
    """
    使用計數排序作為子程序的基數排序

    原理：
    1. 從最低位（個位）開始，對每一位進行穩定排序
    2. 使用計數排序對每一位進行排序
    3. 重複直到最高位

    時間複雜度：O(d * (n + k))，d 是位數，k 是基數（10）
    空間複雜度：O(n + k)

    Args:
        arr: 待排序的非負整數陣列
        max_digits: 最大位數

    Returns:
        排序後的陣列
    """
    if not arr:
        return []

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        # 對當前位數進行計數排序
        count = [0] * 10

        for num in arr:
            digit = (num // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        result = [0] * len(arr)
        for i in range(len(arr) - 1, -1, -1):
            num = arr[i]
            digit = (num // exp) % 10
            count[digit] -= 1
            result[count[digit]] = num

        arr = result
        exp *= 10

    return arr


if __name__ == "__main__":
    print("=== 計數排序 (Counting Sort) 測試 ===\n")

    # 測試 1：基本功能
    print("1. 基本計數排序：")
    test_cases = [
        [4, 2, 2, 8, 3, 3, 1],
        [1, 2, 3, 4, 5],  # 已排序
        [5, 4, 3, 2, 1],  # 反序
        [100, 50, 75, 25],
        [],
        [42],
    ]

    for arr in test_cases:
        result = counting_sort(arr[:])
        print(f"輸入：{arr} -> 輸出：{result}")
    print()

    # 測試 2：包含負數
    print("2. 包含負數的計數排序：")
    arr = [5, -2, 3, -8, 1, -2]
    print(f"輸入：{arr}")
    result = counting_sort_range(arr)
    print(f"輸出：{result}")
    print()

    # 測試 3：穩定性展示
    print("3. 穩定性展示：")
    stability_demo()
    print()

    # 測試 4：基數排序整合
    print("4. 基數排序（使用計數排序作為子程序）：")
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"輸入：{arr}")
    result = radix_sort_with_counting(arr)
    print(f"輸出：{result}")
    print()

    # 測試 5：效能比較（與 Python 內建排序）
    print("5. 大範圍小陣列測試：")
    arr = [7, 3, 7, 3, 1, 9, 9, 2, 2, 5]
    print(f"輸入：{arr}")
    print(f"計數排序：{counting_sort(arr)}")
    print(f"內建排序：{sorted(arr)}")
    print("兩者結果相同且穩定" if counting_sort(arr) == sorted(arr) else "結果不同")
