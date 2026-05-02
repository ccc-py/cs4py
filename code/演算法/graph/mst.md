# 最小生成樹 (Minimum Spanning Tree) 演算法：Prim's 與 Kruskal's

## 歷史背景

最小生成樹問題在網路設計、電路佈局、聚類分析等領域有廣泛應用。給定一個加權無向連通圖，最小生成樹是要找出一棵包含所有頂點且總權重最小的樹。

### Prim's 演算法
- **發明者**：Vojtěch Jarník (1930)，後由 Robert Prim (1957) 和 Edsger Dijkstra (1959) 重新發現
- **別名**：Jarník's algorithm、Prim-Jarník algorithm、DJP algorithm
- **時間複雜度**：O(E log V)（使用二元堆）

### Kruskal's 演算法
- **發明者**：Joseph Kruskal (1956)
- **特點**：基於邊的排序，使用並查集檢測環
- **時間複雜度**：O(E log E)

## Prim's 演算法

### 原理

```
1. 從任意頂點開始，將其加入 MST（最小生成樹）
2. 重複直到所有頂點都在 MST 中：
   選擇連接 MST 與非 MST 頂點的最小權重邊
   將該邊和頂點加入 MST
3. 使用優先佇列（最小堆）高效選取最小邊
```

### 圖示

```
原始圖：
    A --4-- B
    |      /|
    |     / |
    4    2  5
    |   /   |
    |  /    |
    C --5-- D

Prim's 從 A 開始：
1. 選 A-B(4) 或 A-C(4)，假設選 A-B
2. 從 {A,B} 選最小邊：B-C(2)
3. 從 {A,B,C} 選最小邊：B-D(5) 或 C-D(5)，假設選 B-D

MST：A-B(4), B-C(2), B-D(5)，總權重 = 11
```

### 程式碼

```python
def prim_mst(vertices, edges):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    start = vertices[0]
    visited = {start}
    heap = []
    mst_edges = []

    for neighbor, w in adj[start]:
        heapq.heappush(heap, (w, start, neighbor))

    while heap and len(visited) < len(vertices):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))
        for neighbor, weight in adj[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))

    return mst_edges
```

### 核心資料結構

- **優先佇列**：用於快速取得最小權重邊
- **已訪問集合**：避免形成環

## Kruskal's 演算法

### 原理

```
1. 將所有邊按權重從小到大排序
2. 依序選取邊：
   若該邊的兩個端點不在同一集合（不會形成環），則加入 MST
   否則跳過（會形成環）
3. 使用並查集 (Union-Find) 維護連通分量
```

### 圖示

```
原始圖（邊已排序）：
(2) B-C, (4) A-B, (4) A-C, (5) B-D, (5) C-D

Kruskal's：
1. 選 B-C(2)：{B,C}
2. 選 A-B(4)：{A,B,C}
3. 選 A-C(4)：跳過（A 和 C 已在同一集合）
4. 選 B-D(5)：{A,B,C,D}

MST：B-C(2), A-B(4), B-D(5)，總權重 = 11
```

### 程式碼

```python
def kruskal_mst(vertices, edges):
    uf = UnionFind(vertices)
    sorted_edges = sorted(edges, key=lambda e: e[2])
    mst_edges = []

    for u, v, w in sorted_edges:
        if uf.union(u, v):  # 不會形成環
            mst_edges.append((u, v, w))
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges
```

### 並查集 (Union-Find)

```python
class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路徑壓縮
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        # 按秩合併
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1
        return True
```

## 複雜度分析

| 演算法 | 時間複雜度 | 空間複雜度 | 適用圖形 |
|--------|-----------|-----------|---------|
| Prim's | O(E log V) | O(V) | 稠密圖較佳 |
| Kruskal's | O(E log E) | O(V) | 稀疏圖較佳 |

### 為什麼是這樣的複雜度？

**Prim's**：
- 每條邊最多被考慮一次：O(E)
- 堆操作：O(log V)
- 總計：O(E log V)

**Kruskal's**：
- 排序邊：O(E log E)
- 並查集操作：近乎 O(1)（經路徑壓縮和按秩合併）
- 總計：O(E log E)

## 兩者比較

| 特性 | Prim's | Kruskal's |
|------|--------|-----------|
| 策略 | 點擴張（逐步加入頂點） | 邊選擇（從小到大選邊） |
| 資料結構 | 優先佇列 | 並查集 |
| 稀疏圖 | 較慢 | 較快 |
| 稠密圖 | 較快 | 較慢 |
| 邊數 | 只用於權重查詢 | 需要全部排序 |

## 應用場景

### Prim's
- 從某點開始逐步擴建的網路（如廣播）
- 稠密圖（邊數接近 V²）

### Kruskal's
- 全域邊權重資訊重要的場景
- 稀疏圖（邊數接近 V）
- 聚類分析（Kruskal 的變體用於層次聚類）

## 實用考量

1. **圖的表示**：Prim's 需要鄰接表，Kruskal's 需要邊列表
2. **並查集優化**：路徑壓縮和按秩合併使操作近乎 O(1)
3. **唯一性**：若邊權重都不同，MST 唯一；否則可能有多個
4. **最大生成樹**：將權重取負或選最大邊即可

## 參考資料

- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Kruskal, J. B. (1956). [On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem](https://doi.org/10.1090/S0002-9947-1956-0078686-7). *Proceedings of the American Mathematical Society*, 7(1), 48-50.
- Prim, R. C. (1957). [Shortest Connection Networks And Some Generalizations](https://doi.org/10.1002/j.1538-7305.1957.tb01515.x). *Bell System Technical Journal*, 36(6), 1389-1401.
- Jarník, V. (1930). O jistém problému minimálním. *Práce Moravské Přírodovědecké Společnosti*, 6, 57-63.
