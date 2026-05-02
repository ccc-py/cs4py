"""Cohen-Sutherland 直線裁剪演算法

使用 Outcode 位元編碼來快速判斷線段與裁剪視窗的關係。
由 Danny Cohen 和 Ivan Sutherland 在 1960 年代後期開發。
"""

from typing import Tuple, Optional


# Outcode 位元定義
TOP = 1     # 1000
BOTTOM = 2  # 0100
RIGHT = 4   # 0010
LEFT = 8    # 0001


def compute_outcode(x: float, y: float, 
                    xmin: float, ymin: float, 
                    xmax: float, ymax: float) -> int:
    """計算點的 Outcode
    
    Args:
        x, y: 點座標
        xmin, ymin, xmax, ymax: 裁剪視窗邊界
    
    Returns:
        4 位元 Outcode（TOP, BOTTOM, RIGHT, LEFT）
    """
    code = 0
    if y > ymax:
        code |= TOP
    elif y < ymin:
        code |= BOTTOM
    if x > xmax:
        code |= RIGHT
    elif x < xmin:
        code |= LEFT
    return code


def cohen_sutherland_clip(x0: float, y0: float, x1: float, y1: float,
                          xmin: float, ymin: float, 
                          xmax: float, ymax: float) -> Optional[Tuple[float, float, float, float]]:
    """Cohen-Sutherland 直線裁剪
    
    Args:
        x0, y0: 線段起點
        x1, y1: 線段終點
        xmin, ymin, xmax, ymax: 裁剪視窗
    
    Returns:
        裁剪後的線段 (x0, y0, x1, y1)，如果在視窗外則返回 None
    """
    outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    accept = False
    
    while True:
        if not (outcode0 | outcode1):  # 完全在內部
            accept = True
            break
        elif outcode0 & outcode1:  # 完全在外部（同側）
            break
        else:
            # 部分在內部，需要裁剪
            outcode_out = outcode0 if outcode0 else outcode1
            x, y = 0.0, 0.0
            
            # 計算與邊界的交點
            if outcode_out & TOP:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif outcode_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif outcode_out & RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                x = xmax
            elif outcode_out & LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                x = xmin
            
            # 更新端點
            if outcode_out == outcode0:
                x0, y0 = x, y
                outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
            else:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    
    if accept:
        return (x0, y0, x1, y1)
    else:
        return None


def draw_scene(lines: list, clipped_lines: list, 
               xmin: float, ymin: float, xmax: float, ymax: float,
               width: int = 20, height: int = 20) -> str:
    """繪製場景（ASCII）"""
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
    
    # 繪製原始線段（用 +）
    for (x0, y0, x1, y1) in lines:
        # 簡單繪製（僅示意）
        steps = int(max(abs(x1-x0), abs(y1-y0), 1))
        for i in range(steps + 1):
            t = i / steps
            x = int(x0 + (x1-x0) * t)
            y = int(y0 + (y1-y0) * t)
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = '+'
    
    # 繪製裁剪後線段（用 *）
    for (x0, y0, x1, y1) in clipped_lines:
        if (x0, y0, x1, y1) == (None,):
            continue
        steps = int(max(abs(x1-x0), abs(y1-y0), 1))
        for i in range(steps + 1):
            t = i / steps
            x = int(x0 + (x1-x0) * t)
            y = int(y0 + (y1-y0) * t)
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = '*'
    
    return '\n'.join([''.join(row) for row in grid])


if __name__ == "__main__":
    print("Cohen-Sutherland 直線裁剪演算法演示")
    print("=" * 40)
    
    # 裁剪視窗
    xmin, ymin, xmax, ymax = 5, 5, 15, 15
    print(f"裁剪視窗: ({xmin}, {ymin}) 到 ({xmax}, {ymax})")
    
    # 測試線段
    test_lines = [
        (2, 2, 18, 18),    # 對角線穿過
        (10, 2, 10, 18),   # 垂直穿過
        (2, 10, 18, 10),   # 水平穿過
        (1, 1, 3, 3),      # 完全在外
        (8, 8, 12, 12),    # 完全在內
    ]
    
    clipped = []
    for line in test_lines:
        result = cohen_sutherland_clip(*line, xmin, ymin, xmax, ymax)
        clipped.append(result if result else (None,))
        status = "在內部" if result else "在外部"
        print(f"線段 {line[:2]}→{line[2:]}: {status}")
    
    print("\nASCII 視覺化:")
    print("+ = 原始線段, * = 裁剪後, # = 裁剪視窗")
    print(draw_scene(test_lines, 
                     [r for r in clipped if r != (None,)],
                     xmin, ymin, xmax, ymax))
