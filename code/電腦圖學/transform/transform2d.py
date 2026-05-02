"""2D 幾何變換 (2D Geometric Transformations)

使用齊次座標（Homogeneous Coordinates）和矩陣運算實作 2D 幾何變換。
包含平移、縮放、旋轉等基本變換，以及複合變換功能。
"""

from typing import List, Tuple
import math


def identity() -> List[List[float]]:
    """單位矩陣"""
    return [[1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]]


def translation(tx: float, ty: float) -> List[List[float]]:
    """平移矩陣
    
    Args:
        tx: x 方向平移量
        ty: y 方向平移量
    
    Returns:
        3x3 平移矩陣
    """
    return [[1.0, 0.0, tx],
            [0.0, 1.0, ty],
            [0.0, 0.0, 1.0]]


def scaling(sx: float, sy: float) -> List[List[float]]:
    """縮放矩陣
    
    Args:
        sx: x 方向縮放因子
        sy: y 方向縮放因子
    
    Returns:
        3x3 縮放矩陣
    """
    return [[sx, 0.0, 0.0],
            [0.0, sy, 0.0],
            [0.0, 0.0, 1.0]]


def rotation(angle_deg: float) -> List[List[float]]:
    """旋轉矩陣（逆時針）
    
    Args:
        angle_deg: 旋轉角度（度）
    
    Returns:
        3x3 旋轉矩陣
    """
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return [[cos_t, -sin_t, 0.0],
            [sin_t,  cos_t, 0.0],
            [0.0,   0.0,   1.0]]


def multiply(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """矩陣乘法 (3x3)"""
    result = [[0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += m1[i][k] * m2[k][j]
    return result


def transform_point(matrix: List[List[float]], point: Tuple[float, float]) -> Tuple[float, float]:
    """變換單個點
    
    Args:
        matrix: 變換矩陣 (3x3)
        point: 原始點 (x, y)
    
    Returns:
        變換後的點
    """
    x, y = point
    new_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
    new_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
    return (new_x, new_y)


def transform_points(matrix: List[List[float]], points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """變換多個點"""
    return [transform_point(matrix, p) for p in points]


def composite_transform(*matrices: List[List[float]]) -> List[List[float]]:
    """組合多個變換矩陣（從右到左應用）"""
    result = identity()
    for m in reversed(matrices):
        result = multiply(result, m)
    return result


if __name__ == "__main__":
    print("2D 幾何變換演示")
    print("=" * 40)
    
    # 原始三角形
    triangle = [(0, 0), (2, 0), (1, 2)]
    print(f"原始三角形: {triangle}")
    
    # 平移
    T = translation(3, 0)
    translated = transform_points(T, triangle)
    print(f"平移 (3, 0): {translated}")
    
    # 旋轉 90 度
    R = rotation(90)
    rotated = transform_points(R, triangle)
    print(f"旋轉 90 度: {rotated}")
    
    # 縮放
    S = scaling(2, 1.5)
    scaled = transform_points(S, triangle)
    print(f"縮放 (2, 1.5): {scaled}")
    
    # 複合變換：先旋轉 45 度，再平移 (2, 2)
    C = composite_transform(translation(2, 2), rotation(45))
    composite = transform_points(C, triangle)
    print(f"複合變換 (旋轉45°後平移(2,2)): {composite}")
