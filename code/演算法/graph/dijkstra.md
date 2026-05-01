# Dijkstra 最短路徑算法

## 歷史背景

Edsger W. Dijkstra 於 1956 年發明了這個算法，最初是為了解決荷蘭阿姆斯特丹市的地鐵線路問題。

### 重要特性

- **單源最短路徑**：從一個起點到所有其他頂點的最短路徑
- **權重非負**：所有邊權重必須 >= 0
- **貪心算法**：每步選擇當前距離最小的未訪問頂點

## 演算法原理

### 核心思想

```
1. 維護一個集合 S：已確定最短距離的頂點
2. 維護距離陣列 dist[]
3. 每步選擇 dist 最小的頂點加入 S
4. 更新該頂點鄰居的距離
```

### 圖示

```
初始：dist[0] = 0，其他為 ∞

步驟 1：選擇 0，加入 S
       dist = {0: 0, 1: 4, 2: 2, 3: ∞, 4: ∞}
       S = {0}

步驟 2：選擇 2（最小），加入 S
       更新：dist[1] = min(4, 2+1) = 3
       更新：dist[4] = min(∞, 2+10) = 12
       S = {0, 2}

步驟 3：選擇 1（最小），加入 S
       更新：dist[3] = min(∞, 3+5) = 8
       S = {0, 2, 1}

步驟 4：選擇 3，加入 S
       更新：dist[4] = min(12, 8+2) = 10
       S = {0, 2, 1, 3}

步驟 5：選擇 4，完成
       S = {0, 2, 1, 3, 4}
```

## 程式碼說明

### Dijkstra 算法

```python
import heapq

def dijkstra(graph, start):
    distances = {start: 0}
    predecessors = {}
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        if u in visited:
            continue

        visited.add(u)

        for v, weight in graph[u]:
            new_dist = current_dist + weight

            if v not in distances or new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, predecessors
```

### 為什麼用堆積？

- 普通陣列：每次找到最小 dist 需要 O(V)
- 總時間：O(V²)
- 堆積：插入/取出最小值 O(log V)
- 總時間：O((V + E) log V)

## 複雜度分析

| 實現方式 | 時間複雜度 | 空間複雜度 |
|---------|-----------|-----------|
| 簡單陣列 | O(V²) | O(V) |
| 二元堆積 | O((V + E) log V) | O(V) |
| 斐波那契堆 | O(E + V log V) | O(V) |

## 與 Bellman-Ford 比較

| 特性 | Dijkstra | Bellman-Ford |
|------|----------|--------------|
| 時間複雜度 | O((V+E)logV) | O(VE) |
| 負權重 | 不支援 | 支援 |
| 負環檢測 | 無法檢測 | 可檢測 |
| 實用性 | 更快 | 更通用 |

## 變種算法

### 1. A* 搜索

```
f(v) = g(v) + h(v)

g(v)：從起點到 v 的實際距離
h(v)：從 v 到目標的估計距離（啟發式）
```

### 2. 雙向 Dijkstra

- 從起點和終點同時運行
- 在中間相遇時停止

### 3. ALT（A*、Landmark、Triangle Inequality）

- 使用地標節點加速
- 預先計算啟發式距離

## 實際應用

- **GPS 導航**：路徑規劃
- **網路路由**：OSPF 協議
- **航空線路**：航班調度
- **遊戲 AI**：尋路算法（如 A*）

## 注意事項

### 負權重問題

Dijkstra 不能處理負權重：

```
   -2
0 ----→ 1
 \     /
  \   /
   1 \/1
     \/
      2

如果從 0 出發：
- 先選擇 1（dist=1）
- 然後更新 dist[2] = 1 + 1 = 2

但實際上：0→2→1 的距離是 1 + (-2) = -1
```

### 環路問題

算法會忽略已訪問的節點，但如果有負權重，可能需要重新訪問。

## 參考資料

- Dijkstra, E. W. (1959). [A note on two problems in connexion with graphs](https://doi.org/10.1007/BF01386390). *Numerische Mathematik*, 1, 269-271.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Thorup, M. (1999). [Undirected Single-Source Shortest Paths with Positive Integer Weights in Linear Time](https://doi.org/10.1145/301970.301971). *JACM*, 46(3), 362-394.