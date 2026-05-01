# 旅行推銷員問題 (Traveling Salesman Problem, TSP)

## 歷史背景

TSP 是組合最佳化中的經典 NP-hard 問題。

### 重要里程碑

- **1930 年代**：TSP 在維也納和哈佛同時被研究
- **1972 年**：Karp 證明了 TSP 是 NP-hard 的
- **至今**：仍是組合最佳化中最著名的問題之一

## 核心概念

### 問題描述

> 給定一組城市和它們之間的距離，
> 尋找一條經過每個城市恰好一次並回到起始城市的最短路徑。

### TSP 的變體

| 變體 | 說明 |
|------|------|
| 對稱 TSP | 距離矩陣對稱（i 到 j = j 到 i） |
| 非對稱 TSP | 距離矩陣可能不對稱 |
| 歐氏 TSP | 城市在平面上，距離為歐氏距離 |
| 度量 TSP | 滿足三角不等式 |

## 程式碼說明

### `brute_force_tsp(distances)` - 暴力求解

```python
# 列舉所有排列（固定起點為 0）
for perm in itertools.permutations(cities[1:]):
    path = [0] + list(perm) + [0]
    # 計算總距離
    for i in range(n):
        dist += distances[path[i]][path[i+1]]
```

**時間複雜度**：O(n!) - 指數時間，僅適用於很小的 n（n≤10）。

### `nearest_neighbor_tsp(distances)` - 最近鄰居啟發式

```python
# 從起點開始，每次選擇最近的未訪問城市
for _ in range(n - 1):
    for city in range(n):
        if not visited[city] and distances[current][city] < min_dist:
            nearest = city
    path.append(nearest)
    visited[nearest] = True
    current = nearest
```

**時間複雜度**：O(n²) - 多項式時間，但**不保證最優解**。

## 使用範例

```python
from theory.complexity.tsp import create_example_tsp, brute_force_tsp

# 建立範例
distances, cities = create_example_tsp()
print(cities)  # ['A', 'B', 'C', 'D']

# 暴力求解
path, dist = brute_force_tsp(distances)
print(path)  # [0, 2, 3, 1, 0] （A→C→D→B→A）
print(dist)  # 80
```

## 執行測試

```bash
python theory/compleity/tsp.py
```

輸出：
```
=== 旅行推銷員問題 (TSP) 測試 ===

城市： ['A', 'B', 'C', 'D']
距離矩陣：
  A: [0, 10, 15, 20]
  B: [10, 0, 35, 25]
  C: [15, 35, 0, 30]
  D: [20, 25, 30, 0]

暴力求解（適用於小 n）：
  最短路徑：A -> C -> D -> B -> A
  距離：80

最近鄰居啟發式：
  路徑：A -> B -> D -> C -> A
  距離：85

比較：
  最優解：80
  啟發式：85
  比率：1.06x
```

## TSP 的應用

1. **物流排程**：卡車配送路線規劃
2. **電路設計**：印刷電路板的鑽孔路徑
3. **基因組學**：DNA 序列組裝
4. **天文學**：望遠鏡觀測排程

## 近似演算法

由於 TSP 是 NP-hard，通常使用近似演算法：

| 演算法 | 近似比 | 時間複雜度 |
|---------|--------|--------------|
| 最近鄰居 | ≤ 2（度量 TSP） | O(n²) |
| 最小生成樹 | ≤ 2（度量 TSP） | O(n² log n) |
| Christofides | ≤ 1.5（度量 TSP） | O(n³) |

## 參考資料

- Karp, R. M. (1972). [Reducibility among combinatorial problems](https://doi.org/10.1007/978-1-4684-2001-2_9). In *Complexity of Computer Computations* (pp. 85-103). Plenum Press.
- Applegate, D. L., Bixby, R. E., Chvátal, V., & Cook, W. J. (2006). *The Traveling Salesman Problem: A Computational Study*. Princeton University Press.
- Gutin, G., & Punnen, A. P. (Eds.). (2006). *The Traveling Salesman Problem and Its Variations*. Springer.
