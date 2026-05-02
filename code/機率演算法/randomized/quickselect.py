"""
隨機化快速選擇 (Randomized QuickSelect)

Hoare 的選擇演算法，用於在無序列表中找到第 k 小元素。
隨機化版本期望時間複雜度為 O(n)。
"""

import random
from typing import TypeVar, List, Optional

T = TypeVar('T')


def quickselect(arr: List[T], k: int, left: Optional[int] = None, 
               right: Optional[int] = None) -> T:
    """
    快速選擇演算法 - 找到第 k 小的元素 (0-indexed)
    
    參數:
        arr: 輸入列表
        k: 要找的排名 (0-indexed，即第 0 小是最小值)
        left: 子陣列左邊界 (內部使用)
        right: 子陣列右邊界 (內部使用)
    
    返回:
        第 k 小的元素
    
    時間複雜度: O(n) 期望值
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    # 檢查 k 的有效性
    if k < 0 or k >= len(arr):
        raise IndexError(f"k={k} 超出範圍 [0, {len(arr)-1}]")
    
    # 隨機選擇 pivot
    pivot_idx = random.randint(left, right)
    pivot = arr[pivot_idx]
    
    # 將 pivot 移到最左邊
    arr[left], arr[pivot_idx] = arr[pivot_idx], arr[left]
    
    # 分割 (類似 quicksort 的 partition)
    i = left + 1
    j = right
    
    while True:
        while i <= j and arr[i] <= pivot:
            i += 1
        while i <= j and arr[j] >= pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            break
    
    # 將 pivot 放到正確位置
    arr[left], arr[j] = arr[j], arr[left]
    
    # j 現在是 pivot 的最終位置
    if j == k:
        return arr[j]
    elif j > k:
        return quickselect(arr, k, left, j - 1)
    else:
        return quickselect(arr, k, j + 1, right)


def randomized_select(arr: List[T], k: int) -> T:
    """
    隨機化選擇 - 非遞迴版本
    
    參數:
        arr: 輸入列表
        k: 要找的排名 (0-indexed)
    
    返回:
        第 k 小的元素
    """
    if k < 0 or k >= len(arr):
        raise IndexError(f"k={k} 超出範圍 [0, {len(arr)-1}]")
    
    # 建立副本避免修改原陣列
    a = arr.copy()
    left = 0
    right = len(a) - 1
    
    while left <= right:
        # 隨機選擇 pivot
        pivot_idx = random.randint(left, right)
        pivot = a[pivot_idx]
        
        # 分割
        a[left], a[pivot_idx] = a[pivot_idx], a[left]
        i = left + 1
        j = right
        
        while True:
            while i <= j and a[i] <= pivot:
                i += 1
            while i <= j and a[j] >= pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
            else:
                break
        
        a[left], a[j] = a[j], a[left]
        
        if j == k:
            return a[j]
        elif j > k:
            right = j - 1
        else:
            left = j + 1
    
    raise RuntimeError("不應該到達這裡")


def median_of_medians(arr: List[T], k: int) -> T:
    """
    中位數的中位數演算法 (Median of Medians)
    
    提供最壞情況 O(n) 的選擇演算法（非隨機化）。
    
    參數:
        arr: 輸入列表
        k: 要找的排名 (0-indexed)
    
    返回:
        第 k 小的元素
    """
    def select(lst: List[T], k_smallest: int) -> T:
        if len(lst) <= 5:
            return sorted(lst)[k_smallest]
        
        # 將列表分成每組 5 個元素
        groups = [lst[i:i+5] for i in range(0, len(lst), 5)]
        medians = [sorted(group)[len(group)//2] for group in groups]
        
        # 遞迴找到中位數的中位數
        pivot = select(medians, len(medians)//2)
        
        # 分割
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
        
        if k_smallest < len(left):
            return select(left, k_smallest)
        elif k_smallest < len(left) + len(middle):
            return pivot
        else:
            return select(right, k_smallest - len(left) - len(middle))
    
    if k < 0 or k >= len(arr):
        raise IndexError(f"k={k} 超出範圍 [0, {len(arr)-1}]")
    
    return select(arr.copy(), k)


def kth_smallest(arr: List[T], k: int) -> T:
    """
    簡單包裝函數：找到第 k 小的元素 (1-indexed)
    
    參數:
        arr: 輸入列表
        k: 第 k 小 (1-indexed)
    
    返回:
        第 k 小的元素
    """
    return quickselect(arr.copy(), k - 1)


def kth_largest(arr: List[T], k: int) -> T:
    """
    找到第 k 大的元素 (1-indexed)
    
    參數:
        arr: 輸入列表
        k: 第 k 大 (1-indexed)
    
    返回:
        第 k 大的元素
    """
    n = len(arr)
    return quickselect(arr.copy(), n - k)


if __name__ == "__main__":
    print("=== 隨機化快速選擇測試 ===\n")
    
    # 測試 1: 基本功能
    print("1. 基本功能測試")
    arr = [3, 2, 1, 5, 4]
    print(f"   陣列: {arr}")
    for k in range(len(arr)):
        result = quickselect(arr.copy(), k)
        print(f"   第 {k+1} 小: {result}")
    
    # 測試 2: 與排序結果比較
    print(f"\n2. 與排序結果比較")
    import random
    test_arr = [random.randint(1, 100) for _ in range(20)]
    sorted_arr = sorted(test_arr)
    print(f"   原始陣列: {test_arr}")
    print(f"   排序結果: {sorted_arr}")
    for k in [0, 5, 10, 15, 19]:
        qs_result = quickselect(test_arr.copy(), k)
        print(f"   第 {k+1} 小: quickselect={qs_result}, sorted={sorted_arr[k]}")
    
    # 測試 3: 時間比較
    print(f"\n3. 時間比較 (陣列大小: 10000)")
    import time
    big_arr = [random.randint(1, 100000) for _ in range(10000)]
    
    start = time.time()
    result1 = quickselect(big_arr.copy(), 5000)
    time_qs = time.time() - start
    
    start = time.time()
    result2 = sorted(big_arr)[5000]
    time_sort = time.time() - start
    
    print(f"   QuickSelect: {time_qs:.6f} 秒, 結果: {result1}")
    print(f"   Sort:        {time_sort:.6f} 秒, 結果: {result2}")
    
    # 測試 4: 中位數和中位數演算法
    print(f"\n4. 中位數的中位數演算法")
    arr4 = [random.randint(1, 1000) for _ in range(50)]
    mom_result = median_of_medians(arr4, 25)  # 第 26 小 (median)
    qs_result = quickselect(arr4.copy(), 25)
    print(f"   Median of Medians: {mom_result}")
    print(f"   QuickSelect:       {qs_result}")
    print(f"   排序驗證:          {sorted(arr4)[25]}")
    
    # 測試 5: kth_largest
    print(f"\n5. 第 k 大元素")
    arr5 = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"   陣列: {arr5}")
    for k in [1, 3, 5, 9]:
        result = kth_largest(arr5, k)
        print(f"   第 {k} 大: {result}")
