# Z-Buffer 隱面消除演算法 (Z-Buffer Hidden Surface Removal)

## 歷史背景

Z-Buffer 演算法由 Edwin Catmull 在 1974 年的博士論文中首次提出，後來成為 Pixar 渲染器的核心技術之一。Catmull 後來共同創立了 Pixar 並擔任總裁。**Z-Buffer（深度緩衝區）**是解決可見性問題（即哪些物體在前面，哪些在後面）最簡單且最有效的方式，如今已是所有 GPU 的標準功能。

## 核心原理

### 可見性問題

在 3D 場景中，多個物體可能投影到同一個像素。需要決定哪個物體可見：
- **畫家演算法**：從遠到近繪製（需要排序，無法處理循環重疊）
- **Z-Buffer**：儲存每個像素的深度值，動態比較

### Z-Buffer 工作原理

1. **初始化**：Z-Buffer 每個像素設為無限大（或 1.0）
2. **光柵化**：對每個三角形，計算其覆蓋的像素
3. **深度測試**：對每個像素，比較新深度 z_new 與儲存的 z_stored
   - 如果 z_new < z_stored：更新顏色和深度
   - 否則：丟棄（被遮擋）
4. **完成**：Z-Buffer 中儲存的是最近物體的深度

### 重心座標插值

對於三角形內的點 P，可以用三個頂點的加權平均表示：
```
P = w0 * V0 + w1 * V1 + w2 * V2
其中 w0 + w1 + w2 = 1
```

深度值也透過同樣的權重插值：
```
z = w0 * z0 + w1 * z1 + w2 * z2
```

## 使用範例

```python
from render.z_buffer import Triangle, render_with_z_buffer

# 定義兩個三角形（一個近，一個遠）
triangles = [
    Triangle([(50,50,10), (200,50,10), (125,200,10)], (255,0,0)),  # 紅色，遠
    Triangle([(80,80,5), (220,80,5), (150,230,5)], (0,0,255)),     # 藍色，近
]

# 渲染
ppm = render_with_z_buffer(triangles, 300, 250)
```

## 參考資料

- Catmull, E. (1974). *A Subdivision Algorithm for Computer Display of Curved Surfaces* (Ph.D. thesis). University of Utah.
- [Wikipedia: Z-buffering](https://en.wikipedia.org/wiki/Z-buffering)
- Akenine-Möller, T., Haines, E., & Hoffman, N. (2018). *Real-Time Rendering* (4th ed.). A K Peters/CRC Press.
