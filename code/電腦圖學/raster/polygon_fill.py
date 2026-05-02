"""掃描線多邊形填充演算法 (Scan-line Polygon Fill Algorithm)

使用掃描線方法填充多邊形，利用邊表（Edge Table）和活躍邊表（Active Edge Table）。
這是電腦圖學中經典的多邊形填充方法，效率高且易於實作。
"""

from typing import List, Tuple, Dict, Set
import bisect


class Edge:
    """邊資訊類別"""
    def __init__(self, y_max: int, x: float, dx: float, dy: float):
        self.y_max = y_max
        self.x = x  # 當前交點的 x 座標
        self.dx = dx  # 1/m 斜率倒數
        self.dy = dy
    
    def __lt__(self, other):
        return self.x < other.x


def build_edge_table(vertices: List[Tuple[int, int]]) -> Dict[int, List[Edge]]:
    """建立邊表（Edge Table）
    
    Args:
        vertices: 多邊形頂點列表，按順序排列
    
    Returns:
        邊表，key 為掃描線 y 值
    """
    et: Dict[int, List[Edge]] = {}
    n = len(vertices)
    
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        
        # 忽略水平邊
        if y0 == y1:
            continue
        
        # 確保 y0 < y1（從下往上）
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = x1 - x0
        dy = y1 - y0
        slope_inv = dx / dy if dy != 0 else 0
        
        edge = Edge(y1, float(x0), slope_inv, dy)
        if y0 not in et:
            et[y0] = []
        et[y0].append(edge)
    
    return et


def scanline_fill(vertices: List[Tuple[int, int]], width: int, height: int) -> Set[Tuple[int, int]]:
    """掃描線填充多邊形
    
    Args:
        vertices: 多邊形頂點列表
        width: 畫布寬度
        height: 畫布高度
    
    Returns:
        填充的像素點集合
    """
    filled = set()
    et = build_edge_table(vertices)
    aet: List[Edge] = []  # 活躍邊表
    
    # 找出 y 範圍
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    
    for y in range(min_y, max_y + 1):
        # 將新邊加入 AET
        if y in et:
            for edge in et[y]:
                bisect.insort(aet, edge)
        
        # 移除已完成的邊
        aet = [e for e in aet if e.y_max > y]
        
        # 配對交點並填充
        for i in range(0, len(aet) - 1, 2):
            x_start = int(aet[i].x)
            x_end = int(aet[i + 1].x)
            for x in range(max(0, x_start), min(width, x_end + 1)):
                filled.add((x, y))
        
        # 更新 AET 中的 x 值
        for edge in aet:
            edge.x += edge.dx
    
    return filled


def draw_ascii_polygon(filled: Set[Tuple[int, int]], vertices: List[Tuple[int, int]], 
                       width: int = 20, height: int = 20) -> str:
    """將填充的多邊形繪製到 ASCII 網格"""
    grid = [['.' for _ in range(width)] for _ in range(height)]
    vertex_set = set(vertices)
    
    for y in range(height):
        for x in range(width):
            if (x, y) in vertex_set:
                grid[y][x] = 'V'
            elif (x, y) in filled:
                grid[y][x] = '#'
    
    return '\n'.join([''.join(row) for row in grid])


if __name__ == "__main__":
    print("掃描線多邊形填充演算法演示")
    print("=" * 40)
    
    # 演示: 三角形
    triangle = [(5, 5), (15, 5), (10, 15)]
    print("三角形填充:")
    filled = scanline_fill(triangle, 20, 20)
    print(draw_ascii_polygon(filled, triangle))
    
    # 演示: 四邊形
    print("\n四邊形填充:")
    quad = [(5, 5), (15, 5), (15, 15), (5, 15)]
    filled = scanline_fill(quad, 20, 20)
    print(draw_ascii_polygon(filled, quad))
    
    # 演示: 五角形
    print("\n不規則多邊形填充:")
    polygon = [(10, 2), (18, 8), (15, 18), (5, 18), (2, 8)]
    filled = scanline_fill(polygon, 20, 20)
    print(draw_ascii_polygon(filled, polygon))
