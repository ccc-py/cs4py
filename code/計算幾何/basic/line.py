"""
線段相交檢測

實作線段相交的判斷與交點計算。
使用叉積（cross product）進行方向測試，判斷兩線段是否相交。
"""

from typing import Optional, Tuple
import sys
from pathlib import Path

# 添加當前目錄到路徑以導入 Point
sys.path.append(str(Path(__file__).parent))
from point import Point, orientation


def on_segment(p: Point, q: Point, r: Point) -> bool:
    """判斷點 q 是否線上段 pr 上（假設三點共線）
    
    Args:
        p: 線段端點
        q: 待檢查的點
        r: 線段另一端點
    
    Returns:
        q 是否線上段 pr 上
    """
    return (min(p.x, r.x) <= q.x <= max(p.x, r.x) and
            min(p.y, r.y) <= q.y <= max(p.y, r.y))


def segments_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """判斷兩線段 p1q1 與 p2q2 是否相交
    
    使用方向測試（orientation test）判斷線段相交。
    四種情況：
    1. 一般相交：兩線段的端點互相在對方兩側
    2. 特殊情況：共線且重疊
    3. 端點重合
    
    Args:
        p1, q1: 第一條線段的兩端點
        p2, q2: 第二條線段的兩端點
    
    Returns:
        是否相交
    """
    # 計算四個方向
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    # 一般情況：兩線段互相跨越對方
    if o1 != o2 and o3 != o4:
        return True
    
    # 特殊情況：共線
    # p2 在線段 p1q1 上
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    # q2 在線段 p1q1 上
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    # p1 在線段 p2q2 上
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    # q1 在線段 p2q2 上
    if o4 == 0 and on_segment(p2, q1, q2):
        return True
    
    return False


def line_intersection_point(p1: Point, q1: Point, p2: Point, q2: Point) -> Optional[Point]:
    """計算兩線段的交點（若有）
    
    使用參數式表示法求解：
    p1 + t(q1 - p1) = p2 + s(q2 - p2)
    
    Args:
        p1, q1: 第一條線段的兩端點
        p2, q2: 第二條線段的兩端點
    
    Returns:
        交點座標，若不相交則回傳 None
    """
    # 方向向量
    d1 = q1 - p1  # 第一條線段的方向向量
    d2 = q2 - p2  # 第二條線段的方向向量
    
    # 叉積
    cross = d1.cross(d2)
    
    # 平行或共線
    if abs(cross) < 1e-9:
        return None
    
    # 計算參數 t 和 s
    # p1 + t * d1 = p2 + s * d2
    # t * d1 - s * d2 = p2 - p1
    dp = p2 - p1
    
    t = dp.cross(d2) / cross
    s = dp.cross(d1) / cross
    
    # 檢查交點是否線上段上（參數在 [0, 1] 範圍內）
    # 若不檢查則為直線交點
    if 0 <= t <= 1 and 0 <= s <= 1:
        return Point(p1.x + t * d1.x, p1.y + t * d1.y)
    
    return None


def line_intersection(p1: Point, q1: Point, p2: Point, q2: Point) -> Optional[Point]:
    """計算兩「直線」的交點（非線段）
    
    Args:
        p1, q1: 第一條直線上的兩點
        p2, q2: 第二條直線上的兩點
    
    Returns:
        交點座標，若平行則回傳 None
    """
    d1 = q1 - p1
    d2 = q2 - p2
    
    cross = d1.cross(d2)
    
    if abs(cross) < 1e-9:
        return None
    
    dp = p2 - p1
    t = dp.cross(d2) / cross
    
    return Point(p1.x + t * d1.x, p1.y + t * d1.y)


if __name__ == "__main__":
    print("=== 線段相交檢測示範 ===\n")
    
    # 測試案例 1：一般相交
    print("測試 1：一般相交")
    p1, q1 = Point(1, 1), Point(4, 4)
    p2, q2 = Point(1, 4), Point(4, 1)
    print(f"線段 1: {p1} -> {q1}")
    print(f"線段 2: {p2} -> {q2}")
    print(f"是否相交: {segments_intersect(p1, q1, p2, q2)}")
    intersect = line_intersection_point(p1, q1, p2, q2)
    print(f"交點: {intersect}\n")
    
    # 測試案例 2：不相交
    print("測試 2：不相交")
    p1, q1 = Point(1, 1), Point(2, 2)
    p2, q2 = Point(3, 3), Point(4, 4)
    print(f"線段 1: {p1} -> {q1}")
    print(f"線段 2: {p2} -> {q2}")
    print(f"是否相交: {segments_intersect(p1, q1, p2, q2)}\n")
    
    # 測試案例 3：端點重合
    print("測試 3：端點重合")
    p1, q1 = Point(0, 0), Point(2, 2)
    p2, q2 = Point(2, 2), Point(3, 0)
    print(f"線段 1: {p1} -> {q1}")
    print(f"線段 2: {p2} -> {q2}")
    print(f"是否相交: {segments_intersect(p1, q1, p2, q2)}")
    intersect = line_intersection_point(p1, q1, p2, q2)
    print(f"交點: {intersect}\n")
    
    # 測試案例 4：T 型相交
    print("測試 4：T 型相交")
    p1, q1 = Point(0, 0), Point(4, 0)
    p2, q2 = Point(2, -1), Point(2, 1)
    print(f"線段 1: {p1} -> {q1}")
    print(f"線段 2: {p2} -> {q2}")
    print(f"是否相交: {segments_intersect(p1, q1, p2, q2)}")
    intersect = line_intersection_point(p1, q1, p2, q2)
    print(f"交點: {intersect}\n")
    
    # 測試案例 5：共線重疊
    print("測試 5：共線重疊")
    p1, q1 = Point(0, 0), Point(4, 0)
    p2, q2 = Point(2, 0), Point(6, 0)
    print(f"線段 1: {p1} -> {q1}")
    print(f"線段 2: {p2} -> {q2}")
    print(f"是否相交: {segments_intersect(p1, q1, p2, q2)}\n")
