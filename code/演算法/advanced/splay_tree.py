"""
伸展樹 (Splay Tree)

歷史背景：
- 伸展樹由 Daniel Sleator 和 Robert Tarjan 於 1985 年提出
- 是一種自調整（self-adjusting）的二元搜尋樹
- 不維護顯式的平衡資訊，而是通過「伸展」操作調整
- 攤平（amortized）時間複雜度為 O(log n)

應用場景：
- 需要頻繁訪問部分資料的場景
- 快取和記憶體管理
- 序列操作（連續訪問相同或相鄰元素）
- 實作簡單的平衡樹
"""

from typing import Optional, List


class SplayNode:
    """伸展樹節點"""

    def __init__(self, key: int):
        self.key = key
        self.left: Optional['SplayNode'] = None
        self.right: Optional['SplayNode'] = None


class SplayTree:
    """伸展樹（自調整二元搜尋樹）"""

    def __init__(self):
        """初始化伸展樹"""
        self.root: Optional[SplayNode] = None

    def find(self, key: int) -> bool:
        """
        搜尋鍵值

        原理：
        1. 標準 BST 搜尋
        2. 找到後執行 splay 操作（將該節點移到根）
        3. 若未找到，將最後訪問的節點 splay 到根

        攤平時間複雜度：O(log n)

        Args:
            key: 要搜尋的鍵值

        Returns:
            是否存在該鍵值
        """
        if self.root is None:
            return False

        node = self.root
        parent = None

        while node is not None:
            if key == node.key:
                self._splay(node, parent)
                return True
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        # 未找到，將最後訪問的 parent splay 到根
        if parent is not None:
            self._splay(parent, None)
        return False

    def insert(self, key: int) -> None:
        """
        插入鍵值

        原理：
        1. 標準 BST 插入
        2. 將新插入的節點 splay 到根

        攤平時間複雜度：O(log n)

        Args:
            key: 要插入的鍵值
        """
        if self.root is None:
            self.root = SplayNode(key)
            return

        node = self.root
        parent = None

        while node is not None:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # 已存在，splay 該節點並返回
                self._splay(parent, None)
                return

        new_node = SplayNode(key)
        if parent is not None:
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            self._splay(new_node, parent)

    def delete(self, key: int) -> None:
        """
        刪除鍵值

        原理：
        1. 搜尋並 splay 該節點到根
        2. 刪除根節點：
           a. 若無左子樹，直接用右子樹取代
           b. 否則，將左子樹的最大值 splay 到左子樹的根
              然後將右子樹接在左子樹的根的右側

        攤平時間複雜度：O(log n)

        Args:
            key: 要刪除的鍵值
        """
        if self.root is None:
            return

        if not self.find(key):
            return  # 未找到

        # 此時 key 在根
        if self.root.left is None:
            self.root = self.root.right
        elif self.root.right is None:
            self.root = self.root.left
        else:
            left = self.root.left
            right = self.root.right
            self.root = left
            # 將左子樹的最大值 splay 到根
            self._splay_max(left, None)
            self.root.right = right

    def _splay_max(self, node: SplayNode, parent: Optional[SplayNode]) -> None:
        """將子樹中的最大值 splay 到子樹根"""
        curr = node
        par = None
        while curr.right is not None:
            par = curr
            curr = curr.right
        self._splay(curr, par)

    def _splay(self, node: SplayNode, parent: Optional[SplayNode]) -> None:
        """
        伸展操作：將 node 移到根

        使用 zig, zig-zig, zig-zag 三種旋轉
        """
        while parent is not None:
            # 確定 grandparent
            grandparent = self._find_parent(parent)

            if grandparent is None:
                # Zig（單次旋轉）
                if parent.left == node:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            else:
                if parent.left == node and grandparent.left == parent:
                    # Zig-zig（左左）
                    self._rotate_right(grandparent)
                    self._rotate_right(parent)
                elif parent.right == node and grandparent.right == parent:
                    # Zig-zig（右右）
                    self._rotate_left(grandparent)
                    self._rotate_left(parent)
                else:
                    # Zig-zag（左右或右左）
                    if parent.left == node:
                        self._rotate_right(parent)
                        self._rotate_left(grandparent)
                    else:
                        self._rotate_left(parent)
                        self._rotate_right(grandparent)

            parent = self._find_parent(node)

    def _find_parent(self, node: SplayNode) -> Optional[SplayNode]:
        """找 node 的父節點"""
        if self.root == node:
            return None
        curr = self.root
        while curr is not None:
            if curr.left == node or curr.right == node:
                return curr
            if node.key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def _rotate_right(self, node: SplayNode) -> None:
        """右旋：node 的左子節點成為新的根"""
        left_child = node.left
        if left_child is None:
            return

        # 更新根
        if self.root == node:
            self.root = left_child
        else:
            parent = self._find_parent(node)
            if parent is not None:
                if parent.left == node:
                    parent.left = left_child
                else:
                    parent.right = left_child

        node.left = left_child.right
        left_child.right = node

    def _rotate_left(self, node: SplayNode) -> None:
        """左旋：node 的右子節點成為新的根"""
        right_child = node.right
        if right_child is None:
            return

        if self.root == node:
            self.root = right_child
        else:
            parent = self._find_parent(node)
            if parent is not None:
                if parent.left == node:
                    parent.left = right_child
                else:
                    parent.right = right_child

        node.right = right_child.left
        right_child.left = node

    def inorder(self) -> List[int]:
        """中序遍歷"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[SplayNode], result: List[int]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    def height(self) -> int:
        """計算樹高"""
        return self._height(self.root)

    def _height(self, node: Optional[SplayNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


if __name__ == "__main__":
    print("=== 伸展樹 (Splay Tree) 測試 ===\n")

    # 測試 1：基本插入和搜尋
    print("1. 基本插入和搜尋：")
    st1 = SplayTree()
    keys = [10, 5, 15, 3, 8, 12, 20]
    for k in keys:
        st1.insert(k)
    print(f"  插入：{keys}")
    print(f"  中序遍歷：{st1.inorder()}")
    print(f"  樹高：{st1.height()}")
    print(f"  搜尋 8：{st1.find(8)}")
    print(f"  搜尋 100：{st1.find(100)}")
    print()

    # 測試 2：刪除操作
    print("2. 刪除操作：")
    st2 = SplayTree()
    for k in [50, 30, 70, 20, 40, 60, 80]:
        st2.insert(k)
    print(f"  插入後：{st2.inorder()}")
    st2.delete(30)
    print(f"  刪除 30 後：{st2.inorder()}")
    st2.delete(50)
    print(f"  刪除 50 後：{st2.inorder()}")
    print()

    # 測試 3：順序插入（測試自調整）
    print("3. 順序插入 1-10：")
    st3 = SplayTree()
    for i in range(1, 11):
        st3.insert(i)
    print(f"  中序遍歷：{st3.inorder()}")
    print(f"  樹高：{st3.height()}")
    # 搜尋 1，應該會 splay 到根
    st3.find(1)
    print(f"  搜尋 1 後樹高：{st3.height()}")
    print()

    # 測試 4：空樹操作
    print("4. 空樹操作：")
    st4 = SplayTree()
    print(f"  搜尋 1：{st4.find(1)}")
    st4.delete(1)  # 應無錯誤
    print(f"  中序遍歷：{st4.inorder()}")
    print()

    # 測試 5：重複插入
    print("5. 重複插入：")
    st5 = SplayTree()
    for k in [5, 5, 5, 3, 3, 7]:
        st5.insert(k)
    print(f"  插入後：{st5.inorder()}")
    print()
    print("測試完成！")
