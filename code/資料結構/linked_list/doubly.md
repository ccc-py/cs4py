# 雙向鏈結串列（Doubly Linked List）與LRU快取

## 歷史背景
雙向鏈結串列由Allen Newell和J.C. Shaw在1957年為資訊處理語言（IPL）設計時提出，每個節點包含前驅和後繼指針，允許雙向遍歷。LRU（Least Recently Used）快取淘汰策略由Les Belady在1966年提出，用於作業系統的頁面淘汰，結合雙向鏈結串列和雜湊表可實作O(1)時間複雜度的操作。

## 核心概念與原理
### 雙向鏈結串列
- 節點包含：值域、前驅指針（prev）、後繼指針（next）
- 插入刪除需修改兩個指針，時間複雜度O(1)
- 支援雙向遍歷，但增加記憶體開銷

### LRU快取
- 核心思想：淘汰最久未使用的項目
- 實作方式：
  1. 雜湊表：O(1)時間查找節點
  2. 雙向鏈結串列：頭部為最近使用，尾部為最久未使用
- 操作：
  - 訪問/插入：將節點移到頭部
  - 淘汰：刪除尾部節點

## 使用範例
```python
from doubly import DoublyLinkedList, LRUCache

dll = DoublyLinkedList()
n1 = DoublyNode(1, "A")
dll.insert_tail(n1)
print(dll)

lru = LRUCache(2)
lru.put(1, 1)
print(lru.get(1))
```

## 參考資料
- [Wikipedia: Doubly Linked List](https://en.wikipedia.org/wiki/Doubly_linked_list)
- [Wikipedia: LRU Cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU))
