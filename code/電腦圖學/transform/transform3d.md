# 3D 變換與投影 (3D Transformations and Projection)

## 歷史背景

3D 電腦圖學的發展可以追溯到 1960 年代，Ivan Sutherland 的 Sketchpad 系統展示了互動式 3D 圖形的潛力。**透視投影**的概念源自古希臘時期的藝術透視法，而數學形式化則由 15 世紀的 Filippo Brunelleschi 和 Leon Battista Alberti 建立。在電腦圖學中，這些概念被轉化為矩陣運算，使得 3D 場景的渲染變得高效且靈活。

## 核心原理

### 齊次座標（4D）

3D 點 (x, y, z) 表示為 (x, y, z, 1)，使用 4×4 矩陣表示變換。

### 視錐（View Frustum）

透視投影定義了一個金字塔形的可見空間：
- **近平面（Near Plane）**：靠近相機的裁剪平面
- **遠平面（Far Plane）**：遠離相機的裁剪平面
- **視野（Field of View, FOV）**：垂直方向的視角
- **寬高比（Aspect Ratio）**：width / height

### 正交投影 vs 透視投影

| 特性 | 正交投影 | 透視投影 |
|------|---------|---------|
| 平行線 | 保持平行 | 匯聚於消失點 |
| 深度感 | 無 | 有（近大遠小） |
| 應用 | 工程圖、CAD | 遊戲、電影 |

### 透視投影矩陣

```
| f/aspect  0       0               0 |
| 0         f       0               0 |
| 0         0   (f+n)/(n-f)   2fn/(n-f) |
| 0         0       -1              0 |
```
其中 f = cot(FOV/2), n = near, f = far

## 使用範例

```python
from transform.transform3d import *

# 定義一個立方體
cube = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1),
        (-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]

# 建立 3D 變換管線
M = multiply_4x4(
    perspective_projection(fov_y=60, aspect=1.0, near=0.1, far=100.0),
    rotation_y(45),
    translation_3d(0, 0, 5)
)

# 投影所有頂點
projected = [transform_point_3d(M, v) for v in cube]
```

## 參考資料

- Sutherland, I. E. (1963). "Sketchpad: A man-machine graphical communication system". *Proceedings of the AFIPS Spring Joint Computer Conference*.
- [Wikipedia: 3D projection](https://en.wikipedia.org/wiki/3D_projection)
- Lengyel, E. (2019). *Foundations of Game Engine Development, Volume 1: Mathematics*. Terathon Software.
