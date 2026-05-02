# 中點畫圓演算法 (Midpoint Circle Algorithm)

## 歷史背景

中點畫圓演算法是 Bresenham 直線演算法的延伸，同樣由 Jack Bresenham 在 1960 年代後期開發。該演算法利用圓的**八分對稱性（eight-way symmetry）**，只需要計算 45 度弧（1/8 圓）上的點，即可生成整個圓。這大大減少了計算量，成為早期電腦繪圖系統的標準圓繪製方法。

## 核心原理

### 八分對稱性

圓具有高度的對稱性：
- 如果點 (x, y) 在圓上，則 (±x, ±y) 和 (±y, ±x) 也在圓上
- 只需計算從 (0, r) 到 (r/√2, r/√2) 的弧段

### 中點判斷

對於當前點 (x, y)，下一個點要麼是 (x+1, y)，要麼是 (x+1, y-1)。

定義函數 F(x, y) = x² + y² - r²：
- F(x, y) = 0：點在圓上
- F(x, y) < 0：點在圓內
- F(x, y) > 0：點在圓外

中點 M = (x+1, y-0.5)，計算 d = F(M)：
- 若 d < 0：中點在圓內，選 (x+1, y)
- 若 d ≥ 0：中點在圓外，選 (x+1, y-1)

### 增量更新

決策參數 d 可以增量更新，避免重複計算平方：
- 初始：d = 1 - r
- 若 d < 0：d += 2x + 3
- 若 d ≥ 0：d += 2(x - y) + 5, y -= 1

## 使用範例

```python
from raster.midpoint_circle import midpoint_circle

# 計算圓的像素點
points = midpoint_circle(0, 0, 5)
print(f"半徑 5 的圓共有 {len(set(points))} 個像素點")

# 顯示在 ASCII 網格
from raster.midpoint_circle import draw_ascii_circle
print(draw_ascii_circle(points, 0, 0, 5))
```

## 參考資料

- Bresenham, J. E. (1977). "A linear algorithm for incremental digital display of circular arcs". *Communications of the ACM*, 20(2), 100-106.
- [Wikipedia: Midpoint circle algorithm](https://en.wikipedia.org/wiki/Midpoint_circle_algorithm)
- Hearn, D., & Baker, M. P. (2004). *Computer Graphics with OpenGL* (3rd ed.). Pearson.
