# 狀態空間搜尋：廣度優先與深度優先 (BFS and DFS for State Space Search)

## 歷史背景

廣度優先搜尋（BFS）由 Edward F. Moore 於 1959 年提出，最初用於解決迷宮最短路徑問題。深度優先搜尋（DFS）的概念可追溯至 19 世紀末 Charles Sanders Peirce 對邏輯推理的研究。

這兩個演算法是人工智慧領域中狀態空間搜尋的基礎，廣泛應用於問題求解、遊戲 AI、自動規劃等領域。

## 與圖論 BFS/DFS 的差異

| 特性 | 圖論 BFS/DFS | 狀態空間 BFS/DFS |
|------|-------------|-----------------|
| 搜尋對象 | 固定圖結構的節點與邊 | 動態生成的狀態空間 |
| 鄰居定義 | 圖的相鄰節點 | 透過「動作」產生的新狀態 |
| 目標 | 遍歷或尋找特定節點 | 找到從初始狀態到目標狀態的路徑 |
| 擴展方式 | 靜態鄰接表/矩陣 | 動態呼叫 `get_actions()` 和 `get_next_state()` |

## 核心原理

### 廣度優先搜尋（BFS）

```
1. 將初始狀態放入佇列
2. 當佇列不為空時：
   a. 取出佇列前端的狀態
   b. 若為目標狀態，返回路徑
   c. 將所有未訪問的鄰居狀態加入佇列
3. 若佇列為空仍未找到目標，則無解
```

- **資料結構**：佇列（Queue，FIFO）
- **性質**：保證找到步數最少的解（最淺解）
- **時間複雜度**：O(b^d)，b 為分支因子，d 為解的深度
- **空間複雜度**：O(b^d)，需儲存所有已訪問節點

### 深度優先搜尋（DFS）

```
1. 將初始狀態放入堆疊
2. 當堆疊不為空時：
   a. 取出堆疊頂端的狀態
   b. 若為目標狀態，返回路徑
   c. 將所有未訪問的鄰居狀態加入堆疊
3. 若堆疊為空仍未找到目標，則無解
```

- **資料結構**：堆疊（Stack，LIFO）
- **性質**：深度優先探索，不保證最短路徑
- **時間複雜度**：O(b^m)，m 為最大深度
- **空間複雜度**：O(bm)，優於 BFS
- **深度限制**：可加入深度限制避免無限遞迴

## 應用範例

### 8-拼圖問題

3×3 的滑動拼圖，目標是將打亂的數字重新排列成目標順序。

```python
from search.bfs_dfs_ai import EightPuzzleProblem, bfs_search

initial = [1, 2, 3, 4, 0, 5, 6, 7, 8]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

puzzle = EightPuzzleProblem(initial, goal)
result = bfs_search(puzzle)

if result:
    print(f"找到解，步數：{len(result.actions)}")
```

### 水壺問題

給定兩個不同容量的水壺，透過裝滿、倒空、互相倒水等操作，量出特定體積的水。

```python
from search.bfs_dfs_ai import WaterJugProblem, bfs_search

# 3 加侖和 5 加侖的水壺，量出 4 加侖
problem = WaterJugProblem(capacity1=3, capacity2=5, goal=4)
result = bfs_search(problem)
```

## 在人工智慧中的應用

1. **問題求解**：規劃路徑、拼圖、謎題
2. **遊戲 AI**：棋類遊戲的基礎搜尋
3. **自動規劃**：機器人路徑規劃、任務規劃
4. **約束滿足問題**：透過狀態枚舉尋找滿足條件的解

## 參考資料

- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Moore, E. F. (1959). The shortest path through a maze. *Proceedings of the International Symposium on Theory of Switching*.
- Pearl, J. (1984). *Heuristics: Intelligent Search Strategies for Computer Problem Solving*. Addison-Wesley.
