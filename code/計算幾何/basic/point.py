"""
計算幾何基礎：點與向量運算

提供 Point 類別，支援二維點的基本運算，包括向量操作、方向測試等。
此模組是其他計算幾何演算法的基礎。
"""

from typing import Tuple
import math


class Point:
    """二維點類別，支援向量運算與幾何測試"""
    
    def __init__(self, x: float, y: float) -> None:
        """初始化點座標
        
        Args:
            x: x 座標
            y: y 座標
        """
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Point') -> 'Point':
        """向量加法"""
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        """向量減法"""
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Point':
        """向量數乘"""
        return Point(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other: object) -> bool:
        """判斷兩點是否相等"""
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9
    
    def __hash__(self) -> int:
        """計算點的雜湊值（用於集合操作）"""
        return hash((round(self.x, 9), round(self.y, 9)))
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def dot(self, other: 'Point') -> float:
        """計算點積（內積）
        
        Args:
            other: 另一個點（視為向量）
        
        Returns:
            點積值
        """
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Point') -> float:
        """計算叉積（外積）
        
        二維叉積結果為純量，表示有向面積的 2 倍。
        
        Args:
            other: 另一個點（視為向量）
        
        Returns:
            叉積值（正表示逆時針，負表示順時針）
        """
        return self.x * other.y - self.y * other.x
    
    def distance_to(self, other: 'Point') -> float:
        """計算兩點間的歐氏距離
        
        Args:
            other: 另一個點
        
        Returns:
            距離值
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def norm_squared(self) -> float:
        """計算向量長度的平方
        
        Returns:
            向量長度的平方
        """
        return self.x * self.x + self.y * self.y
    
    def norm(self) -> float:
        """計算向量長度
        
        Returns:
            向量長度
        """
        return math.sqrt(self.norm_squared())


def orientation(p: Point, q: Point, r: Point) -> int:
    """判斷三個點的順序方向
    
    使用叉積判斷點 p, q, r 的相對方向。
    
    Args:
        p: 第一個點
        q: 第二個點
        r: 第三個點
    
    Returns:
        1: 逆時針方向 (CCW)
        -1: 順時針方向 (CW)
        0: 共線 (collinear)
    """
    cross_product = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
    
    if abs(cross_product) < 1e-9:
        return 0  # 共線
    elif cross_product > 0:
        return 1  # 逆時針
    else:
        return -1  # 順時針


def collinear(p: Point, q: Point, r: Point) -> bool:
    """判斷三個點是否共線
    
    Args:
        p, q, r: 三個點
    
    Returns:
        是否共線
    """
    return orientation(p, q, r) == 0


def ccw(p: Point, q: Point, r: Point) -> bool:
    """判斷三個點是否為逆時針方向
    
    Args:
        p, q, r: 三個點
    
    Returns:
        是否為逆時針方向
    """
    return orientation(p, q, r) == 1


def cw(p: Point, q: Point, r: Point) -> bool:
    """判斷三個點是否為順時針方向
    
    Args:
        p, q, r: 三個點
    
    Returns:
        是否為順時針方向
    """
    return orientation(p, q, r) == -1


def polar_angle(p: Point, q: Point) -> float:
    """計算從 p 到 q 的極角（相對於 x 軸）
    
    Args:
        p: 參考點
        q: 目標點
    
    Returns:
        極角（弧度），範圍 [-π, π]
    """
    return math.atan2(q.y - p.y, q.x - p.x)


def distance_squared(p: Point, q: Point) -> float:
    """計算兩點間距離的平方
    
    Args:
        p, q: 兩個點
    
    Returns:
        距離平方
    """
    dx = p.x - q.x
    dy = p.y - q.y
    return dx * dx + dy * dy


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


if __name__ == "__main__":
    # 示範使用
    print("=== 點與向量運算示範 ===\n")
    
    # 建立點
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    p3 = Point(1, 2)
    
    print(f"點 p1: {p1}")
    print(f"點 p2: {p2}")
    print(f"點 p3: {p3}\n")
    
    # 向量加法
    p4 = p1 + p3
    print(f"向量加法 p1 + p3 = {p4}")
    
    # 向量減法
    diff = p2 - p1
    print(f"向量減法 p2 - p1 = {diff}")
    
    # 點積
    dot_result = p2.dot(p3)
    print(f"點積 p2 · p3 = {dot_result}")
    
    # 叉積
    cross_result = p2.cross(p3)
    print(f"叉積 p2 × p3 = {cross_result}")
    
    # 距離
    dist = p1.distance_to(p2)
    print(f"p1 到 p2 的距離 = {dist}")
    
    # 方向測試
    print("\n=== 方向測試 ===")
    a = Point(0, 0)
    b = Point(4, 0)
    c = Point(4, 3)
    d = Point(2, 2)
    
    print(f"點 A: {a}, B: {b}, C: {c}, D: {d}")
    print(f"orientation(A, B, C) = {orientation(a, b, c)} (1=CCW, -1=CW, 0=共線)")
    print(f"orientation(A, B, D) = {orientation(a, b, d)}")
    
    # 共線測試
    e = Point(2, 0)
    print(f"\n點 E: {e}")
    print(f"collinear(A, B, E) = {collinear(a, b, e)}")
    
    # 極角計算
    print("\n=== 極角計算 ===")
    origin = Point(0, 0)
    angles = [
        Point(1, 0),   # 0 度
        Point(0, 1),   # 90 度
        Point(-1, 0),  # 180 度
        Point(0, -1),  # -90 度
    ]
    
    for pt in angles:
        angle = polar_angle(origin, pt)
        print(f"極角({origin} -> {pt}) = {angle:.4f} 弧度 = {math.degrees(angle):.1f} 度")
