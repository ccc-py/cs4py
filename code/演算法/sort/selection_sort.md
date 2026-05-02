# 選擇排序 (Selection Sort)

## 歷史背景

選擇排序是一種簡單直觀的比較排序演算法，其概念可以追溯到計算機誕生初期。雖然效率不如更先進的排序演算法，但由於其邏輯簡單、容易實作，常被用於教學目的，幫助初學者理解排序的基本概念。

## 核心原理

### 基本選擇排序

選擇排序的工作原理如下：
1. 在未排序序列中找到最小（大）元素
2. 存放到排序序列的起始位置
3. 從剩餘未排序元素中繼續尋找最小（大）元素
4. 放到已排序序列的末尾
5. 重複步驟 3~4 直到所有元素排序完畢

**時間複雜度**：
- 最佳情況：O(n²)
- 最差情況：O(n²)
- 平均情況：O(n²)

**空間複雜度**：O(1)（原地排序）

### 雙向選擇排序

雙向選擇排序是選擇排序的改進版本，又稱為雙向選擇排序或改進的雞尾酒選擇排序。其核心思想是：
- 每次迭代同時找到未排序部分的最小值和最大值
- 將最小值放到左邊，最大值放到右邊
- 減少迭代次數，比較次數約為基本選擇排序的一半

## 使用範例

```python
from selection_sort import selection_sort, bidirectional_selection_sort

# 基本選擇排序
arr = [64, 34, 25, 12, 22, 11, 90]
result = selection_sort(arr)
print(result)  # [11, 12, 22, 25, 34, 64, 90]

# 雙向選擇排序
result2 = bidirectional_selection_sort(arr)
print(result2)  # [11, 12, 22, 25, 34, 64, 90]
```

## 演算法比較

| 排序演算法 | 時間複雜度 | 空間複雜度 | 穩定性 |
|-----------|-----------|-----------|--------|
| 選擇排序 | O(n²) | O(1) | 不穩定 |
| 雙向選擇排序 | O(n²) | O(1) | 不穩定 |
| 冒泡排序 | O(n²) | O(1) | 穩定 |
| 插入排序 | O(n²) | O(1) | 穩定 |

## 參考資料

1. [Selection Sort - Wikipedia](https://en.wikipedia.org/wiki/Selection_sort)
2. [雙向選擇排序 - 演算法筆記](http://www.csie.ntnu.edu.tw/~u91029/Sort.html)
3. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
