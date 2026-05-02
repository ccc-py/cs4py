# 拓撲排序 (Topological Sort)

## 歷史背景

拓撲排序是針對有向無環圖（DAG, Directed Acyclic Graph）的一種排序方法，將圖中的節點排成一個線性序列，使得對於圖中的每一條有向邊 (u → v)，u 在序列中都出現在 v 之前。

### 發展歷程

- **拓扑学起源**：拓撲排序的概念源自拓撲學
- **1962 年**：Arthur B. Kahn 提出了基於入度的 BFS 演算法（Kahn's Algorithm）
- **1970 年代**：深度優先搜尋（DFS）版本的拓撲排序被廣泛應用

## 演算法原理

### Kahn's Algorithm（基於入度的 BFS）

```
1. 計算所有節點的入度（有多少邊指向該節點）
2. 將所有入度為 0 的節點放入佇列
3. 當佇列不為空時：
   a. 取出佇列中的一個節點 u，加入結果序列
   b. 對於 u 的每個鄰居 v：
      - 減少 v 的入度
      - 如果 v 的入度變為 0，將 v 加入佇列
4. 如果結果序列的長度等於節點數，排序成功；否則圖中存在循環
```

**時間複雜度**：O(V + E)，其中 V 是節點數，E 是邊數
**空間複雜度**：O(V)

### DFS-based Algorithm（深度優先搜尋）

```
1. 對每個未訪問的節點進行 DFS
2. 在 DFS 完成後（後序位置），將節點加入結果
3. 最後反轉結果序列
4. 使用遞迴堆疊（recursion stack）檢測循環
```

**時間複雜度**：O(V + E)
**空間複雜度**：O(V)（遞迴呼叫堆疊）

## 迴圈檢測

拓撲排序只能用於有向無環圖（DAG）。如果圖中存在循環，則無法進行拓撲排序。

### 檢測方法

1. **Kahn's Algorithm**：如果最後結果序列的長度小於節點總數，表示存在循環
2. **DFS Method**：使用遞迴堆疊（rec_stack）追蹤當前 DFS 路徑，如果遇到已在當前路徑上的節點，則存在循環

## 程式碼說明

### Kahn's Algorithm 核心

```python
def topological_sort_kahn(graph):
    # 計算入度
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # 入度為 0 的節點入隊
    queue = deque([n for n in in_degree if in_degree[n] == 0])

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
```

### DFS-based 核心

```python
def dfs(node):
    visited.add(node)
    rec_stack.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)
        elif neighbor in rec_stack:
            # 檢測到循環

    rec_stack.remove(node)
    result.append(node)  # 後序位置
```

## 應用場景

### 1. 課程排程

大學課程的先修關係規劃，確保學生按照正確順序修課。

```
CS101 (計算機概論)
  └── CS201 (資料結構)
        ├── CS301 (演算法)
        └── CS302 (作業系統)
              └── CS401 (編譯器)
```

### 2. 編譯器依賴分析

在編譯程式時，確定各個模組的編譯順序。

### 3. 建構系統

如 Make、Gradle 等工具，根據依賴關係決定編譯順序。

### 4. 工作流程排程

專案管理中的任務依賴關係，決定任務執行順序。

## 複雜度比較

| 演算法 | 時間複雜度 | 空間複雜度 | 循環檢測 |
|--------|-----------|-----------|---------|
| Kahn's Algorithm | O(V + E) | O(V) | 容易（結果長度 < V） |
| DFS-based | O(V + E) | O(V) | 需要額外遞迴堆疊追蹤 |

## 參考資料

- Kahn, A. B. (1962). *Topological sorting of large networks*. Communications of the ACM, 5(11), 558-562.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 22.4)
- Knuth, D. E. (1997). *The Art of Computer Programming, Volume 1: Fundamental Algorithms* (3rd ed.). Addison-Wesley.
