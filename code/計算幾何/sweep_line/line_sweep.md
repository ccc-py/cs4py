# Sweep Line - 掃描線算法

## 歷史背景

掃描線（Sweep Line）是一種強大的幾何算法技術，由 Jon Bentley 和 Thomas Ottmann 在 1979 年提出 Bentley-Ottmann 算法，用於在 O((n+k) log n) 時間內檢測 n 條線段的 k 個交點。

## 核心原理

### 基本概念
想像一條垂直（或水平）的線從左到右掃過平面，追蹤當前掃描線穿過的幾何物件。

### 事件驅動
- **事件佇列**：按 x 座標排序的點（線段起點、終點、交點）。
- **掃描線狀態**：維護當前掃描線穿過的線段（按 y 順序排列）。

### 處理流程
1. 將所有線段的起點和終點加入事件佇列。
2. 處理每個事件：
   - **起點事件**：加入線段到狀態，檢查與相鄰線段是否相交。
   - **終點事件**：移除線段，檢查其鄰居是否相交。

### 時間複雜度
O((n+k) log n)，其中 n 為線段數，k 為交點數。

## 使用範例

```python
from point import Point
from line_sweep import line_sweep_intersections

segments = [(Point(1,1), Point(4,4)), (Point(1,4), Point(4,1))]
result = line_sweep_intersections(segments)
print(len(result))  # 1
```

## 參考資料

- [Bentley–Ottmann algorithm - Wikipedia](https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm)
- [Line Segment Intersection - GeeksforGeeks](https://www.geeksforgeeks.org/given-a-set-of-line-segments-find-if-any-two-segments-intersect/)
- de Berg, M., et al. (2008). *Computational Geometry: Algorithms and Applications*.