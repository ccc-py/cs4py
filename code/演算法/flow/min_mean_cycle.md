# 最小平均權重環（Minimum Mean Cycle）

## 歷史背景

### Karp 的突破

1968 年，Richard Karp在日本舉行的資訊科學研討會上發表了這篇論文：
《A Deterministic O(n²m) Algorithm for the Minimum Mean Cycle》
（確定性 O(n²m) 最小平均環演算法）

這個發現的重要性：
- 首次使用動態規劃思想處理環檢測問題
- 為後續的環分析演算法奠定基礎
- 應用於馬爾可夫鏈的平穩分佈計算

### 應用領域

1. **馬爾可夫鏈分析**
   - 計算平均回訪時間
   - 分析鏈的長期行為
   - 解決 " Gambler's Ruin " 類問題

2. **網絡優化**
   - 電信網絡的最小成本環
   - 航空網絡的線路規劃
   - 交通網絡的拥塞檢測

3. **電路設計**
   - 時序分析中的臨界環
   - 晶片設計中的時鐘調度

## 核心原理

### 問題定義

給定有向圖 G = (V, E)，每條邊有權重 w(e)，
找到一個環 C，使得：
```
mean(C) = Σ w(e) / |C|  最小化
```

### Karp 演算法的直覺

利用動態規劃計算所有節點對的最短路徑，
然後利用這些資訊找到最小平均環。

**關鍵觀察**：
對於任意節點 v，考慮：
- dist[k][v][v]：從 v 回到 v 恰好經過 k 條邊的最短路徑

如果圖中存在環，那麼對於某個 k ≥ 1：
```
dist[k][v][v] - dist[0][v][v] = dist[k][v][v]
```
代表 v 到 v 的環的最短路徑。

### 平均值的界

對於 n 個節點的圖，最小平均環必包含在 [1, n] 條邊之間：
- 小於 n 條邊的環：直接計算
- 正好 n 條邊的環：使用 dist[n][v][v]

## 演算法步驟

```
MinimumMeanCycle(G):
  1. 初始化：
     dist[0][u][v] = 0 if u = v, else ∞

  2. 對於 k = 1 到 n：
     對於每條邊 (u, v, w)：
       dist[k][u][v] = min(dist[k-1][u][v], dist[k-1][u][u] + w)

  3. 對於每個節點 v：
     mean_v = dist[n][v][v] / n
     如果 dist[n][v][v] < ∞，更新全局最小值

  4. 重構最小環並返回
```

## 複雜度分析

| 步驟 | 時間複雜度 |
|------|----------|
| 初始化 | O(n²) |
| DP 計算（n 次迭代）| O(n × m) |
| 最小值搜尋 | O(n) |
| **總時間** | **O(nm)** |

其中：
- n = 節點數
- m = 邊數

## 與其他演算法的比較

| 演算法 | 時間複雜度 | 適用場景 |
|--------|-----------|---------|
| Karp | O(nm) | 一般情況 |
| Floyd-Warshall 變體 | O(n³) | 稠密圖 |
| 枚舉法 | O(n!) | 教學用途 |

## 使用範例

```python
from min_mean_cycle import DiGraph, MinimumMeanCycle

g = DiGraph(4)
g.add_edge(0, 1, 1.0)
g.add_edge(1, 2, 2.0)
g.add_edge(2, 0, 3.0)
g.add_edge(2, 3, 1.0)
g.add_edge(3, 1, 4.0)

solver = MinimumMeanCycle(g)
mean, cycle = solver.find_min_mean_cycle()

print(f"最小平均權重: {mean}")
print(f"環: {cycle}")
```

## 進階應用

### 1. 馬爾可夫鏈的平均回報

對於轉移機率矩陣 P，平均回報時間等於
最小平均環的倒數。

### 2. 網絡成本優化

在通信網絡中找最小成本環，可用於：
- 備援路徑規劃
- 網絡分割檢測

### 3. 博弈論中的循環局面

在有限博弈中，量化每個循環的 "價值"。

## 參考資料

1. Karp, R.M. (1968). A Deterministic O(n²m) Algorithm for the Minimum Mean Cycle. IFIP Congress.
2. Karp, R.M., & Held, M. (1967). Minimum-height binary tree insertion. SIAM Journal on Applied Mathematics.
3. Cormen, T.H., et al. (2009). Introduction to Algorithms, Chapter 25. MIT Press.
4. Lawler, E.L. (2001). Combinatorial Optimization: Networks and Matroids. Dover Publications.