# 基數排序 (Radix Sort)

## 歷史背景

基數排序由 Herman Hollerith 於 1887 年為美國人口普查設計。Hollerith 發明了打孔卡片製表機（tabulating machine），使用基數排序原理對人口普查資料進行快速處理。這項發明不僅大大提高了人口普查的效率，也促成了後來 IBM 公司的成立。

### 重要特性

- **時間複雜度**：O(d × (n + b))
  - d：最大數的位數
  - n：元素數量
  - b：基數（十進制為 10）
- **空間複雜度**：O(n + b)
- **穩定排序**：是（當使用穩定子排序時）
- **比較排序**：否（非比較排序演算法）
- **適用範圍**：整數、字串等可分位處理的資料

## 演算法原理

### 核心思想

基數排序不直接比較元素大小，而是按位數進行排序：
- **LSD (Least Significant Digit)**：從最低位（個位）開始排序
- **MSD (Most Significant Digit)**：從最高位開始排序

### LSD 基數排序

```
原始陣列：[170, 45, 75, 90, 802, 24, 2, 66]

第1輪（個位）：
   170 (0), 90 (0), 802 (2), 2 (2), 24 (4), 45 (5), 75 (5), 66 (6)
   結果：[170, 90, 802, 2, 24, 45, 75, 66]

第2輪（十位）：
   2 (0), 802 (0), 24 (2), 45 (4), 66 (6), 170 (7), 75 (7), 90 (9)
   結果：[2, 802, 24, 45, 66, 170, 75, 90]

第3輪（百位）：
   2 (0), 24 (0), 45 (0), 66 (0), 75 (0), 90 (0), 170 (1), 802 (8)
   結果：[2, 24, 45, 66, 75, 90, 170, 802]

排序完成！
```

### 圖示

```
LSD 排序過程（以個位為例）：

原始：    170  45  75  90  802  24  2  66
按個位：  0   5   5   0   2    4   2  6
桶分佈：
  0: 170, 90
  1:
  2: 802, 2
  3:
  4: 24
  5: 45, 75
  6: 66
  7:
  8:
  9:

合併：    170, 90, 802, 2, 24, 45, 75, 66
```

## 程式碼說明

### 計數排序（子程序）

```python
def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # 統計每個數字出現次數
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    # 將計數轉換為位置
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 從後往前建構（保持穩定性）
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    return output
```

### LSD 基數排序

```python
def radix_sort_lsd(arr):
    if not arr:
        return []

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr
```

## MSD 基數排序

### 原理

MSD 從最高位開始排序，使用遞迴處理每個桶：

```python
def radix_sort_msd(arr, exp=None, start=0, end=None):
    if end is None:
        end = len(arr)

    if end - start <= 1:
        return arr

    # 建立 10 個桶
    buckets = [[] for _ in range(10)]

    # 分配到桶中
    for i in range(start, end):
        digit = (arr[i] // exp) % 10
        buckets[digit].append(arr[i])

    # 合併回原陣列
    idx = start
    for bucket in buckets:
        if bucket:
            arr[start:start + len(bucket)] = bucket
            start += len(bucket)

    # 遞迴處理每個桶
    start = idx
    for bucket in buckets:
        if len(bucket) > 1:
            radix_sort_msd(arr, exp // 10, start, start + len(bucket))
            start += len(bucket)

    return arr
```

### LSD vs MSD

| 特性 | LSD | MSD |
|------|-----|-----|
| 排序方向 | 從低位到高位 | 從高位到低位 |
| 是否需要遞迴 | 否 | 是 |
| 穩定性 | 穩定 | 可穩定 |
| 提前終止 | 否（必須處理所有位） | 是（桶大小 <= 1 時停止） |
| 實現難度 | 簡單 | 較複雜 |

## 字串基數排序

基數排序也可以應用於字串：

```python
def radix_sort_string(arr, max_len=None):
    if not arr:
        return []

    if max_len is None:
        max_len = max(len(s) for s in arr)

    for pos in range(max_len - 1, -1, -1):
        buckets = [[] for _ in range(27)]  # 26 字母 + 空字元

        for s in arr:
            if pos < len(s):
                char_idx = ord(s[pos]) - ord('a') + 1
            else:
                char_idx = 0  # 空字元排前面
            buckets[char_idx].append(s)

        arr = []
        for bucket in buckets:
            arr.extend(bucket)

    return arr
```

## 複雜度分析

| 情況 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| d 位數，基數 b | O(d × (n + b)) | O(n + b) |

### 為什麼是 O(d × (n + b))？

- 對每一位進行計數排序：O(n + b)
- 共有 d 位：乘以 d
- 總計：O(d × (n + b))

### 與比較排序比較

| 特性 | 基數排序 | 快速排序 | 合併排序 |
|------|---------|---------|---------|
| 時間複雜度 | O(dn) | O(n log n) | O(n log n) |
| 空間複雜度 | O(n+b) | O(log n) | O(n) |
| 穩定 | 是 | 否 | 是 |
| 比較 | 否 | 是 | 是 |
| 適用資料 | 整數、字串 | 任意可比較資料 | 任意可比較資料 |

## 應用場景

### 適合使用基數排序的情況

1. **固定長度整數**：如身分證字號、信用卡號
2. **字串排序**：特別是長度相近的字串
3. **大量資料**：當 d 相對較小時，可以比 O(n log n) 更快
4. **需要穩定排序**：且資料適合基數排序

### 不適合的情況

1. **資料範圍很大**：如 32 位元整數，d=10（十進制）
2. **浮點數**：不易按位處理
3. **任意比較函數**：基數排序依賴資料的位表示

## 實用考量

### 基數選擇

- **十進制 (b=10)**：人類直觀，程式碼簡單
- **二進制 (b=256)**：一次處理一個位元組，效率更高
- **更大的基數**：減少 d，但增加 b（空間換時間）

### 最佳化技巧

```python
# 使用位元組作為基數（b=256）
def radix_sort_bytes(arr):
    for shift in [0, 8, 16, 24]:  # 假設 32 位元整數
        # 對每個位元組進行計數排序
        ...
```

### 與內建排序比較

Python 的 `sorted()` 使用 Timsort，對於：
- 小資料：Timsort 可能更快（常數項小）
- 大資料：基數排序可能更快（當 d 不大時）

## 參考資料

- Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching* (2nd ed.). Addison-Wesley.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Seward, H. H. (1954). *Information sorting in the application of electronic digital computers to business operations*. Master's thesis, MIT.
- Hollerith, H. (1889). [Art of Compiling Statistics](https://doi.org/10.1145/1010626.1010642). U.S. Patent 395,782.
