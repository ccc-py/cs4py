"""
堆積排序 (Heap Sort)

歷史背景：
- 1964 年由 J. W. J. Williams 發明
- 配合 Robert Floyd 的原地堆積化演算法
- 利用堆積資料結構的排序演算法
- 時間複雜度恆定 O(n log n)
"""

from typing import List


class MinHeap:
    """最小堆積"""

    def __init__(self):
        self.heap = []

    def parent(self, i: int) -> int:
        return (i - 1) // 2

    def left(self, i: int) -> int:
        return 2 * i + 1

    def right(self, i: int) -> int:
        return 2 * i + 2

    def insert(self, val: int) -> None:
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty")
        min_val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return min_val

    def _sift_up(self, i: int) -> None:
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def _sift_down(self, i: int) -> None:
        n = len(self.heap)
        while True:
            smallest = i
            l = self.left(i)
            r = self.right(i)

            if l < n and self.heap[l] < self.heap[smallest]:
                smallest = l
            if r < n and self.heap[r] < self.heap[smallest]:
                smallest = r

            if smallest == i:
                break

            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    def __len__(self) -> int:
        return len(self.heap)


def heap_sort(arr: List[int]) -> List[int]:
    """
    堆積排序

    原理：
    1. 建立最大堆積
    2. 逐步取出最大元素放到陣列末端

    時間複雜度：O(n log n)
    空間複雜度：O(1)
    穩定排序：否
    """
    n = len(arr)
    if n <= 1:
        return arr[:]

    def sift_down(start: int, end: int) -> None:
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] < arr[child]:
                arr[root], arr[child] = arr[child], arr[root]
                root = child
            else:
                break

    for start in range((n - 2) // 2, -1, -1):
        sift_down(start, n - 1)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end - 1)

    return arr


def heap_sort_inplace(arr: List[int]) -> None:
    """原地堆積排序"""
    n = len(arr)

    def sift_down(start: int, end: int) -> None:
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] < arr[child]:
                arr[root], arr[child] = arr[child], arr[root]
                root = child
            else:
                break

    for start in range((n - 2) // 2, -1, -1):
        sift_down(start, n - 1)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end - 1)


def build_max_heap(arr: List[int]) -> None:
    """將陣列轉換為最大堆積"""
    n = len(arr)
    for start in range((n - 2) // 2, -1, -1):
        _sift_down(arr, start, n - 1)


def _sift_down(arr: List[int], start: int, end: int) -> None:
    root = start
    while True:
        child = 2 * root + 1
        if child > end:
            break
        if child + 1 <= end and arr[child] < arr[child + 1]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break


def heap_sort_with_steps(arr: List[int]) -> List[List[int]]:
    """返回排序過程的每一步（用於視覺化）"""
    steps = [arr[:]]
    n = len(arr)
    arr = arr[:]

    def sift_down(start: int, end: int) -> None:
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] < arr[child]:
                arr[root], arr[child] = arr[child], arr[root]
                root = child
            else:
                break

    for start in range((n - 2) // 2, -1, -1):
        sift_down(start, n - 1)
        steps.append(arr[:])

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        steps.append(arr[:])
        sift_down(0, end - 1)
        if end > 1:
            steps.append(arr[:])

    return steps


if __name__ == "__main__":
    print("=== 堆積排序 (Heap Sort) 測試 ===\n")

    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 3, 1, 1, 2, 2],
    ]

    print("【基本測試】")
    for arr in test_cases:
        original = arr[:]
        result = heap_sort(arr[:])
        print(f"輸入：{original}")
        print(f"輸出：{result}")
        print()

    print("【原地排序測試】")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"排序前：{arr}")
    heap_sort_inplace(arr)
    print(f"排序後：{arr}")
    print()

    print("【最小堆積演示】")
    heap = MinHeap()
    for val in [5, 3, 8, 1, 9, 2]:
        heap.insert(val)
        print(f"插入 {val}：{[heap.heap]}")

    print("\n取出元素：")
    while len(heap) > 0:
        val = heap.extract_min()
        print(f"  取出 {val}，剩餘：{heap.heap}")