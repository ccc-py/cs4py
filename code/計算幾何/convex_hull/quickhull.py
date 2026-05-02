"""
凸包算法：QuickHull

使用 QuickHull 方法計算點集的凸包。
採用分治法（divide and conquer）策略，平均時間複雜度 O(n log n)。
"""

from typing import List, Set
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point, orientation


def quickhull(points: List[Point]) -> List[Point]:
    """使用 QuickHull 算法計算凸包
    
    Args:
        points: 輸入的點集
    
    Returns:
        凸包的頂點列表
    """
    if len(points) < 3:
        return points.copy()
    
    hull: Set[Point] = set()
    
    # 找到最左和最右的點
    min_x_point = min(points, key=lambda p: p.x)
    max_x_point = max(points, key=lambda p: p.x)
    
    # 處理上凸包（點在線段左側）
    hull.add(min_x_point)
    hull.add(max_x_point)
    
    # 上凸包：在 min_x -> max_x 左側的點
    upper = [p for p in points if p != min_x_point and p != max_x_point and orientation(min_x_point, max_x_point, p) == 1]
    _quickhull(min_x_point, max_x_point, upper, hull)
    
    # 下凸包：在 min_x -> max_x 右側的點
    lower = [p for p in points if p != min_x_point and p != max_x_point and orientation(min_x_point, max_x_point, p) == -1]
    _quickhull(max_x_point, min_x_point, lower, hull)
    
    return list(hull)


def _quickhull(p1: Point, p2: Point, points: List[Point], hull: Set[Point]):
    """遞迴處理一側的凸包
    
    Args:
        p1, p2: 當前考慮的線段端點
        points: 候選點集（都在線段同一側）
        hull: 凸包集合（會被修改）
    """
    if not points:
        return
    
    # 找到距離線段最遠的點
    farthest = None
    max_dist = -1
    for p in points:
        dist = abs(orientation(p1, p2, p))
        if dist > max_dist:
            max_dist = dist
            farthest = p
    
    if farthest is None:
        return
    
    hull.add(farthest)
    
    # 遞迴處理：只傳遞在子線段左側的點
    # 左側：在 p1->farthest 左側的點
    left_points = [p for p in points if p != farthest and orientation(p1, farthest, p) == 1]
    _quickhull(p1, farthest, left_points, hull)
    
    # 右側：在 farthest->p2 左側的點
    right_points = [p for p in points if p != farthest and orientation(farthest, p2, p) == 1]
    _quickhull(farthest, p2, right_points, hull)


if __name__ == "__main__":
    print("=== QuickHull 凸包算法示範 ===\n")
    
    # 測試點集
    points = [
        Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 1),
        Point(2, 0), Point(1, 0), Point(0, 1), Point(3, 0)
    ]
    print(f"輸入點集: {[str(p) for p in points]}")
    
    hull = quickhull(points)
    print(f"凸包頂點: {[str(p) for p in hull]}")
    
    # 與其他方法比較
    print("\n--- 與其他算法比較 ---")
    from graham_scan import graham_scan
    from jarvis_march import jarvis_march
    
    hull_gs = graham_scan(points)
    hull_jm = jarvis_march(points)
    
    print(f"Graham Scan: {[str(p) for p in hull_gs]}")
    print(f"Jarvis March: {[str(p) for p in hull_jm]}")
    print(f"QuickHull: {[str(p) for p in hull]}")
    
    # 檢查結果一致性
    set_gs = set((p.x, p.y) for p in hull_gs)
    set_jm = set((p.x, p.y) for p in hull_jm)
    set_qh = set((p.x, p.y) for p in hull)
    print(f"三種方法結果一致: {set_gs == set_jm == set_qh}")
    
    # 另一個測試案例
    print("\n--- 另一個測試案例 ---")
    points2 = [
        Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4),
        Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)
    ]
    hull2 = quickhull(points2)
    print(f"凸包頂點: {[str(p) for p in hull2]}")
