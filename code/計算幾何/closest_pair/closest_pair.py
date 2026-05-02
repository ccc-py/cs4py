"""
最近點對算法（Closest Pair of Points）

使用分治法（divide and conquer）找出平面上距離最近的兩個點。
時間複雜度 O(n log n)，優於暴力法的 O(n²)。
"""

from typing import List, Tuple, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point


def dist(p1: Point, p2: Point) -> float:
    """計算兩點間的歐氏距離
    
    Args:
        p1, p2: 兩個點
    
    Returns:
        距離值
    """
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def brute_force_closest_pair(points: List[Point]) -> Tuple[Point, Point, float]:
    """暴力法找出最近點對
    
    Args:
        points: 點集（至少包含 2 個點）
    
    Returns:
        (點1, 點2, 最小距離平方)
    """
    min_dist = float('inf')
    p1, p2 = points[0], points[1]
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if d < min_dist:
                min_dist = d
                p1, p2 = points[i], points[j]
    
    return p1, p2, min_dist


def closest_pair(points: List[Point]) -> Tuple[Optional[Point], Optional[Point], float]:
    """使用分治法找出最近點對
    
    Args:
        points: 點集
    
    Returns:
        (點1, 點2, 最小距離)
    """
    if len(points) < 2:
        return None, None, float('inf')
    
    if len(points) <= 3:
        p1, p2, d2 = brute_force_closest_pair(points)
        return p1, p2, d2 ** 0.5
    
    # 按 x 座標排序
    points_sorted = sorted(points, key=lambda p: p.x)
    
    mid = len(points_sorted) // 2
    mid_point = points_sorted[mid]
    
    # 遞迴處理左右兩半
    left = points_sorted[:mid]
    right = points_sorted[mid:]
    
    p1_left, p2_left, d_left = closest_pair(left)
    p1_right, p2_right, d_right = closest_pair(right)
    
    # 取較小距離
    if d_left < d_right:
        best_p1, best_p2, d = p1_left, p2_left, d_left
    else:
        best_p1, best_p2, d = p1_right, p2_right, d_right
    
    # 檢查跨越中線的點對
    strip = [p for p in points_sorted if abs(p.x - mid_point.x) < d]
    strip.sort(key=lambda p: p.y)
    
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j].y - strip[i].y) >= d:
                break
            d2 = dist(strip[i], strip[j])
            if d2 < d * d:
                d = d2 ** 0.5
                best_p1, best_p2 = strip[i], strip[j]
    
    return best_p1, best_p2, d


if __name__ == "__main__":
    print("=== 最近點對算法示範 ===\n")
    
    # 測試點集
    points = [
        Point(2, 3), Point(12, 30), Point(40, 50),
        Point(5, 1), Point(12, 10), Point(3, 4)
    ]
    print(f"輸入點集: {[str(p) for p in points]}")
    
    p1, p2, d = closest_pair(points)
    print(f"最近點對: {p1} 和 {p2}")
    print(f"距離: {d:.4f}")
    
    # 與暴力法比較
    print("\n--- 與暴力法比較 ---")
    bp1, bp2, bd = brute_force_closest_pair(points)
    print(f"分治法: {p1}, {p2}, 距離={d:.4f}")
    print(f"暴力法: {bp1}, {bp2}, 距離={bd**0.5:.4f}")
    
    # 另一個測試案例
    print("\n--- 另一個測試案例 ---")
    points2 = [
        Point(0, 0), Point(1, 1), Point(2, 2),
        Point(3, 3), Point(1, 0), Point(0, 1)
    ]
    p1_2, p2_2, d_2 = closest_pair(points2)
    print(f"最近點對: {p1_2} 和 {p2_2}")
    print(f"距離: {d_2:.4f}")