# Point in Polygon - 點在多邊形內部檢測

## 歷史背景

點在多邊形內部檢測是計算幾何中的基本問題，最早由 Ray Casting（射線法）解決，該方法由 Victor Scheinerman 在 1960 年代提出。Winding Number（環繞數）方法則基於更深刻的拓撲學概念，能處理更複雜的多邊形（如自相交）。

## 核心原理

### Ray Casting（射線法）
從待測點向右發射一條水平射線，計算與多邊形邊的交點數：
- 奇數個交點 → 點在內部
- 偶數個交點 → 點在外部

### Winding Number（環繞數）
計算多邊形圍繞待測點的總角度變化：
- 環繞數 ≠ 0 → 點在內部
- 環繞數 = 0 → 點在外部

### 邊界檢測
使用 `on_segment` 函數檢查點是否在任何邊上。

## 使用範例

```python
from point import Point
from point_in_polygon import point_in_polygon, ray_casting

polygon = [Point(0,0), Point(4,0), Point(4,4), Point(0,4)]
point = Point(2, 2)
print(point_in_polygon(point, polygon))  # 'inside'
```

## 參考資料

- [Point in Polygon - Wikipedia](https://en.wikipedia.org/wiki/Point_in_polygon)
- [Ray Casting Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/)
- Haines, E. (1994). *Point in Polygon Strategies*. Graphics Gems IV.