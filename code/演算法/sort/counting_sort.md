# 計數排序 (Counting Sort)

## 歷史背景

計數排序是一種非比較排序演算法，由 Harold H. Seward 於 1954 年在他的碩士論文中提出。

### 非比較排序

傳統的比較排序（如合併排序、快速排序）有 O(n log n) 的下界，但計數排序利用整數鍵值的特性，可以達到線性時間 O(n + k)。

### 應用場景

- 排序整數，且數值範圍 k 不太大
- 作為基數排序（Radix Sort）的子程序
- 需要穩定排序的場合

## 演算法原理

### 標準計數排序

```
步驟：
1. 找出陣列中的最大值 max_val
2. 建立大小為 max_val + 1 的計數陣列 count
3. 遍歷輸入陣列，統計每個值的出現次數
4. 將 count 轉換為累積計數：
   count[i] 表示 ≤ i 的元素個數
5. 從後往前遍歷原陣列（保持穩定性）：
   - 對於元素 arr[i] = x
   - 將其放入結果陣列的索引 count[x] - 1
   - count[x] -= 1
```

**圖示**：
```
輸入：arr = [4, 2, 2, 8, 3, 3, 1]

Step 1: 統計次數
count = [1, 2, 2, 1, 1, 0, 0, 0, 1]  (索引 0-8)

Step 2: 累積計數
count = [1, 3, 5, 6, 7, 7, 7, 7, 8]

Step 3: 從後往前放置
i=6: arr[6]=1, count[1]=3 -> result[2]=1, count[1]=2
i=5: arr[5]=3, count[3]=6 -> result[5]=3, count[3]=5
...
結果：[1, 2, 2, 3, 3, 4, 8]
```

## 複雜度分析

| 情況 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 一般情況 | O(n + k) | O(k) |
| 最佳 | O(n + k) | O(k) |
| 最壞 | O(n + k) | O(k) |

其中 k 是數值範圍（max_val - min_val + 1）。

### 適用條件

- **優點**：當 k = O(n) 時，時間複雜度為 O(n)
- **缺點**：當 k 很大（如排序 32 位元整數）時，空間消耗過大

## 穩定性

計數排序是穩定排序，因為：
1. 使用累積計數確定位置
2. 從後往前遍歷原陣列，相同值的元素保持原始相對順序

## 程式碼說明

### 核心程式碼

```python
def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)

    # 統計次數
    for num in arr:
        count[num] += 1

    # 累積計數
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # 從後往前放置（穩定）
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        count[num] -= 1
        result[count[num]] = num

    return result
```

### 處理負數

```python
def counting_sort_range(arr):
    min_val, max_val = min(arr), max(arr)
    range_size = max_val - min_val + 1
    count = [0] * range_size

    # 偏移：num - min_val 作為索引
    for num in arr:
        count[num - min_val] += 1
    # ...
```

## 基數排序中的應用

計數排序是基數排序的核心子程序：

```
基數排序：
1. 從最低位（個位）開始
2. 對當前位數使用穩定排序（計數排序）
3. 重複直到最高位

時間複雜度：O(d * (n + k))
- d: 最大位數
- k: 基數（10 進位則 k=10）
```

## 應用場景

### 1. 年齡排序

年齡範圍通常在 0-150，非常適合計數排序。

### 2. 成績排序

0-100 分的成績，直接計數排序。

### 3. 字元排序

ASCII 字元（0-127）或 Unicode 字元（BMP 0-65535）。

### 4. 作為基數排序的子程序

處理大量整數時，基數排序使用計數排序對每位進行穩定排序。

## 與其他排序比較

| 特性 | 計數排序 | 合併排序 | 快速排序 |
|------|---------|---------|---------|
| 比較次數 | 0（非比較） | O(n log n) | O(n log n) |
| 時間複雜度 | O(n + k) | O(n log n) | O(n log n) |
| 空間複雜度 | O(k) | O(n) | O(log n) |
| 穩定 | 是 | 是 | 否 |
| 適用資料 | 整數（範圍小） | 任意可比較 | 任意可比較 |

## 參考資料

- Seward, H. H. (1954). *Information sorting in the application of electronic digital computers to business operations*. Master's thesis, MIT.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 8.2)
- Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching* (2nd ed.). Addison-Wesley.
