"""
掃描線算法：線段相交檢測

實作 Bentley-Ottmann 算法的簡化概念，使用掃描線（sweep line）
和事件佇列（event queue）來檢測線段相交。
"""

from typing import List, Tuple, Set, Dict
import sys
from pathlib import Path
import heapq

sys.path.append(str(Path(__file__).parent.parent / 'basic'))
from point import Point
from line import segments_intersect


class SweepLine:
    """掃描線狀態管理"""
    
    def __init__(self):
        self.status = []  # 當前掃描線穿過的線段（按交叉點 y 排序）
    
    def add_segment(self, seg: Tuple[Point, Point]):
        """加入線段到狀態中"""
        self.status.append(seg)
    
    def remove_segment(self, seg: Tuple[Point, Point]):
        """從狀態中移除線段"""
        if seg in self.status:
            self.status.remove(seg)
    
    def get_neighbors(self, seg: Tuple[Point, Point]) -> Tuple:
        """取得線段在狀態中的相鄰線段"""
        idx = self.status.index(seg) if seg in self.status else -1
        if idx == -1:
            return None, None
        prev_seg = self.status[idx - 1] if idx > 0 else None
        next_seg = self.status[idx + 1] if idx < len(self.status) - 1 else None
        return prev_seg, next_seg


def line_sweep_intersections(segments: List[Tuple[Point, Point]]) -> Set[Tuple[Point, Point, Point, Point]]:
    """使用掃描線算法找出所有相交的線段對
    
    Args:
        segments: 線段列表，每個線段為 (p1, p2)
    
    Returns:
        相交線段對的集合
    """
    # 事件佇列（按 x 座標排序）
    events = []
    for i, (p1, p2) in enumerate(segments):
        # 確保 p1.x <= p2.x
        if p1.x > p2.x or (p1.x == p2.x and p1.y > p2.y):
            p1, p2 = p2, p1
        events.append((p1.x, p1.y, 'start', i, p1, p2))
        events.append((p2.x, p2.y, 'end', i, p1, p2))
    
    # 按 x 座標排序事件
    events.sort(key=lambda e: (e[0], e[1]))
    
    sweep = SweepLine()
    intersections = set()
    active = {}  # 索引 -> 線段
    
    for event in events:
        x, y, typ, idx, p1, p2 = event
        
        if typ == 'start':
            # 加入線段
            seg = (p1, p2)
            active[idx] = seg
            sweep.add_segment(seg)
            
            # 檢查與相鄰線段是否相交
            prev_seg, next_seg = sweep.get_neighbors(seg)
            if prev_seg and segments_intersect(prev_seg[0], prev_seg[1], p1, p2):
                intersections.add(tuple(sorted([(prev_seg[0], prev_seg[1]), (p1, p2)], key=lambda s: (s[0].x, s[0].y))))
            if next_seg and segments_intersect(next_seg[0], next_seg[1], p1, p2):
                intersections.add(tuple(sorted([(next_seg[0], next_seg[1]), (p1, p2)], key=lambda s: (s[0].x, s[0].y))))
        
        elif typ == 'end':
            # 移除線段
            seg = active.get(idx)
            if seg:
                prev_seg, next_seg = sweep.get_neighbors(seg)
                if prev_seg and next_seg:
                    if segments_intersect(prev_seg[0], prev_seg[1], next_seg[0], next_seg[1]):
                        intersections.add(tuple(sorted([(prev_seg[0], prev_seg[1]), (next_seg[0], next_seg[1])], key=lambda s: (s[0].x, s[0].y))))
                sweep.remove_segment(seg)
                del active[idx]
    
    return intersections


if __name__ == "__main__":
    print("=== 掃描線算法：線段相交檢測示範 ===\n")
    
    # 測試案例
    segments = [
        (Point(1, 1), Point(4, 4)),  # 對角線 1
        (Point(1, 4), Point(4, 1)),  # 對角線 2
        (Point(0, 2), Point(5, 2)),  # 水平線
        (Point(2, 0), Point(2, 5)),  # 垂直線
    ]
    
    print("線段:")
    for i, (p1, p2) in enumerate(segments):
        print(f"  S{i}: {p1} -> {p2}")
    
    intersections = line_sweep_intersections(segments)
    print(f"\n相交線段對: {len(intersections)} 對")
    for pair in intersections:
        s1, s2 = pair
        print(f"  {s1[0]}->{s1[1]} 與 {s2[0]}->{s2[1]} 相交")