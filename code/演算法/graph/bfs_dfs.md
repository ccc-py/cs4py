# 圖的遍歷：廣度優先搜索 (BFS) 和深度優先搜索 (DFS)

## 歷史背景

圖遍歷是圖論中的基礎算法，應用於網路路由、社交網路分析、迷宮求解等領域。

- **BFS**：由 E. F. Codd 的學生於 1959 年提出
- **DFS**：概念源於早期人工智慧研究的迷宮搜索

## BFS vs DFS

| 特性 | BFS | DFS |
|------|-----|-----|
| 資料結構 | 佇列 (Queue) | 堆疊 (Stack) |
| 遍歷順序 | 按層級（由近到遠） | 深度優先（儘量深入） |
| 空間複雜度 | O(V) | O(V) |
| 最短路徑 | 可找到 | 不保證 |
| 適合場景 | 最短路徑、層級關係 | 拓撲排序、連通分量 |

## 廣度優先搜索 (BFS)

### 原理

```
1. 從起點開始，將其加入佇列
2. 取出佇列前端節點，訪問它
3. 將所有未訪問的相鄰節點加入佇列
4. 重複直到佇列為空
```

### 圖示

```
       0
      / \
     1   2
    / \ / \
   3   4 5   6

BFS 從 0 開始：
層級 0：0
層級 1：1, 2
層級 2：3, 4, 5, 6
順序：[0, 1, 2, 3, 4, 5, 6]
```

### 程式碼

```python
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        vertex = queue.popleft()
        if vertex in visited:
            continue

        visited.add(vertex)
        result.append(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                queue.append(neighbor)

    return result
```

### 應用

- **最短路徑**：在无权图中，BFS 找到的是边数最少的最短路径
- **二分圖檢測**：用兩種顏色交替染色
- **連通分量計算**：洪水填充演算法的基礎

## 深度優先搜索 (DFS)

### 原理

```
1. 從起點開始，訪問並標記
2. 選擇一個未訪問的相鄰節點，遞迴訪問
3. 退回並選擇下一個分支（回溯）
4. 直到所有節點都被訪問
```

### 圖示

```
       0
      / \
     1   2
    / \ / \
   3   4 5   6

DFS 從 0 開始（一個可能的順序）：
[0, 1, 3, 4, 2, 5, 6]
```

### 程式碼

```python
def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    result.append(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

    return result
```

### 應用

- **拓撲排序**：依賴關係排序
- **連通分量**：深度優先搜索可找到所有連通分量
- **路徑搜索**：可以記錄路徑
- **生成迷宮**：DFS 生成迷宮

## 複雜度分析

| 演算法 | 時間複雜度 | 空間複雜度 |
|--------|-----------|-----------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |

- V：頂點數
- E：邊數

## Tarjan's Algorithm（連通分量）

DFS 的經典應用：用於找到有向圖中的強連通分量

```python
def tarjan_scc(graph):
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlinks = {}
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph[v]:
            if w not in indices:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in on_stack:
                lowlinks[v] = min(lowlinks[v], indices[w])

        if lowlinks[v] == indices[v]:
            scc = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.add(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in graph:
        if v not in indices:
            strongconnect(v)

    return sccs
```

## 實用考量

1. **遞迴深度**：大量節點時注意 Python 的遞迴限制
2. **記憶體**：BFS 需要儲存整層節點，DFS 需要儲存呼叫堆疊
3. **圖的表示**：鄰接矩陣 vs 鄰接列表的選擇

```python
import sys
sys.setrecursionlimit(10000)  # 增加遞迴深度限制
```

## 參考資料

- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Sedgewick, R. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- Tarjan, R. E. (1972). [Depth-First Search and Linear Graph Algorithms](https://doi.org/10.1137/0201010). *SIAM Journal on Computing*, 1(2), 146-160.