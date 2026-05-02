"""AVL樹（平衡二元搜尋樹）實作。

歷史背景：
AVL樹由蘇聯數學家Adelson-Velsky和Landis在1962年提出，是第一個自平衡二元搜尋樹，保證所有操作的最壞時間複雜度為O(log n)。

核心概念：
- 平衡因子：左子樹高度 - 右子樹高度，絕對值 <= 1
- 四種失衡情況：LL、RR、LR、RL
- 旋轉操作：右旋（LL）、左旋（RR）、左右旋（LR）、右左旋（RL）
"""

from typing import Optional, Any


class AVLNode:
    """AVL樹節點。"""
    def __init__(self, val: Any) -> None:
        self.val: Any = val
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1


class AVLTree:
    """AVL樹實作。"""
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _balance_factor(self, node: AVLNode) -> int:
        return self._height(node.left) - self._height(node.right)

    def _right_rotate(self, y: AVLNode) -> AVLNode:
        """右旋操作（處理LL情況）。"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    def _left_rotate(self, x: AVLNode) -> AVLNode:
        """左旋操作（處理RR情況）。"""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def insert(self, val: Any) -> None:
        """插入值。"""
        def dfs(node: Optional[AVLNode], val: Any) -> AVLNode:
            if not node:
                return AVLNode(val)
            if val < node.val:
                node.left = dfs(node.left, val)
            elif val > node.val:
                node.right = dfs(node.right, val)
            else:
                return node

            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)

            if balance > 1 and val < node.left.val:
                return self._right_rotate(node)
            if balance < -1 and val > node.right.val:
                return self._left_rotate(node)
            if balance > 1 and val > node.left.val:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
            if balance < -1 and val < node.right.val:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

            return node

        self.root = dfs(self.root, val)

    def delete(self, val: Any) -> None:
        """刪除值。"""
        def find_min(node: AVLNode) -> AVLNode:
            while node.left:
                node = node.left
            return node

        def dfs(node: Optional[AVLNode], val: Any) -> Optional[AVLNode]:
            if not node:
                return None
            if val < node.val:
                node.left = dfs(node.left, val)
            elif val > node.val:
                node.right = dfs(node.right, val)
            else:
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left
                successor = find_min(node.right)
                node.val = successor.val
                node.right = dfs(node.right, successor.val)

            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)

            if balance > 1 and self._balance_factor(node.left) >= 0:
                return self._right_rotate(node)
            if balance > 1 and self._balance_factor(node.left) < 0:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
            if balance < -1 and self._balance_factor(node.right) <= 0:
                return self._left_rotate(node)
            if balance < -1 and self._balance_factor(node.right) > 0:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

            return node

        self.root = dfs(self.root, val)

    def inorder(self) -> list:
        """中序遍歷。"""
        result = []
        def dfs(node: Optional[AVLNode]) -> None:
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)
        dfs(self.root)
        return result

    def get_balance_factors(self) -> dict:
        """返回所有節點的平衡因子。"""
        factors = {}
        def dfs(node: Optional[AVLNode], path: str = "root") -> None:
            if not node:
                return
            factors[path] = self._balance_factor(node)
            dfs(node.left, f"{path}.left")
            dfs(node.right, f"{path}.right")
        dfs(self.root)
        return factors


if __name__ == "__main__":
    print("=== AVL樹測試 ===")
    avl = AVLTree()
    for val in [10, 20, 30, 40, 50, 25]:
        avl.insert(val)
        print(f"插入{val}，當前中序: {avl.inorder()}")
    print(f"平衡因子: {avl.get_balance_factors()}")
    avl.delete(30)
    print(f"刪除30後中序: {avl.inorder()}")
    print(f"平衡因子: {avl.get_balance_factors()}")
