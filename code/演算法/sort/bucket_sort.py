"""
桶排序 (Bucket Sort)

包含：
1. 桶排序 - 適用於均勻分佈的資料
2. 可配置的桶數量
3. 桶內使用插入排序
4. 均勻分佈與偏斜資料的效能比較示範
"""

from typing import List, Callable, TypeVar
import random
import time
import math

T = TypeVar('T', int, float)

def insertion_sort(arr: List[T]) -> List[T]:
    """
    插入排序，用於桶內排序
    
    Args:
        arr: 待排序的列表
        
    Returns:
        排序後的列表
    """
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def bucket_sort(
    arr: List[float],
    num_buckets: int = 10,
    key_func: Callable[[float], float] = None
) -> List[float]:
    """
    桶排序
    
    將資料分配到多個桶中，每個桶內部使用插入排序，
    最後合併所有桶的結果。
    
    適用於均勻分佈在 [0, 1) 區間的資料。
    對於其他範圍的資料，會自動計算範圍並調整。
    
    時間複雜度：
    - 最佳情況：O(n) - 資料均勻分佈
    - 平均情況：O(n + n²/k + k) - k 為桶數
    - 最差情況：O(n²) - 所有資料都在同一個桶
    
    Args:
        arr: 待排序的列表（數值型）
        num_buckets: 桶的數量，預設 10
        key_func: 可選的鍵值函數，用於計算分配依據
        
    Returns:
        排序後的列表
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    
    # 計算資料範圍
    if key_func is None:
        min_val = min(result)
        max_val = max(result)
    else:
        min_val = min(key_func(x) for x in result)
        max_val = max(key_func(x) for x in result)
    
    # 處理所有元素相同的情況
    if max_val == min_val:
        return result
    
    # 建立桶
    buckets = [[] for _ in range(num_buckets)]
    
    # 將元素分配到各個桶
    for item in result:
        if key_func is None:
            key = item
        else:
            key = key_func(item)
        
        # 計算桶索引
        bucket_index = int(((key - min_val) / (max_val - min_val)) * num_buckets)
        # 確保索引在有效範圍內
        bucket_index = min(bucket_index, num_buckets - 1)
        buckets[bucket_index].append(item)
    
    # 對每個桶進行排序（使用插入排序）
    result.clear()
    for bucket in buckets:
        if bucket:
            sorted_bucket = insertion_sort(bucket)
            result.extend(sorted_bucket)
    
    return result


def bucket_sort_uniform(arr: List[float], num_buckets: int = None) -> List[float]:
    """
    針對 [0, 1) 均勻分佈的桶排序
    
    Args:
        arr: 在 [0, 1) 區間的數值列表
        num_buckets: 桶數，預設為 len(arr)
        
    Returns:
        排序後的列表
    """
    if not arr:
        return []
    
    if num_buckets is None:
        num_buckets = len(arr)
    
    # 建立桶
    buckets = [[] for _ in range(num_buckets)]
    
    # 分配元素到桶中
    for value in arr:
        # 確保值在 [0, 1) 範圍
        bucket_index = int(value * num_buckets)
        # 處理 value = 1.0 的邊界情況
        if bucket_index == num_buckets:
            bucket_index -= 1
        buckets[bucket_index].append(value)
    
    # 對每個桶排序並合併
    result = []
    for bucket in buckets:
        if bucket:
            result.extend(insertion_sort(bucket))
    
    return result


def generate_uniform_data(n: int, low: float = 0.0, high: float = 1.0) -> List[float]:
    """生成均勻分佈的資料"""
    return [random.uniform(low, high) for _ in range(n)]


def generate_skewed_data(n: int) -> List[float]:
    """生成偏斜分佈的資料（指數分佈）"""
    return [random.expovariate(1.0) for _ in range(n)]


def benchmark(func: Callable, arr: List, *args, **kwargs) -> tuple:
    """基準測試"""
    start = time.perf_counter()
    result = func(arr, *args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def demo_basic():
    """基本桶排序示範"""
    print("=" * 60)
    print("桶排序基本示範")
    print("=" * 60)
    
    # 在 [0, 1) 區間的均勻分佈資料
    print("\n1. [0, 1) 區間的均勻分佈資料")
    data1 = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print(f"原始資料: {data1}")
    result1 = bucket_sort_uniform(data1, num_buckets=5)
    print(f"排序結果: {result1}")
    
    # 任意範圍的數值資料
    print("\n2. 任意範圍的整數資料")
    data2 = [42, 17, 85, 23, 69, 12, 99, 56, 31, 78]
    print(f"原始資料: {data2}")
    result2 = bucket_sort(data2, num_buckets=5)
    print(f"排序結果: {result2}")
    
    # 顯示桶的分配
    print("\n3. 桶分配示範（使用 3 個桶）")
    data3 = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    min_val, max_val = min(data3), max(data3)
    bucket_range = (max_val - min_val) / 3
    print(f"資料: {data3}")
    print(f"範圍: [{min_val}, {max_val}], 每個桶的範圍: {bucket_range:.2f}")
    
    buckets = [[] for _ in range(3)]
    for item in data3:
        idx = int((item - min_val) / (max_val - min_val) * 3)
        idx = min(idx, 2)
        buckets[idx].append(item)
    
    for i, bucket in enumerate(buckets):
        print(f"桶 {i} ({min_val + i*bucket_range:.1f}~{min_val + (i+1)*bucket_range:.1f}): {bucket}")


def demo_performance():
    """效能比較示範"""
    print("\n" + "=" * 60)
    print("桶排序效能比較 - 均勻分佈 vs 偏斜資料")
    print("=" * 60)
    
    # 測試不同大小的資料
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"\n資料量: {size}")
        print("-" * 40)
        
        # 均勻分佈資料
        uniform_data = generate_uniform_data(size)
        _, t1 = benchmark(bucket_sort_uniform, uniform_data, num_buckets=int(math.sqrt(size)))
        print(f"均勻分佈: {t1 * 1000:.3f} ms")
        
        # 偏斜分佈資料
        skewed_data = generate_skewed_data(size)
        # 正規化到 [0, 1)
        max_val = max(skewed_data)
        normalized = [x / max_val for x in skewed_data]
        _, t2 = benchmark(bucket_sort_uniform, normalized, num_buckets=int(math.sqrt(size)))
        print(f"偏斜分佈: {t2 * 1000:.3f} ms")
        
        # 比較不同桶數的影響
        print(f"\n  不同桶數對均勻分佈資料的影響 (n={size}):")
        for num_buckets in [10, 50, 100, 500]:
            if num_buckets <= size:
                _, t = benchmark(bucket_sort_uniform, uniform_data[:size], num_buckets=num_buckets)
                print(f"    桶數 {num_buckets:3d}: {t * 1000:8.3f} ms")


def demo_bucket_count_impact():
    """桶數量對效能的影響"""
    print("\n" + "=" * 60)
    print("桶數量對效能的影響")
    print("=" * 60)
    
    data = generate_uniform_data(1000)
    
    print("\n桶數量 | 時間 (ms) | 說明")
    print("-" * 40)
    
    for num_buckets in [1, 5, 10, 50, 100, 500, 1000]:
        _, elapsed = benchmark(bucket_sort, data, num_buckets)
        note = ""
        if num_buckets == 1:
            note = "（退化為插入排序）"
        elif num_buckets >= len(data):
            note = "（接近計數排序）"
        print(f"{num_buckets:8d} | {elapsed * 1000:9.3f} | {note}")


if __name__ == "__main__":
    demo_basic()
    demo_performance()
    demo_bucket_count_impact()
