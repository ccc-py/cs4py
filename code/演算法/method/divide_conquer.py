"""
分治法 (Divide and Conquer)
實作經典的分治演算法：最近點對、二分搜尋
"""

from typing import List, Tuple, Optional
import math


def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    迭代版二分搜尋
    
    Args:
        arr: 已排序的陣列（升序）
        target: 目標值
        
    Returns:
        目標值的索引，沒找到則返回 -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(arr: List[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
    """
    遞迴版二分搜尋
    
    Args:
        arr: 已排序的陣列（升序）
        target: 目標值
        left: 搜尋範圍左邊界
        right: 搜尋範圍右邊界
        
    Returns:
        目標值的索引，沒找到則返回 -1
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def closest_pair(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """
    最近點對問題 - 使用分治法，O(n log n)
    
    Args:
        points: 二維點的列表 [(x1, y1), (x2, y2), ...]
        
    Returns:
        (點1, 點2, 最小距離)
    """
    # 按 x 座標排序
    points_sorted_x = sorted(points, key=lambda p: p[0])
    
    def dist(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """計算兩點間歐氏距離"""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    def brute_force(pairs: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
        """暴力法求最近點對（點數少時使用）"""
        min_dist = float('inf')
        pair = (pairs[0], pairs[1])
        
        n = len(pairs)
        for i in range(n):
            for j in range(i + 1, n):
                d = dist(pairs[i], pairs[j])
                if d < min_dist:
                    min_dist = d
                    pair = (pairs[i], pairs[j])
        
        return pair[0], pair[1], min_dist
    
    def closest_pair_recursive(px: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
        """遞迴求解最近點對"""
        n = len(px)
        
        # 基準情況：點數 ≤ 3 時使用暴力法
        if n <= 3:
            return brute_force(px)
        
        # 分治：分成左右兩半
        mid = n // 2
        left_points = px[:mid]
        right_points = px[mid:]
        
        # 遞迴求解左右兩邊
        (p1_l, p2_l, d1) = closest_pair_recursive(left_points)
        (p1_r, p2_r, d2) = closest_pair_recursive(right_points)
        
        # 取較小者
        if d1 < d2:
            min_dist = d1
            best_pair = (p1_l, p2_l)
        else:
            min_dist = d2
            best_pair = (p1_r, p2_r)
        
        # 檢查跨過中線的點對
        mid_x = px[mid][0]
        
        # 找出距中線 ± min_dist 範圍內的點
        strip = [p for p in px if abs(p[0] - mid_x) < min_dist]
        
        # 按 y 座標排序
        strip.sort(key=lambda p: p[1])
        
        # 檢查 strip 中的點對（只需檢查 y 相差 < min_dist 的點）
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= min_dist:
                    break
                d = dist(strip[i], strip[j])
                if d < min_dist:
                    min_dist = d
                    best_pair = (strip[i], strip[j])
        
        return best_pair[0], best_pair[1], min_dist
    
    return closest_pair_recursive(points_sorted_x)


def power(x: float, n: int) -> float:
    """
    快速冪 - 分治思想計算 x^n
    
    Args:
        x: 底數
        n: 指數（非負整數）
        
    Returns:
        x^n 的值
    """
    if n == 0:
        return 1.0
    if n < 0:
        return 1.0 / power(x, -n)
    
    # 分治：x^n = (x^(n/2))^2（若 n 偶數）或 x * x^(n-1)（若 n 奇數）
    if n % 2 == 0:
        half = power(x, n // 2)
        return half * half
    else:
        return x * power(x, n - 1)


if __name__ == "__main__":
    # 測試二分搜尋
    print("=== 二分搜尋 ===")
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    targets = [7, 1, 15, 8]
    
    print(f"陣列: {arr}")
    for target in targets:
        idx1 = binary_search_iterative(arr, target)
        idx2 = binary_search_recursive(arr, target)
        print(f"搜尋 {target}: 迭代版索引={idx1}, 遞迴版索引={idx2}")
    
    # 測試最近點對
    print("\n=== 最近點對問題 ===")
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print(f"點集合: {points}")
    p1, p2, dist = closest_pair(points)
    print(f"最近點對: {p1} 和 {p2}")
    print(f"距離: {dist:.4f}")
    
    # 測試快速冪
    print("\n=== 快速冪 ===")
    test_cases = [(2, 10), (3, 5), (5, 0), (2, -3)]
    for x, n in test_cases:
        result = power(x, n)
        print(f"{x}^{n} = {result}")
