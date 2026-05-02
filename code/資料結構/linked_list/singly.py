"""單向鏈結串列（Singly Linked List）實作。

歷史背景：
鏈結串列是一種基礎的動態資料結構，最早由多個計算機科學家獨立提出，用於解決陣列大小固定的問題。
單向鏈結串列每個節點只包含指向下一個節點的指針，實作簡單且插入刪除效率高。

核心概念：
- 節點（Node）：儲存值和下一個節點的引用
- 頭指針（head）：指向第一個節點
- 動態大小：無需預先分配固定空間
"""

from typing import Optional, Any


class Node:
    """單向鏈結串列的節點。"""
    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.next: Optional[Node] = None


class SinglyLinkedList:
    """單向鏈結串列實作。"""
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.size: int = 0

    def insert_head(self, value: Any) -> None:
        """在頭部插入節點。"""
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_tail(self, value: Any) -> None:
        """在尾部插入節點。"""
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    def insert_at(self, index: int, value: Any) -> None:
        """在指定位置插入節點（0-based）。"""
        if index < 0 or index > self.size:
            raise IndexError("索引超出範圍")
        if index == 0:
            self.insert_head(value)
            return
        if index == self.size:
            self.insert_tail(value)
            return
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        new_node = Node(value)
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1

    def delete(self, value: Any) -> bool:
        """刪除第一個值為value的節點，成功返回True。"""
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return True
        curr = self.head
        while curr.next:
            if curr.next.value == value:
                curr.next = curr.next.next
                self.size -= 1
                return True
            curr = curr.next
        return False

    def search(self, value: Any) -> Optional[Node]:
        """搜尋值為value的第一個節點，找不到返回None。"""
        curr = self.head
        while curr:
            if curr.value == value:
                return curr
            curr = curr.next
        return None

    def reverse(self) -> None:
        """反轉鏈結串列。"""
        prev = None
        curr = self.head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head = prev

    def has_cycle(self) -> bool:
        """使用Floyd龜兔賽跑演算法檢測環。"""
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        values = []
        curr = self.head
        while curr:
            values.append(str(curr.value))
            curr = curr.next
        return " -> ".join(values) if values else "Empty"


if __name__ == "__main__":
    print("=== 單向鏈結串列測試 ===")
    ll = SinglyLinkedList()
    ll.insert_tail(1)
    ll.insert_tail(2)
    ll.insert_tail(3)
    print(f"初始串列: {ll}")
    ll.insert_head(0)
    print(f"頭部插入0: {ll}")
    ll.insert_at(2, 1.5)
    print(f"位置2插入1.5: {ll}")
    ll.delete(1)
    print(f"刪除值1: {ll}")
    print(f"搜尋2: {ll.search(2).value if ll.search(2) else '未找到'}")
    ll.reverse()
    print(f"反轉後: {ll}")
    print(f"長度: {len(ll)}")
    print(f"是否有環: {ll.has_cycle()}")
