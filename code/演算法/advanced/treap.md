# Treap (樹堆 - Tree + Heap)

## 歷史背景

Treap 是一種結合二元搜尋樹和堆積特性的平衡樹，由 Cecilia R. Aragon 和 Raimund Seidel 於 1989 年提出。

### 發展歷程

- **1989 年**：Aragon 和 Seidel 提出 Treap
- **概念來源**：結合 BST（搜尋）和 Heap（優先佇列）
- **隨機化**：使用隨機優先級來達到期望平衡
- **應用**：平衡樹的簡單實作，適合教學和實戰

## 演算法原理

### Treap 性質

```
Treap = Tree + Heap

1. BST 性質（按 key）：
   - 左子樹所有 key < 根節點 key
   - 右子樹所有 key > 根節點 key

2. Heap 性質（按 priority）：
   - 父節點的 priority <= 子節點的 priority（min-heap）
   - 或相反（max-heap）

因為 priority 是隨機的，期望樹高為 O(log n)
```

### 插入操作

```
1. 按照 BST 規則插入新節點
2. 給予新節點隨機 priority
3. 通過旋轉（rotation）維持堆積性質：
   - 若左子節點 priority < 父節點，執行右旋
   - 若右子節點 priority < 父節點，執行左旋

時間複雜度：O(log n) 期望值
```

### 刪除操作

```
1. 找到要刪除的節點
2. 通過旋轉將其移到葉節點：
   - 比較左右子節點的 priority
   - 將 priority 較小的子節點旋轉上來
3. 刪除葉節點

時間複雜度：O(log n) 期望值
```

### 旋轉（Rotation）

```
右旋（處理左子節點優先級太小）：
    A              B
   / \            / \
  B   C   =>      D   A
 / \                / \
D   E              E   C

左旋（處理右子節點優先級太小）：
  A                B
 / \              / \
C   B    =>       A   E
   / \          / \
  D   E        C   D
```

## 程式碼說明

### 插入實作

```python
def _insert_node(self, node, key, priority):
    if node is None:
        return TreapNode(key, priority)

    if key < node.key:
        node.left = self._insert_node(node.left, key, priority)
        if node.left.priority < node.priority:
            node = self._rotate_right(node)
    elif key > node.key:
        node.right = self._insert_node(node.right, key, priority)
        if node.right.priority < node.priority:
            node = self._rotate_left(node)
    return node
```

### 旋轉操作

```python
def _rotate_right(self, node):
    left_child = node.left
    node.left = left_child.right
    left_child.right = node
    return left_child  # 新的根
```

## 應用場景

### 1. 平衡的關聯陣列

```
需要快速插入、刪除、搜尋的場景，
且需要簡單的實作（不需要複雜的平衡調整）。
```

### 2. 教學工具

```
Treap 是理解平衡樹和旋轉操作的良好範例。
```

### 3. 隨機化資料結構

```
展示如何使用隨機化來簡化平衡樹的實作。
```

## 效能分析

```
操作       期望時間  最壞時間
搜尋       O(log n)  O(n)
插入       O(log n)  O(n)
刪除       O(log n)  O(n)

注意：最壞情況極罕見（概率趨近於 0）
```

## 與其他平衡樹比較

| 資料結構 | 平衡方式 | 實作難度 | 說明 |
|---------|---------|---------|------|
| AVL | 高度平衡 | 中等 | 嚴格平衡，查詢快 |
| 紅黑樹 | 顏色標記 | 困難 | STL map 使用 |
| Treap | 隨機優先級 | 簡單 | 期望平衡 |
| Splay | 自調整 | 中等 | 攤平複雜度 |

## 參考資料

- Aragon, C. R., & Seidel, R. (1989). *Randomized search trees*. Proceedings of the 30th Annual Symposium on Foundations of Computer Science, 540-545.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 13)
- Goodrich, M. T., & Tamassia, R. (2002). *Algorithm Design: Foundations, Analysis, and Internet Examples*. Wiley.
