# 最小成本最大流 (Minimum Cost Maximum Flow)

## 歷史背景

最小成本流問題是經典最大流問題的推廣，不僅要最大化流量，還要最小化總運輸成本。

### 發展歷程

- **1951 年**：George Dantzig 提出線性規劃公式化
- **1961 年**：Busacker 和 Gowen 提出連續最短路徑演算法（Successive Shortest Path）
- **1970 年代**：Klein 提出負環消除演算法
- **現代應用**：運輸問題、網路路由、供應鏈優化

## 演算法原理

### 問題定義

給定一個流網路，每條邊除了容量限制外，還有單位流量的運輸成本。目標是：
1. 最大化從源點到匯點的流量
2. 在滿足最大流的前提下，最小化總成本

### 連續最短路徑演算法 (Successive Shortest Path)

```
核心概念：
1. 殘留網路：
   - 每條邊有殘留容量和成本
   - 反向邊的成本為正向邊成本的負值

2. 迭代過程：
   while 存在從源點到匯點的路徑:
       使用 Bellman-Ford 找「成本最短路徑」
       （考慮成本作為邊權重，僅考慮殘留容量 > 0 的邊）
       找出路徑上的瓶頸容量
       沿路徑增廣流量
       更新殘留網路（正向減容量，反向加容量）
       總成本 += 瓶頸容量 × 路徑成本

3. 終止：當不存在從源點到匯點的路徑時
```

### 為什麼使用 Bellman-Ford？

- 殘留網路中可能出現負成本邊（反向邊）
- Bellman-Ford 能處理負權重邊
- 時間複雜度 O(V * E)

### 成本殘留圖

```
原始邊：u --(容量 c, 成本 w)--> v
當發送 f 單位流量後：
  正向殘留：u --(c-f, w)--> v
  反向殘留：u <--(f, -w)-- v

反向邊的負成本允許演算法「反悔」並重新分配流量。
```

## 程式碼說明

### 核心資料結構

```python
class Edge:
    def __init__(self, u, v, capacity, cost):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.cost = cost
        self.reverse = None  # 指向反向邊
```

### 最短路徑搜尋

```python
def bellman_ford(self, source, sink):
    # 使用 Bellman-Ford 找成本最短路徑
    dist = {node: inf for node in nodes}
    dist[source] = 0

    for _ in range(len(nodes) - 1):
        for u in nodes:
            for edge in graph[u]:
                if edge.capacity > 0:  # 只考慮殘留容量 > 0
                    if dist[u] + edge.cost < dist[edge.v]:
                        dist[edge.v] = dist[u] + edge.cost
                        # 記錄前驅邊以便重建路徑
```

### 流量增廣

```python
def min_cost_max_flow(self, source, sink):
    total_flow = 0
    total_cost = 0

    while True:
        path, path_cost = bellman_ford(source, sink)
        if path is None:
            break

        bottleneck = min(edge.capacity for edge in path_edges)
        for edge in path_edges:
            edge.capacity -= bottleneck
            edge.reverse.capacity += bottleneck

        total_flow += bottleneck
        total_cost += bottleneck * path_cost

    return total_flow, total_cost
```

## 應用場景

### 1. 運輸問題

```
工廠（源點）要運送貨物到倉庫（匯點）
有多條路徑，每條路徑有不同的運輸成本
目標：最大化運輸量，同時最小化總運輸成本
```

### 2. 網路路由

在電腦網路中，選擇成本最低（延遲最小）的路徑傳輸資料，
同時最大化頻寬使用率。

### 3. 資源分配

雲端運算中，將任務分配給伺服器，考慮伺服器的處理能力和
通訊成本。

## 圖例

```
示例網路：

       (4,2)    (3,3)
    s ----> a -----> t
     \       |       ^
      \ (2,5)\|(1,1) | (3,2)
       \     v       /
        ----> b ----+

數字格式：(容量, 成本)
最小成本最大流：
  最大流量 = 4
  最小成本 = 4×2 + 1×1 + 1×3 + 3×2 = 17
```

## 演算法比較

| 演算法 | 時間複雜度 | 說明 |
|--------|-----------|------|
| 連續最短路徑 | O(V * E * F) | F 為最大流量 |
| 成本縮放演算法 | O(V * E * log V) | 更適合大流量 |
| 網路單純形法 | 實務上很快 | 線性規劃方法 |

## 參考資料

- Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). *Network Flows: Theory, Algorithms, and Applications*. Prentice Hall.
- Busacker, R. G., & Gowen, P. J. (1961). *A Procedure for Determining a Family of Minimum-Cost Network Flow Patterns*. Office of Technical Services.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 26)
