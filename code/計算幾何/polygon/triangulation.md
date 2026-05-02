# Polygon Triangulation - 多邊形三角化（Ear Clipping）

## 歷史背景

多邊形三角化是將多邊形分解為三角形的過程，是電腦圖學中網格處理、物體渲染的基礎。Ear Clipping 算法由 Godfried Toussaint 在 1991 年推廣，其原理簡單且易於實作。

## 核心原理

### Ear（耳尖）
對於簡單多邊形的一個頂點，若與其相鄰兩個頂點構成的三角形內部不包含其他頂點，則稱該頂點為一個 ear。

### 定理
任何具有 n ≥ 4 個頂點的簡單多邊形至少有一個 ear。

### 算法步驟
1. 找到一個 ear 頂點。
2. 移除該頂點，將其相鄰頂點與之構成的三角形加入結果。
3. 重複直到剩餘 3 個頂點（最後一個三角形）。

### 時間複雜度
O(n²)，因為每次需要掃描尋找 ear，且需要檢查其他點是否在三角形內部。

## 使用範例

```python
from point import Point
from triangulation import ear_clipping_triangulation

polygon = [Point(0,0), Point(0,4), Point(4,4), Point(4,0)]
triangles = ear_clipping_triangulation(polygon)
for tri in triangles:
    print(tri)
```

## 參考資料

- [Polygon Triangulation - Wikipedia](https://en.wikipedia.org/wiki/Polygon_triangulation)
- [Ear Clipping - GeeksforGeeks](https://www.geeksforgeeks.org/polygon-triangulation/)
- Toussaint, G. (1991). *Efficiency of the Algorithm for Recognizing Violin Patterns*.