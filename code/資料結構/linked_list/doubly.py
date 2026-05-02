"""雙向鏈結串列（Doubly Linked List）與LRU快取實作。

歷史背景：
雙向鏈結串列在單向鏈結串列基礎上增加指向前一個節點的指針，允許雙向遍歷，由Allen Newell等人在1957年提出。
LRU（Least Recently Used）快取是一種常用快取淘汰策略，利用雙向鏈結串列和雜湊表可實作O(1)時間複雜度的操作。

核心概念：
- 雙向節點：包含前驅、後繼和值域
- 雙向串列：可雙向遍歷，插入刪除需修改兩個指針
- LRU快取：最近最少使用淘汰，訪問或插入的節點移到頭部，淘汰尾部節點
"""

from typing import Optional, Any, Dict


class DoublyNode:
    """雙向鏈結串列的節點。"""
    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key: Any = key
        self.value: Any = value
        self.prev: Optional[DoublyNode] = None
        self.next: Optional[DoublyNode] = None


class DoublyLinkedList:
    """雙向鏈結串列實作。"""
    def __init__(self) -> None:
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self.size: int = 0

    def insert_head(self, node: DoublyNode) -> None:
        """在頭部插入節點。"""
        if not self.head:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def insert_tail(self, node: DoublyNode) -> None:
        """在尾部插入節點。"""
        if not self.tail:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def insert_at(self, index: int, node: DoublyNode) -> None:
        """在指定位置插入節點（0-based）。"""
        if index < 0 or index > self.size:
            raise IndexError("索引超出範圍")
        if index == 0:
            self.insert_head(node)
            return
        if index == self.size:
            self.insert_tail(node)
            return
        curr = self.head
        for _ in range(index):
            curr = curr.next
        node.prev = curr.prev
        node.next = curr
        curr.prev.next = node
        curr.prev = node
        self.size += 1

    def delete_node(self, node: DoublyNode) -> None:
        """刪除指定節點。"""
        if not node:
            return
        if node == self.head:
            self.head = node.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif node == self.tail:
            self.tail = node.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        self.size -= 1

    def delete_head(self) -> Optional[DoublyNode]:
        """刪除頭部節點並返回。"""
        if not self.head:
            return None
        node = self.head
        self.delete_node(node)
        return node

    def delete_tail(self) -> Optional[DoublyNode]:
        """刪除尾部節點並返回。"""
        if not self.tail:
            return None
        node = self.tail
        self.delete_node(node)
        return node

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        values = []
        curr = self.head
        while curr:
            values.append(f"({curr.key}:{curr.value})")
            curr = curr.next
        return " <-> ".join(values) if values else "Empty"


class LRUCache:
    """LRU快取實作（使用雙向鏈結串列和雜湊表）。"""
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache: Dict[Any, DoublyNode] = {}
        self.dll = DoublyLinkedList()

    def get(self, key: Any) -> Any:
        """獲取鍵對應的值，若不存在返回-1。"""
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.dll.delete_node(node)
        self.dll.insert_head(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """插入或更新鍵值對。"""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.dll.delete_node(node)
            self.dll.insert_head(node)
        else:
            if len(self.cache) >= self.capacity:
                tail = self.dll.delete_tail()
                if tail:
                    del self.cache[tail.key]
            new_node = DoublyNode(key, value)
            self.dll.insert_head(new_node)
            self.cache[key] = new_node

    def __str__(self) -> str:
        return f"LRU Cache (容量{self.capacity}): {self.dll}"


if __name__ == "__main__":
    print("=== 雙向鏈結串列測試 ===")
    dll = DoublyLinkedList()
    n1 = DoublyNode(1, "A")
    n2 = DoublyNode(2, "B")
    dll.insert_tail(n1)
    dll.insert_tail(n2)
    print(f"初始串列: {dll}")
    n3 = DoublyNode(3, "C")
    dll.insert_head(n3)
    print(f"頭部插入: {dll}")
    dll.delete_node(n1)
    print(f"刪除節點1: {dll}")
    print(f"長度: {len(dll)}")

    print("\n=== LRU快取測試 ===")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(f"get(1): {lru.get(1)}")
    lru.put(3, 3)
    print(f"get(2): {lru.get(2)}")
    print(f"快取狀態: {lru}")
