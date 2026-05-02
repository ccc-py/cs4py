# 紅黑樹（Red-Black Tree）

## 歷史背景
紅黑樹由Leonidas J. Guibas和Robert Sedgewick在1978年提出，是一種高效的自我平衡二元搜尋樹。它通過為每個節點添加顏色屬性（紅或黑）並維護五個紅黑性質，保證樹的高度始終為O(log n)，所有操作的最壞時間複雜度均為O(log n)。紅黑樹被廣泛應用於許多語言的標準庫中，如Java的TreeMap、C++的std::map等。

## 核心概念與原理
### 紅黑性質
1. 每個節點是紅色或黑色
2. 根節點是黑色
3. 所有葉子節點（NIL空節點）是黑色
4. 紅色節點的子節點必須是黑色（無連續紅節點）
5. 從任一節點到其所有後代NIL節點的路徑包含相同數目的黑色節點

### 插入後的修正
插入新節點（默認紅色）後，可能破壞紅黑性質，需通過以下操作修正：
1. **顏色翻轉**：若當前節點的左右子節點均為紅色，則翻轉當前節點與子節點的顏色
2. **左旋**：若右子節點為紅色且左子節點不為紅色，則左旋當前節點
3. **右旋**：若左子節點為紅色且其左子節點也為紅色，則右旋當前節點

## 使用範例
```python
from red_black import RedBlackTree

rb = RedBlackTree()
rb.insert(10)
rb.insert(20)
print(rb.inorder())
```

## 參考資料
- [Wikipedia: Red-Black Tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)
- [Sedgewick's RedBlackBST Implementation](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/RedBlackBST.java.html)
