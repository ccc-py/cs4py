# 二元搜尋樹（Binary Search Tree, BST）

## 歷史背景
二元搜尋樹由P.F. Windley在1960年正式提出，是早期用於動態資料集搜尋的核心結構。它的有序性質使其成為後續平衡樹（如AVL、紅黑樹）的基礎。

## 核心概念與原理
BST的基本性質：
- 左子樹所有節點值 < 根節點值
- 右子樹所有節點值 > 根節點值
- 中序遍歷可得到升序序列

操作時間複雜度：
- 搜尋、插入、刪除：平均O(log n)，最壞O(n)（傾斜樹）
- 刪除操作的三種情況：
  1. 葉子節點：直接刪除
  2. 單孩子節點：用孩子替換
  3. 雙孩子節點：用後繼（右子樹最小值）或前驅（左子樹最大值）替換

## 使用範例
```python
from bst import BinarySearchTree

bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
print(bst.inorder())
```

## 參考資料
- [Wikipedia: Binary Search Tree](https://en.wikipedia.org/wiki/Binary_search_tree)
- [GeeksforGeeks: BST](https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/)
