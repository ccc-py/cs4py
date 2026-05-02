"""3D 幾何變換與投影 (3D Transformations and Projection)

實作 3D 空間中的幾何變換、正交投影和透視投影。
包含視錐（View Frustum）概念和完整的 3D 管線矩陣運算。
"""

from typing import List, Tuple
import math


def identity_4x4() -> List[List[float]]:
    """4x4 單位矩陣"""
    return [[1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def multiply_4x4(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """4x4 矩陣乘法"""
    result = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += m1[i][k] * m2[k][j]
    return result


def translation_3d(tx: float, ty: float, tz: float) -> List[List[float]]:
    """3D 平移矩陣"""
    return [[1.0, 0.0, 0.0, tx],
            [0.0, 1.0, 0.0, ty],
            [0.0, 0.0, 1.0, tz],
            [0.0, 0.0, 0.0, 1.0]]


def scaling_3d(sx: float, sy: float, sz: float) -> List[List[float]]:
    """3D 縮放矩陣"""
    return [[sx, 0.0, 0.0, 0.0],
            [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotation_x(angle_deg: float) -> List[List[float]]:
    """繞 X 軸旋轉"""
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)
    return [[1.0, 0.0, 0.0, 0.0],
            [0.0,  c,  -s, 0.0],
            [0.0,  s,   c, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotation_y(angle_deg: float) -> List[List[float]]:
    """繞 Y 軸旋轉"""
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)
    return [[ c, 0.0,  s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0,  c, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotation_z(angle_deg: float) -> List[List[float]]:
    """繞 Z 軸旋轉"""
    theta = math.radians(angle_deg)
    c, s = math.cos(theta), math.sin(theta)
    return [[ c,  -s, 0.0, 0.0],
            [ s,   c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def orthographic_projection(left: float, right: float, 
                            bottom: float, top: float,
                            near: float, far: float) -> List[List[float]]:
    """正交投影矩陣
    
    將視錐映射至標準化裝置座標 (NDC) [-1, 1]
    """
    return [[2/(right-left), 0.0, 0.0, -(right+left)/(right-left)],
            [0.0, 2/(top-bottom), 0.0, -(top+bottom)/(top-bottom)],
            [0.0, 0.0, -2/(far-near), -(far+near)/(far-near)],
            [0.0, 0.0, 0.0, 1.0]]


def perspective_projection(fov_y: float, aspect: float, 
                           near: float, far: float) -> List[List[float]]:
    """透視投影矩陣（視野角度版本）
    
    Args:
        fov_y: 垂直視野角度（度）
        aspect: 寬高比 (width/height)
        near: 近平面距離
        far: 遠平面距離
    """
    fov_rad = math.radians(fov_y)
    f = 1.0 / math.tan(fov_rad / 2)
    return [[f/aspect, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, (far+near)/(near-far), (2*far*near)/(near-far)],
            [0.0, 0.0, -1.0, 0.0]]


def transform_point_3d(matrix: List[List[float]], point: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """變換 3D 點"""
    x, y, z = point
    w = matrix[3][0]*x + matrix[3][1]*y + matrix[3][2]*z + matrix[3][3]
    new_x = (matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]*z + matrix[0][3]) / w
    new_y = (matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]*z + matrix[1][3]) / w
    new_z = (matrix[2][0]*x + matrix[2][1]*y + matrix[2][2]*z + matrix[2][3]) / w
    return (new_x, new_y, new_z)


def project_to_2d(point_3d: Tuple[float, float, float], 
                 width: int, height: int) -> Tuple[int, int]:
    """將 3D 點投影到 2D 螢幕座標
    
    假設點已經在 NDC 空間 [-1, 1]
    """
    x, y, _ = point_3d
    screen_x = int((x + 1) / 2 * width)
    screen_y = int((1 - y) / 2 * height)  # 翻轉 y 軸
    return (screen_x, screen_y)


if __name__ == "__main__":
    print("3D 變換與投影演示")
    print("=" * 40)
    
    # 定義一個立方體（8 個頂點）
    cube = [
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
    ]
    print(f"原始立方體頂點:")
    for v in cube:
        print(f"  {v}")
    
    # 應用變換：旋轉 + 平移
    M = multiply_4x4(
        translation_3d(0, 0, 5),  # 遠離相機
        rotation_y(30)
    )
    
    transformed = [transform_point_3d(M, v) for v in cube]
    print(f"\n變換後頂點:")
    for v in transformed:
        print(f"  {v}")
    
    # 透視投影
    P = perspective_projection(fov_y=60, aspect=1.0, near=0.1, far=100.0)
    projected = [transform_point_3d(P, v) for v in transformed]
    
    print(f"\n透視投影後 (NDC):")
    for v in projected:
        print(f"  {v}")
    
    # 投影到 2D 螢幕
    screen_points = [project_to_2d(v, 40, 40) for v in projected]
    print(f"\n螢幕座標:")
    for p in screen_points:
        print(f"  {p}")
