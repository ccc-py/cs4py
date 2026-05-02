"""Xiaolin Wu 反鋸齒直線演算法

使用強度混合繪製平滑直線，減少鋸齒效果。
由 Xiaolin Wu 於 1991 年提出，是反鋸齒技術的經典演算法。
"""

from typing import List, Tuple


def _draw_pixel(grid: dict, x: int, y: int, intensity: float, max_x: int, max_y: int):
    """在網格中繪製帶強度的像素"""
    if 0 <= x < max_x and 0 <= y < max_y:
        grid[(x, y)] = max(grid.get((x, y), 0.0), intensity)


def wu_line(x0: float, y0: float, x1: float, y1: float, 
            width: int = 20, height: int = 20) -> dict:
    """Xiaolin Wu 反鋸齒直線演算法
    
    Args:
        x0, y0: 起點座標（可為浮點數）
        x1, y1: 終點座標（可為浮點數）
        width: 畫布寬度
        height: 畫布高度
    
    Returns:
        像素強度字典 {(x, y): intensity}
    """
    grid = {}
    steep = abs(y1 - y0) > abs(x1 - x0)
    
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    
    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1.0
    
    # 起始點
    x_end = round(x0)
    y_end = y0 + gradient * (x_end - x0)
    x_start = x_end
    y_start = y_end
    
    # 結束點
    x_end = round(x1)
    y_end = y1 + gradient * (x_end - x1)
    x_end = x_end  # 包含終點
    
    intery = y_start
    for x in range(x_start, min(int(x_end) + 1, width)):
        y_base = int(intery)
        frac = intery - y_base
        
        if steep:
            _draw_pixel(grid, y_base, x, 1.0 - frac, width, height)
            _draw_pixel(grid, y_base + 1, x, frac, width, height)
        else:
            _draw_pixel(grid, x, y_base, 1.0 - frac, width, height)
            _draw_pixel(grid, x, y_base + 1, frac, width, height)
        
        intery += gradient
    
    return grid


def draw_ascii_aa(grid: dict, width: int = 20, height: int = 20) -> str:
    """將反鋸齒線繪製為 ASCII 藝術，使用不同字元表示強度"""
    chars = ' .:;+=xX$#'
    lines = []
    for y in range(height):
        line = ''
        for x in range(width):
            intensity = grid.get((x, y), 0.0)
            idx = min(int(intensity * (len(chars) - 1)), len(chars) - 1)
            line += chars[idx]
        lines.append(line)
    return '\n'.join(lines)


if __name__ == "__main__":
    print("Xiaolin Wu 反鋸齒直線演算法演示")
    print("=" * 40)
    
    # 演示 1: 斜線
    print("反鋸齒斜線 (2,2) → (18,18):")
    grid1 = wu_line(2.0, 2.0, 18.0, 18.0, width=21, height=21)
    print(draw_ascii_aa(grid1, width=21, height=21))
    
    # 演示 2: 與 Bresenham 比較
    print("\n比較：")
    print("Bresenham (鋸齒):")
    from raster.bresenham import bresenham_line, draw_ascii_grid
    line = bresenham_line(2, 2, 18, 18)
    print(draw_ascii_grid(line, width=21, height=21))
    
    print("\nWu 反鋸齒 (平滑):")
    grid2 = wu_line(2.0, 2.0, 18.0, 18.0, width=21, height=21)
    print(draw_ascii_aa(grid2, width=21, height=21))
