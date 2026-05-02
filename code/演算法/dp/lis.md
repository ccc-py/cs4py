# 最長遞增子序列 (Longest Increasing Subsequence, LIS)

## 歷史背景

最長遞增子序列是經典的動態規劃問題，在計算機科學和生物資訊學中都有廣泛應用。

### 演算法發展

- **O(n²) DP**：經典的動態規劃解法
- **O(n log n)**：基於 patience sorting（耐心排序）的概念，由 David Aldous 和 Persi Diaconis 在 1999 年解釋
- **應用**：股票價格分析（最長上漲趨勢）、版本控制（最長公共前綴）

## 演算法原理

### O(n²) 動態規劃

```
定義 dp[i] = 以 nums[i] 結尾的最長遞增子序列長度

遞推式：
dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])

基底：每個元素至少可以自成序列，dp[i] >= 1

答案：max(dp[i] for all i)
```

**時間複雜度**：O(n²)
**空間複雜度**：O(n)

### O(n log n) Patience Sorting

```
核心概念：
維護一個陣列 tails，其中：
tails[i] = 長度為 i+1 的遞增子序列的最小可能結尾元素

對於每個 num：
1. 使用二分搜尋找到第一個 >= num 的位置 idx
2. 如果 idx == len(tails)，追加 num
3. 否則，tails[idx] = num

最後，len(tails) 就是 LIS 長度
```

**時間複雜度**：O(n log n)
**空間複雜度**：O(n)

## Patience Sorting 圖示

```
輸入：nums = [10, 9, 2, 5, 3, 7, 101, 18]

處理過程：
num=10: tails = [10]
num=9:  tails = [9]    (替換 10)
num=2:  tails = [2]    (替換 9)
num=5:  tails = [2, 5]
num=3:  tails = [2, 3] (替換 5)
num=7:  tails = [2, 3, 7]
num=101:tails = [2, 3, 7, 101]
num=18: tails = [2, 3, 7, 18] (替換 101)

LIS 長度 = 4
```

## 重建 LIS

### O(n²) 方法

使用 `prev` 陣列記錄每個元素的前驅：
```
prev[i] = 在 LIS 中 nums[i] 的前一個元素索引
重建：從 max_len 的結尾開始，沿著 prev 回溯
```

### O(n log n) 方法

需要維護 parent 指針：
```
對於每個 num，記錄：
- 它被放在哪個長度的子序列中
- 該子序列的前一個元素是誰
```

## 程式碼說明

### O(n log n) 核心

```python
def lis_patience_sorting(nums):
    tails = []
    for num in nums:
        idx = bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
    return len(tails)
```

### 重建 LIS（O(n²)）

```python
def lis_with_reconstruction(nums):
    dp = [1] * n
    prev = [-1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # 找到結尾
    end = max(range(n), key=lambda i: dp[i])

    # 回溯
    lis = []
    while end != -1:
        lis.append(nums[end])
        end = prev[end]
    lis.reverse()
```

## 應用場景

### 1. 股票分析

找出最長的股價上漲期間。

### 2. 生物資訊學

DNA 序列比對中的最長公共子序列（LCS）問題可以轉化為 LIS。

### 3. 版本控制

找出兩個版本之間的最長公共前綴。

### 4. 排程問題

在任務排程中，找出可以順利完成的任務序列。

## 變體問題

| 變體 | 說明 |
|------|------|
| LDS (最長遞減子序列) | 將序列反轉或取負數 |
| 非嚴格遞增 | 使用 <= 而非 < |
| 最長公共子序列 (LCS) | 兩個序列的 LCS 可以轉為 LIS |

## 複雜度比較

| 方法 | 時間 | 空間 | 可重建 |
|------|------|------|--------|
| O(n²) DP | O(n²) | O(n) | 容易 |
| O(n log n) | O(n log n) | O(n) | 較複雜 |

## 參考資料

- Fredman, M. L. (1975). *On computing the length of longest increasing subsequences*. Discrete Mathematics, 11(1), 29-35.
- Aldous, D., & Diaconis, P. (1999). *Longest increasing subsequences: from patience sorting to the Baik-Deift-Johansson theorem*. Bulletin of the American Mathematical Society, 36(4), 413-432.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
