# 子集和問題 (Subset Sum Problem)

## 歷史背景

子集和問題是計算複雜度理論中的一個經典 NP-完全問題。它屬於 Karp 在 1972 年提出的 21 個 NP-完全問題之一。這個問題在密碼學（如 Merkle-Hellman 背包密碼系統）和資源分配問題中有重要應用。

## 核心原理

### 問題定義

給定一個整數集合 `nums` 和目標值 `target`，判斷是否存在一個子集，其元素和恰好等於 `target`。

### 動態規劃解法

使用二維布林 DP 表 `dp[i][j]`：
- `i` 表示考慮前 `i` 個元素
- `j` 表示目標和
- `dp[i][j] = True` 表示使用前 `i` 個元素可以組成和 `j`

**狀態轉移方程**：
```
dp[i][j] = dp[i-1][j] OR dp[i-1][j-nums[i-1]]
```

**優化**：可以使用滾動陣列將空間複雜度從 O(n×target) 降為 O(target)。

### 時間與空間複雜度

- **時間複雜度**：O(n × target)
- **空間複雜度**：O(n × target) 或 O(target)（優化後）

注意：這是偽多項式時間演算法，因為時間複雜度與目標值（輸入數值）有關，而非輸入大小。

## 使用範例

```python
from subset_sum import subset_sum_decision, subset_sum_reconstruct

# 決策版本
nums = [3, 34, 4, 12, 5, 2]
print(subset_sum_decision(nums, 9))   # True
print(subset_sum_decision(nums, 30))  # False

# 找出滿足條件的子集
subset = subset_sum_reconstruct(nums, 9)
print(subset)  # [4, 5] 或 [3, 4, 2] 等

# 計算子集數量
from subset_sum import subset_sum_count
print(subset_sum_count([1, 2, 3, 4, 5], 5))  # 3 (有 3 個子集和為 5)
```

## 回溯法找子集

當 DP 表填完後，可以通過回溯找出實際的子集：
1. 從 `dp[n][target]` 開始
2. 如果 `dp[i-1][j]` 為 True，表示沒有使用第 i 個元素
3. 如果 `dp[i-1][j-nums[i-1]]` 為 True，表示使用了第 i 個元素

## 應用場景

- **背包問題**的特例（每個物品的價值和重量相同）
- **密碼學**：背包密碼系統
- **資源分配**：預算分配問題
- **財務分析**：投資組合選擇

## 參考資料

1. [Subset Sum Problem - Wikipedia](https://en.wikipedia.org/wiki/Subset_sum_problem)
2. [NP-Complete Problems - Karp (1972)](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems)
3. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. pp. 1097-1100.
4. Kleinberg, J., & Tardos, É. (2006). *Algorithm Design*. Pearson Education.
