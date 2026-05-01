# 頂點覆蓋問題 (Vertex Cover Problem)

## 歷史背景

頂點覆蓋 (Vertex Cover) 是圖論中的經典 NP-Hard 問題。

### 重要里程碑

- **1972 年**：Karp 證明了 Vertex Cover 是 NP-Hard 的
- **應用**：網絡安全、生物資訊學、電路測試
- **近似演算法**：2-近似（最優解的 2 倍以內）

## 核心概念

### 問題描述

> 給定一個圖 G=(V,E) 和整數 k，
> 是否存在大小為 k 的頂點集合 S ⊆ V，
> 使得每條邊都至少有一個端點在 S 中？

### 頂點覆蓋的定義

**頂點覆蓋**：圖 G 的頂點子集 S，使得每條邊至少有一個端點在 S 中。

**例子**：
```
頂點：{0, 1, 2, 3, 4}
邊：(0,1), (0,2), (1,2), (2,3), (3,4)
→ {0, 2, 3} 是一個大小為 3 的頂點覆蓋
```

## 程式碼說明

### `brute_force_vertex_cover(vertices, edges, k)` - 暴力求解

```python
# 列舉所有 k-頂點組合
for combo in itertools.combinations(vertices, k):
    cover = set(combo)
    # 檢查是否覆蓋所有邊
    for u, v in edges:
        if u not in cover and v not in cover:
            is_cover = False
```

**時間複雜度**：O(C(|V|, k) × |E|) - 指數時間。

### `greedy_vertex_cover(vertices, edges)` - 貪婪啟發式

```python
while uncovered_edges:
    # 選擇度數最大的頂點
    for v in vertices:
        degree = sum(1 for u, w in uncovered_edges if u == v or w == v)
    # 加入覆蓋並移除相關邊
    cover.add(best)
    uncovered_edges = {(u, w) for u, w in uncovered_edges 
                    if u != best and w != best}
```

**時間複雜度**：O(|V|²) - 多項式時間，但**不保證最優解**。

### 與 Clique 的歸約

**定理**：G 有大小為 k 的團 ⇔ 補圖 G' 有大小為 |V|-k 的頂點覆蓋。

**思路**：
1. 團中的頂點在補圖中沒有邊相連
2. 因此這些頂點在補圖中需要被覆蓋的邊都不與它們相連
3. 只需要覆蓋剩下的頂點

## 使用範例

```python
from theory.complexity.vertex_cover import create_example_graph, brute_force_vertex_cover

# 建立範例
vertices, edges = create_example_graph()
print(vertices)  # [0, 1, 2, 3, 4]

# 暴力求解 k=3
exists, cover = brute_force_vertex_cover(vertices, edges, 3)
print(exists)  # True
print(cover)    # {0, 2, 3}
```

## 執行測試

```bash
python theory/complexity/vertex_cover.py
```

輸出：
```
=== 頂點覆蓋問題 (Vertex Cover) 測試 ====

頂點：[0, 1, 2, 3, 4]
邊：[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]

暴力求解 k=3：
  是否存在大小為 3 的頂點覆蓋：True
  頂點覆蓋：{0, 2, 3}

暴力求解 k=2：
  是否存在大小為 2 的頂點覆蓋：False

貪婪啟發式：
  找到的頂點覆蓋：{0, 2, 3}
  大小：3
```

## 近似演算法

| 演算法 | 近似比 | 時間複雜度 |
|---------|--------|--------------|
| 貪婪啟發式 | ≤ 2 | O(|V|²) |
| 線性規劃捨捨 | ≤ 2 | O(|V|³) |
| 局部搜尋 | ≤ 2-ε | 較慢 |

## 參考資料

- Karp, R. M. (1972). [Reducibility among combinatorial problems](https://doi.org/10.1007/978-1-4684-2001-2_9). In *Complexity of Computer Computations* (pp. 85-103). Plenum Press.
- Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.
- Vazirani, V. V. (2001). *Approximation Algorithms*. Springer.
