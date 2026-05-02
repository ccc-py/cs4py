"""二元堆積（Binary Heap）實作，包含最大堆與最小堆。

歷史背景：
堆積是一種特殊的完全二元樹，最早由J. W. J. Williams在1964年提出，用於實作堆積排序（Heapsort）。二元堆積分為最大堆（父節點≥子節點）和最小堆（父節點≤子節點）。

核心概念：
- 完全二元樹：用陣列儲存，索引i的左右子節點為2i+1和2i+2，父節點為(i-1)//2
- 堆積化（heapify）：維持堆積性質的操作
- O(n)建堆：從最後一個非葉子節點開始heapify
"""

from typing import Any, List, Optional


class MaxHeap:
    """最大堆實作。"""
    def __init__(self) -> None:
        self.heap: List[Any] = []

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _heapify_up(self, i: int) -> None:
        """向上堆積化（插入後使用）。"""
        while i > 0 and self.heap[i] > self.heap[self._parent(i)]:
            self.heap[i], self.heap[self._parent(i)] = self.heap[self._parent(i)], self.heap[i]
            i = self._parent(i)

    def _heapify_down(self, i: int) -> None:
        """向下堆積化（刪除後使用）。"""
        while True:
            largest = i
            left = self._left(i)
            right = self._right(i)
            if left < len(self.heap) and self.heap[left] > self.heap[largest]:
                largest = left
            if right < len(self.heap) and self.heap[right] > self.heap[largest]:
                largest = right
            if largest == i:
                break
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            i = largest

    def push(self, val: Any) -> None:
        """插入元素。"""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> Any:
        """彈出最大值。"""
        if not self.heap:
            raise IndexError("堆積為空")
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek(self) -> Any:
        """查看最大值（不彈出）。"""
        if not self.heap:
            raise IndexError("堆積為空")
        return self.heap[0]

    @classmethod
    def heapify(cls, arr: List[Any]) -> 'MaxHeap':
        """從陣列建立堆積（O(n)時間）。"""
        heap = cls()
        heap.heap = arr[:]
        for i in range(len(arr) // 2 - 1, -1, -1):
            heap._heapify_down(i)
        return heap

    def __len__(self) -> int:
        return len(self.heap)


class MinHeap:
    """最小堆實作。"""
    def __init__(self) -> None:
        self.heap: List[Any] = []

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _heapify_up(self, i: int) -> None:
        while i > 0 and self.heap[i] < self.heap[self._parent(i)]:
            self.heap[i], self.heap[self._parent(i)] = self.heap[self._parent(i)], self.heap[i]
            i = self._parent(i)

    def _heapify_down(self, i: int) -> None:
        while True:
            smallest = i
            left = self._left(i)
            right = self._right(i)
            if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest == i:
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    def push(self, val: Any) -> None:
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> Any:
        if not self.heap:
            raise IndexError("堆積為空")
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek(self) -> Any:
        if not self.heap:
            raise IndexError("堆積為空")
        return self.heap[0]

    @classmethod
    def heapify(cls, arr: List[Any]) -> 'MinHeap':
        heap = cls()
        heap.heap = arr[:]
        for i in range(len(arr) // 2 - 1, -1, -1):
            heap._heapify_down(i)
        return heap

    def __len__(self) -> int:
        return len(self.heap)


def heapsort(arr: List[Any], reverse: bool = False) -> List[Any]:
    """使用堆積實作排序。"""
    if reverse:
        heap = MaxHeap.heapify(arr)
    else:
        heap = MinHeap.heapify(arr)
    return [heap.pop() for _ in range(len(heap))]


class PriorityQueue:
    """優先佇列（基於最小堆）。"""
    def __init__(self) -> None:
        self.heap = MinHeap()

    def enqueue(self, item: Any, priority: int) -> None:
        self.heap.push((priority, item))

    def dequeue(self) -> Any:
        return self.heap.pop()[1]

    def __len__(self) -> int:
        return len(self.heap)


if __name__ == "__main__":
    print("=== 最大堆測試 ===")
    max_heap = MaxHeap()
    for val in [3, 1, 4, 1, 5, 9, 2, 6]:
        max_heap.push(val)
    print(f"堆積: {max_heap.heap}")
    print(f"最大值: {max_heap.peek()}")
    print(f"彈出: {max_heap.pop()}")
    print(f"彈出後: {max_heap.heap}")

    print("\n=== 最小堆測試 ===")
    min_heap = MinHeap.heapify([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"堆積: {min_heap.heap}")
    print(f"最小值: {min_heap.peek()}")

    print("\n=== 堆積排序測試 ===")
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"升序: {heapsort(arr)}")
    print(f"降序: {heapsort(arr, reverse=True)}")

    print("\n=== 優先佇列測試 ===")
    pq = PriorityQueue()
    pq.enqueue("任務1", 3)
    pq.enqueue("任務2", 1)
    pq.enqueue("任務3", 2)
    print(f"處理順序: {pq.dequeue()}, {pq.dequeue()}, {pq.dequeue()}")
