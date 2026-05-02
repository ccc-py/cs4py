# 強連通分量 (Strongly Connected Components, SCC)

## 歷史背景

強連通分量是有向圖中的一個重要概念。在有向圖中，如果對於任意兩個節點 u 和 v，都存在從 u 到 v 和從 v 到 u 的路徑，則稱該子圖為強連通分量。

### 演算法發展

- **1972 年**：Robert Tarjan 提出了基於深度優先搜尋的線性時間演算法
- **1978 年**：S. Rao Kosaraju 獨立提出了另一個基於兩次 DFS 的演算法
- Tarjan's algorithm 只需要一次 DFS，效率略高於 Kosaraju's algorithm

## 演算法原理

### Kosaraju's Algorithm

Kosaraju 演算法利用「圖的反轉」和「兩次 DFS」來找出強連通分量。

```
步驟：
1. 第一次 DFS（原圖）：
   - 對原圖進行深度優先搜尋
   - 記錄每個節點的完成時間（後序遍歷順序）

2. 反轉圖：
   - 將原圖的所有邊方向反轉
   - 如果原圖有邊 u → v，反轉圖就有邊 v → u

3. 第二次 DFS（反轉圖）：
   - 按照第一次 DFS 完成時間的逆序，對反轉圖進行 DFS
   - 每次 DFS 訪問到的所有節點構成一個強連通分量
```

**時間複雜度**：O(V + E)（需要兩次 DFS 和一次建反轉圖）
**空間複雜度**：O(V + E)

### Tarjan's Algorithm

Tarjan 演算法只需一次 DFS，使用 `disc`（發現時間）和 `low`（low-link value）兩個陣列。

```
核心概念：
- disc[u]：節點 u 被首次發現的時間
- low[u]：從 u 出發，通過樹邊和最多一條後向邊能到達的最早發現的節點

步驟：
1. 對圖進行 DFS，為每個節點分配 disc 和 low
2. 使用堆疊追踪當前 DFS 路徑上的節點
3. 當發現節點 u 滿足 low[u] == disc[u] 時：
   - u 是一個 SCC 的根節點
   - 從堆疊中彈出節點，直到彈出 u，這些節點構成一個 SCC
```

**時間複雜度**：O(V + E)（只進行一次 DFS）
**空間複雜度**：O(V)

## Low-link Value 解釋

Low-link value 是 Tarjan 演算法的核心概念：

```
low[u] = min(
    disc[u],                    # 自己的發現時間
    disc[v] for each v where u -> v is a tree edge and v is visited,
    disc[w] for each w where u -> w is a back edge
)
```

當 `low[u] == disc[u]` 時，表示從 u 無法通過其子樹到達更早的節點，因此 u 是一個 SCC 的根。

## 程式碼說明

### Tarjan 核心程式碼

```python
def strongconnect(node):
    indices[node] = index_counter
    lowlinks[node] = index_counter
    index_counter += 1
    stack.append(node)
    on_stack.add(node)

    for neighbor in graph[node]:
        if neighbor not in indices:
            strongconnect(neighbor)
            lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
        elif neighbor in on_stack:
            lowlinks[node] = min(lowlinks[node], indices[neighbor])

    if lowlinks[node] == indices[node]:
        # node 是 SCC 的根
        component = []
        while True:
            w = stack.pop()
            on_stack.remove(w)
            component.append(w)
            if w == node:
                break
        sccs.append(component)
```

## 應用場景

### 1. 編譯器優化

在編譯器中，SCC 可以用來分析程式中的循環依賴，進行相關優化。

### 2. 社群網絡分析

找出社交網絡中互相連接緊密的群體。

### 3. 電路設計

分析電路中的反饋迴路。

### 4. 依賴分析

檢測軟體包之間的循環依賴。

## 演算法比較

| 特性 | Kosaraju | Tarjan |
|------|----------|--------|
| DFS 次數 | 2 次 | 1 次 |
| 需要反轉圖 | 是 | 否 |
| 時間複雜度 | O(V + E) | O(V + E) |
| 實現難度 | 較簡單 | 較複雜 |
| 實際效率 | 稍慢 | 較快 |

## 圖例

```
示例圖（包含 3 個 SCC）:

    A ←── E
   ↙ ↓     ↓
  B   ↓     F ←── G
   ↘ ↓     ↑     ↑
      C → D       (F ↔ G 形成循環)

SCC1: {A, B, E}
SCC2: {C, D}
SCC3: {F, G}
```

## 參考資料

- Tarjan, R. (1972). *Depth-first search and linear graph algorithms*. SIAM Journal on Computing, 1(2), 146-160.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 22.5)
- Kosaraju, S. R. (1978). *Unpublished notes*.
