# 合併排序 (Merge Sort)

## 歷史背景

合併排序是經典的分治法排序演算法，由 John von Neumann 於 1945 年發明。

### 重要特性

- **穩定排序**：相同元素的相對順序不會改變
- **平均/最壞時間複雜度**：O(n log n)
- **空間複雜度**：O(n)（傳統實現）、O(n log n)（呼叫堆疊）
- **優點**：效能穩定，不會退化到 O(n²)
- **缺點**：需要額外記憶體空間

## 演算法原理

### 分治法 (Divide and Conquer)

```
1. 分 (Divide)：將陣列從中間分成兩半
2. 治 (Conquer)：遞迴排序兩個子陣列
3. 合併 (Merge)：將兩個有序子陣列合併
```

### 圖示

```
初始：[38, 27, 43, 3, 9, 82, 10]

分：
[38, 27, 43, 3]  [9, 82, 10]
[38, 27]  [43, 3]  [9, 82]  [10]
[38] [27]  [43] [3]  [9] [82]  [10]

治：
[27, 38]  [3, 43]  [9, 82]  [10]

合併：
[3, 27, 38, 43]  [9, 10, 82]
[3, 9, 10, 27, 38, 43, 82]
```

## 程式碼說明

### 核心函數

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)
```

### 合併函數

```python
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## 複雜度分析

| 情況 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 最佳 | O(n log n) | O(n) |
| 平均 | O(n log n) | O(n) |
| 最壞 | O(n log n) | O(n) |

### 為什麼是 O(n log n)？

```
遞迴深度：log n 層
每層合併：O(n)
總計：O(n log n)
```

## 與快速排序比較

| 特性 | 合併排序 | 快速排序 |
|------|---------|---------|
| 時間複雜度 | 穩定 O(n log n) | 平均 O(n log n)，最壞 O(n²) |
| 空間複雜度 | O(n) | O(log n) |
| 穩定排序 | 是 | 否 |
| 快取友善度 | 普通 | 較佳 |
| 原地實現 | 困難 | 容易 |

## 改良版本

### 底部優化

- 小陣列時改用插入排序（減少遞迴開銷）
- 典型閾值：16-32 個元素

### 自然合併排序

- 檢測已排序的片段，減少不必要的分割
- 適合部分有序的資料

### 並行合併排序

- 將左右半邊並行排序
- 在多核心系統上可達接近線性加速

## Python 實現要點

```python
# 原地版本（節省記憶體但實現複雜）
def merge_sort_inplace(arr, start=0, end=None):
    if end is None:
        end = len(arr)

    if end - start <= 1:
        return

    mid = (start + end) // 2
    merge_sort_inplace(arr, start, mid)
    merge_sort_inplace(arr, mid, end)

    # 原地合併操作...
```

## 參考資料

- Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching*. Addison-Wesley.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Sedgewick, R. (1978). *Implementing Quicksort Programs*. *Communications of the ACM*, 21(10), 847-857.