# Polygon Area - 多邊形面積計算

## 歷史背景

鞋帶公式（Shoelace Formula）又稱 Surveyor's Formula，由美國測量師在 18 世紀發現，因計算過程類似繫鞋帶而得名。該公式可以在 O(n) 時間內計算簡單多邊形的面積。

## 核心原理

### Shoelace Formula

對於頂點為 (x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ) 的多邊形：

```
Area = 0.5 * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|
```

其中 xₙ₊₁ = x₁, yₙ₊₁ = y₁。

### 有符號面積

若頂點按逆時針（CCW）順序排列，面積為正；順時針（CW）則為負。可以用來判斷多邊形的方向。

## 使用範例

```python
from point import Point
from polygon_area import polygon_area, polygon_orientation

polygon = [Point(0,0), Point(0,4), Point(4,4), Point(4,0)]
print(polygon_area(polygon))  # 16.0
print(polygon_orientation(polygon))  # 'ccw'
```

## 參考資料

- [Shoelace Formula - Wikipedia](https://en.wikipedia.org/wiki/Shoelace_formula)
- [Polygon Area - MathWorld](https://mathworld.wolfram.com/PolygonArea.html)