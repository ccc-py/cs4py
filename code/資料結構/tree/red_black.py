"""紅黑樹（Red-Black Tree）實作。

歷史背景：
紅黑樹由Guibas和Sedgewick在1978年提出，是一種自平衡二元搜尋樹，通過顏色標記和旋轉維持平衡，保證所有操作O(log n)時間。

核心概念（紅黑性質）：
1. 每個節點是紅色或黑色
2. 根節點是黑色
3. 所有葉子節點（NIL）是黑色
4. 紅色節點的子節點必須是黑色
5. 從任一節點到其所有後代NIL節點的路徑包含相同數目的黑色節點
"""

from typing import Optional, Any

RED = True
BLACK = False


class RBNode:
    """紅黑樹節點。"""
    def __init__(self, val: Any, color: bool = RED) -> None:
        self.val: Any = val
        self.left: Optional[RBNode] = None
        self.right: Optional[RBNode] = None
        self.color: bool = color


class RedBlackTree:
    """紅黑樹實作。"""
    def __init__(self) -> None:
        self.NIL = RBNode(None, BLACK)
        self.root: RBNode = self.NIL

    def _is_red(self, node: RBNode) -> bool:
        return node.color == RED if node else False

    def _right_rotate(self, h: RBNode) -> RBNode:
        """右旋操作。"""
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def _left_rotate(self, h: RBNode) -> RBNode:
        """左旋操作。"""
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def _flip_colors(self, h: RBNode) -> None:
        """翻轉節點及其子節點的顏色。"""
        h.color = RED
        h.left.color = BLACK
        h.right.color = BLACK

    def insert(self, val: Any) -> None:
        """插入值。"""
        def dfs(node: RBNode, val: Any) -> RBNode:
            if node == self.NIL:
                return RBNode(val)
            if val < node.val:
                node.left = dfs(node.left, val)
            elif val > node.val:
                node.right = dfs(node.right, val)
            else:
                return node

            if self._is_red(node.right) and not self._is_red(node.left):
                node = self._left_rotate(node)
            if self._is_red(node.left) and self._is_red(node.left.left):
                node = self._right_rotate(node)
            if self._is_red(node.left) and self._is_red(node.right):
                self._flip_colors(node)

            return node

        self.root = dfs(self.root, val)
        self.root.color = BLACK

    def inorder(self) -> list:
        """中序遍歷。"""
        result = []
        def dfs(node: RBNode) -> None:
            if node == self.NIL:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)
        dfs(self.root)
        return result

    def get_colors(self) -> dict:
        """返回所有節點的顏色。"""
        colors = {}
        def dfs(node: RBNode, path: str = "root") -> None:
            if node == self.NIL:
                return
            colors[path] = "RED" if node.color == RED else "BLACK"
            dfs(node.left, f"{path}.left")
            dfs(node.right, f"{path}.right")
        dfs(self.root)
        return colors


if __name__ == "__main__":
    print("=== 紅黑樹測試 ===")
    rb = RedBlackTree()
    for val in [7, 3, 18, 10, 22, 8, 11, 26]:
        rb.insert(val)
        print(f"插入{val}，當前中序: {rb.inorder()}")
    print(f"節點顏色: {rb.get_colors()}")
    print(f"根節點顏色: {'RED' if rb.root.color == RED else 'BLACK'}")
