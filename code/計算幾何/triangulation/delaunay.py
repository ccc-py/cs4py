"""
Delaunay 三角化

使用 Bowyer-Watson 增量算法實作 Delaunay 三角化。
Delaunay 三角化的性質：任意三角形的外接圓不包含其他點。
"""

from typing import List, Tuple, Set, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point, orientation, distance_squared


def circumcircle_contains(p: Point, a: Point, b: Point, c: Point) -> bool:
    """判斷點 p 是否在三角形 abc 的外接圓內部
    
    使用 4x4 行列式方法：
    若行列式 > 0，則點在外接圓內部（對於逆時針頂點順序）。
    
    Args:
        p: 待檢查的點
        a, b, c: 三角形三個頂點
    
    Returns:
        點是否在外接圓內部（不含邊界）
    """
    # 計算行列式
    # | ax ay ax²+ay² 1 |
    # | bx by bx²+by² 1 |
    # | cx cy cx²+cy² 1 |
    # | px py px²+py² 1 |
    
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y
    px, py = p.x, p.y
    
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    p2 = px * px + py * py
    
    # 展開行列式
    det = (ax * by * c2 * 1 + ay * b2 * cx * 1 + a2 * bx * cy * 1 + 1 * by * cx * p2 +
           ax * b2 * cy * 1 + ay * bx * c2 * 1 + a2 * by * cx * 1 + 1 * bx * cy * p2 +
           ax * b2 * cy * 1 + ay * bx * c2 * 1 + a2 * by * cx * 1 + 1 * bx * cy * p2) - \
          (1 * by * c2 * ax + b2 * cy * ax * 1 + c2 * py * a2 * 1 + p2 * cy * ax * 1 +
           1 * b2 * cy * ax + by * c2 * ax * 1 + c2 * py * a2 * 1 + p2 * cy * ax * 1 +
           1 * b2 * cy * ax + by * c2 * ax * 1 + c2 * py * a2 * 1 + p2 * cy * ax * 1)
    
    # 簡化：使用更簡單的判斷方法
    # 計算外接圓圓心和半徑
    # 使用線性方程求解
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9:
        return False  # 共線，不是三角形
    
    ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
    uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d
    
    center = Point(ux, uy)
    r2 = center.distance_to(a) ** 2
    p_dist2 = center.distance_to(p) ** 2
    
    return p_dist2 < r2


def bowyer_watson(points: List[Point]) -> Set[Tuple[Point, Point, Point]]:
    """使用 Bowyer-Watson 算法進行 Delaunay 三角化
    
    Args:
        points: 輸入點集
    
    Returns:
        Delaunay 三角形集合
    """
    if len(points) < 3:
        return set()
    
    # 超級三角形（包含所有點）
    max_coord = max(max(abs(p.x), abs(p.y)) for p in points) * 3
    super_tri = (
        Point(-max_coord, -max_coord),
        Point(max_coord * 2, -max_coord),
        Point(-max_coord, max_coord * 2)
    )
    
    triangulation = {super_tri}
    
    # 增量加入每個點
    for p in points:
        bad_triangles = set()
        
        # 找出所有外接圓包含 p 的三角形
        for tri in triangulation:
            if circumcircle_contains(p, tri[0], tri[1], tri[2]):
                bad_triangles.add(tri)
        
        # 找出邊界多邊形（被多個良三角形共用的邊）
        edge_count = {}
        for tri in bad_triangles:
            edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
            for e in edges:
                # 規範化邊（確保方向一致以利比較）
                norm_e = tuple(sorted(e, key=lambda pt: (pt.x, pt.y)))
                edge_count[norm_e] = edge_count.get(norm_e, 0) + 1
        
        # 移除不良三角形
        triangulation -= bad_triangles
        
        # 加入以 p 為頂點的新三角形
        for edge, count in edge_count.items():
            if count == 1:  # 邊界邊
                p1, p2 = edge
                triangulation.add((p1, p2, p))
    
    # 移除包含超級三角形頂點的三角形
    triangulation = {tri for tri in triangulation 
                    if not any(p in tri for p in super_tri)}
    
    return triangulation


def delaunay_triangulation(points: List[Point]) -> List[Tuple[Point, Point, Point]]:
    """Delaunay 三角化（包裝函數）
    
    Args:
        points: 輸入點集
    
    Returns:
        三角形列表
    """
    result = bowyer_watson(points)
    return list(result)


if __name__ == "__main__":
    print("=== Delaunay 三角化示範（Bowyer-Watson 算法）===\n")
    
    # 測試點集
    points = [
        Point(0, 0), Point(2, 0), Point(1, 1),
        Point(0, 2), Point(2, 2), Point(1, 3)
    ]
    print(f"輸入點集: {[str(p) for p in points]}")
    
    triangles = delaunay_triangulation(points)
    print(f"\nDelaunay 三角形（共 {len(triangles)} 個）:")
    for i, (a, b, c) in enumerate(triangles):
        print(f"  三角形 {i+1}: {a}, {b}, {c}")
    
    # 檢查外接圓性質
    print("\n--- 外接圓檢查 ---")
    for tri in triangles:
        a, b, c = tri
        print(f"三角形 {a}, {b}, {c}:")
        for p in points:
            if p not in (a, b, c):
                if circumcircle_contains(p, a, b, c):
                    print(f"  警告: 點 {p} 在外接圓內部！")