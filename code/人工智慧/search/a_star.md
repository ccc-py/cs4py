# A* 搜尋演算法 (A-Star Search Algorithm)

## 歷史背景

A* 搜尋演算法由 Peter Hart、Nils Nilsson 和 Bertram Raphael 於 1968 年在斯坦福研究所（SRI International）發表。它結合了 Dijkstra 演算法的完整性（保證找到最短路徑）和貪婪最佳優先搜尋的高效性。

## 核心原理

A* 的核心公式：

```
f(n) = g(n) + h(n)
```

- **g(n)**：從起點到節點 n 的實際累積成本
- **h(n)**：從節點 n 到目標的估計成本（啟發函數）
- **f(n)**：評估節點優先順序的總分數

### 啟發函數的選擇

| 啟發函數 | 適用場景 | 特性 |
|----------|---------|------|
| 曼哈頓距離 | 網格（四方向） | Admissible，簡單快速 |
| 歐幾里得距離 | 網格（八方向） | Admissible，更精確 |
| 對角線距離 | 允許對角移動 | Admissible，平衡 |

### 關鍵性質

1. **Admissible（可採納）**：h(n) 不高估實際成本 → 保證最優
2. **Consistent（一致）**：h(n) 滿足三角不等式 → 每個節點只擴展一次
3. **加權 A***：f(n) = g(n) + w·h(n)，w > 1 時加快搜尋但可能非最優

## 使用範例

```python
from search.a_star import astar

grid = [
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
]

path = astar(grid, start=(0, 0), end=(2, 3))
# 返回 [(0, 0), (0, 1), (0, 2), (1, 3), (2, 3)] 或類似路徑
```

## 複雜度

- **時間**：O(E log V)，E 為邊數，V 為節點數
- **空間**：O(V)，需要儲存 open set 和 closed set

## 參考資料

- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. IEEE Transactions on Systems Science and Cybernetics.
