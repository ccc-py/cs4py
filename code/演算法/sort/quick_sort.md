# 快速排序 (Quick Sort)

## 歷史背景

快速排序由英國計算機科學家 Tony Hoare 於 1960 年提出，當時他在訪問莫斯科國立大學時發明了這個演算法。Hoare 最初是為了對俄語單字進行字典排序而設計的。

### 重要特性

- **平均時間複雜度**：O(n log n)
- **最壞時間複雜度**：O(n²)（已排序或反序陣列）
- **空間複雜度**：O(log n)（遞迴呼叫堆疊）
- **穩定排序**：否
- **原地排序**：是（大多數實現）

## 演算法原理

### 分治法 (Divide and Conquer)

```
1. 選擇一個 pivot（基準點）
2. 分割 (Partition)：將陣列分成兩部分
   - 左邊：<= pivot
   - 右邊：> pivot
3. 遞迴對左右兩部分進行快速排序
```

### 圖示

```
原始陣列：[38, 27, 43, 3, 9, 82, 10]
選擇 pivot = 10（最後一個元素）

分割過程：
[38, 27, 43, 3, 9, 82, 10]
 i                       pivot

比較 38 > 10，i 不動
比較 27 > 10，i 不動
比較 43 > 10，i 不動
比較 3 <= 10，交換 3 和 38：i=0
[3, 27, 43, 38, 9, 82, 10]
 i

比較 27 > 10，i 不動
比較 43 > 10，i 不動
比較 38 > 10，i 不動
比較 9 <= 10，交換 9 和 27：i=1
[3, 9, 43, 38, 27, 82, 10]
    i

最後交換 pivot 到正確位置：
[3, 9, 10, 38, 27, 82, 43]
         ↑ pivot 位置

遞迴排序左右兩部分：[3, 9] 和 [38, 27, 82, 43]
```

## 分割方法

### Lomuto 分割法

```python
def lomuto_partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**特點**：
- 簡單易懂
- 交換次數較多
- pivot 在最後

### Hoare 分割法（原始版本）

```python
def hoare_partition(arr, low, high):
    pivot = arr[(low + high) // 2]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]
```

**特點**：
- 效率更高（平均交換次數較少）
- 從兩端向中間掃描
- 返回值是分割點（不是 pivot 位置）

## 程式碼說明

### 基本快速排序

```python
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
```

## 改良版本

### 隨機化快速排序

```python
def randomized_partition(arr, low, high):
    random_idx = random.randint(low, high)
    arr[random_idx], arr[high] = arr[high], arr[random_idx]
    return lomuto_partition(arr, low, high)
```

**優點**：避免最壞情況（已排序陣列）的發生機率
**期望時間複雜度**：O(n log n)

### 三路快速排序 (Dutch National Flag)

```python
def quick_sort_3way(arr, low, high):
    if low >= high:
        return

    pivot = arr[(low + high) // 2]
    lt = low      # < pivot
    gt = high     # > pivot
    i = low       # == pivot

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    quick_sort_3way(arr, low, lt - 1)
    quick_sort_3way(arr, gt + 1, high)
```

**應用**：對於有大量重複元素的陣列特別有效
**時間複雜度**：接近 O(n)（當所有元素都相同時）

## 複雜度分析

| 情況 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 最佳 | O(n log n) | O(log n) |
| 平均 | O(n log n) | O(log n) |
| 最壞 | O(n²) | O(n) |

### 為什麼最壞是 O(n²)？

當陣列已排序，且每次都選最後一個元素作為 pivot：
- 第一次：分割出 1 個元素，剩下 n-1 個
- 第二次：分割出 1 個元素，剩下 n-2 個
- ...
- 總比較次數：n + (n-1) + ... + 1 = n(n+1)/2 = O(n²)

### 如何避免最壞情況？

1. **隨機選擇 pivot**：期望值 O(n log n)
2. **三數取中法**：選擇首尾中間三個元素的中位數
3. **切換閾值**：小陣列改用插入排序

## 與其他排序比較

| 特性 | 快速排序 | 合併排序 | 堆排序 |
|------|---------|---------|--------|
| 平均時間 | O(n log n) | O(n log n) | O(n log n) |
| 最壞時間 | O(n²) | O(n log n) | O(n log n) |
| 空間 | O(log n) | O(n) | O(1) |
| 穩定 | 否 | 是 | 否 |
| 原地 | 是 | 否 | 是 |

## 實用考量

### Python 的 sorted() 和 list.sort()

Python 使用 **Timsort**（混合排序），不是快速排序：
- 結合合併排序和插入排序
- 對部分有序資料特別快
- 穩定排序

### 何時使用快速排序？

- 資料隨機分布
- 記憶體有限（原地排序）
- 不需要穩定性
- 實務上通常比合併排序快（常數項小）

### 小陣列優化

```python
def quick_sort_optimized(arr, low, high):
    # 小陣列改用插入排序
    if high - low < 16:
        insertion_sort(arr, low, high)
        return

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_optimized(arr, low, pivot_idx - 1)
        quick_sort_optimized(arr, pivot_idx + 1, high)
```

## 參考資料

- Hoare, C. A. R. (1961). [Algorithm 64: Quicksort](https://doi.org/10.1145/366622.366644). *Communications of the ACM*, 4(7), 321.
- Sedgewick, R. (1978). [Implementing Quicksort Programs](https://doi.org/10.1145/355744.355749). *Communications of the ACM*, 21(10), 847-857.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Bentley, J. L., & McIlroy, M. D. (1993). [Engineering a Sort Function](https://doi.org/10.1137/0222071). *Software: Practice and Experience*, 23(11), 1249-1265.
