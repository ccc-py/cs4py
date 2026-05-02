"""
凸包算法：Jarvis March（Gift Wrapping）

使用 Jarvis March 方法計算點集的凸包，也稱為 Gift Wrapping 算法。
時間複雜度 O(nh)，其中 h 是凸包頂點數，屬於輸出敏感算法。
"""

from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point, orientation


def jarvis_march(points: List[Point]) -> List[Point]:
    """使用 Jarvis March 算法計算凸包
    
    Args:
        points: 輸入的點集
    
    Returns:
        凸包的頂點列表（按逆時針順序）
    """
    if len(points) < 3:
        return points.copy()
    
    # 找到最左側的點作為起點
    hull = []
    leftmost = min(points, key=lambda p: p.x)
    current = leftmost
    hull.append(current)
    
    while True:
        # 選擇下一個點：與當前點連線，其他所有點都在右側
        next_point = None
        for candidate in points:
            if candidate == current:
                continue
            if next_point is None:
                next_point = candidate
            else:
                # 若 candidate 在 current->next_point 的右側，則更新
                if orientation(current, next_point, candidate) == -1:
                    next_point = candidate
                # 共線時保留較遠的
                elif orientation(current, next_point, candidate) == 0:
                    if current.distance_to(candidate) > current.distance_to(next_point):
                        next_point = candidate
        
        current = next_point
        # 回到起點則結束
        if current == leftmost:
            break
        hull.append(current)
    
    return hull


if __name__ == "__main__":
    print("=== Jarvis March（Gift Wrapping）凸包算法示範 ===\n")
    
    # 測試點集
    points = [
        Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 1),
        Point(2, 0), Point(1, 0), Point(0, 1), Point(3, 0)
    ]
    print(f"輸入點集: {[str(p) for p in points]}")
    
    hull = jarvis_march(points)
    print(f"凸包頂點（逆時針）: {[str(p) for p in hull]}")
    
    # 與 Graham Scan 比較
    print("\n--- 與 Graham Scan 比較 ---")
    from graham_scan import graham_scan
    hull_gs = graham_scan(points)
    print(f"Graham Scan 結果: {[str(p) for p in hull_gs]}")
    print(f"Jarvis March 結果: {[str(p) for p in hull]}")
    print(f"結果是否一致: {set((p.x, p.y) for p in hull_gs) == set((p.x, p.y) for p in hull)}")
    
    # 另一個測試案例
    print("\n--- 另一個測試案例 ---")
    points2 = [
        Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4),
        Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)
    ]
    print(f"輸入點集: {[str(p) for p in points2]}")
    hull2 = jarvis_march(points2)
    print(f"凸包頂點: {[str(p) for p in hull2]}")