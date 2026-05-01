# 堆積排序 (Heap Sort)

## 歷史背景

堆積排序由 J. W. J. Williams 於 1964 年發明，配合 Robert Floyd 的原地堆積化演算法，成為經典的 O(n log n) 排序演算法。

### 重要特性

- **時間複雜度**：恆定 O(n log n)
- **空間複雜度**：O(1)
- **穩定排序**：否
- **原地排序**：是

## 堆積資料結構

### 什麼是堆積？

堆積是一個完全二元樹，滿足堆積屬性：
- **最大堆積**：父節點 >= 子節點
- **最小堆積**：父節點 <= 子節點

### 陣列表示

由於是完全二元樹，可以用陣列高效表示：

```
索引 i 的節點：
- 父節點：(i - 1) // 2
- 左子節點：2 * i + 1
- 右子節點：2 * i + 2
```

```
        90
       /  \
     82    43
    /  \   / \
   12  34 25  11

陣列：[90, 82, 43, 12, 34, 25, 11]
```

## 演算法原理

### 兩個階段

```
1. 建立最大堆積：将数组重新排列成最大堆積
2. 逐步取出：不断取出最大元素放到陣列末端
```

### 圖示

```
初始：[4, 10, 3, 5, 1]

階段1：建立最大堆積
       4              4              10
      / \            / \            / \
    10    3    →   10    3    →    4    3
    /            /                 /
   5            5                 5

       10
      /  \
     4    3
    / \
   5   1

階段2：逐步取出最大
  [10, 4, 3, 5, 1] → 交換 10 和 1 → sift_down → [5, 4, 3, 1, 10]
  [5, 4, 3, 1, 10] → 交換 5 和 1 → sift_down → [1, 4, 3, 5, 10]
  ...
  [1, 2, 3, 5, 10]
```

## 程式碼說明

### 核心：sift_down

```python
def sift_down(arr, start, end):
    root = start
    while True:
        child = 2 * root + 1
        if child > end:
            break
        # 選較大的子節點
        if child + 1 <= end and arr[child] < arr[child + 1]:
            child += 1
        # 如果子節點更大，交換並繼續
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break
```

### 建立堆積

```python
# 從最後一個非葉節點開始
for start in range((n - 2) // 2, -1, -1):
    sift_down(start, n - 1)
```

### 排序

```python
for end in range(n - 1, 0, -1):
    # 將最大元素移到末端
    arr[0], arr[end] = arr[end], arr[0]
    # 對根節點進行 sift_down
    sift_down(0, end - 1)
```

## 複雜度分析

| 階段 | 時間複雜度 | 說明 |
|------|-----------|------|
| 建立堆積 | O(n) | 從 n/2 個節點開始 sift_down |
| 排序 | O(n log n) | n-1 次 extract_max，每次 O(log n) |
| 總計 | O(n log n) | 恆定 |

## 與其他排序比較

| 特性 | 堆積排序 | 快速排序 | 合併排序 |
|------|---------|---------|---------|
| 時間複雜度 | O(n log n) | 平均 O(n log n) | O(n log n) |
| 空間複雜度 | O(1) | O(log n) | O(n) |
| 穩定排序 | 否 | 否 | 是 |
| 快取效能 | 較差 | 較好 | 較好 |
| 最壞情況 | O(n log n) | O(n²) | O(n log n) |

## Python 的 heapq 模組

```python
import heapq

# 最小堆積
heap = [1, 3, 5, 7, 9]
heapq.heapify(heap)  # 建立堆積
heapq.heappush(heap, 2)  # 插入
heapq.heappop(heap)  # 彈出最小值

# 最大堆積：存入負值
heapq.nlargest(k, arr)  # 前 k 大的元素
heapq.nsmallest(k, arr)  # 前 k 小的元素
```

## 優缺點

### 優點
- 最壞情況也是 O(n log n)
- 原地排序，空間效率高
- 可用於優先級佇列實現

### 缺點
- 不是穩定排序
- 快取效能較差
- 實際效能通常比快速排序慢

## 參考資料

- Williams, J. W. J. (1964). [Algorithm 232: Heapsort](https://doi.org/10.1145/512274.512284). *Communications of the ACM*, 7(6), 347-348.
- Floyd, R. W. (1964). [Algorithm 245: Treesort](https://doi.org/10.1145/512274.512285). *Communications of the ACM*, 7(12), 701.
- Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching*. Addison-Wesley.