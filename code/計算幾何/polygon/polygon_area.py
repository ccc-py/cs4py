"""
多邊形面積計算

使用 Shoelace Formula（鞋帶公式，又稱 Surveyor's Formula）
計算簡單多邊形的面積，並可判斷頂點順序（順時針或逆時針）。
"""

from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point


def polygon_area(polygon: List[Point]) -> float:
    """使用鞋帶公式計算多邊形面積（無符號）
    
    Shoelace Formula:
    Area = 0.5 * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|
    
    Args:
        polygon: 多邊形頂點列表（順時針或逆時針）
    
    Returns:
        多邊形面積（正值）
    """
    n = len(polygon)
    if n < 3:
        return 0.0
    
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i].x * polygon[j].y
        area -= polygon[j].x * polygon[i].y
    
    return abs(area) / 2.0


def signed_polygon_area(polygon: List[Point]) -> float:
    """計算有符號的多邊形面積
    
    若頂點為逆時針順序，面積為正；
    若為順時針順序，面積為負。
    
    Args:
        polygon: 多邊形頂點列表
    
    Returns:
        有符號面積
    """
    n = len(polygon)
    if n < 3:
        return 0.0
    
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i].x * polygon[j].y
        area -= polygon[j].x * polygon[i].y
    
    return area / 2.0


def polygon_orientation(polygon: List[Point]) -> str:
    """判斷多邊形的頂點順序
    
    Args:
        polygon: 多邊形頂點列表
    
    Returns:
        'ccw'（逆時針）、'cw'（順時針）或 'collinear'（共線）
    """
    area = signed_polygon_area(polygon)
    if abs(area) < 1e-9:
        return 'collinear'
    elif area > 0:
        return 'ccw'
    else:
        return 'cw'


if __name__ == "__main__":
    print("=== 多邊形面積計算示範 ===\n")
    
    # 正方形（逆時針）
    square_ccw = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]
    print(f"正方形（逆時針）: {[str(p) for p in square_ccw]}")
    print(f"面積: {polygon_area(square_ccw)}")
    print(f"有符號面積: {signed_polygon_area(square_ccw)}")
    print(f"頂點順序: {polygon_orientation(square_ccw)}")
    
    # 正方形（順時針）
    square_cw = [Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)]
    print(f"\n正方形（順時針）: {[str(p) for p in square_cw]}")
    print(f"面積: {polygon_area(square_cw)}")
    print(f"有符號面積: {signed_polygon_area(square_cw)}")
    print(f"頂點順序: {polygon_orientation(square_cw)}")
    
    # 三角形
    print("\n--- 三角形 ---")
    triangle = [Point(0, 0), Point(3, 0), Point(0, 4)]
    print(f"三角形: {[str(p) for p in triangle]}")
    print(f"面積: {polygon_area(triangle)}")
    print(f"頂點順序: {polygon_orientation(triangle)}")
    
    # 不規則多邊形
    print("\n--- 不規則多邊形 ---")
    polygon = [Point(0, 0), Point(2, 0), Point(3, 1), Point(2, 3), Point(0, 2)]
    print(f"多邊形: {[str(p) for p in polygon]}")
    print(f"面積: {polygon_area(polygon)}")
    print(f"頂點順序: {polygon_orientation(polygon)}")