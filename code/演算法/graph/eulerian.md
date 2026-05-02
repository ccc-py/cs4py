# 歐拉路徑與歐拉迴路 (Eulerian Path and Circuit)

## 歷史背景

歐拉路徑問題是圖論的第一個問題，起源於著名的「柯尼斯堡七橋問題」。

### 柯尼斯堡七橋問題（1736 年）

柯尼斯堡（今俄羅斯加里寧格勒）有七座橋連接普雷戈爾河上的兩個島嶼和兩岸。市民們想知道：是否存在一條路徑，恰好經過每座橋一次？

```
柯尼斯堡的地圖：

    北岸(A)
     /  |  \
    /   |   \
  橋1  橋2  橋3
   /    |    \
  /     |     \
東島(C) 橋4  西島(D)
  \     |     /
   \    |    /
    \   |   /
    橋5 橋6 橋7
      \ | /
       南岸(B)
```

### Euler 的貢獻

Leonhard Euler 在 1736 年證明：**不存在這樣的路徑**。他將問題抽象化為圖論問題，建立了歐拉路徑的判定條件，這標誌著圖論的誕生。

## 定義與判定條件

### 歐拉路徑 (Eulerian Path)

- 經過圖中每條邊恰好一次的路徑
- 不要求起點等於終點

### 歐拉迴路 (Eulerian Circuit)

- 經過圖中每條邊恰好一次的迴路
- 起點等於終點

### 無向圖的判定條件

| 條件 | 歐拉路徑 | 歐拉迴路 |
|------|---------|---------|
| 連通性 | 必須連通 | 必須連通 |
| 奇數度節點數 | 0 或 2 | 必須為 0 |
| 起點/終點 | 奇數度節點（若有） | 任意節點 |

### 有向圖的判定條件

| 條件 | 歐拉路徑 | 歐拉迴路 |
|------|---------|---------|
| 連通性 | 必須連通 | 必須連通 |
| 入度 vs 出度 | 最多一個節點出度-入度=1（起點）<br>最多一個節點入度-出度=1（終點） | 所有節點入度==出度 |

## Hierholzer's Algorithm

Hierholzer 演算法是找出歐拉路徑/迴路的有效方法。

### 演算法步驟

```
1. 選擇起點（有歐拉迴路則任意選，有歐拉路徑則選奇數度節點）
2. 開始 DFS，隨機選擇未使用的邊走
3. 當走到某個節點沒有未使用的邊時，將該節點加入路徑
4. 回溯，繼續處理還有未使用邊的節點
5. 最後將路徑反轉即為答案
```

### 圖示

```
找到子迴路：A -> B -> C -> A
插入子迴路：A -> B -> D -> B -> C -> A

最終路徑：A -> B -> D -> B -> C -> A
```

**時間複雜度**：O(E)，其中 E 是邊數
**空間複雜度**：O(E)

## 程式碼說明

### 無向圖判定

```python
def is_eulerian_undirected(graph):
    # 計算度數
    degree = defaultdict(int)
    for node in graph:
        degree[node] += len(graph[node])

    # 統計奇數度節點
    odd_degree_nodes = [n for n in degree if degree[n] % 2 == 1]

    has_circuit = len(odd_degree_nodes) == 0
    has_path = len(odd_degree_nodes) == 0 or len(odd_degree_nodes) == 2

    return has_path, has_circuit
```

### Hierholzer 核心

```python
def hierholzer(graph, start):
    stack = [start]
    path = []

    while stack:
        current = stack[-1]
        if edges[current]:  # 還有未使用的邊
            next_node = edges[current].pop()
            stack.append(next_node)
        else:
            path.append(stack.pop())

    path.reverse()
    return path
```

## 應用場景

### 1. 郵差問題

郵差要經過每條街道恰好一次，回到郵局（中國郵差問題是變體）。

### 2. 路線規劃

垃圾車、掃街車等需要經過每條街道的路線規劃。

### 3. 基因組組裝

在 DNA 序列組裝中，歐拉路徑用於重建基因序列。

### 4. 電路設計

測試電路板的每一條線路是否能被一條探針路徑覆蓋。

## 柯尼斯堡七橋為什麼無解？

```
區域的度數：
- 北岸(A): 3（奇數）
- 南岸(B): 3（奇數）
- 東島(C): 5（奇數）
- 西島(D): 3（奇數）

共有 4 個奇數度節點，不符合歐拉路徑條件（最多 2 個）。
```

## 參考資料

- Euler, L. (1736). *Solutio problematis ad geometriam situs pertinentis*. Commentarii academiae scientiarum Petropolitanae, 8, 128-140.
- Hierholzer, C. (1873). *Ueber die Möglichkeit, einen Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren*. Mathematische Annalen, 6(1), 30-32.
- Fleischner, H. (1990). *Eulerian Graphs and Related Topics*. North-Holland.
