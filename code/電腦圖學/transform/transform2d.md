# 2D 幾何變換 (2D Geometric Transformations)

## 歷史背景

2D 幾何變換是電腦圖學的基礎，起源於 1960 年代的 CAD（電腦輔助設計）系統。**齊次座標（Homogeneous Coordinates）**的引入是關鍵突破，由 August Ferdinand Möbius 在 19 世紀提出，後來被應用於電腦圖學。使用齊次座標可以將平移、旋轉、縮放等變換統一表示為矩陣乘法，使得複合變換的計算變得簡潔高效。

## 核心原理

### 齊次座標

在 2D 空間中，點 (x, y) 表示為 (x, y, 1)。這樣可以使用 3×3 矩陣表示所有仿射變換。

### 基本變換矩陣

#### 平移 (Translation)
```
| 1  0  tx |
| 0  1  ty |
| 0  0   1 |
```

#### 縮放 (Scaling)
```
| sx  0   0 |
| 0  sy   0 |
| 0   0   1 |
```

#### 旋轉 (Rotation)
```
| cosθ  -sinθ  0 |
| sinθ   cosθ  0 |
|   0      0    1 |
```

### 複合變換

多個變換可以通過矩陣乘法組合：
```
M = M_n × ... × M_2 × M_1
```

注意：矩陣乘法不滿足交換律，變換順序很重要！

應用順序：先應用 M_1，最後應用 M_n（從右到左）。

## 使用範例

```python
from transform.transform2d import *

# 定義一個正方形
square = [(0, 0), (1, 0), (1, 1), (0, 1)]

# 複合變換：先縮放 2 倍，再旋轉 45 度，最後平移 (3, 3)
M = composite_transform(
    translation(3, 3),
    rotation(45),
    scaling(2, 2)
)

transformed = transform_points(M, square)
print(transformed)
```

## 參考資料

- Foley, J. D., et al. (1996). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.
- [Wikipedia: Transformation matrix](https://en.wikipedia.org/wiki/Transformation_matrix)
- Shirley, P., & Marschner, S. (2009). *Fundamentals of Computer Graphics* (3rd ed.). A K Peters/CRC Press.
