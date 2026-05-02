# Push-Relabel 演算法

## 歷史背景

Push-Relabel 演算法由 Alexander Goldberg 和 Robert Tarjan 於 1986 年提出，
發表在論文《A New Approach to the Maximum Flow Problem》中。這是繼
Ford-Fulkerson 方法之後，最大流領域的重大突破。

 Goldberg 和 Tarjan 的貢獻：
- 首次提出使用前饋（preflow）而非守恆流的概念
- 引入高度函數（height function）指導流量推送
- 實現了比傳統增廣路方法更快的時間複雜度

 後續改進包括：
- 1993 年：Goldberg 引入 Gap heuristic，將複雜度降至 O(n²√m)
- 1996 年：Boykov-Kolmogorov 算法在實踐中表現優秀
- 2004 年：Orlin 提出了 O(nm) 或更快的算法

## 核心原理

### 傳統方法 vs Push-Relabel

**Ford-Fulkerson（增廣路方法）**：
- 每次找一條增廣路
- 沿路徑推送流量
- 維持流守恆（每節點進 = 出）

**Push-Relabel（前饋方法）**：
- 允許暫時的「溢位」（excess flow）
- 使用高度函數控制流向
- 最後消除溢位得到合法最大流

### 關鍵概念

1. **Preflow（前饋）**：
   - 流入節點的流量可以超過流出流量
   - 每條邊的流量 ≤ 容量
   - 滿足流量反對稱性（flow[u][v] = -flow[v][u]）

2. **Height Function（高度函數）**：
   - h(s) = n（源點最高）
   - h(t) = 0（匯點最低）
   - 流量只能從高度 h 流向 h' < h 的節點
   - 有效防止無效的來回推送

3. **Excess Flow（溢位流量）**：
   - excess[u] = 總流入量 - 總流出量
   - excess[u] > 0 表示節點 u 有溢位需要推送

### Push 操作

```
Push(u, v):
  如果 h[u] = h[v] + 1 且 capacity[u][v] - flow[u][v] > 0
    推送 min(excess[u], capacity[u][v] - flow[u][v]) 的流量
```

### Relabel 操作

```
Relabel(u):
  如果 u 有溢位但無法推送
  找到所有相鄰可推送的節點
  h[u] = min(h[v]) + 1（其中 v 可接收流量）
```

### Gap Heuristic

當某個高度級別沒有節點時，所有高度更高的節點都不可能到達匯點，
可以將它們的高度標記為 n+1（無效），大幅減少搜索空間。

## 演算法步驟

```
Push-Relabel(G, s, t):
  1. 初始化：
     - h[s] = n, 其他 h[v] = 0
     - 從 s 流出所有可能的流量到相鄰節點
     - 計算每個節點的 excess

  2. 當存在溢位節點時：
     a. 選取一個溢位節點 u
     b. 如果可以推送，執行 Push(u, v)
     c. 否則執行 Relabel(u)

  3. 返回 max flow = excess[t]
```

## 時間複雜度

| 版本 | 時間複雜度 |
|------|----------|
| 基本版本 | O(n³) |
| FIFO 實現 | O(n³) |
| Highest-Label | O(n²√m) |
| Gap Heuristic | O(n²) for dense graphs |

其中：
- n = 節點數
- m = 邊數

## 使用範例

```python
from push_relabel import PushRelabel

# 建立 6 節點網絡
pr = PushRelabel(6, source=0, sink=5)

# 添加邊（起點, 終點, 容量）
pr.add_edge(0, 1, 16)
pr.add_edge(0, 2, 13)
pr.add_edge(1, 3, 12)
pr.add_edge(2, 4, 14)
pr.add_edge(3, 5, 20)
pr.add_edge(4, 5, 4)

# 計算最大流
maxflow = pr.max_flow()
print(f"最大流: {maxflow}")  # 輸出: 23

# 取得最小割
cut = pr.get_min_cut()
print(f"最小割節點: {cut}")
```

## 與 Edmonds-Karp 的比較

| 特性 | Push-Relabel | Edmonds-Karp |
|------|-------------|--------------|
| 時間複雜度 | O(n³) | O(nm²) |
| 實際效能 | 通常更快 | 實現簡單 |
| Gap Heuristic | 支持 | 不適用 |
| 實現難度 | 中等 | 簡單 |

## 參考資料

1. Goldberg, A.V., & Tarjan, R.E. (1986). A new approach to the maximum flow problem. STOC '86.
2. Goldberg, A.V. (1993). Scaling algorithms for the shortest paths problem. SIAM Journal on Computing.
3. Cormen, T.H., et al. (2009). Introduction to Algorithms, Chapter 26. MIT Press.