# Line Segment Intersection - 線段相交檢測

## 歷史背景

線段相交檢測是計算幾何中最基礎的問題之一，廣泛應用於電腦圖學（如光線追蹤、碰撞檢測）、地理資訊系統（GIS）和機器人路徑規劃等領域。

早期的演算法直接求解線性方程組，但現代方法多使用叉積（cross product）進行方向測試，這種方法更穩健且易於實作。

## 核心原理

### 方向測試（Orientation Test）

給定三個點 p, q, r，計算叉積：

```
orientation = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
```

### 線段相交判斷

兩線段 p1q1 與 p2q2 相交的條件：

1. **一般情況**：兩線段的端點互相在對方的兩側
   - orientation(p1, q1, p2) ≠ orientation(p1, q1, q2)
   - orientation(p2, q2, p1) ≠ orientation(p2, q2, q1)

2. **特殊情況**：共線且重疊
   - 某端點落在另一線段上（使用 `on_segment` 檢查）

### 交點計算

使用參數式表示法：

```
p1 + t(q1 - p1) = p2 + s(q2 - p2)
```

求解參數 t 和 s：

```
t = ((p2 - p1) × d2) / (d1 × d2)
s = ((p2 - p1) × d1) / (d1 × d2)
```

其中 d1 = q1 - p1, d2 = q2 - p2。

若 0 ≤ t ≤ 1 且 0 ≤ s ≤ 1，則交點線上段上。

## 使用範例

```python
from point import Point
from line import segments_intersect, line_intersection_point

# 定義兩線段
p1, q1 = Point(1, 1), Point(4, 4)
p2, q2 = Point(1, 4), Point(4, 1)

# 檢查是否相交
print(segments_intersect(p1, q1, p2, q2))  # True

# 計算交點
intersect = line_intersection_point(p1, q1, p2, q2)
print(intersect)  # Point(2.5, 2.5)
```

## 參考資料

- [Line Segment Intersection - Wikipedia](https://en.wikipedia.org/wiki/Line_segment_intersection)
- [Orientation and Line Intersection - GeeksforGeeks](https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/)
- O'Rourke, J. (1998). *Computational Geometry in C*. Cambridge University Press.
