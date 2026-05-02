# 布雷森漢姆直線演算法 (Bresenham's Line Algorithm)

## 歷史背景

1962 年，IBM 的 Jack Bresenham 開發了這個演算法，用於繪圖機和早期電腦顯示器。當時硬體運算能力有限，浮點數運算昂貴，因此需要一種純整數運算的直線繪製方法。該演算法成為電腦圖學的基礎演算法之一，至今仍廣泛應用於各種繪圖系統中。

## 核心原理

布雷森漢姆演算法使用**誤差項（error term）**來決定下一個像素點的位置。核心思想是：

1. 從起點開始，沿著主要方向（x 或 y，取變化較大者）逐步移動
2. 每一步計算誤差項，判斷是否需要在次要方向上移動一個像素
3. 誤差項更新公式：`err = err - dy` 或 `err = err + dx`

### 整數運算優勢

- 不使用浮點數、乘法或除法
- 僅使用加法、減法和比較運算
- 適合硬體實作和嵌入式系統

### 演算法步驟

```
dx = |x1 - x0|, dy = |y1 - y0|
err = dx - dy
while (x, y) != (x1, y1):
    繪製點 (x, y)
    if 2*err > -dy:  # 需要移動 x
        err -= dy
        x += sx
    if 2*err < dx:   # 需要移動 y
        err += dx
        y += sy
```

## 使用範例

```python
from raster.bresenham import bresenham_line

# 繪製一條從 (2, 3) 到 (10, 8) 的直線
points = bresenham_line(2, 3, 10, 8)
print(points)
# 輸出: [(2, 3), (3, 4), (4, 5), (5, 5), (6, 6), (7, 7), (8, 7), (9, 8), (10, 8)]

# 在 ASCII 網格中顯示
from raster.bresenham import draw_ascii_grid
print(draw_ascii_grid(points, width=12, height=10))
```

## 參考資料

- Bresenham, J. E. (1965). "Algorithm for computer control of a digital plotter". *IBM Systems Journal*, 4(1), 25-30.
- [Wikipedia: Bresenham's line algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)
- Foley, J. D., et al. (1996). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.
