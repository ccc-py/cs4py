"""
Treap (樹堆 - Tree + Heap)

歷史背景：
- Treap 由 Cecilia R. Aragon 和 Raimund Seidel 於 1989 年提出
- 結合了二元搜尋樹（BST）和堆積（Heap）的特性
- 使用隨機優先級來保持樹的平衡
- 期望高度 O(log n)，支援所有操作在 O(log n) 時間

應用場景：
- 需要平衡的 BST 且實作簡單
- 優先佇列與搜尋樹的結合
- 動態集合操作
- 平衡樹的教學範例
"""

from typing import Optional, List, Tuple
import random


class TreapNode:
    """Treap 節點"""

    def __init__(self, key: int, priority: float):
        self.key = key
        self.priority = priority  # 堆積屬性：父節點優先級 <= 子節點
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None


class Treap:
    """Treap（隨機平衡二元搜尋樹）"""

    def __init__(self, seed: Optional[int] = None):
        """
        初始化 Treap

        Args:
            seed: 隨機種子（用於重現結果）
        """
        self.root: Optional[TreapNode] = None
        if seed is not None:
            random.seed(seed)

    def insert(self, key: int) -> None:
        """
        插入鍵值

        原理：
        1. 按照 BST 規則插入新節點
        2. 給予隨機優先級
        3. 通過旋轉維持堆積性質（優先級）

        期望時間複雜度：O(log n)
        空間複雜度：O(1)（不含節點）

        Args:
            key: 要插入的鍵值
        """
        priority = random.random()
        self.root = self._insert_node(self.root, key, priority)

    def _insert_node(self, node: Optional[TreapNode], key: int, priority: float) -> TreapNode:
        """遞迴插入"""
        if node is None:
            return TreapNode(key, priority)

        if key < node.key:
            node.left = self._insert_node(node.left, key, priority)
            # 維持堆積性質（left priority < parent priority）
            if node.left.priority < node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, priority)
            # 維持堆積性質
            if node.right.priority < node.priority:
                node = self._rotate_left(node)
        # 若 key == node.key，不插入重複鍵

        return node

    def delete(self, key: int) -> None:
        """
        刪除鍵值

        原理：
        1. 找到要刪除的節點
        2. 通過旋轉將其移到葉節點
        3. 刪除葉節點

        期望時間複雜度：O(log n)

        Args:
            key: 要刪除的鍵值
        """
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, node: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        """遞迴刪除"""
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # 找到要刪除的節點
            # 通過旋轉將其移到葉節點
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # 將優先級較小的子節點旋轉上來
            if node.left.priority < node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete_node(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete_node(node.left, key)

        return node

    def search(self, key: int) -> bool:
        """
        搜尋鍵值

        Args:
            key: 要搜尋的鍵值

        Returns:
            是否存在該鍵值
        """
        curr = self.root
        while curr is not None:
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                return True
        return False

    def _rotate_right(self, node: TreapNode) -> TreapNode:
        """右旋"""
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def _rotate_left(self, node: TreapNode) -> TreapNode:
        """左旋"""
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child

    def inorder(self) -> List[int]:
        """中序遍歷（返回排序結果）"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[TreapNode], result: List[int]) -> None:
        """中序遍歷輔助函數"""
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    def height(self) -> int:
        """計算樹高"""
        return self._height(self.root)

    def _height(self, node: Optional[TreapNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


if __name__ == "__main__":
    print("=== Treap (樹堆) 測試 ===\n")

    # 測試 1：基本插入和搜尋
    print("1. 基本插入和搜尋：")
    treap1 = Treap(seed=42)
    keys = [5, 3, 7, 1, 9, 4, 6]
    for k in keys:
        treap1.insert(k)
    print(f"  插入鍵值：{keys}")
    print(f"  中序遍歷：{treap1.inorder()}")
    print(f"  樹高：{treap1.height()}")
    print(f"  搜尋 7：{treap1.search(7)}")
    print(f"  搜尋 2：{treap1.search(2)}")
    print()

    # 測試 2：刪除操作
    print("2. 刪除操作：")
    treap2 = Treap(seed=42)
    for k in [10, 20, 30, 15, 25]:
        treap2.insert(k)
    print(f"  插入後：{treap2.inorder()}")
    treap2.delete(20)
    print(f"  刪除 20 後：{treap2.inorder()}")
    treap2.delete(10)
    print(f"  刪除 10 後：{treap2.inorder()}")
    print()

    # 測試 3：重複插入相同鍵值
    print("3. 重複插入：")
    treap3 = Treap(seed=123)
    for k in [5, 5, 5, 3, 3]:
        treap3.insert(k)
    print(f"  插入 [5,5,5,3,3] 後：{treap3.inorder()}")
    print()

    # 測試 4：空樹
    print("4. 空樹操作：")
    treap4 = Treap()
    print(f"  搜尋 1：{treap4.search(1)}")
    treap4.delete(1)  # 應無錯誤
    print(f"  中序遍歷：{treap4.inorder()}")
    print()

    # 測試 5：順序插入的表現（檢驗隨機平衡）
    print("5. 順序插入 1-20：")
    treap5 = Treap(seed=999)
    for i in range(1, 21):
        treap5.insert(i)
    print(f"  插入 1-20")
    print(f"  樹高：{treap5.height()}")
    print(f"  中序遍歷（前 10 個）：{treap5.inorder()[:10]}...")
    print()
    print("測試完成！")
