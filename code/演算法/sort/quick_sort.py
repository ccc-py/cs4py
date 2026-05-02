"""
快速排序 (Quick Sort)

歷史背景：
- 由 Tony Hoare 於 1960 年提出
- 基於分治法 (Divide and Conquer) 的高效排序演算法
- 平均時間複雜度 O(n log n)，但最壞情況為 O(n²)
- 實務上通常比 merge sort 快，因為常數項較小
"""

from typing import List, Callable, Optional
import random


def lomuto_partition(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto 分割法

    原理：
    選擇最後一個元素作為 pivot，將陣列分割成：
    - 左邊：<= pivot
    - 右邊：> pivot

    時間複雜度：O(n)
    空間複雜度：O(1)

    Args:
        arr: 要分割的陣列
        low: 起始索引
        high: 結束索引

    Returns:
        pivot 的最終位置
    """
    pivot = arr[high]
    i = low - 1  # i 指向 <= pivot 區域的最後一個元素

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def hoare_partition(arr: List[int], low: int, high: int) -> int:
    """
    Hoare 分割法（Tony Hoare 原始版本）

    原理：
    從兩端向中間掃描，交換錯位的元素對
    比 Lomuto 分割法效率更高（平均交換次數較少）

    時間複雜度：O(n)
    空間複雜度：O(1)

    Args:
        arr: 要分割的陣列
        low: 起始索引
        high: 結束索引

    Returns:
        pivot 的位置（左子陣列的結束位置）
    """
    pivot = arr[low + (high - low) // 2]  # 選擇中間元素作為 pivot
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]


def quick_sort_lomuto(arr: List[int], low: int = 0, high: Optional[int] = None) -> None:
    """
    使用 Lomuto 分割的快速排序

    時間複雜度：
    - 平均：O(n log n)
    - 最壞：O(n²)（當陣列已排序或反序時）
    空間複雜度：O(log n)（遞迴呼叫堆疊）
    穩定：否
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = lomuto_partition(arr, low, high)
        quick_sort_lomuto(arr, low, pivot_idx - 1)
        quick_sort_lomuto(arr, pivot_idx + 1, high)


def quick_sort_hoare(arr: List[int], low: int = 0, high: Optional[int] = None) -> None:
    """
    使用 Hoare 分割的快速排序

    時間複雜度：O(n log n) 平均
    空間複雜度：O(log n)
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = hoare_partition(arr, low, high)
        quick_sort_hoare(arr, low, pivot_idx)
        quick_sort_hoare(arr, pivot_idx + 1, high)


def randomized_partition(arr: List[int], low: int, high: int) -> int:
    """
    隨機化分割：隨機選擇 pivot

    原理：
    隨機選擇一個元素作為 pivot，與最後一個元素交換
    然後使用 Lomuto 分割

    好處：避免最壞情況（已排序陣列）的發生機率
    """
    random_idx = random.randint(low, high)
    arr[random_idx], arr[high] = arr[high], arr[random_idx]
    return lomuto_partition(arr, low, high)


def quick_sort_randomized(arr: List[int], low: int = 0, high: Optional[int] = None) -> None:
    """
    隨機化快速排序

    原理：
    每次隨機選擇 pivot，使得最壞情況的機率極低
    期望值時間複雜度：O(n log n)

    Args:
        arr: 要排序的陣列
        low: 起始索引
        high: 結束索引
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = randomized_partition(arr, low, high)
        quick_sort_randomized(arr, low, pivot_idx - 1)
        quick_sort_randomized(arr, pivot_idx + 1, high)


def quick_sort_3way(arr: List[int], low: int = 0, high: Optional[int] = None) -> None:
    """
    三路快速排序（Dutch National Flag 演算法）

    原理：
    將陣列分成三個區域：< pivot, == pivot, > pivot
    對於有大量重複元素的陣列特別有效

    時間複雜度：O(n) ~ O(n log n)，重複元素多時接近 O(n)
    """
    if high is None:
        high = len(arr) - 1

    if low >= high:
        return

    pivot = arr[low + (high - low) // 2]

    # 三個指針：lt, i, gt
    lt = low      # arr[low..lt-1] < pivot
    gt = high     # arr[gt+1..high] > pivot
    i = low       # arr[lt..i-1] == pivot

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    quick_sort_3way(arr, low, lt - 1)
    quick_sort_3way(arr, gt + 1, high)


if __name__ == "__main__":
    print("=== 快速排序 (Quick Sort) 測試 ===\n")

    # 測試 Lomuto 版本
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 3, 1, 1, 2, 2],
        [random.randint(0, 100) for _ in range(20)],
    ]

    for i, arr in enumerate(test_cases):
        original = arr[:]

        # 測試 Lomuto
        arr_lomuto = arr[:]
        quick_sort_lomuto(arr_lomuto)
        print(f"測試案例 {i+1} (Lomuto):")
        print(f"  輸入：{original}")
        print(f"  輸出：{arr_lomuto}")
        print(f"  是否排序正確：{arr_lomuto == sorted(original)}")

        # 測試 Hoare
        arr_hoare = arr[:]
        quick_sort_hoare(arr_hoare)
        print(f"  測試 Hoare：{arr_hoare == sorted(original)}")

        # 測試隨機化
        arr_rand = arr[:]
        quick_sort_randomized(arr_rand)
        print(f"  測試隨機化：{arr_rand == sorted(original)}")

        # 測試三路
        arr_3way = arr[:]
        quick_sort_3way(arr_3way)
        print(f"  測試三路：{arr_3way == sorted(original)}")
        print()

    print("=== 重複元素測試（三路快排效果較好）===\n")

    dup_arr = [5, 2, 5, 8, 2, 5, 1, 2, 5]
    print(f"原始陣列：{dup_arr}")
    quick_sort_3way(dup_arr)
    print(f"三路快排結果：{dup_arr}")

    print("\n=== 效能比較 ===\n")

    import time

    for n in [100, 1000, 5000, 10000]:
        arr = [random.randint(0, n) for _ in range(n)]

        # Lomuto
        arr1 = arr[:]
        start = time.time()
        quick_sort_lomuto(arr1)
        t_lomuto = time.time() - start

        # Hoare
        arr2 = arr[:]
        start = time.time()
        quick_sort_hoare(arr2)
        t_hoare = time.time() - start

        # Randomized
        arr3 = arr[:]
        start = time.time()
        quick_sort_randomized(arr3)
        t_rand = time.time() - start

        # 3-way
        arr4 = arr[:]
        start = time.time()
        quick_sort_3way(arr4)
        t_3way = time.time() - start

        print(f"n={n}:")
        print(f"  Lomuto: {t_lomuto:.6f} 秒")
        print(f"  Hoare:  {t_hoare:.6f} 秒")
        print(f"  隨機化:  {t_rand:.6f} 秒")
        print(f"  三路:    {t_3way:.6f} 秒")
        print()
