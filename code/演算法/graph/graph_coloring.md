# 圖著色 (Graph Coloring / Vertex Coloring)

## 歷史背景

圖著色問題起源於著名的四色猜想，是圖論中最著名的問題之一。

### 發展歷程

- **1852 年**：Francis Guthrie 提出四色猜想（任何平面地圖可用 4 色著色）
- **1976 年**：Appel 和 Haken 使用電腦證明四色定理（首個電腦輔助的重大數學證明）
- **1972 年**：Karp 證明圖著色是 NP-完全問題
- **現代應用**：編譯器暫存器分配、課程排課、頻道分配

## 演算法原理

### 問題定義

```
圖著色：給每個節點分配一種顏色，使得相鄰節點顏色不同。
色數（chromatic number）：著色所需的最少顏色數，記作 χ(G)。
```

### Welsh-Powell 演算法

```
貪婪演算法的一種改進版本：

1. 將所有節點按度數（相鄰節點數）降序排列
2. 依序處理每個未著色節點：
   a. 給予最小的可行顏色（未出現在鄰居中）
3. 返回結果

為什麼按度數排序？
高度數節點限制更多，先處理它們可以得到更好的結果。
```

### 回溯法（精確解）

```
對於小圖，可以使用回溯法找到精確的色數：

backtrack(node):
  if node == n: return True  # 完成
  for color in 0..max_colors-1:
    if color 對 node 安全（鄰居都沒有此顏色）:
      assign color to node
      if backtrack(node+1): return True
      remove color (回溯)

時間複雜度：O(k^V)，k 為顏色數，V 為節點數
```

### 色數的性質

```
χ(G) >= 最大團的大小（clique number）
χ(二分圖) = 2（除非無邊，則為 1）
χ(完全圖 K_n) = n
χ(偶環) = 2
χ(奇環) = 3
```

## 程式碼說明

### Welsh-Powell 實作

```python
def welsh_powell(self):
    # 按度數降序排序
    nodes_by_degree = sorted(range(n),
        key=lambda x: len(graph[x]), reverse=True)

    for node in nodes_by_degree:
        # 找出鄰居使用的顏色
        neighbor_colors = {color[nei] for nei in graph[node]
                          if nei in color}

        # 找最小可行顏色
        c = 0
        while c in neighbor_colors:
            c += 1
        color[node] = c
```

### 回溯法檢查

```python
def backtrack_coloring(self, max_colors):
    color = {}
    return self._backtrack_helper(0, color, max_colors)

def _backtrack_helper(self, node, color, max_colors):
    if node == n: return True
    for c in range(max_colors):
        if self._is_safe(node, c, color):
            color[node] = c
            if self._backtrack_helper(node+1, color, max_colors):
                return True
            del color[node]  # 回溯
    return False
```

## 應用場景

### 1. 編譯器暫存器分配

```
將變數視為節點，若兩變數生命週期重疊則連邊。
顏色 = 暫存器編號。
用最少的暫存器完成分配。
```

### 2. 課程排課

```
課程 = 節點，若有學生同時選修則連邊。
顏色 = 時間槽。
目標：用最少的時間槽完成排課。
```

### 3. 無線頻道分配

```
基地台 = 節點，若兩基地台距離太近會干擾則連邊。
顏色 = 頻道。
避免相鄰基地台使用相同頻道。
```

## 圖例

```
示例：三角形（3 個節點互相連接）

    0
   / \
  /   \
 1-----2

需要 3 種顏色：
  0 -> 顏色 0
  1 -> 顏色 1
  2 -> 顏色 2

示例：偶環（六邊形）

  0 --- 1
  |     |
  5 --- 2
  |     |
  4 --- 3

只需 2 種顏色（二分圖）：
  0,2,4 -> 顏色 0
  1,3,5 -> 顏色 1
```

## 演算法比較

| 演算法 | 時間複雜度 | 說明 |
|--------|-----------|------|
| 貪婪法 | O(V^2) | 簡單快速，但不是最優 |
| Welsh-Powell | O(V^2) | 較好的貪婪策略 |
| 回溯法 | O(k^V) | 指數時間，僅適合小圖 |
| DSATUR | O(V^2) | 動態選擇飽和度最高的節點 |

## 四色定理

```
四色定理（Appel-Haken, 1976）：
任何平面圖都可以用 4 種顏色完成著色。

注意：
- 僅適用於平面圖
- 非平面圖可能需要更多顏色（如 K5 需要 5 色）
```

## 參考資料

- Appel, K., & Haken, W. (1977). *Every planar map is four colorable*. Illinois Journal of Mathematics, 21(3), 429-490.
- Karp, R. M. (1972). *Reducibility among combinatorial problems*. In Complexity of Computer Computations (pp. 85-103).
- Jensen, T. R., & Toft, B. (1995). *Graph Coloring Problems*. Wiley-Interscience.
