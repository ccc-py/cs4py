# QuickHull - 凸包算法

## 歷史背景

QuickHull 算法由 C. Bradford Barber 等人於 1996 年提出，其名稱和策略類似於 QuickSort，採用分治法（divide and conquer）來計算凸包。平均時間複雜度為 O(n log n)，但最壞情況下可能達到 O(n²)。

## 核心原理

### 算法步驟
1. **找端點**：選擇 x 坐標最小和最大的兩個點，構成一條線段。
2. **分割**：將點集分為兩部分：
   - 在線段上方的點（形成上凸包）
   - 在線段下方的點（形成下凸包）
3. **遞迴**：
   - 對每個子集，找到距離線段最遠的點（形成三角形）。
   - 遞迴處理左右兩側的子集。
4. **合併**：將所有找到的凸包點合併。

### 時間複雜度
- 平均：O(n log n)
- 最壞：O(n²)

## 使用範例

```python
from point import Point
from quickhull import quickhull

points = [Point(0,0), Point(1,1), Point(2,2), Point(3,1), Point(2,0)]
hull = quickhull(points)
print(hull)
```

## 參考資料

- [QuickHull - Wikipedia](https://en.wikipedia.org/wiki/Quickhull)
- Barber, C. B., et al. (1996). *The Quickhull Algorithm for Convex Hulls*. ACM Transactions on Mathematical Software.