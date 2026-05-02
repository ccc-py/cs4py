# 矩陣鏈乘積最佳化 (Matrix Chain Multiplication)

## 歷史背景

矩陣鏈乘積最佳化問題是動態規劃的經典例題之一，由 Alfred V. Aho、John E. Hopcroft 和 Jeffrey D. Ullman 在 1974 年的《The Design and Analysis of Computer Algorithms》中系統化介紹。該問題展示了動態規劃如何處理具有最優子結構（Optimal Substructure）特性的問題。

## 核心原理

### 問題定義

給定 n 個矩陣的鏈 A1, A2, ..., An，其中矩陣 Ai 的維度為 p[i-1] × p[i]。目標是找出計算乘積 A1 × A2 × ... × An 的最優括號化方式，使得標量乘法次數最少。

### 為什麼需要最佳化？

矩陣乘法滿足結合律，但不同的括號化方式會導致不同的計算成本。

**例子**：三個矩陣 A(10×30), B(30×5), C(5×60)
- (AB)C：10×30×5 + 10×5×60 = 1500 + 3000 = 4500 次乘法
- A(BC)：10×30×60 + 30×5×60 = 18000 + 9000 = 27000 次乘法

差距達 6 倍之多！

### 動態規劃解法

**狀態定義**：`m[i][j]` 表示計算矩陣鏈 Ai..j 的最少乘法次數。

**狀態轉移方程**：
```
m[i][j] = min(m[i][k] + m[k+1][j] + p[i-1]×p[k]×p[j]), for i ≤ k < j
```

**最優子結構**：問題的最優解包含子問題的最優解。

**重疊子問題**：相同的子鏈會被重複計算，用 DP 表存儲避免重複。

## 複雜度分析

- **時間複雜度**：O(n³)，三層循環
- **空間複雜度**：O(n²)，存儲 m 表和 s 表

## 重建最佳括號化

使用分割點表 s[i][j] 記錄每個子問題的最優分割點：
- 若 s[i][j] = k，表示在 k 處分割最優
- 遞迴重建：`(A[i..k])(A[k+1..j])`

## 應用場景

1. **編譯器優化**：表達式計算的順序優化
2. **圖形學**：矩陣變換的組合
3. **科學計算**：大型矩陣運算的最佳化
4. **張量運算**：深度學習中的維度轉換

## 與其他問題的關係

- **最優二叉搜尋樹**：同樣的 DP 框架
- **凸多邊形三角剖分**：數學結構相似
- **語法分析**：某些文法的分析表構建

## 參考資料

- [Matrix Chain Multiplication - Wikipedia](https://en.wikipedia.org/wiki/Matrix_chain_multiplication)
- 《算法导论》（Introduction to Algorithms）- Chapter 15.2
- Aho, A. V., Hopcroft, J. E., & Ullman, J. D. (1974). "The Design and Analysis of Computer Algorithms"
- 《动态规划算法详解》
