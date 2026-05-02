# 最大流 (Maximum Flow)

## 歷史背景

最大流問題是網路流理論中的核心問題之一，研究如何在給定的容量限制下，從源點（source）傳送最多的流量到匯點（sink）。

### 發展歷程

- **1955 年**：Theodore E. Harris 和 F. S. Ross 在研究鐵路運輸時首次提出最大流問題
- **1956 年**：L. R. Ford Jr. 和 D. R. Fulkerson 提出了 Ford-Fulkerson 方法
- **1972 年**：Jack Edmonds 和 Richard Karp 提出了使用 BFS 找增廣路徑的改進版本（Edmonds-Karp）
- **最大流最小割定理**：由 Ford 和 Fulkerson 證明，是網路流理論的基石

## 演算法原理

### Ford-Fulkerson 方法

Ford-Fulkerson 是一個迭代方法，不斷尋找增廣路徑（augmenting path）並增加流量。

```
核心概念：
1. 殘留網路（Residual Network）：
   - 每條邊 e 有殘留容量 = 原始容量 - 當前流量
   - 每條邊 e 有反向邊，容量 = 當前流量（允許「取消」流量）

2. 增廣路徑：
   - 從源點到匯點的一條路徑，所有邊的殘留容量都 > 0

3. 迭代過程：
   while 存在增廣路徑:
      找出路徑上的最小殘留容量（瓶頸）
       沿著路徑更新殘留容量（正向減，反向加）
       總流量 += 瓶頸容量
```

### Edmonds-Karp 演算法

Edmonds-Karp 是 Ford-Fulkerson 的具體實現，使用 BFS 來尋找最短的增廣路徑。

**時間複雜度**：O(V * E²)
**空間複雜度**：O(V + E)

### 最大流最小割定理

```
定理：在任何流網路中，最大流的流量等於最小割的容量。

最小割（Minimum Cut）：
- 將節點分成兩個集合 S 和 T（源點在 S，匯點在 T）
- 割的容量 = 所有從 S 到 T 的邊的容量之和
- 最小割 = 容量最小的割
```

## 殘留網路與反向邊

反向邊是 Ford-Fulkerson 方法的關鍵創新：

```
原始邊：u --(容量 c)--> v
當發送 f 單位流量後：
  正向邊殘留：u --(c-f)--> v
  反向邊：    u <--(f)-- v

反向邊允許演算法「反悔」，將流量重新分配到其他路徑。
```

## 程式碼說明

### Edmonds-Karp 核心

```python
def edmonds_karp(source, sink):
    max_flow = 0
    while True:
        # BFS 找增廣路徑
        path, bottleneck = bfs_path(source, sink)
        if path is None:
            break

        # 更新殘留網路
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            graph[u][v] -= bottleneck  # 正向減
            graph[v][u] += bottleneck  # 反向加

        max_flow += bottleneck
    return max_flow
```

### 最小割的找法

```
從源點出發，在殘留網路中進行 BFS/DFS，
所有可達的節點構成最小割的源點側 S，
其餘節點構成匯點側 T。
```

## 應用場景

### 1. 網路頻寬分配

在電腦網路中，計算兩點之間的最大資料傳輸率。

### 2. 交通流量規劃

城市交通網路中，計算從起點到終點的最大車流量。

### 3. 二分圖匹配

最大流可以用來解決二分圖的最大匹配問題。

### 4. 專案排程

在關鍵路徑法中，計算專案的最短完成時間。

## 圖例

```
示例網路：

       (10)  a ----(4)---- b
      /     / \           |
    s(10)  /   \          (10)
      \   (2)  (8)        |
       \   \     \        |
        c ----(9)--- d ---+
             
最大流 = 19
```

## 演算法比較

| 演算法 | 時間複雜度 | 說明 |
|--------|-----------|------|
| Ford-Fulkerson | O(E * max_flow) | 可能很慢，取決於容量 |
| Edmonds-Karp | O(V * E²) | 多項式時間，穩定 |
| Dinic | O(V² * E) | 實務上更快 |
| Push-Relabel | O(V² * E) | 適合稠密圖 |

## 參考資料

- Ford, L. R., & Fulkerson, D. R. (1956). *Maximal flow through a network*. Canadian Journal of Mathematics, 8, 399-404.
- Edmonds, J., & Karp, R. M. (1972). *Theoretical improvements in algorithmic efficiency for network flow problems*. Journal of the ACM, 19(2), 248-264.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 26)
