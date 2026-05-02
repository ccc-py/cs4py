"""
選擇排序 (Selection Sort)

包含：
1. 基本選擇排序 - 每次找最小值並交換
2. 雙向選擇排序 - 同時找最小和最大值
3. 與其他排序比較的示範
"""

from typing import List, Callable, TypeVar
import time
import random

T = TypeVar('T', int, float)

def selection_sort(arr: List[T]) -> List[T]:
    """
    基本選擇排序
    
    每次迭代找到未排序部分的最小值，放到已排序部分的末尾。
    時間複雜度：O(n²)，空間複雜度：O(1)
    
    Args:
        arr: 待排序的列表
        
    Returns:
        排序後的列表（原地排序）
    """
    n = len(arr)
    result = arr.copy()
    
    for i in range(n):
        min_idx = i
        # 在未排序部分找最小值
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        # 將最小值交換到位置 i
        if min_idx != i:
            result[i], result[min_idx] = result[min_idx], result[i]
    
    return result


def bidirectional_selection_sort(arr: List[T]) -> List[T]:
    """
    雙向選擇排序（改進的雞尾酒選擇排序）
    
    每次迭代同時找到未排序部分的最小值和最大值，
    分別放到未排序部分的開頭和末尾。
    
    時間複雜度：O(n²)，但比較次數約為基本選擇排序的一半
    
    Args:
        arr: 待排序的列表
        
    Returns:
        排序後的列表（原地排序）
    """
    n = len(arr)
    result = arr.copy()
    
    left = 0
    right = n - 1
    
    while left < right:
        min_idx = left
        max_idx = left
        
        # 在 [left, right] 範圍內找最小值和最大值
        for i in range(left + 1, right + 1):
            if result[i] < result[min_idx]:
                min_idx = i
            if result[i] > result[max_idx]:
                max_idx = i
        
        # 將最小值放到左邊
        if min_idx != left:
            result[left], result[min_idx] = result[min_idx], result[left]
            # 如果最大值原本在 left 位置，交換後需要更新 max_idx
            if max_idx == left:
                max_idx = min_idx
        
        # 將最大值放到右邊
        if max_idx != right:
            # 如果 min_idx 變成了 right，需要更新
            if max_idx == left:
                max_idx = right
            result[right], result[max_idx] = result[max_idx], result[right]
        
        left += 1
        right -= 1
    
    return result


def bubble_sort(arr: List[T]) -> List[T]:
    """冒泡排序（用於比較）"""
    result = arr.copy()
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def insertion_sort(arr: List[T]) -> List[T]:
    """插入排序（用於比較）"""
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def benchmark_sort(sort_func: Callable, arr: List[T], name: str) -> tuple:
    """基準測試"""
    start = time.perf_counter()
    result = sort_func(arr)
    elapsed = time.perf_counter() - start
    return result, elapsed


def demo_comparison():
    """比較不同排序演算法的效能"""
    print("=" * 60)
    print("選擇排序與其他排序演算法比較")
    print("=" * 60)
    
    # 測試不同大小的陣列
    test_cases = [
        ("小型陣列 (10 個元素)", list(range(10))[::-1]),  # 逆序
        ("中型陣列 (100 個元素)", [random.randint(1, 1000) for _ in range(100)]),
        ("大型陣列 (1000 個元素)", [random.randint(1, 10000) for _ in range(1000)]),
    ]
    
    sorters = [
        ("選擇排序", selection_sort),
        ("雙向選擇排序", bidirectional_selection_sort),
        ("冒泡排序", bubble_sort),
        ("插入排序", insertion_sort),
    ]
    
    for case_name, arr in test_cases:
        print(f"\n{case_name}")
        print("-" * 40)
        print(f"原始陣列前 10 個: {arr[:10]}")
        
        results = []
        for name, func in sorters:
            sorted_arr, elapsed = benchmark_sort(func, arr, name)
            results.append((name, elapsed, sorted_arr))
            print(f"{name:15s}: {elapsed * 1000:8.3f} ms")
        
        # 驗證所有結果都正確
        reference = sorted(arr)
        for name, _, result in results:
            assert result == reference, f"{name} 排序結果錯誤！"
        
        print("✓ 所有排序結果正確")


def demo_selection_sort():
    """選擇排序示範"""
    print("=" * 60)
    print("選擇排序演算法示範")
    print("=" * 60)
    
    # 基本選擇排序
    print("\n1. 基本選擇排序")
    arr1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始陣列: {arr1}")
    result1 = selection_sort(arr1)
    print(f"排序結果: {result1}")
    
    # 顯示每步過程
    print("\n排序過程:")
    arr = arr1.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(f"  第 {i+1} 輪: {arr}")
    
    # 雙向選擇排序
    print("\n2. 雙向選擇排序")
    arr2 = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始陣列: {arr2}")
    result2 = bidirectional_selection_sort(arr2)
    print(f"排序結果: {result2}")
    
    # 比較兩種選擇排序
    print("\n3. 比較基本與雙向選擇排序")
    test_arr = [random.randint(1, 1000) for _ in range(500)]
    
    _, t1 = benchmark_sort(selection_sort, test_arr, "基本")
    _, t2 = benchmark_sort(bidirectional_selection_sort, test_arr, "雙向")
    
    print(f"基本選擇排序 (500 個元素): {t1 * 1000:.3f} ms")
    print(f"雙向選擇排序 (500 個元素): {t2 * 1000:.3f} ms")
    print(f"雙向選擇排序約為基本選擇排序的 {t2/t1:.2%}")


if __name__ == "__main__":
    demo_selection_sort()
    print("\n")
    demo_comparison()
