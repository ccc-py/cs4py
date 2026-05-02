# Jarvis March - 凸包算法（Gift Wrapping）

## 歷史背景

Jarvis March 由 R. A. Jarvis 在 1973 年提出，又稱為 Gift Wrapping 算法，因為其過程類似用紙包裹禮物。它是一種輸出敏感的凸包算法，時間複雜度為 O(nh)，其中 n 是點數，h 是凸包頂點數。

## 核心原理

### 算法步驟
1. **找起點**：選擇最左側的點作為凸包起點。
2. **包裹過程**：
   - 對於當前點，遍歷所有其他點，選擇使得所有其他點都在當前點到候選點連線右側的點。
   - 若共線，則選擇距離較遠的點。
3. **終止條件**：回到起點時結束。

### 時間複雜度
O(nh)，當 h 很小時（如點集接近凸集）效率很高，但當 h 接近 n 時效率較低。

## 使用範例

```python
from point import Point
from jarvis_march import jarvis_march

points = [Point(0,0), Point(1,1), Point(2,2), Point(3,1), Point(2,0)]
hull = jarvis_march(points)
print(hull)
```

## 參考資料

- [Jarvis March - Wikipedia](https://en.wikipedia.org/wiki/Gift_wrapping_algorithm)
- [Convex Hull Jarvis March - GeeksforGeeks](https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/)