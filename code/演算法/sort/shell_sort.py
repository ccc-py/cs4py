"""
希爾排序 (Shell Sort)

包含：
1. 希爾排序實作
2. 多種間隔序列（Shell's, Hibbard's, Knuth's）
3. 不同間隔序列的效能比較
4. 示範程式
"""

from typing import List, Callable, Tuple, TypeVar
import time
import random

T = TypeVar('T', int, float)

def shell_sort_with_gaps(arr: List[T], gaps: List[int]) -> List[T]:
    """
    使用指定間隔序列進行希爾排序
    
    希爾排序是插入排序的改進版，通過比較相距一定間隔的元素來工作，
    各趟比較所用的距離（間隔）隨算法的進行而減小。
    
    時間複雜度取決於間隔序列：
    - Shell's 序列：O(n²) 到 O(n log² n)
    - Hibbard's 序列：O(n^(3/2))
    - Knuth's 序列：O(n^(3/2))
    
    Args:
        arr: 待排序的列表
        gaps: 間隔序列（遞減）
        
    Returns:
        排序後的列表（原地排序）
    """
    result = arr.copy()
    n = len(result)
    
    # 對每個間隔進行插入排序
    for gap in gaps:
        # 從 gap 開始，逐個對其所在組進行插入排序
        for i in range(gap, n):
            temp = result[i]
            j = i
            
            # 對間隔為 gap 的元素進行插入排序
            while j >= gap and result[j - gap] > temp:
                result[j] = result[j - gap]
                j -= gap
            
            result[j] = temp
    
    return result


def shell_gaps(n: int) -> List[int]:
    """
    Shell 的原始間隔序列：n/2, n/4, ..., 1
    
    Shell 提出的初始序列，但會導致某些情況下效能不佳。
    
    Args:
        n: 陣列大小
        
    Returns:
        間隔序列
    """
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps


def hibbard_gaps(n: int) -> List[int]:
    """
    Hibbard 間隔序列：2^k - 1
    
    使用 1, 3, 7, 15, 31, ... 2^k - 1 < n 的序列。
    時間複雜度約為 O(n^(3/2))。
    
    Args:
        n: 陣列大小
        
    Returns:
        間隔序列
    """
    gaps = []
    k = 1
    while True:
        gap = (1 << k) - 1  # 2^k - 1
        if gap >= n:
            break
        gaps.append(gap)
        k += 1
    return list(reversed(gaps))


def knuth_gaps(n: int) -> List[int]:
    """
    Knuth 間隔序列：(3^k - 1) / 2
    
    Knuth 提出的序列：1, 4, 13, 40, 121, ...
    實務上常用的最高間隔不超過 n/3。
    
    Args:
        n: 陣列大小
        
    Returns:
        間隔序列
    """
    gaps = []
    gap = 1
    # 先生成所有小於 n 的間隔
    while gap < n:
        gaps.append(gap)
        gap = gap * 3 + 1  # (3^k - 1) / 2 的遞推形式
    return list(reversed(gaps))


def sedgewick_gaps(n: int) -> List[int]:
    """
    Sedgewick 間隔序列
    
    使用已知的 Sedgewick 序列值，這是已知最好的序列之一，
    時間複雜度約為 O(n^(4/3))。
    
    Args:
        n: 陣列大小
        
    Returns:
        間隔序列
    """
    # 已知的 Sedgewick 序列值
    known_gaps = [
        1, 8, 23, 77, 281, 1073, 4193, 16577, 65921, 262913,
        1050113, 4197377, 16783361, 67125249, 268468225, 1073790977
    ]
    
    gaps = [g for g in known_gaps if g < n]
    return list(reversed(gaps))


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


def benchmark(func: Callable, arr: List, *args, **kwargs) -> Tuple[List, float]:
    """基準測試"""
    start = time.perf_counter()
    result = func(arr, *args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def demo_basic():
    """基本希爾排序示範"""
    print("=" * 60)
    print("希爾排序基本示範")
    print("=" * 60)
    
    arr = [64, 34, 25, 12, 22, 11, 90, 45, 78, 33]
    print(f"\n原始陣列: {arr}")
    
    # 使用 Shell's 序列
    gaps = shell_gaps(len(arr))
    print(f"Shell 間隔序列: {gaps}")
    result = shell_sort_with_gaps(arr, gaps)
    print(f"排序結果: {result}")
    
    # 顯示排序過程
    print("\n排序過程（使用 Shell 序列）:")
    result = arr.copy()
    n = len(result)
    gap = n // 2
    step = 1
    while gap > 0:
        print(f"  間隔 {gap}: ", end="")
        for i in range(gap, n):
            temp = result[i]
            j = i
            while j >= gap and result[j - gap] > temp:
                result[j] = result[j - gap]
                j -= gap
            result[j] = temp
        print(f"{result}")
        gap //= 2
        step += 1


def demo_gap_comparison():
    """比較不同間隔序列的效能"""
    print("\n" + "=" * 60)
    print("不同間隔序列效能比較")
    print("=" * 60)
    
    # 準備測試資料
    sizes = [100, 500, 1000, 5000]
    
    gap_functions = [
        ("Shell's", shell_gaps),
        ("Hibbard's", hibbard_gaps),
        ("Knuth's", knuth_gaps),
        ("Sedgewick's", sedgewick_gaps),
    ]
    
    for size in sizes:
        print(f"\n資料量: {size}")
        print("-" * 50)
        print(f"{'間隔序列':15s} {'間隔序列內容':25s} {'時間 (ms)':10s}")
        print("-" * 50)
        
        # 生成測試資料
        random.seed(42)
        data = [random.randint(1, size * 10) for _ in range(size)]
        
        for name, gap_func in gap_functions:
            gaps = gap_func(size)
            gap_str = str(gaps[:5]) + ("..." if len(gaps) > 5 else "")
            _, elapsed = benchmark(shell_sort_with_gaps, data, gaps)
            print(f"{name:15s} {gap_str:25s} {elapsed * 1000:10.3f}")
        
        # 與插入排序比較
        _, t_insert = benchmark(insertion_sort, data)
        print(f"{'插入排序':15s} {'N/A':25s} {t_insert * 1000:10.3f}")


def demo_gap_impact():
    """展示間隔序列對排序的影響"""
    print("\n" + "=" * 60)
    print("間隔序列對排序的影響")
    print("=" * 60)
    
    arr = [random.randint(1, 1000) for _ in range(50)]
    
    gap_funcs = [
        ("Shell", shell_gaps),
        ("Hibbard", hibbard_gaps),
        ("Knuth", knuth_gaps),
    ]
    
    for name, func in gap_funcs:
        gaps = func(len(arr))
        print(f"\n{name} 間隔序列: {gaps}")
        print(f"間隔數量: {len(gaps)}")
        
        # 計算比較次數（簡化模擬）
        comparisons = 0
        n = len(arr)
        result = arr.copy()
        for gap in gaps:
            for i in range(gap, n):
                comparisons += 1
                temp = result[i]
                j = i
                while j >= gap and result[j - gap] > temp:
                    result[j] = result[j - gap]
                    j -= gap
                    comparisons += 1
                result[j] = temp
        print(f"近似比較次數: {comparisons}")


if __name__ == "__main__":
    demo_basic()
    demo_gap_comparison()
    demo_gap_impact()
