"""
插入排序與其變體 (Insertion Sort and Variants)

歷史背景：
- 插入排序是人類整理撲克牌時自然使用的排序方法
- 最早的文獻記錄可追溯到 1945 年 John von Neumann 的工作
- 對於小型或近乎有序的陣列非常高效
- 是自適應排序（Adaptive Sort）的典型代表

特性：
- 穩定排序
- 原地排序
- 自適應：輸入越有序，執行越快
- 適合小資料量或近乎有序的資料
"""

from typing import List, Tuple, Optional
import bisect


def insertion_sort(arr: List[int]) -> List[int]:
    """
    標準插入排序

    原理：
    1. 從第二個元素開始（索引 1）
    2. 將當前元素與已排序部分的元素從後往前比較
    3. 找到正確位置並插入

    時間複雜度：
    - 最佳（已排序）：O(n)
    - 平均：O(n²)
    - 最壞（反序）：O(n²)
    空間複雜度：O(1)
    穩定：是

    Args:
        arr: 待排序陣列

    Returns:
        排序後的陣列（原地排序，也返回參考）
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # 將大於 key 的元素往後移
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def binary_insertion_sort(arr: List[int]) -> List[int]:
    """
    二分插入排序

    原理：
    - 使用二分搜尋找到插入位置（減少比較次數）
    - 仍需移動元素，所以時間複雜度仍是 O(n²)
    - 比較次數從 O(n²) 降到 O(n log n)

    時間複雜度：O(n²)（移動元素占主導）
    空間複雜度：O(1)
    穩定：是

    Args:
        arr: 待排序陣列

    Returns:
        排序後的陣列
    """
    for i in range(1, len(arr)):
        key = arr[i]
        # 使用二分搜尋找到插入位置
        pos = bisect.bisect_left(arr, key, 0, i)
        # 將元素往後移
        for j in range(i, pos, -1):
            arr[j] = arr[j - 1]
        arr[pos] = key
    return arr


def shell_sort(arr: List[int]) -> List[int]:
    """
    Shell 排序（希爾排序）

    原理：
    - 插入排序的推廣，由 Donald Shell 於 1959 年提出
    - 使用間隔序列（gap sequence）逐步減小間隔
    - 初期使用大間隔，可以將元素快速移動到大致位置
    - 最後間隔為 1 時，就是標準插入排序

    時間複雜度：取決於間隔序列
    - 平均：約 O(n^1.5)（使用 Shell 原始序列）
    - 最好：O(n log n)
    - 最壞：O(n²)
    空間複雜度：O(1)
    穩定：否

    Args:
        arr: 待排序陣列

    Returns:
        排序後的陣列
    """
    n = len(arr)
    # 使用 Knuth 的間隔序列：1, 4, 13, 40, 121, ...
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    while gap > 0:
        # 對每個間隔進行插入排序
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 3

    return arr


def is_adaptive_demo(arr: List[int], sort_func) -> Tuple[List[int], int, int]:
    """
    展示插入排序的自適應特性

    Args:
        arr: 輸入陣列
        sort_func: 排序函數

    Returns:
        (排序後陣列, 比較次數, 移動次數)
    """
    comparisons = 0
    moves = 0

    arr_copy = arr[:]
    n = len(arr_copy)

    for i in range(1, n):
        key = arr_copy[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr_copy[j] > key:
                arr_copy[j + 1] = arr_copy[j]
                moves += 1
                j -= 1
            else:
                break
        arr_copy[j + 1] = key
        moves += 1

    return arr_copy, comparisons, moves


if __name__ == "__main__":
    print("=== 插入排序與變體 (Insertion Sort and Variants) 測試 ===\n")

    # 測試 1：標準插入排序
    print("1. 標準插入排序：")
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 3, 1, 1, 2, 2],
    ]

    for arr in test_cases:
        original = arr[:]
        result = insertion_sort(arr)
        print(f"輸入：{original} -> 輸出：{result}")
    print()

    # 測試 2：二分插入排序
    print("2. 二分插入排序：")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"輸入：{arr}")
    result = binary_insertion_sort(arr[:])
    print(f"輸出：{result}")
    print()

    # 測試 3：Shell 排序
    print("3. Shell 排序：")
    arr = [64, 34, 25, 12, 22, 11, 90, 88, 77, 66, 55]
    print(f"輸入：{arr}")
    result = shell_sort(arr[:])
    print(f"輸出：{result}")
    print()

    # 測試 4：自適應特性展示
    print("4. 自適應特性展示：")
    already_sorted = list(range(10))
    reverse_sorted = list(range(10, 0, -1))
    random_arr = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]

    for name, arr in [("已排序", already_sorted), ("反序", reverse_sorted), ("隨機", random_arr)]:
        _, comp, moves = is_adaptive_demo(arr, insertion_sort)
        print(f"  {name}：比較 {comp} 次，移動 {moves} 次")
    print()

    # 測試 5：穩定性測試
    print("5. 穩定性測試（相同元素保持順序）：")
    arr = [(5, 'a'), (2, 'b'), (5, 'c'), (2, 'd'), (1, 'e')]
    # 只按元組第一個元素排序，看第二個元素是否保持原始順序
    arr_copy = arr[:]
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        while j >= 0 and arr_copy[j][0] > key[0]:
            arr_copy[j + 1] = arr_copy[j]
            j -= 1
        arr_copy[j + 1] = key
    print(f"輸入：{arr}")
    print(f"輸出：{arr_copy}")
    print("（相同鍵值 'a' 在 'c' 前，'b' 在 'd' 前，表示穩定）")
