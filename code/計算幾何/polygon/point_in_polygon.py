"""
點在多边形內部檢測

實作 Ray Casting（射線法）和 Winding Number（環繞數）算法，
判斷點是否在多邊形內部、外部或邊界上。
"""

from typing import List, Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point, orientation, on_segment

# 也可以從 line 模組導入（若需要其他功能）
# from line import segments_intersect


def point_on_boundary(point: Point, polygon: List[Point]) -> bool:
    """檢查點是否在多邊形邊界上
    
    Args:
        point: 待檢查的點
        polygon: 多邊形頂點列表（順時針或逆時針）
    
    Returns:
        點是否在邊界上
    """
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        if on_segment(p1, point, p2):
            return True
    return False


def ray_casting(point: Point, polygon: List[Point]) -> bool:
    """使用射線法判斷點是否在多邊形內部
    
    從點向右發射水平射線，計算與多邊形邊的交點數。
    若交點數為奇數，則點在內部；否則在外部。
    
    Args:
        point: 待檢查的點
        polygon: 多邊形頂點列表
    
    Returns:
        點是否在多邊形內部
    """
    n = len(polygon)
    inside = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        # 檢查射線是否與邊相交
        # 射線：從 point 向右的水平線
        if ((p1.y > point.y) != (p2.y > point.y)) and \
           (point.x < (p2.x - p1.x) * (point.y - p1.y) / (p2.y - p1.y) + p1.x):
            inside = not inside
    
    return inside


def winding_number(point: Point, polygon: List[Point]) -> int:
    """計算環繞數（Winding Number）
    
    環繞數表示多邊形圍繞點的圈數。
    若環繞數不為 0，則點在內部。
    
    Args:
        point: 待檢查的點
        polygon: 多邊形頂點列表
    
    Returns:
        環繞數
    """
    n = len(polygon)
    wn = 0
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        
        if p1.y <= point.y:
            if p2.y > point.y and orientation(p1, p2, point) == 1:
                wn += 1
        else:
            if p2.y <= point.y and orientation(p1, p2, point) == -1:
                wn -= 1
    
    return wn


def point_in_polygon(point: Point, polygon: List[Point], method: str = 'ray') -> str:
    """綜合判斷點與多邊形的關係
    
    Args:
        point: 待檢查的點
        polygon: 多邊形頂點列表
        method: 使用方法 'ray' 或 'winding'
    
    Returns:
        'inside', 'outside', 或 'boundary'
    """
    if point_on_boundary(point, polygon):
        return 'boundary'
    
    if method == 'ray':
        inside = ray_casting(point, polygon)
    else:
        inside = winding_number(point, polygon) != 0
    
    return 'inside' if inside else 'outside'


if __name__ == "__main__":
    print("=== 點在多邊形內部檢測示範 ===\n")
    
    # 定義一個正方形
    square = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
    print(f"多邊形（正方形）: {[str(p) for p in square]}")
    
    # 測試點
    test_points = [
        Point(2, 2),  # 內部
        Point(5, 5),  # 外部
        Point(0, 0),  # 頂點
        Point(2, 0),  # 邊上
        Point(4, 2),  # 邊上
    ]
    
    for pt in test_points:
        result = point_in_polygon(pt, square, 'ray')
        in_ray = ray_casting(pt, square)
        wn = winding_number(pt, square)
        print(f"點 {pt}: {result}, ray={in_ray}, winding_number={wn}")
    
    # 測試複雜多邊形（星形）
    print("\n--- 星形多邊形 ---")
    star = [Point(0, 0), Point(3, 4), Point(6, 0), Point(1, 3), Point(5, 3)]
    print(f"多邊形: {[str(p) for p in star]}")
    
    test_pt = Point(3, 2)
    result_ray = point_in_polygon(test_pt, star, 'ray')
    result_wind = point_in_polygon(test_pt, star, 'winding')
    print(f"點 {test_pt}: ray={result_ray}, winding={result_wind}")