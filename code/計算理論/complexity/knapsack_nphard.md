# 背包問題（NP-Hard）(Knapsack Problem)

## 為什麼背包問題是 NP-Hard？

**背包問題 (Knapsack Problem)** 是組合最佳化中的經典問題，於 1972 年被 **Richard Karp** 證明為 NP-Hard。

### 問題定義（0-1 背包）

給定 n 個物品，每個物品 i 有：
- 重量 w[i]
- 價值 v[i]

以及背包容量 W。目標是選擇物品的子集，使得：
- 總重量不超過 W
- 總價值最大化

### NP-Hard 證明概要

Karp 在 1972 年的論文《Reducibility among combinatorial problems》中證明了：

1. **子集和問題 (Subset Sum Problem)** 可以歸約到背包問題
   - 子集和：給定集合 S 和目標 T，是否存在子集和等於 T？
   - 轉換：設每個物品重量 = 價值 = s[i]，容量 W = T
   - 如果存在子集和 = T，則最大價值 = T

2. 子集和問題是 NP-Complete 的（可以從 3SAT 歸約）

3. 因此背包問題也是 NP-Hard 的

### 重要結論

- 背包問題的**最佳化版本**是 NP-Hard
- 背包問題的**判定版本**是 NP-Complete
- 目前沒有已知的**多項式時間**演算法能解決所有情況

## 核心原理

### 0-1 背包的特性

每個物品只能選或不選（0 或 1），不能部分選擇。

### 解法比較

| 方法 | 時間複雜度 | 說明 |
|------|-----------|------|
| 暴力法 | O(2ⁿ) | 列舉所有 2ⁿ 個子集 |
| 動態規劃 | O(nW) | 偽多項式時間 (Pseudo-polynomial) |
| 近似演算法 | 多項式 | 可以得到接近最佳的解 |

### 偽多項式時間 (Pseudo-polynomial Time)

動態規劃的 O(nW) 不是真正的多項式時間，因為：

- 輸入大小：n 個物品 + log(W) 位元表示容量
- 實際時間：O(n × 2^log(W))
- 這是指數於輸入大小的

因此，背包問題仍然是 NP-Hard，但對於「小」容量，動態規劃非常實用！

## 使用範例

```python
from knapsack_nphard import (
    brute_force_knapsack, dp_knapsack,
    create_example_knapsack
)

# 建立範例
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 8
names = ['物品A', '物品B', '物品C', '物品D']

# 暴力求解（適用於小 n）
max_val, items = brute_force_knapsack(weights, values, capacity)
print(f"最大價值: {max_val}")
print(f"選中物品: {[names[i] for i in items]}")

# 動態規劃求解
max_val, items = dp_knapsack(weights, values, capacity)
print(f"最大價值: {max_val}")
print(f"選中物品: {[names[i] for i in items]}")
```

輸出：
```
最大價值: 10
選中物品: ['物品B', '物品C']
總重量: 7
```

## 參考資料

1. Karp, R. M. (1972). *Reducibility among combinatorial problems*. In R. E. Miller & J. W. Thatcher (Eds.), Complexity of Computer Computations (pp. 85-103). Plenum Press.

2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 16.2: Dynamic Programming - 0-1 Knapsack)

3. Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.

4. Martello, S., & Toth, P. (1990). *Knapsack Problems: Algorithms and Computer Implementations*. John Wiley & Sons.
