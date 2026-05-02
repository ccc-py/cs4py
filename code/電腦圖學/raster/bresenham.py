"""布雷森漢姆直線演算法 (Bresenham's Line Algorithm)

使用整數運算在像素網格上繪製直線，避免浮點數計算，效率極高。
由 Jack Bresenham 於 1962 年在 IBM 開發，用於繪圖機和早期顯示器。
"""

from typing import List, Tuple


def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """計算從 (x0, y0) 到 (x1, y1) 的布雷森漢姆直線像素點
    
    Args:
        x0: 起點 x 座標
        y0: 起點 y 座標
        x1: 終點 x 座標
        y1: 終點 y 座標
    
    Returns:
        像素點列表，每個點為 (x, y) 元組
    """
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points


def draw_ascii_grid(points: List[Tuple[int, int]], width: int = 20, height: int = 20) -> str:
    """將像素點繪製到 ASCII 網格
    
    Args:
        points: 像素點列表
        width: 網格寬度
        height: 網格高度
    
    Returns:
        ASCII 網格字串
    """
    grid = [['.' for _ in range(width)] for _ in range(height)]
    point_set = set(points)
    for y in range(height):
        for x in range(width):
            if (x, y) in point_set:
                grid[y][x] = '#'
    return '\n'.join([''.join(row) for row in grid])


if __name__ == "__main__":
    # 演示 1: 繪製對角線
    print("布雷森漢姆直線演算法演示")
    print("=" * 40)
    line1 = bresenham_line(2, 2, 18, 18)
    print("對角線 (2,2) → (18,18):")
    print(draw_ascii_grid(line1))
    
    # 演示 2: 繪製水平線
    print("\n水平線 (5,10) → (15,10):")
    line2 = bresenham_line(5, 10, 15, 10)
    print(draw_ascii_grid(line2))
    
    # 演示 3: 繪製陡峭線
    print("\n陡峭線 (10,2) → (12,18):")
    line3 = bresenham_line(10, 2, 12, 18)
    print(draw_ascii_grid(line3))
