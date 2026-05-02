# Graham Scan - 凸包算法

## 歷史背景

Graham Scan 由 Ronald Graham 在 1972 年提出，是一種高效的凸包算法，時間複雜度為 O(n log n)，其中 n 是點的數量。它是第一個達到最優時間複雜度的凸包算法之一，廣泛應用於計算機圖形學、地理信息系統等領域。

## 核心原理

### 凸包（Convex Hull）
凸包是包含給定點集的最小凸多邊形。

### Graham Scan 步驟
1. **找支點**：選擇 y 坐標最小（若相同則 x 最小）的點作為支點（pivot）。
2. **排序**：將剩餘點按相對於支點的極角（polar angle）排序。
3. **掃描**：使用堆疊（stack）維護凸包頂點：
   - 初始放入支點和前兩個排序後的點。
   - 對於每個後續點，若堆疊頂部兩點與該點不構成左轉（orientation 不為 CCW），則彈出堆疊頂部點。
   - 將該點壓入堆疊。
4. **結果**：堆疊中的點即為凸包頂點（按逆時針順序）。

### 時間複雜度
O(n log n)，主要來自排序步驟。

## 使用範例

```python
from point import Point
from graham_scan import graham_scan

points = [Point(0,0), Point(1,1), Point(2,2), Point(3,1), Point(2,0)]
hull = graham_scan(points)
print(hull)  # [Point(0,0), Point(2,0), Point(3,1), Point(1,1)]
```

## 參考資料

- [Graham Scan - Wikipedia](https://en.wikipedia.org/wiki/Graham_scan)
- [Convex Hull Algorithms - GeeksforGeeks](https://www.geeksforgeeks.org/convex-hull-set-2-graham-scan/)
- Graham, R. L. (1972). *An Efficient Algorithm for Determining the Convex Hull of a Finite Planar Set*. Information Processing Letters.