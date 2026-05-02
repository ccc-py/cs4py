# Delaunay Triangulation - Delaunay 三角化

## 歷史背景

Delaunay 三角化由俄羅斯數學家 Boris Delaunay 在 1934 年提出。它是一種特殊的三角化方法，滿足「空外接圓」性質：任意三角形的外接圓內不包含其他點。這種三角化在有限元素分析、地理資訊系統、電腦圖學等領域有廣泛應用。

## 核心原理

### Delaunay 性質
對於三角化中的每個三角形，其外接圓內不包含任何其他點。

### Bowyer-Watson 算法（增量法）
1. 建立一個包含所有點的「超級三角形」。
2. 逐一將點加入：
   - 找出所有外接圓包含新點的三角形（bad triangles）。
   - 移除這些三角形，形成一個多邊形孔洞。
   - 用新點與孔洞的邊界邊構成新三角形。
3. 移除包含超級三角形頂點的三角形。

### 時間複雜度
O(n²)，其中 n 為點數。優化後可達 O(n log n)。

## 使用範例

```python
from point import Point
from delaunay import delaunay_triangulation

points = [Point(0,0), Point(2,0), Point(1,1), Point(0,2), Point(2,2)]
triangles = delaunay_triangulation(points)
for tri in triangles:
    print(tri)
```

## 參考資料

- [Delaunay Triangulation - Wikipedia](https://en.wikipedia.org/wiki/Delaunay_triangulation)
- [Bowyer-Watson Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/delaunay-triangulation/)
- Delaunay, B. (1934). *Sur la sphère vide*. Bulletin de l'Académie des Sciences de l'URSS.