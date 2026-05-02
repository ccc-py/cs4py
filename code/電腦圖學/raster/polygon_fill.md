# 掃描線多邊形填充演算法 (Scan-line Polygon Fill Algorithm)

## 歷史背景

掃描線演算法是電腦圖學中最基礎的多邊形填充方法之一，起源於 1960 年代的向量顯示器時代。該演算法模擬了阴极射线管（CRT）顯示器的掃描過程，逐行掃描螢幕並決定哪些像素需要填充。這種方法至今仍是許多圖形系統（包括 OpenGL 等）的底層填充策略。

## 核心原理

### 邊表（Edge Table, ET）

記錄每條邊的資訊，按邊的最小 y 值組織：
- **y_max**：邊的最大 y 值（結束掃描線）
- **x**：當前交點的 x 座標
- **dx/dy**：斜率的倒數，用於更新 x 值

### 活躍邊表（Active Edge Table, AET）

記錄當前掃描線與多邊形相交的所有邊，按 x 值排序。

### 奇偶規則（Even-Odd Rule）

對於每條掃描線：
1. 計算與多邊形的所有交點
2. 將交點按 x 座標排序
3. 兩兩配對，配對之間的像素填入顏色

### 演算法步驟

```
1. 建立邊表 ET
2. 對每條掃描線 y 從 min_y 到 max_y:
   a. 將 ET[y] 中的邊加入 AET
   b. 移除 AET 中 y_max <= y 的邊
   c. 將 AET 中的邊按 x 排序
   d. 兩兩配對交點，填充之間的像素
   e. 更新 AET 中每條邊的 x 值：x += dx/dy
```

## 使用範例

```python
from raster.polygon_fill import scanline_fill, draw_ascii_polygon

# 定義三角形
triangle = [(5, 5), (15, 5), (10, 15)]

# 填充
filled = scanline_fill(triangle, width=20, height=20)

# 顯示
print(draw_ascii_polygon(filled, triangle))
```

## 參考資料

- Rogers, D. F. (2001). *Procedural Elements for Computer Graphics* (2nd ed.). McGraw-Hill.
- [Wikipedia: Scanline rendering](https://en.wikipedia.org/wiki/Scanline_rendering)
- Glassner, A. S. (Ed.). (1990). *Graphics Gems*. Academic Press.
