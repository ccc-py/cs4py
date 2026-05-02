# 桶排序 (Bucket Sort)

## 歷史背景

桶排序（Bucket Sort）由 E. J. Isaac 和 R. C. Singleton 在 1956 年提出，是一種分散式排序演算法。它將陣列分到有限數量的桶子裡，每個桶子再個別排序（通常使用其他排序演算法或遞迴使用桶排序）。桶排序是基數排序（Radix Sort）的廣義化。

## 核心原理

### 基本思想

桶排序的工作原理：
1. 設定一定數量的桶（bucket）
2. 將資料根據其值分配到對應的桶中
3. 對每個桶內的資料進行排序
4. 按順序合併所有桶的結果

### 時間複雜度

- **最佳情況**：O(n) - 當資料均勻分佈，每個桶只有一個元素
- **平均情況**：O(n + n²/k + k)，其中 k 是桶的數量
- **最差情況**：O(n²) - 當所有資料都分配到同一個桶

### 空間複雜度

O(n + k)，其中 k 是桶的數量

### 適用場景

桶排序特別適合：
- 資料均勻分佈在某一範圍內
- 可以預估資料的範圍
- 外部排序（External Sort）的基礎

## 使用範例

```python
from bucket_sort import bucket_sort, bucket_sort_uniform

# 均勻分佈在 [0, 1) 的資料
data1 = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21]
result1 = bucket_sort_uniform(data1, num_buckets=5)
print(result1)

# 任意範圍的資料
data2 = [42, 17, 85, 23, 69, 12, 99, 56]
result2 = bucket_sort(data2, num_buckets=5)
print(result2)
```

## 桶數量的選擇

桶數量對效能有顯著影響：

| 桶數量 | 效果 | 說明 |
|-------|------|------|
| 太少（如 1） | 退化為插入排序 | O(n²) |
| 適中 | 最佳效能 | 資料均勻分佈時接近 O(n) |
| 太多（接近 n） | 接近計數排序 | 空間開銷大 |

一般建議：桶數量約為 `√n` 或 `n/c`（c 為常數）

## 均勻分佈 vs 偏斜資料

桶排序對資料分佈很敏感：

- **均勻分佈**：每個桶的元素數量相近，效能接近 O(n)
- **偏斜分佈**：某些桶可能包含大量元素，效能會下降

## 參考資料

1. [Bucket Sort - Wikipedia](https://en.wikipedia.org/wiki/Bucket_sort)
2. [Sorting in Linear Time - MIT OCW](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-introduction-to-algorithms-sma-5503-fall-2005/)
3. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. pp. 198-202.
