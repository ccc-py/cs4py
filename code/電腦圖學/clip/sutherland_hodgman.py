"""Sutherland-Hodgman 多邊形裁剪演算法

使用多邊形裁剪（Sutherland-Hodgman）演算法，將多邊形裁剪於凸視窗內。
由 Sutherland 和 Hodgman 在 1974 年提出，是電腦圖學中多邊形裁剪的標準方法。
"""

from typing import List, Tuple


def clip_polygon_against_edge(polygon: List[Tuple[float, float]],
                              x0: float, y0: float, 
                              x1: float, y1: float,
                              is_inside_func) -> List[Tuple[float, float]]:
    """針對單一邊界裁剪多邊形
    
    Args:
        polygon: 輸入多邊形頂點列表
        x0, y0, x1, y1: 裁剪邊界的兩個端點
        is_inside_func: 判斷點是否在內部的函數
    
    Returns:
        裁剪後的多邊形
    """
    if not polygon:
        return []
    
    result = []
    n = len(polygon)
    
    for i in range(n):
        current = polygon[i]
        next_pt = polygon[(i + 1) % n]
        
        current_inside = is_inside_func(current, x0, y0, x1, y1)
        next_inside = is_inside_func(next_pt, x0, y0, x1, y1)
        
        if current_inside and next_inside:
            # 兩點都在內部：加入下一點
            result.append(next_pt)
        elif current_inside and not next_inside:
            # 從內到外：加入交點
            intersection = compute_intersection(current, next_pt, x0, y0, x1, y1)
            result.append(intersection)
        elif not current_inside and next_inside:
            # 從外到內：加入交點和下一點
            intersection = compute_intersection(current, next_pt, x0, y0, x1, y1)
            result.append(intersection)
            result.append(next_pt)
        # 兩點都在外：不加入任何點
    
    return result


def compute_intersection(p1: Tuple[float, float], p2: Tuple[float, float],
                         x0: float, y0: float, x1: float, y1: float) -> Tuple[float, float]:
    """計算線段 (p1-p2) 與 裁剪邊界 (x0,y0)-(x1,y1) 的交點"""
    # 使用參數式計算
    dx1 = p2[0] - p1[0]
    dy1 = p2[1] - p1[1]
    dx2 = x1 - x0
    dy2 = y1 - y0
    
    # 計算行列式
    det = dx1 * dy2 - dy1 * dx2
    
    if abs(det) < 1e-10:
        return p1  # 平行，返回 p1
    
    t = ((x0 - p1[0]) * dy2 - (y0 - p1[1]) * dx2) / det
    return (p1[0] + t * dx1, p1[1] + t * dy1)


def clip_polygon(polygon: List[Tuple[float, float]],
                 xmin: float, ymin: float, 
                 xmax: float, ymax: float) -> List[Tuple[float, float]]:
    """Sutherland-Hodgman 多邊形裁剪
    
    Args:
        polygon: 多邊形頂點列表
        xmin, ymin, xmax, ymax: 矩形裁剪視窗
    
    Returns:
        裁剪後的多邊形
    """
    result = polygon[:]
    
    # 定義四個邊界的內部判斷函數
    def is_inside_left(p, x0, y0, x1, y1):
        return p[0] >= xmin
    
    def is_inside_right(p, x0, y0, x1, y1):
        return p[0] <= xmax
    
    def is_inside_bottom(p, x0, y0, x1, y1):
        return p[1] >= ymin
    
    def is_inside_top(p, x0, y0, x1, y1):
        return p[1] <= ymax
    
    # 依序裁剪四個邊界
    result = clip_polygon_against_edge(result, xmin, ymin, xmin, ymax, is_inside_left)
    result = clip_polygon_against_edge(result, xmax, ymin, xmax, ymax, is_inside_right)
    result = clip_polygon_against_edge(result, xmin, ymin, xmax, ymin, is_inside_bottom)
    result = clip_polygon_against_edge(result, xmin, ymax, xmax, ymax, is_inside_top)
    
    return result


def draw_polygon_comparison(original: List[Tuple[float, float]], 
                           clipped: List[Tuple[float, float]],
                           xmin: float, ymin: float, 
                           xmax: float, ymax: float,
                           width: int = 20, height: int = 20) -> str:
    """繪製原多邊形和裁剪後的比較圖（ASCII）"""
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    # 繪製裁剪視窗
    for x in range(max(0, int(xmin)), min(width, int(xmax) + 1)):
        if 0 <= int(ymin) < height:
            grid[int(ymin)][x] = '#'
        if 0 <= int(ymax) < height:
            grid[int(ymax)][x] = '#'
    for y in range(max(0, int(ymin)), min(height, int(ymax) + 1)):
        if 0 <= int(xmin) < width:
            grid[y][int(xmin)] = '#'
        if 0 <= int(xmax) < width:
            grid[y][int(xmax)] = '#'
    
    # 繪製原多邊形（用 +）
    def draw_poly(poly, char):
        n = len(poly)
        for i in range(n):
            x0, y0 = int(poly[i][0]), int(poly[i][1])
            x1, y1 = int(poly[(i+1)%n][0]), int(poly[(i+1)%n][1])
            steps = int(max(abs(x1-x0), abs(y1-y0), 1))
            for t in range(steps + 1):
                x = int(x0 + (x1-x0) * t / steps)
                y = int(y0 + (y1-y0) * t / steps)
                if 0 <= x < width and 0 <= y < height:
                    grid[y][x] = char
    
    draw_poly(original, '+')
    draw_poly(clipped, '*')
    
    return '\n'.join([''.join(row) for row in grid])


if __name__ == "__main__":
    print("Sutherland-Hodgman 多邊形裁剪演算法演示")
    print("=" * 40)
    
    # 裁剪視窗
    xmin, ymin, xmax, ymax = 5, 5, 15, 15
    print(f"裁剪視窗: ({xmin}, {ymin}) 到 ({xmax}, {ymax})")
    
    # 測試多邊形（一個五角形，部分在視窗外）
    polygon = [(10, 2), (18, 8), (15, 18), (5, 18), (2, 8)]
    print(f"原始多邊形: {polygon}")
    
    clipped = clip_polygon(polygon, xmin, ymin, xmax, ymax)
    print(f"裁剪後多邊形: {clipped}")
    
    print("\nASCII 視覺化:")
    print("+ = 原始多邊形, * = 裁剪後, # = 裁剪視窗")
    print(draw_polygon_comparison(polygon, clipped, xmin, ymin, xmax, ymax))
