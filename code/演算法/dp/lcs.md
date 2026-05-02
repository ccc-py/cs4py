# 最長公共子序列 (Longest Common Subsequence, LCS)

## 歷史背景

最長公共子序列問題是計算機科學中的經典問題，最早由 David H. Lehmer 在 1960 年代研究。LCS 問題在差異比較工具（如 diff）、生物資訊學（DNA 序列比對）等領域有廣泛應用。

## 核心原理

### 問題定義

給定兩個序列，找出它們的最長公共子序列。子序列不要求連續，但必須保持原有順序。

### 動態規劃解法

**狀態定義**：`dp[i][j]` 表示第一個序列前 i 個字元與第二個序列前 j 個字元的 LCS 長度。

**狀態轉移方程**：
```
若 text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
否則:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**邊界條件**：`dp[0][j] = dp[i][0] = 0`

### 重建子序列

從 `dp[m][n]` 開始回溯：
- 若當前字元相同，加入結果，向左上移動
- 否則向較大的方向移動（上或左）

## 複雜度分析

| 方法 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 標準 DP | O(m × n) | O(m × n) |
| 空間優化 | O(m × n) | O(min(m, n)) |

其中 m, n 分別為兩個序列的長度。

## 應用場景

### 1. 差異比較工具 (diff)

比較兩個文件的差異，找出最長的公共部分。

### 2. 生物資訊學

- DNA/RNA/蛋白質序列比對
- 基因組序列分析
- 系統發育樹構建

### 3. 版本控制

Git 等版本控制系統使用類似算法來顯示文件差異。

### 4. 拼寫檢查與糾錯

計算編輯距離的基礎之一。

## 與其他問題的關係

- **最長公共子串 (Longest Common Substring)**：要求連續，解法類似但轉移方程不同
- **編輯距離 (Edit Distance)**：允許插入、刪除、替換操作
- **最短公共超序列 (Shortest Common Supersequence)**：LCS 的對偶問題

## 參考資料

- [Longest Common Subsequence - Wikipedia](https://en.wikipedia.org/wiki/Longest_common_subsequence_problem)
- 《算法导论》（Introduction to Algorithms）- Chapter 15.4
- 《生物学序列分析》（Biological Sequence Analysis）
- Hunt, J. W., & Szymanski, T. G. (1977). "A fast algorithm for computing longest common subsequences"
