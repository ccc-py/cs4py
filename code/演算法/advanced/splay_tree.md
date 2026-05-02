# 伸展樹 (Splay Tree)

## 歷史背景

伸展樹是一種自調整的二元搜尋樹，由 Daniel Sleator 和 Robert Tarjan 於 1985 年提出。

### 發展歷程

- **1985 年**：Sleator 和 Tarjan 提出伸展樹
- **關鍵創新**：不維護顯式平衡資訊，通過「伸展」操作自調整
- **攤平分析**：證明攤平時間複雜度為 O(log n)
- **應用**：實作簡單，適合部分訪問場景

## 演算法原理

### 伸展（Splay）操作

```
每次訪問節點後，將其移到根。
這使得最近訪問的節點靠近根，加速後續訪問。

三種旋轉：
1. Zig（單次旋轉）：
   當要 splay 的節點是根的子節點時
        parent            node
         /                / \
       node    =>        /   \
       /                /     parent

2. Zig-zig（左左或右右）：
   當 node 是 parent 的左子節點，
   且 parent 是 grandparent 的左子節點
        grand           node
         /             / \
       parent   =>    /   \
        /             /     parent
      node                 \
                            grand

3. Zig-zag（左右或右左）：
   當 node 是 parent 的左子節點，
   但 parent 是 grandparent 的右子節點
        grand          node
          \            / \
          parent  =>  /   \
           /         grand  parent
         node
```

### 時間複雜度（攤平）

```
操作      攤平時間   最壞時間
搜尋      O(log n)   O(n)
插入      O(log n)   O(n)
刪除      O(log n)   O(n)

注意：攤平分析假設操作序列，單次操作可能很慢。
```

### 為什麼高效？

```
伸展樹利用了「局部性原理」：
- 若頻繁訪問某些節點，它們會靠近根
- 對於訪問模式有偏的場景，表現優於平衡樹
```

## 程式碼說明

### Splay 操作

```python
def _splay(self, node, parent):
    while parent is not None:
        grandparent = self._find_parent(parent)

        if grandparent is None:
            # Zig
            if parent.left == node:
                self._rotate_right(parent)
            else:
                self._rotate_left(parent)
        else:
            if parent.left == node and grandparent.left == parent:
                # Zig-zig (左左)
                self._rotate_right(grandparent)
                self._rotate_right(parent)
            # ... 其他情況
```

### 刪除操作

```python
def delete(self, key):
    if not self.find(key):  # 先找到並 splay 到根
        return
    # 此時 key 在根
    if root.left is None:
        root = root.right
    elif root.right is None:
        root = root.left
    else:
        # 將左子樹的最大值 splay 上來
        # 然後接上右子樹
```

## 應用場景

### 1. 快取實作

```
利用局部性原理，最近訪問的資料在「根」附近，
存取速度快。
```

### 2. 垃圾回收

```
某些垃圾回收演算法使用伸展樹來管理物件。
```

### 3. 字串搜尋

```
序列操作中，伸展樹能快速處理重複搜尋。
```

## 圖例

```
Zig-zig（右右）示意：

     G              P
    / \            / \
   P   C   =>     /   \
  / \            /     \
 N   B          N       G
 /                /     / \
A                A      B   C
```

## 與其他平衡樹比較

| 資料結構 | 平衡方式 | 實作難度 | 攤平時間 |
|---------|---------|---------|---------|
| AVL | 高度平衡 | 中等 | O(log n) |
| 紅黑樹 | 顏色標記 | 困難 | O(log n) |
| Treap | 隨機優先級 | 簡單 | O(log n) |
| Splay | 自調整 | 中等 | O(log n) |

## 參考資料

- Sleator, D. D., & Tarjan, R. E. (1985). *Self-adjusting binary search trees*. Journal of the ACM, 32(3), 652-686.
- Tarjan, R. E. (1985). *Amortized computational complexity*. SIAM Journal on Algebraic and Discrete Methods, 6(2), 306-318.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 13)
