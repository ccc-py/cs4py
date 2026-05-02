"""二元搜尋樹（Binary Search Tree, BST）實作。

歷史背景：
二元搜尋樹由P.F. Windley在1960年提出，是一種有序的二元樹結構，支援高效的搜尋、插入、刪除操作。
中序遍歷BST可得到有序序列，平均時間複雜度O(log n)，最壞情況O(n)（傾斜樹）。

核心概念：
- 左子樹所有節點值 < 根節點值
- 右子樹所有節點值 > 根節點值
- 無重複值（或可定義重複值處理方式）
"""

from typing import Optional, Any


class TreeNode:
    """BST節點。"""
    def __init__(self, val: Any) -> None:
        self.val: Any = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BinarySearchTree:
    """二元搜尋樹實作。"""
    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    def insert(self, val: Any) -> None:
        """插入值到BST。"""
        if not self.root:
            self.root = TreeNode(val)
            return
        curr = self.root
        while True:
            if val < curr.val:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = TreeNode(val)
                    break
            elif val > curr.val:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = TreeNode(val)
                    break
            else:
                break

    def search(self, val: Any) -> Optional[TreeNode]:
        """搜尋值，返回節點或None。"""
        curr = self.root
        while curr:
            if val < curr.val:
                curr = curr.left
            elif val > curr.val:
                curr = curr.right
            else:
                return curr
        return None

    def delete(self, val: Any) -> None:
        """刪除值為val的節點。"""
        def find_min(node: TreeNode) -> TreeNode:
            while node.left:
                node = node.left
            return node

        def dfs(node: Optional[TreeNode], val: Any) -> Optional[TreeNode]:
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
            return node

        self.root = dfs(self.root, val)

    def inorder(self) -> list:
        """中序遍歷，返回有序序列。"""
        result = []
        def dfs(node: Optional[TreeNode]) -> None:
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)
        dfs(self.root)
        return result

    def find_min(self) -> Optional[Any]:
        """找到最小值。"""
        if not self.root:
            return None
        curr = self.root
        while curr.left:
            curr = curr.left
        return curr.val

    def find_max(self) -> Optional[Any]:
        """找到最大值。"""
        if not self.root:
            return None
        curr = self.root
        while curr.right:
            curr = curr.right
        return curr.val

    def floor(self, val: Any) -> Optional[Any]:
        """找到小於或等於val的最大值。"""
        result = None
        curr = self.root
        while curr:
            if curr.val < val:
                result = curr.val
                curr = curr.right
            elif curr.val > val:
                curr = curr.left
            else:
                return curr.val
        return result

    def ceiling(self, val: Any) -> Optional[Any]:
        """找到大於或等於val的最小值。"""
        result = None
        curr = self.root
        while curr:
            if curr.val > val:
                result = curr.val
                curr = curr.left
            elif curr.val < val:
                curr = curr.right
            else:
                return curr.val
        return result


if __name__ == "__main__":
    print("=== 二元搜尋樹測試 ===")
    bst = BinarySearchTree()
    for val in [5, 3, 7, 2, 4, 6, 8]:
        bst.insert(val)
    print(f"中序遍歷（有序）: {bst.inorder()}")
    print(f"搜尋4: {bst.search(4).val if bst.search(4) else '未找到'}")
    print(f"最小值: {bst.find_min()}")
    print(f"最大值: {bst.find_max()}")
    print(f"floor(5): {bst.floor(5)}")
    print(f"ceiling(5): {bst.ceiling(5)}")
    print(f"floor(3.5): {bst.floor(3.5)}")
    bst.delete(3)
    print(f"刪除3後中序遍歷: {bst.inorder()}")
