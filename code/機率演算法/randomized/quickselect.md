# 隨機化快速選擇 (Randomized QuickSelect)

## 歷史背景

快速選擇演算法由 Tony Hoare 在 1961 年提出，與他發明的快速排序 (Quicksort) 演算法密切相關。Hoare 當時在開發翻譯俄語的程式時發現了這個演算法。

這個演算法解決了「選擇問題」：在未排序的列表中找到第 k 小（或第 k 大）的元素。與先排序再選擇的 O(n log n) 方法相比，快速選擇只需 O(n) 期望時間。

## 核心原理

### 演算法步驟

1. **選擇樞軸 (Pivot)**: 隨機選擇一個元素作為樞軸
2. **分割 (Partition)**: 將陣列分成小於樞軸、等於樞軸、大於樞軸的三部分
3. **遞迴選擇**: 根據樞軸的位置決定遞迴到哪個子陣列

### 時間複雜度分析

- **期望時間**: O(n)
- **最壞情況**: O(n²)（樞軸總是選到最小或最大元素）
- **隨機化的作用**: 確保最壞情況極不可能發生

### 為什麼是 O(n)？

每次遞迴呼叫處理的陣列大小約為上一次的 1/2（期望值），因此總工作量是：

$$
n + \frac{n}{2} + \frac{n}{4} + \cdots \approx 2n = O(n)
$$

## 使用範例

```python
from randomized.quickselect import quickselect, kth_largest

arr = [3, 2, 1, 5, 4]

# 找到第 3 小的元素 (0-indexed: k=2)
result = quickselect(arr, 2)
print(f"第 3 小: {result}")  # 輸出: 3

# 找到第 2 大的元素
result = kth_largest(arr, 2)
print(f"第 2 大: {result}")  # 輸出: 4
```

## 與其他方法比較

| 方法 | 時間複雜度 | 空間複雜度 | 是否修改原陣列 |
|------|-----------|-----------|---------------|
| 排序後選擇 | O(n log n) | O(1) 或 O(n) | 否 |
| QuickSelect | O(n) 期望 | O(log n) 遞迴 | 是（可用副本） |
| 中位數的中位數 | O(n) 最壞 | O(n) | 否 |
| 堆 (Heap) | O(n + k log n) | O(k) | 否 |

## 參考資料

1. Hoare, C. A. R. (1961). Algorithm 65: find. *Communications of the ACM*, 4(7), 321-322.
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Chapter 9.
3. Blum, M., Floyd, R. W., Pratt, V., Rivest, R. L., & Tarjan, R. E. (1973). Time bounds for selection. *Journal of Computer and System Sciences*, 7(4), 448-461.
