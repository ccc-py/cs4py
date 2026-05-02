# 二元樹（Binary Tree）

## 歷史背景
二元樹的概念最早可追溯到數學家凱萊（Arthur Cayley）在1857年對樹結構的研究，計算機科學中則在20世紀50年代被用於編譯器的語法樹表示。二元樹的遍歷方法是後續搜尋演算法、排序演算法的基礎。

## 核心概念與原理
### 二元樹結構
- 每個節點最多有兩個子節點（左子節點、右子節點）
- 常見遍歷方式：
  1. **前序遍歷**：根節點 → 左子樹 → 右子樹
  2. **中序遍歷**：左子樹 → 根節點 → 右子樹（BST中可得到有序序列）
  3. **後序遍歷**：左子樹 → 右子樹 → 根節點
  4. **層序遍歷**：按層次從上到下、從左到右遍歷（BFS）

### 進階操作
- **高度**：從根節點到最遠葉子節點的邊數
- **直徑**：樹中任意兩節點間最長路徑的邊數
- **平衡樹**：左右子樹高度差不超過1

## 使用範例
```python
from binary_tree import TreeNode, BinaryTree

root = TreeNode(1)
root.left = TreeNode(2)
tree = BinaryTree(root)
print(tree.inorder_recursive())
```

## 參考資料
- [Wikipedia: Binary Tree](https://en.wikipedia.org/wiki/Binary_tree)
- [GeeksforGeeks: Tree Traversals](https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/)
