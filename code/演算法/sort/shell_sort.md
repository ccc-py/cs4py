# 希爾排序 (Shell Sort)

## 歷史背景

希爾排序（Shell Sort）由 Donald Shell 於 1959 年提出，是第一批突破 O(n²) 時間複雜度的排序演算法之一。這個演算法是插入排序的改進版本，通過允許交換相距較遠的元素來解決插入排序只能相鄰元素交換的問題。

Shell 的原始序列使用了 `n/2, n/4, ..., 1` 的間隔，後來許多研究者提出了更優秀的間隔序列，如 Hibbard、Knuth、Sedgewick 等。

## 核心原理

### 基本思想

希爾排序的核心概念是：
1. 先將整個待排序的記錄序列分割成若干子序列
2. 對每個子序列進行插入排序
3. 逐漸減小間隔（gap），重複上述過程
4. 最後當間隔為 1 時，就是普通的插入排序

### 為什麼有效？

- 較大的間隔可以讓元素快速移動到大致正確的位置
- 隨著間隔減小，陣列變得越來越「接近排序好」
- 最後的插入排序（gap=1）只需要做少量的調整

### 間隔序列

不同的間隔序列會影響演算法的效能：

| 序列名稱 | 公式 | 時間複雜度 | 說明 |
|---------|------|-----------|------|
| Shell | n/2, n/4, ... | O(n²) ~ O(n log² n) | 原始序列 |
| Hibbard | 2^k - 1 | O(n^(3/2)) | 較佳的序列 |
| Knuth | (3^k - 1)/2 | O(n^(3/2)) | 實務常用 |
| Sedgewick | 混合序列 | O(n^(4/3)) | 已知最佳之一 |

## 使用範例

```python
from shell_sort import shell_sort_with_gaps, shell_gaps, hibbard_gaps

# 使用 Shell 的間隔序列
arr = [64, 34, 25, 12, 22, 11, 90]
gaps = shell_gaps(len(arr))
result = shell_sort_with_gaps(arr, gaps)
print(result)  # [11, 12, 22, 25, 34, 64, 90]

# 使用 Hibbard 的間隔序列
gaps = hibbard_gaps(len(arr))
result = shell_sort_with_gaps(arr, gaps)
print(result)
```

## 時間與空間複雜度

- **時間複雜度**：取決於間隔序列
  - 最差：O(n²)
  - 使用好的序列：O(n^(3/2)) 或更好
- **空間複雜度**：O(1)（原地排序）
- **穩定性**：不穩定

## 適用場景

希爾排序適合：
- 中等大小的陣列（幾千個元素）
- 希望比 O(n²) 快，但不需要 O(n log n) 的複雜實作
- 記憶體受限的環境（原地排序）

## 參考資料

1. [Shell Sort - Wikipedia](https://en.wikipedia.org/wiki/Shellsort)
2. [Shellsort - National Institute of Standards and Technology](https://www.nist.gov/publications/shellsort)
3. Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching* (2nd ed.). Addison-Wesley.
4. Sedgewick, R. (1986). "A New Upper Bound for Shellsort". *Journal of Algorithms*.
