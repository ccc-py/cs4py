# 二元堆積（Binary Heap）與堆積排序

## 歷史背景
堆積由J. W. J. Williams在1964年提出，用於實作堆積排序（Heapsort）。二元堆積是一種特殊的完全二元樹，分為最大堆和最小堆，廣泛應用於優先佇列、圖演算法的Dijkstra、排程系統等場景。

## 核心概念與原理
### 二元堆積性質
- **完全二元樹**：所有層除最後一層外均填滿，最後一層靠左對齊
- **最大堆**：父節點值 ≥ 子節點值，根節點為最大值
- **最小堆**：父節點值 ≤ 子節點值，根節點為最小值

### 陣列儲存
完全二元樹可用陣列緊湊儲存，索引關係：
- 父節點：`(i - 1) // 2`
- 左子節點：`2i + 1`
- 右子節點：`2i + 2`

### 操作時間複雜度
- 插入（push）：O(log n)
- 彈出（pop）：O(log n)
- 建堆（heapify）：O(n)（從最後一個非葉子節點開始向下調整）

## 使用範例
```python
from binary_heap import MaxHeap, heapsort

heap = MaxHeap()
heap.push(5)
heap.push(3)
print(heap.pop())
print(heapsort([3,1,2]))
```

## 參考資料
- [Wikipedia: Binary Heap](https://en.wikipedia.org/wiki/Binary_heap)
- [GeeksforGeeks: Binary Heap](https://www.geeksforgeeks.org/binary-heap/)
