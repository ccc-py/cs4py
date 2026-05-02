"""Z-Buffer 隱面消除演算法 (Z-Buffer Hidden Surface Removal)

使用深度緩衝區（Z-Buffer）來決定哪些像素可見，處理重疊三角形的可見性問題。
這是現代 GPU 管線中標準的隱面消除方法。
"""

from typing import List, Tuple, Dict
import struct


class Triangle:
    """三角形類別"""
    def __init__(self, v0: Tuple[float, float, float], 
                 v1: Tuple[float, float, float],
                 v2: Tuple[float, float, float],
                 color: Tuple[int, int, int]):
        self.vertices = [v0, v1, v2]
        self.color = color  # RGB 0-255


def compute_bounding_box(tri: Triangle, width: int, height: int) -> Tuple[int, int, int, int]:
    """計算三角形的包圍盒"""
    xs = [v[0] for v in tri.vertices]
    ys = [v[1] for v in tri.vertices]
    min_x = max(0, int(min(xs)))
    max_x = min(width - 1, int(max(xs)))
    min_y = max(0, int(min(ys)))
    max_y = min(height - 1, int(max(ys)))
    return min_x, min_y, max_x, max_y


def barycentric(v0: Tuple[float, float], v1: Tuple[float, float], v2: Tuple[float, float],
                p: Tuple[float, float]) -> Tuple[float, float, float]:
    """計算重心座標"""
    # 計算分母
    denom = (v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1])
    if abs(denom) < 1e-10:
        return (-1, -1, -1)
    
    # 計算重心座標
    w0 = ((v1[1] - v2[1]) * (p[0] - v2[0]) + (v2[0] - v1[0]) * (p[1] - v2[1])) / denom
    w1 = ((v2[1] - v0[1]) * (p[0] - v2[0]) + (v0[0] - v2[0]) * (p[1] - v2[1])) / denom
    w2 = 1.0 - w0 - w1
    
    return (w0, w1, w2)


def rasterize_triangle(tri: Triangle, width: int, height: int, 
                       z_buffer: List[List[float]]) -> Dict[Tuple[int, int], Tuple[int, int, int]]:
    """光柵化三角形並更新 Z-Buffer
    
    Returns:
        像素顏色字典
    """
    pixels = {}
    min_x, min_y, max_x, max_y = compute_bounding_box(tri, width, height)
    
    v0, v1, v2 = tri.vertices
    
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # 計算重心座標
            w0, w1, w2 = barycentric((v0[0], v0[1]), (v1[0], v1[1]), (v2[0], v2[1]), (x + 0.5, y + 0.5))
            
            # 檢查是否在三角形內
            if w0 < 0 or w1 < 0 or w2 < 0:
                continue
            
            # 插值計算 z 值
            z = w0 * v0[2] + w1 * v1[2] + w2 * v2[2]
            
            # Z-Buffer 測試
            if z < z_buffer[y][x]:
                z_buffer[y][x] = z
                pixels[(x, y)] = tri.color
    
    return pixels


def render_with_z_buffer(triangles: List[Triangle], width: int, height: int) -> str:
    """使用 Z-Buffer 渲染場景，輸出 PPM"""
    # 初始化 Z-Buffer（無限遠）
    z_buffer = [[float('inf')] * width for _ in range(height)]
    pixels = {}
    
    # 處理所有三角形
    for tri in triangles:
        tri_pixels = rasterize_triangle(tri, width, height, z_buffer)
        pixels.update(tri_pixels)
    
    # 生成 PPM
    lines = [f"P3\n# Z-Buffer Rendering\n{width} {height}\n255"]
    for y in range(height):
        for x in range(width):
            if (x, y) in pixels:
                r, g, b = pixels[(x, y)]
                lines.append(f"{r} {g} {b}")
            else:
                lines.append("0 0 0")  # 背景黑色
    
    return '\n'.join(lines)


if __name__ == "__main__":
    print("Z-Buffer 隱面消除演示")
    print("=" * 40)
    
    # 定義三個重疊的三角形（不同深度）
    triangles = [
        # 遠處的紅色三角形（z 較大）
        Triangle(
            [(50, 20, 10), (200, 20, 10), (125, 180, 10)],
            (255, 0, 0)
        ),
        # 中間的綠色三角形
        Triangle(
            [(80, 40, 5), (220, 40, 5), (150, 200, 5)],
            (0, 255, 0)
        ),
        # 近處的藍色三角形（z 較小，應該遮擋其他）
        Triangle(
            [(110, 60, 1), (240, 60, 1), (175, 220, 1)],
            (0, 0, 255)
        ),
    ]
    
    print("渲染三個重疊三角形...")
    print("- 紅色三角形: z=10 (最遠)")
    print("- 綠色三角形: z=5 (中間)")
    print("- 藍色三角形: z=1 (最近，應該可見)")
    
    ppm = render_with_z_buffer(triangles, 300, 250)
    
    with open("/Users/Shared/ccc/project/cs4py/code/電腦圖學/render/zbuffer_output.ppm", "w") as f:
        f.write(ppm)
    print("\n已儲存至 render/zbuffer_output.ppm")
    print("藍色三角形應該遮擋其他三角形")
