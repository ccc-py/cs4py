# AVL樹（自平衡二元搜尋樹）

## 歷史背景
AVL樹由蘇聯數學家Georgy Adelson-Velsky和Evgenii Landis在1962年的論文《An algorithm for the organization of information》中提出，是第一個自平衡二元搜尋樹，確保所有操作的最壞時間複雜度為O(log n)。

## 核心概念與原理
### 平衡條件
- 平衡因子：左子樹高度 - 右子樹高度，絕對值 ≤ 1
- 若插入/刪除後平衡因子絕對值 > 1，則需要旋轉調整

### 四種失衡與旋轉
1. **LL（左左）**：右旋
2. **RR（右右）**：左旋
3. **LR（左右）**：先左旋左子節點，再右旋當前節點
4. **RL（右左）**：先右旋右子節點，再左旋當前節點

### 時間複雜度
所有操作均為O(log n)，因為樹高度始終保持在O(log n)。

## 使用範例
```python
from avl import AVLTree

avl = AVLTree()
avl.insert(10)
avl.insert(20)
print(avl.inorder())
```

## 參考資料
- [Wikipedia: AVL Tree](https://en.wikipedia.org/wiki/AVL_tree)
- [Original Paper](https://www.math.tau.ac.il/~nachumd/papers/avl.pdf)
