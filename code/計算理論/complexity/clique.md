# 團問題 (Clique Problem)

## 歷史背景

團 (Clique) 是圖論中的經典 NP-Complete 問題。

### 重要里程碑

- **1972 年**：Karp 證明了 Clique 是 NP-Complete 的
- **應用**：社交網絡分析（找社群）、生物資訊學（蛋白質交互）、電路設計

## 核心概念

### 問題描述

> 給定一個圖 G=(V,E) 和整數 k，
> 是否存在大小為 k 的團（完全子圖）？

### 團的定義

**團**：圖 G 的子圖，其中每對頂點之間都有邊相連。

**例子**：
```
頂點：{0, 1, 2, 3}
邊：(0,1), (1,2), (2,3), (0,2)
→ {0, 1, 2} 是一個大小為 3 的團
```

## 程式碼說明

### `brute_force_clique(vertices, edges, k)` - 暴力求解

```python
# 列舉所有 k-頂點組合
for combo in itertools.combinations(vertices, k):
    # 檢查是否為團（每對頂點都有邊）
    for i in range(len(combo)):
        for j in range(i+1, len(combo)):
            if combo[j] not in adj[combo[i]]:
                is_clique = False
```

**時間複雜度**：O(C(|V|, k) × k²) - 指數時間。

### `greedy_clique(vertices, edges)` - 貪婪啟發式

```python
while candidates:
    # 選取與當前團中最多頂點相連的候選人
    for v in candidates:
        count = sum(1 for u in clique if u in adj[v])
    # 如果與 clique 中所有頂點相連，加入
    if all(best in adj[u] for u in clique):
        clique.add(best)
```

**時間複雜度**：O(|V|²) - 多項式時間，但**不保證最優解**。

## 使用範例

```python
from theory.complexity.clique import create_example_graph, brute_force_clique

# 建立範例
vertices, edges = create_example_graph()
print(vertices)  # [0, 1, 2, 3, 4]

# 暴力求解 k=3
exists, clique = brute_force_clique(vertices, edges, 3)
print(exists)  # True
print(clique)   # {0, 1, 2}
```

## 執行測試

```bash
python theory/complexity/clique.py
```

輸出：
```
=== 團問題 (Clique Problem) 測試 ===

頂點：[0, 1, 2, 3, 4]
邊：[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]

暴力求解 k=3：
  是否存在大小為 3 的團：True
  團：{0, 1, 2}

暴力求解 k=4：
  是否存在大小為 4 的團：False

貪婪啟發式：
  找到的團：{0, 1, 2}
  大小：3
```

## 與 SAT 的歸約

**3-SAT ≤p Clique**：

1. 每個子句對應一個組（組的大小 = 子句長度）
2. 每個文字是一個頂點：(子句索引, 文字)
3. 連接「相容」的頂點對（不同子句，且文字不矛盾）
4. 存在大小 = 子句數的團 ⇔ 公式可滿足

## 參考資料

- Karp, R. M. (1972). [Reducibility among combinatorial problems](https://doi.org/10.1007/978-1-4684-2001-2_9). In *Complexity of Computer Computations* (pp. 85-103). Plenum Press.
- Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.
