# 背包問題 FPTAS (Knapsack FPTAS)

## 歷史背景

0/1 背包問題是組合優化中的經典 NP-完全問題，FPTAS 提供了一個多項式時間近似方案。

### 發展歷程

- **1957 年**：Danskin 提出背包問題的動態規劃解法
- **1972 年**：Karp 證明背包問題是 NP-完全問題
- **1975 年**：Ibarra 和 Kim 提出第一個 FPTAS
- **1979 年**：Lawler 提出更簡潔的 FPTAS

## 演算法原理

### 問題定義

```
給定 n 個物品，每個物品有重量 w_i 和價值 v_i，
背包容量 W。

目標：選擇物品子集，使得總重量 <= W，
且總價值最大化。

0/1 限制：每個物品要麼全選，要麼不選。
```

### 精確動態規劃（偽多項式時間）

```
dp[i][w] = 前 i 個物品，重量恰好 w 時的最大價值

遞推式：
dp[i][w] = max(dp[i-1][w], dp[i-1][w-w_i] + v_i)

時間複雜度：O(n * W)（偽多項式，依賴於 W）
```

### FPTAS（完全多項式時間近似方案）

```
核心思想：縮放價值以減少值域

步驟：
1. 設 max_v = max(v_i)
   計算縮放因子 k = (epsilon * max_v) / n
2. 縮放價值：v'_i = floor(v_i / k)
   （現在 v'_i 在 [0, n/epsilon] 範圍內）
3. 對縮放後的價值跑動態規劃
4. 返回對應原價值的結果

近似保證：得到的價值 >= (1 - epsilon) * OPT
時間複雜度：O(n^2 / epsilon)
```

### 為什麼叫「完全」近似方案？

```
PTAS (Polynomial Time Approximation Scheme)：
  對固定的 epsilon，存在多項式時間演算法
  但多項式的階數可能依賴於 epsilon

FPTAS (Fully PTAS)：
  執行時間是 n 和 1/epsilon 的多項式
  即 O(n^k * poly(1/epsilon))
```

## 程式碼說明

### 價值縮放

```python
# 計算縮放因子
k = (epsilon * max_val) / n

# 縮放為整數
scaled_values = [int(v / k) for v in values]
```

### 縮放後的動態規劃

```python
# 值域縮小到 O(n/epsilon)
max_scaled = max(scaled_values)
dp = [[inf] * (max_scaled + 1) for _ in range(n + 1)]

# 狀態：dp[i][v] = 前 i 個物品，縮放價值為 v 時的最小重量
```

## 應用場景

### 1. 投資組合選擇

```
預算有限，多個投資項目各有成本和預期收益，
選擇項目組合以最大化總收益。
```

### 2. 貨物裝載

```
貨船有載重限制，選擇貨物以最大化總價值。
```

### 3. 廣告預算分配

```
預算限制下，選擇廣告渠道以最大化覆蓋或轉化。
```

## 圖例

```
示例：n=4, W=8
物品：(重量, 價值)
  0: (2, 3)
  1: (3, 4)
  2: (4, 5)
  3: (5, 6)

精確解：選物品 0, 1, 2（重量 9 > 8，不行）
        選物品 0, 1, 3（重量 10 > 8，不行）
        選物品 1, 2（重量 7，價值 9）✓
        選物品 0, 3（重量 7，價值 9）✓

最大價值 = 9
```

## 演算法比較

| 演算法 | 近似比 | 時間複雜度 | 說明 |
|--------|--------|-----------|------|
| 貪婪（價值密度） | 無保證 | O(n log n) | 快速啟發式 |
| 動態規劃 | 1 (精確) | O(nW) | 偽多項式 |
| FPTAS | (1-ε) | O(n²/ε) | 完全近似方案 |

## 參考資料

- Ibarra, O. H., & Kim, C. E. (1975). *Fast approximation algorithms for the knapsack and sum of subset problems*. Journal of the ACM, 22(4), 463-468.
- Lawler, E. L. (1979). *Fast approximation algorithms for knapsack problems*. Mathematics of Operations Research, 4(4), 339-356.
- Vazirani, V. V. (2001). *Approximation Algorithms*. Springer.
