"""中點畫圓演算法 (Midpoint Circle Algorithm)

使用整數運算繪製圓，利用八分對稱性只需要計算 1/8 圓弧。
由 Bresenham 改進自原始的圓繪製演算法，廣泛應用於電腦圖學中。
"""

from typing import List, Tuple


def midpoint_circle(cx: int, cy: int, r: int) -> List[Tuple[int, int]]:
    """計算圓的像素點（中點演算法）
    
    Args:
        cx: 圓心 x 座標
        cy: 圓心 y 座標
        r: 半徑
    
    Returns:
        圓的所有像素點列表
    """
    points = []
    x = 0
    y = r
    d = 1 - r  # 決策參數
    
    def add_eight_points(x: int, y: int):
        """利用八分對稱性加入八個點"""
        points.extend([
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ])
    
    while x <= y:
        add_eight_points(x, y)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    
    return points


def draw_ascii_circle(points: List[Tuple[int, int]], cx: int, cy: int, r: int) -> str:
    """將圓繪製到 ASCII 網格
    
    Args:
        points: 圓的像素點列表
        cx: 圓心 x 座標
        cy: 圓心 y 座標
        r: 半徑
    
    Returns:
        ASCII 網格字串
    """
    size = r * 2 + 3
    grid = [['.' for _ in range(size)] for _ in range(size)]
    point_set = set(points)
    for y in range(size):
        for x in range(size):
            if (x, y) in point_set:
                grid[y][x] = '#'
    return '\n'.join([''.join(row) for row in grid])


if __name__ == "__main__":
    print("中點畫圓演算法演示")
    print("=" * 40)
    
    # 演示 1: 半徑 5 的圓
    print("圓心 (10, 10), 半徑 5:")
    points1 = midpoint_circle(10, 10, 5)
    print(draw_ascii_circle(points1, 10, 10, 5))
    print(f"總像素點數: {len(set(points1))}")
    
    # 演示 2: 半徑 3 的圓
    print("\n圓心 (5, 5), 半徑 3:")
    points2 = midpoint_circle(5, 5, 3)
    print(draw_ascii_circle(points2, 5, 5, 3))
