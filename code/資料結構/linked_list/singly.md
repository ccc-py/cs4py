# 單向鏈結串列（Singly Linked List）

## 歷史背景
鏈結串列（Linked List）的概念最早由計算機科學家在20世紀50年代提出，用於解決陣列（Array）大小固定、插入刪除效率低的問題。單向鏈結串列是最基礎的鏈結串列形式，每個節點僅包含指向下一個節點的指針，實作簡單且動態擴展。

## 核心概念與原理
單向鏈結串列由一系列節點組成，每個節點包含兩個部分：
1. **值域**：儲存節點的資料
2. **指針域**：儲存指向下一個節點的引用

基本操作原理：
- **插入**：修改指針指向，無需移動其他元素，時間複雜度O(1)（頭尾插入）或O(n)（指定位置）
- **刪除**：修改前一個節點的指針，跳過目標節點，時間複雜度O(n)
- **搜尋**：遍歷串列直到找到目標，時間複雜度O(n)
- **反轉**：迭代修改每個節點的指針方向，時間複雜度O(n)
- **環檢測**：使用Floyd龜兔賽跑演算法，快指針每次走兩步，慢指針每次走一步，若存在環則兩者會相遇

## 使用範例
```python
from singly import SinglyLinkedList

ll = SinglyLinkedList()
ll.insert_tail(10)
ll.insert_tail(20)
ll.insert_head(5)
print(ll)  # 5 -> 10 -> 20
ll.reverse()
print(ll)  # 20 -> 10 -> 5
```

## 參考資料
- [Wikipedia: Linked List](https://en.wikipedia.org/wiki/Linked_list)
- [GeeksforGeeks: Singly Linked List](https://www.geeksforgeeks.org/singly-linked-list/)
