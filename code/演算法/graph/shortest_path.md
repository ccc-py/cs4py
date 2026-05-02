# 最短路徑演算法：Bellman-Ford 與 Floyd-Warshall

## 歷史背景

最短路徑問題是圖論中的核心問題，應用於網路路由、地圖導航、交通規劃等領域。

### Bellman-Ford 演算法
- **發明者**：Richard Bellman (1958) 和 Lester Ford (1956) 分別獨立提出
- **特點**：可處理負權邊，能檢測負環
- **時間複雜度**：O(V × E)

### Floyd-Warshall 演算法
- **發明者**：Robert Floyd (1962)，基於 Stephen Warshall 的傳遞閉包演算法 (1962)
- **特點**：解決所有點對最短路徑問題
- **時間複雜度**：O(V³)

## Bellman-Ford 演算法

### 原理

```
1. 初始化：起點距離設為 0，其餘設為無限大
2. 重複 |V|-1 次：
   對每條邊 (u, v, w) 進行鬆弛操作：
     if dist[u] + w < dist[v]:
         dist[v] = dist[u] + w
3. 再檢查一次：若還能鬆弛，說明存在負環
```

### 圖示

```
圖例（有負權邊）：
    A --4--> B --2--> C
    |         |
    +---(-1)--+
    
初始：dist[A]=0, dist[B]=∞, dist[C]=∞
第1輪後：dist[A]=0, dist[B]=-1, dist[C]=∞
第2輪後：dist[A]=0, dist[B]=-1, dist[C]=1 (透過 B)
```

### 程式碼

```python
def bellman_ford(vertices, edges, source):
    dist = {v: float('inf') for v in vertices}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # 檢查負環
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None  # 存在負環

    return dist
```

### 負環檢測

負環是指總權重為負的循環，若存在負環，則最短路徑無定義（可以不斷繞環使距離無限小）。

## Floyd-Warshall 演算法

### 原理

```
1. 初始化距離矩陣 D，D[i][i] = 0，有邊則為權重，否則為 ∞
2. 對每個中間點 k：
   對每對 (i, j)：
     D[i][j] = min(D[i][j], D[i][k] + D[k][j])
3. 最終 D[i][j] 即為 i 到 j 的最短路徑
```

### 圖示

```
初始距離矩陣：
     A    B    C    D
A    0    3    ∞    ∞
B    ∞    0    1    ∞
C    ∞    ∞    0    2
D    ∞    ∞    ∞    0

經過 k=A 更新：
     A    B    C    D
A    0    3    ∞    ∞
B    ∞    0    1    ∞
C    ∞    ∞    0    2
D    ∞    ∞    ∞    0

...（逐步更新）
```

### 程式碼

```python
def floyd_warshall(vertices, edges):
    n = len(vertices)
    dist = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist
```

### 路徑重建

Floyd-Warshall 可以同時記錄下一跳頂點，用於重建路徑：

```python
next_vertex[i][j] = j  # 初始化：直接到達

# 更新時：
if dist[i][k] + dist[k][j] < dist[i][j]:
    dist[i][j] = dist[i][k] + dist[k][j]
    next_vertex[i][j] = next_vertex[i][k]
```

## 複雜度分析

| 演算法 | 時間複雜度 | 空間複雜度 | 負權邊 | 負環檢測 |
|--------|-----------|-----------|--------|---------|
| Bellman-Ford | O(V × E) | O(V) | 支援 | 支援 |
| Floyd-Warshall | O(V³) | O(V²) | 支援 | 可檢測 |
| Dijkstra | O(E log V) | O(V) | 不支援 | 不適用 |

## 應用場景

### Bellman-Ford
- 網路路由協定（如 RIP）
- 需要處理負權邊的場景
- 檢測負環（套利機會檢測）

### Floyd-Warshall
- 所有點對最短路徑
- 傳遞閉包計算
- 網路連通性分析

## 與 Dijkstra 比較

| 特性 | Bellman-Ford | Dijkstra |
|------|-------------|----------|
| 負權邊 | 支援 | 不支援 |
| 時間複雜度 | O(VE) | O(E log V) |
| 適用場景 | 稀疏圖、有負權 | 稠密圖、無負權 |

## 實用考量

1. **稀疏圖**：Bellman-Ford 可能比 Floyd-Warshall 更快
2. **稠密圖**：Floyd-Warshall 的 O(V³) 可能可以接受
3. **負環**：實務上應先檢查負環再使用結果
4. **空間優化**：Floyd-Warshall 可以原地更新（但要小心順序）

## 參考資料

- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Bellman, R. (1958). [On a Routing Problem](https://doi.org/10.1287/mnsc.2.3.275). *Quarterly of Applied Mathematics*, 16(1), 87-90.
- Floyd, R. W. (1962). [Algorithm 97: Shortest Path](https://doi.org/10.1145/367766.368168). *Communications of the ACM*, 5(6), 345.
- Warshall, S. (1962). [A Theorem on Boolean Matrices](https://doi.org/10.1145/321105.321107). *Journal of the ACM*, 9(1), 11-12.
