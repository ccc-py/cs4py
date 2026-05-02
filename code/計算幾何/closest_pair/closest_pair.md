# Closest Pair of Points - 最近點對算法

## 歷史背景

最近點對問題是計算幾何中的經典問題，最早由 Michael Shamos 在 1975 年的博士論文中提出 O(n log n) 的分治算法。該問題在電腦圖學、地理資訊系統、聚類分析等領域有廣泛應用。

## 核心原理

### 暴力法
枚舉所有點對，時間複雜度 O(n²)。

### 分治法
1. **排序**：按 x 坐標排序點集。
2. **分割**：找到中線，將點集分為左右兩半。
3. **遞迴**：分別求出左右兩半的最近點對距離 d_left 和 d_right，取較小值 d。
4. **跨越中線的檢查**：
   - 只考慮 x 坐標距離中線小於 d 的點（strip）。
   - 按 y 坐標排序這些點。
   - 對於每個點，只需檢查後續 y 差小於 d 的點（最多 7 個）。
5. **合併**：返回最小距離。

### 時間複雜度
O(n log n)

## 使用範例

```python
from point import Point
from closest_pair import closest_pair

points = [Point(2,3), Point(12,30), Point(40,50), Point(5,1), Point(12,10), Point(3,4)]
p1, p2, d = closest_pair(points)
print(f"最近點對: {p1}, {p2}, 距離: {d}")
```

## 參考資料

- [Closest Pair of Points - Wikipedia](https://en.wikipedia.org/wiki/Closest_pair_of_points_problem)
- [Closest Pair Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/closest-pair-of-points-using-divide-and-conquer-algorithm/)
- Shamos, M. I. (1975). *Geometric Complexity*. Proceedings of the 7th ACM Symposium on Theory of Computing.