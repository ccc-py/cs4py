# TSP 近似演算法 (TSP Approximation)

## 歷史背景

旅行推銷員問題（TSP）是組合優化中最著名的問題之一，尋找訪問所有城市並返回起點的最短路徑。

### 發展歷程

- **1930 年代**：TSP 問題正式提出
- **1972 年**：Karp 證明 TSP 是 NP-完全問題
- **1976 年**：Christofides 提出 1.5-近似演算法（度量 TSP）
- **1977 年**：Rosenkrantz 等人提出基於 MST 的 2-近似演算法

## 演算法原理

### 問題定義

```
給定 n 個城市和各城市間的距離，
找出一條經過每個城市恰好一次並返回起點的最短路徑。

度量 TSP：距離滿足三角不等式 d(a,c) <= d(a,b) + d(b,c)
```

### 2-近似演算法（基於 MST）

```
核心步驟：
1. 計算最小生成樹（MST）
2. 對 MST 進行 DFS 遍歷，得到所有邊的訪問序列
3. 去除重複訪問的城市（捷徑法 shortcut）
4. 得到哈密頓迴圈

為什麼是 2-近似？
- MST 長度 <= 最優 TSP 路徑長度（去掉一條邊）
- DFS 遍歷長度 = 2 * MST 長度（每條邊走兩次）
- 捷徑法不會增加長度（三角不等式）
- 因此：我們的解 <= 2 * OPT

時間複雜度：O(V^2)
```

### Christofides 演算法（1.5-近似）

```
步驟：
1. 計算 MST
2. 找出奇度數節點（必有偶數個）
3. 在奇度數節點上計算最小權重完美匹配
4. 將 MST 和匹配合併，得到歐拉圖
5. 找出歐拉回路，捷徑化得到哈密頓迴圈

近似比：1.5（對於度量 TSP）
```

### 最近鄰居啟發式

```
貪婪策略：
從起點開始，每次選擇最近的未訪問城市。

注意：無近似比保證，但在實務上通常表現不錯。
最壞情況可以達到 Ω(log n) 倍的最優解。
```

## 程式碼說明

### MST 計算（Prim 演算法）

```python
def _prim_mst(self):
    in_mst = [False] * n
    key = [inf] * n
    parent = [-1] * n
    key[0] = 0

    for _ in range(n):
        u = min_key(key, in_mst)
        in_mst[u] = True
        # 更新鄰居的 key 值
```

### DFS 遍歷 MST

```python
def _dfs(self, u, adj, visited, tour):
    visited[u] = True
    tour.append(u)
    for v in adj[u]:
        if not visited[v]:
            self._dfs(v, adj, visited, tour)
```

## 應用場景

### 1. 物流路徑規劃

```
貨車需要配送多個地點，尋找最短的配送路徑。
```

### 2. PCB 鑽孔

```
印刷電路板需要鑽上千個孔，尋找最短的鑽孔路徑。
```

### 3. 基因定序

```
DNA 片段組裝中，TSP 用於尋找最小的重疊路徑。
```

## 圖例

```
4 城市示例：

    0 ---- 1
    | \     |
    |  \    |
    |   \   |
    |    \  |
    3 ---- 2

MST：選擇邊 (0,1), (0,3), (3,2)
DFS 遍歷：0 -> 1 -> 0 -> 3 -> 2 -> 3 -> 0
捷徑後：0 -> 1 -> 2 -> 3 -> 0
```

## 演算法比較

| 演算法 | 近似比 | 時間複雜度 | 說明 |
|--------|--------|-----------|------|
| MST 2-近似 | 2 | O(V^2) | 簡單，有保證 |
| Christofides | 1.5 | O(V^3) | 度量 TSP 最佳 |
| 最近鄰居 | 無保證 | O(V^2) | 快速啟發式 |
| 最優解 | 1 | O(2^V) | 指數時間 |

## 參考資料

- Christofides, N. (1976). *Worst-case analysis of a new heuristic for the travelling salesman problem*. Carnegie-Mellon University.
- Rosenkrantz, D. J., Stearns, R. E., & Lewis, P. M. (1977). *An analysis of several heuristics for the traveling salesman problem*. SIAM Journal on Computing, 6(3), 563-581.
- Applegate, D. L., et al. (2006). *The Traveling Salesman Problem: A Computational Study*. Princeton University Press.
