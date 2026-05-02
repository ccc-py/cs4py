"""二元樹（Binary Tree）實作與遍歷。

歷史背景：
二元樹是一種每個節點最多有兩個子節點的樹結構，最早由數學家和計算機科學家在20世紀50年代用於表達式解析和資料儲存。
遍歷方法是二元樹操作的基礎，分為深度優先（前序、中序、後序）和廣度優先（層序）遍歷。

核心概念：
- 節點：包含值域、左子節點、右子節點
- 遍歷：按特定順序訪問所有節點
- 高度：從節點到最遠葉子節點的邊數
- 直徑：樹中最長路徑的邊數
- 平衡：左右子樹高度差不超過1
"""

from typing import Optional, List, Any
from collections import deque


class TreeNode:
    """二元樹節點。"""
    def __init__(self, val: Any) -> None:
        self.val: Any = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinaryTree:
    """二元樹實作。"""
    def __init__(self, root: Optional[TreeNode] = None) -> None:
        self.root: Optional[TreeNode] = root

    def preorder_recursive(self) -> List[Any]:
        """前序遍歷（遞迴）：根 -> 左 -> 右。"""
        result = []
        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            result.append(node.val)
            dfs(node.left)
            dfs(node.right)
        dfs(self.root)
        return result

    def preorder_iterative(self) -> List[Any]:
        """前序遍歷（迭代）。"""
        if not self.root:
            return []
        result = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            result.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    def inorder_recursive(self) -> List[Any]:
        """中序遍歷（遞迴）：左 -> 根 -> 右。"""
        result = []
        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)
        dfs(self.root)
        return result

    def inorder_iterative(self) -> List[Any]:
        """中序遍歷（迭代）。"""
        result = []
        stack = []
        curr = self.root
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right
        return result

    def postorder_recursive(self) -> List[Any]:
        """後序遍歷（遞迴）：左 -> 右 -> 根。"""
        result = []
        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            result.append(node.val)
        dfs(self.root)
        return result

    def postorder_iterative(self) -> List[Any]:
        """後序遍歷（迭代）。"""
        if not self.root:
            return []
        result = []
        stack = [self.root]
        prev = None
        while stack:
            curr = stack[-1]
            if not prev or prev.left == curr or prev.right == curr:
                if curr.left:
                    stack.append(curr.left)
                elif curr.right:
                    stack.append(curr.right)
            elif curr.left == prev:
                if curr.right:
                    stack.append(curr.right)
            else:
                result.append(curr.val)
                stack.pop()
            prev = curr
        return result

    def level_order(self) -> List[List[Any]]:
        """層序遍歷（BFS），返回每層的節點值。"""
        if not self.root:
            return []
        result = []
        queue = deque([self.root])
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result

    def height(self) -> int:
        """計算樹的高度（邊數）。"""
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return -1
            return 1 + max(dfs(node.left), dfs(node.right))
        return dfs(self.root)

    def diameter(self) -> int:
        """計算樹的直徑（最長路徑邊數）。"""
        max_diameter = 0
        def dfs(node: Optional[TreeNode]) -> int:
            nonlocal max_diameter
            if not node:
                return -1
            left_height = dfs(node.left) + 1
            right_height = dfs(node.right) + 1
            max_diameter = max(max_diameter, left_height + right_height)
            return max(left_height, right_height)
        dfs(self.root)
        return max_diameter

    def is_balanced(self) -> bool:
        """檢查樹是否平衡（左右子樹高度差不超過1）。"""
        def dfs(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            left = dfs(node.left)
            if left == -1:
                return -1
            right = dfs(node.right)
            if right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        return dfs(self.root) != -1


if __name__ == "__main__":
    print("=== 二元樹測試 ===")
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    tree = BinaryTree(root)

    print(f"前序遍歷（遞迴）: {tree.preorder_recursive()}")
    print(f"前序遍歷（迭代）: {tree.preorder_iterative()}")
    print(f"中序遍歷（遞迴）: {tree.inorder_recursive()}")
    print(f"中序遍歷（迭代）: {tree.inorder_iterative()}")
    print(f"後序遍歷（遞迴）: {tree.postorder_recursive()}")
    print(f"後序遍歷（迭代）: {tree.postorder_iterative()}")
    print(f"層序遍歷: {tree.level_order()}")
    print(f"樹的高度: {tree.height()}")
    print(f"樹的直徑: {tree.diameter()}")
    print(f"是否平衡: {tree.is_balanced()}")
