"""
多邊形三角化：Ear Clipping 算法

使用 Ear Clipping（耳尖裁剪）方法將簡單多邊形分解為三角形。
時間複雜度 O(n²)，其中 n 為多邊形頂點數。
"""

from typing import List, Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point, orientation

# 用於調試
import os
# print("Current file:", __file__)
# print("Parent parent:", Path(__file__).parent.parent / 'basic')


def is_convex(p1: Point, p2: Point, p3: Point) -> bool:
    """判斷由三個點構成的角是否為凸角
    
    Args:
        p1, p2, p3: 三個點（p2 為頂點）
    
    Returns:
        是否為凸角（逆時針轉向，即 orientation == 1）
    """
    return orientation(p1, p2, p3) == 1


def ensure_ccw(polygon: List[Point]) -> List[Point]:
    """確保多邊形頂點為逆時針順序
    
    Args:
        polygon: 多邊形頂點列表
    
    Returns:
        逆時針順序的頂點列表
    """
    # 計算有符號面積
    n = len(polygon)
    if n < 3:
        return polygon.copy()
    
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i].x * polygon[j].y
        area -= polygon[j].x * polygon[i].y
    
    # 若面積為負，則為順時針，需要反轉
    if area < 0:
        return polygon[::-1]
    return polygon.copy()


def point_in_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    """判斷點 p 是否在三角形 abc 內部
    
    Args:
        p: 待檢查的點
        a, b, c: 三角形三個頂點
    
    Returns:
        點是否在三角形內部（不含邊界）
    """
    # 使用重心座標或方向測試
    d1 = orientation(p, a, b)
    d2 = orientation(p, b, c)
    d3 = orientation(p, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)


def is_ear(polygon: List[Point], i: int) -> bool:
    """判斷頂點 i 是否為 ear（耳尖）
    
    Ear 的定義：頂點 i 與其相鄰頂點構成的三角形內部不包含其他頂點。
    
    Args:
        polygon: 多邊形頂點列表
        i: 待檢查的頂點索引
    
    Returns:
        是否為 ear
    """
    n = len(polygon)
    prev_idx = (i - 1) % n
    next_idx = (i + 1) % n
    
    p1 = polygon[prev_idx]
    p2 = polygon[i]
    p3 = polygon[next_idx]
    
    # 若不是凸角，則不是 ear
    if not is_convex(p1, p2, p3):
        return False
    
    # 檢查是否有其他頂點在三角形內部
    for j in range(n):
        if j == i or j == prev_idx or j == next_idx:
            continue
        if point_in_triangle(polygon[j], p1, p2, p3):
            return False
    
    return True


def ear_clipping_triangulation(polygon: List[Point]) -> List[Tuple[Point, Point, Point]]:
    """使用 Ear Clipping 算法進行多邊形三角化
    
    Args:
        polygon: 簡單多邊形頂點列表（逆時針順序）
    
    Returns:
        三角形列表，每個三角形為 (p1, p2, p3)
    """
    if len(polygon) < 3:
        return []
    
    # 複製一份可修改的列表，並確保逆時針順序
    vertices = ensure_ccw(polygon)
    triangles = []
    n = len(vertices)
    
    while n > 3:
        # 找到一個 ear
        ear_found = False
        for i in range(n):
            if is_ear(vertices, i):
                # 找到 ear，裁剪之
                prev_idx = (i - 1) % n
                next_idx = (i + 1) % n
                
                # 記錄三角形
                triangles.append((vertices[prev_idx], vertices[i], vertices[next_idx]))
                
                # 移除頂點 i
                vertices.pop(i)
                n -= 1
                ear_found = True
                break
        
        if not ear_found:
            # 理論上不應發生（簡單多邊形必有 ear）
            break
    
    # 剩餘三個點構成一個三角形
    if n == 3:
        triangles.append((vertices[0], vertices[1], vertices[2]))
    
    return triangles


if __name__ == "__main__":
    print("=== Ear Clipping 三角化示範 ===\n")
    
    # 正方形三角化
    square = [Point(0, 0), Point(0, 4), Point(4, 4), Point(4, 0)]
    print(f"正方形: {[str(p) for p in square]}")
    triangles = ear_clipping_triangulation(square)
    print("三角化結果:")
    for i, tri in enumerate(triangles):
        print(f"  三角形 {i+1}: {tri[0]}, {tri[1]}, {tri[2]}")
    
    # 五邊形
    print("\n--- 五邊形 ---")
    pentagon = [Point(0, 0), Point(2, 0), Point(3, 2), Point(1, 4), Point(-1, 2)]
    print(f"五邊形: {[str(p) for p in pentagon]}")
    triangles2 = ear_clipping_triangulation(pentagon)
    print(f"產生 {len(triangles2)} 個三角形:")
    for i, tri in enumerate(triangles2):
        print(f"  三角形 {i+1}: {tri[0]}, {tri[1]}, {tri[2]}")