# 硬幣找零問題 (Coin Change Problem)

## 歷史背景

硬幣找零問題是動態規劃中的經典問題，屬於無界背包（Unbounded Knapsack）問題的特例。

### 相關問題

- **0-1 背包**：每種物品只能選一次
- **無界背包**：每種物品可以選無限次（硬幣找零屬於此類）
- **完全背包**：同無界背包

## 演算法原理

### 問題 1：最小硬幣數

```
定義 dp[x] = 湊成金額 x 所需的最少硬幣數

基底：
dp[0] = 0（金額 0 不需要硬幣）
dp[x] = ∞ for x > 0

遞推式：
對於每個金額 x 和每種硬幣 coin：
如果 coin <= x：
    dp[x] = min(dp[x], dp[x - coin] + 1)
```

**時間複雜度**：O(amount * len(coins))
**空間複雜度**：O(amount)

### 問題 2：組合數

```
定義 dp[x] = 湊成金額 x 的方式數

基底：
dp[0] = 1（空組合）

遞推式：
對於每種硬幣 coin：
    對於 x 從 coin 到 amount：
        dp[x] += dp[x - coin]
```

**注意**：這計算的是組合數（不考慮順序），例如使用 [1, 2] 湊 3：
- 1+1+1 和 1+1+1 算同一種（順序不同不算新方式）

### 重建硬幣使用

使用 `used_coin` 陣列記錄每個金額所使用的硬幣：
```
used_coin[x] = 湊成金額 x 時，最後使用的硬幣面額

重建：
while x > 0:
    coin = used_coin[x]
    加入 coin 到結果
    x -= coin
```

## 程式碼說明

### 最小硬幣數核心

```python
def min_coins(coins, amount):
    dp = [inf] * (amount + 1)
    dp[0] = 0

    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x:
                dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != inf else -1
```

### 組合數核心

```python
def count_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]
```

## 應用場景

### 1. 自動販賣機

計算找零所需的最少硬幣數。

### 2. 貨幣系統分析

給定一組硬幣面額，判斷是否能夠湊成任意金額（Canonical Coin System）。

### 3. 資源分配

在預算限制下，選擇最少的資源組合。

### 4. 付款優化

使用最少數量的紙鈔和硬幣進行付款。

## 經典範例

```
硬幣：[1, 5, 10, 25]
金額：67

最少硬幣數：
67 = 25 + 25 + 10 + 5 + 1 + 1 = 6 枚
或 67 = 25 + 25 + 10 + 5 + 1 + 1 = 6 枚

其他組合：
67 = 25*2 + 10*1 + 5*2 + 1*2 = 7 枚（不是最少）
```

## 變體問題

| 變體 | 說明 |
|------|------|
| 最少硬幣數 | 本文件主要討論的問題 |
| 組合數 | 計算有多少種湊成方式 |
| 排列數 | 考慮順序的方式數 |
| 恰好 vs 不超過 | 是否允許金額小於目標 |

## 複雜度分析

| 問題 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 最小硬幣數 | O(amount * n) | O(amount) |
| 組合數 | O(amount * n) | O(amount) |

其中 n = len(coins)。

## 參考資料

- Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 16.2)
- Kozen, D. C. (1992). *The Design and Analysis of Algorithms*. Springer.
