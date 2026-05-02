"""
凸包算法：Graham Scan

使用 Graham Scan 方法計算點集的凸包（Convex Hull）。
時間複雜度 O(n log n)，其中 n 為點的數量。
"""

from typing import List
import sys
from pathlib import Path

# 添加 basic 目錄到路徑以導入 Point
sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point, orientation, polar_angle


def graham_scan(points: List[Point]) -> List[Point]:
    """使用 Graham Scan 算法計算凸包
    
    Args:
        points: 輸入的點集
    
    Returns:
        凸包的頂點列表（按逆時針順序）
    """
    if len(points) < 3:
        return points.copy()
    
    # 1. 找到支點：y 最小，若相同則 x 最小
    pivot = min(points, key=lambda p: (p.y, p.x))
    
    # 2. 排序其他點按極角（相對於 pivot）
    other_points = [p for p in points if p != pivot]
    other_points.sort(key=lambda p: (polar_angle(pivot, p), p.x, p.y))
    
    # 移除共線的點（保留最遠的）
    filtered = []
    for p in other_points:
        if not filtered:
            filtered.append(p)
        else:
            # 若與前一個點共線，保留較遠的
            if orientation(pivot, filtered[-1], p) == 0:
                dist_prev = pivot.distance_to(filtered[-1])
                dist_curr = pivot.distance_to(p)
                if dist_curr > dist_prev:
                    filtered[-1] = p
            else:
                filtered.append(p)
    
    # 3. 初始化堆疊
    stack = [pivot, filtered[0], filtered[1]]
    
    # 4. 處理剩餘點
    for p in filtered[2:]:
        while len(stack) >= 2 and orientation(stack[-2], stack[-1], p) != 1:
            stack.pop()
        stack.append(p)
    
    return stack


if __name__ == "__main__":
    print("=== Graham Scan 凸包算法示範 ===\n")
    
    # 測試點集
    points = [
        Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 1),
        Point(2, 0), Point(1, 0), Point(0, 1), Point(3, 0)
    ]
    print(f"輸入點集: {[str(p) for p in points]}")
    
    hull = graham_scan(points)
    print(f"凸包頂點（逆時針）: {[str(p) for p in hull]}")
    
    # 另一個測試案例
    print("\n--- 另一個測試案例 ---")
    points2 = [
        Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4),
        Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)
    ]
    print(f"輸入點集: {[str(p) for p in points2]}")
    hull2 = graham_scan(points2)
    print(f"凸包頂點: {[str(p) for p in hull2]}")
    
    # 視覺化輸出（文字）
    print("\n--- 凸包視覺化（文字） ---")
    print("點集:")
    for y in range(5, -1, -1):
        line = ""
        for x in range(0, 5):
            pt = Point(x, y)
            if pt in points2:
                if pt in hull2:
                    line += "● "
                else:
                    line += "○ "
            else:
                line += "  "
        print(line)