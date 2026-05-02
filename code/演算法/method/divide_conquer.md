# 分治法 (Divide and Conquer)

## 分治法原理

分治法將一個難以直接解決的大問題，分割成一些規模較小的相同問題，逐個擊破。

### 三個步驟

1. **分解 (Divide)**：將原問題分解為若干個規模較小的子問題
2. **解決 (Conquer)**：遞迴地求解各子問題；若子問題夠小則直接求解
3. **合併 (Combine)**：將子問題的解合併成原問題的解

## 主定理 (Master Theorem)

對於遞迴式 T(n) = aT(n/b) + f(n)，其中 a ≥ 1, b > 1：

| 情況 | 條件 | 結果 |
|------|------|------|
| 1 | f(n) = O(n^(log_b(a)-ε)), ε > 0 | T(n) = Θ(n^(log_b(a))) |
| 2 | f(n) = Θ(n^(log_b(a)) * log^k(n)) | T(n) = Θ(n^(log_b(a)) * log^(k+1)(n)) |
| 3 | f(n) = Ω(n^(log_b(a)+ε)), ε > 0 且滿足正則條件 | T(n) = Θ(f(n)) |

### 常見例子

- **二分搜尋**：T(n) = T(n/2) + O(1) → O(log n)
- **合併排序**：T(n) = 2T(n/2) + O(n) → O(n log n)
- **快速冪**：T(n) = T(n/2) + O(1) → O(log n)

## 經典問題

### 1. 最近點對問題 (Closest Pair of Points)

**問題**：給定平面上 n 個點，找出距離最近的兩個點。

**暴力法**：O(n²) 檢查所有點對

**分治法**：
1. 按 x 座標排序，分成左右兩半
2. 遞迴求解左右兩邊的最近點對
3. 檢查跨過中線的點對

**時間複雜度**：O(n log n)

**關鍵優化**：對於跨越中線的點，只需檢查 y 座標相差小於目前最小距離的點，且每個點最多檢查常數個鄰居。

### 2. 二分搜尋 (Binary Search)

**問題**：在已排序陣列中尋找目標值。

**分治策略**：每次比較中間元素，將搜尋範圍減半。

**時間複雜度**：O(log n)

### 3. 快速冪 (Fast Power)

**問題**：計算 x^n。

**分治策略**：
- n 為偶數：x^n = (x^(n/2))²
- n 為奇數：x^n = x × x^(n-1)

**時間複雜度**：O(log n)

## 與動態規劃的比較

| 特性 | 分治法 | 動態規劃 |
|------|--------|---------|
| 子問題 | 獨立 | 重疊 |
| 解決方式 | 遞迴 | 遞迴或迭代 |
| 典型例子 | 合併排序、快速排序 | 背包問題、LCS |

## 應用場景

- **排序**：合併排序、快速排序
- **搜尋**：二分搜尋、k-d tree 搜尋
- **數值計算**：快速傅立葉變換 (FFT)
- **幾何問題**：最近點對、凸包
- **矩陣運算**：Strassen 矩陣乘法

## 參考資料

- [Divide and Conquer Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm)
- 《算法导论》（Introduction to Algorithms）- Chapter 4
- 《算法设计与分析》（Algorithm Design）- Kleinberg & Tardos
- Bentley, J. L., & Shamos, M. I. (1976). "Divide and conquer in multidimensional space"
