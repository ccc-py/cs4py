"""
合併排序 (Merge Sort)

歷史背景：
- 1945 年由 John von Neumann 發明
- 基於分治法 (Divide and Conquer) 的經典排序演算法
- 穩定排序，平均/最壞時間複雜度 O(n log n)
- 缺點：需要 O(n) 額外空間
"""

from typing import List, Optional
import random


def merge_sort(arr: List[int]) -> List[int]:
    """
    合併排序

    原理：
    1. 分：將陣列從中間分成兩半
    2. 治：遞迴排序兩個子陣列
    3. 合併：將兩個有序子陣列合併

    時間複雜度：O(n log n)
    空間複雜度：O(n)
    穩定：是
    """
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """合併兩個有序陣列"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_inplace(arr: List[int], start: int = 0, end: Optional[int] = None) -> None:
    """
    原地合併排序（使用輔助空間但不改變介面）

    時間複雜度：O(n log n)
    空間複雜度：O(n log n)（呼叫堆疊）
    """
    if end is None:
        end = len(arr)

    if end - start <= 1:
        return

    mid = (start + end) // 2
    merge_sort_inplace(arr, start, mid)
    merge_sort_inplace(arr, mid, end)

    left = arr[start:mid]
    right = arr[mid:end]

    i = j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def visualize_sort(arr: List[int]) -> List[List[int]]:
    """返回排序過程中的狀態（用於視覺化）"""
    states = [arr[:]]
    _merge_sort_visualize(arr, 0, len(arr), states)
    return states


def _merge_sort_visualize(arr: List[int], start: int, end: int, states: List[List[int]]) -> None:
    """附帶視覺化的合併排序"""
    if end - start <= 1:
        return

    mid = (start + end) // 2
    _merge_sort_visualize(arr, start, mid, states)
    _merge_sort_visualize(arr, mid, end, states)

    left = arr[start:mid]
    right = arr[mid:end]

    i = j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    states.append(arr[:])


def benchmark_merge_sort(n: int = 1000) -> dict:
    """效能基準測試"""
    import time

    arr = [random.randint(0, 10000) for _ in range(n)]

    start = time.time()
    result = merge_sort(arr)
    elapsed = time.time() - start

    return {
        "n": n,
        "time": elapsed,
        "sorted": arr == result
    }


if __name__ == "__main__":
    print("=== 合併排序 (Merge Sort) 測試 ===\n")

    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 3, 1, 1, 2, 2],
        [random.randint(0, 100) for _ in range(20)],
    ]

    for arr in test_cases:
        original = arr[:]
        sorted_arr = merge_sort(arr)
        print(f"輸入：{original}")
        print(f"輸出：{sorted_arr}")
        print()

    print("=== 原地排序測試 ===")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"排序前：{arr}")
    merge_sort_inplace(arr)
    print(f"排序後：{arr}")
    print()

    print("=== 效能測試 ===")
    for n in [100, 1000, 5000]:
        result = benchmark_merge_sort(n)
        print(f"n={result['n']}: {result['time']:.6f} 秒")