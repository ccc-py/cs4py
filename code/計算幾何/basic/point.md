# Point - 點與向量運算

## 歷史背景

計算幾何（Computational Geometry）起源於 1970 年代，隨著電腦圖學、地理資訊系統（GIS）和機器人學的發展而興起。點（Point）作為幾何的基本元素，其運算構成了所有計算幾何演算法的基礎。

二維幾何中的向量運算（加法、減法、點積、叉積）源自於線性代數，而方向測試（orientation test）則是許多幾何演算法的核心判斷依據。

## 核心原理

### Point 類別

`Point` 類別封裝了二維點的座標 (x, y)，並提供以下運算：

1. **向量加法與減法**：`p + q`、`p - q`
2. **數乘**：`p * scalar`
3. **點積（Dot Product）**：`p · q = p.x * q.x + p.y * q.y`
   - 用於計算投影、判斷垂直等
4. **叉積（Cross Product）**：`p × q = p.x * q.y - p.y * q.x`
   - 二維叉積為純量，表示有向面積的 2 倍
   - 正號表示逆時針（CCW），負號表示順時針（CW）

### 方向測試（Orientation Test）

給定三個點 p, q, r，計算叉積：

```
orientation = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
```

- `orientation > 0`：p → q → r 為逆時針方向（CCW）
- `orientation < 0`：p → q → r 為順時針方向（CW）
- `orientation = 0`：三點共線（collinear）

### 極角（Polar Angle）

極角計算使用 `atan2(dy, dx)`，給出點相對於原點的方向角（弧度）。

## 使用範例

```python
from point import Point, orientation, ccw

# 建立點
p1 = Point(0, 0)
p2 = Point(3, 4)
p3 = Point(1, 2)

# 向量運算
print(p1 + p3)  # Point(1, 2)
print(p2 - p1)  # Point(3, 4)
print(p2.dot(p3))  # 11
print(p2.cross(p3))  # 2

# 距離計算
print(p1.distance_to(p2))  # 5.0

# 方向測試
a = Point(0, 0)
b = Point(4, 0)
c = Point(4, 3)
print(orientation(a, b, c))  # 1 (CCW)
```

## 參考資料

- [Computational Geometry - Wikipedia](https://en.wikipedia.org/wiki/Computational_geometry)
- [Orientation of Points - GeeksforGeeks](https://www.geeksforgeeks.org/orientation-3-ordered-points/)
- de Berg, M., et al. (2008). *Computational Geometry: Algorithms and Applications*. Springer.
