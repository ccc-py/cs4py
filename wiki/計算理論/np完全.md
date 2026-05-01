# NP-完備性簡介 (NP-Completeness)

## 歷史背景

NP-完備 (NP-Complete) 是計算複雜度理論中最重要的概念之一。

### 重要里程碑

- **1971 年**：Stephen Cook 證明了 SAT 是 NP-完備的（Cook-Levin 定理）
- **1972 年**：Richard Karp 證明了 21 個問題是 NP-完備的
- **至今**：已發現數千個 NP-完備問題

## 核心概念

### 定義

問題 L 是 NP-完備的，如果：
1. **L ∈ NP**（L 在 NP 中）
2. **L 是 NP-hard**：所有 NP 問題都可以在多項式時間內歸約到 L

### 意義

- 如果任何 NP-完備問題有 P 演算法，則 **P = NP**
- 目前沒有發現 NP-完備問題的 P 演算法（強烈暗示 P ≠ NP）

## Cook-Levin 定理

> SAT 是 NP-完備的。

**證明思路**：
1. 任何 NP 問題都有多項式時間的 NDTM（非確定性圖靈機）
2. 將 NDTM 的執行編碼為布林公式
3. 公式可滿足 ⇔ 圖靈機接受輸入
4. 因此所有 NP 問題可歸約到 SAT

## Karp 的 21 個 NP-完備問題

Richard Karp 在 1972 年證明了 21 個組合問題是 NP-完備的，建立了 NP-完備問題之間的聯繫網絡。

| # | 問題 | 領域 |
|---|------|------|
| 1 | SAT | 邏輯 |
| 2 | 3-SAT | 邏輯 |
| 3 | TSP | 圖論/優化 |
| 4 | Knapsack | 組合優化 |
| 5 | Partition | 數論 |
| 6 | Max Cut | 圖論 |
| 7 | Clique | 圖論 |
| 8 | Vertex Cover | 圖論 |
| 9 | Set Cover | 集合論 |
| 10 | Hamiltonian Cycle | 圖論 |
| ... | ... | ... |

## 歸約 (Reduction)

### 定義

A ≤p B（A 多項式時間歸約到 B）表示：
- 存在多項式時間可計算函數 f
- 使得：x ∈ A ⇔ f(x) ∈ B

### 重要性

```
如果 A ≤p B 且 B ∈ P，則 A ∈ P（因為可以用 f 將 A 轉為 B，然後用 B 的多項式演算法）
```

### 歸約鏈

```
3-SAT ≤p Clique ≤p Vertex Cover ≤p Hamiltonian Cycle ≤p TSP
```

如果 TSP ∈ P，則所有上述問題 ∈ P！

## NP-完備性的後果

1. **如果任何 NP-完備問題 ∈ P**：
   → 所有 NP 問題 ∈ P
   → P = NP（百萬美元獎金！）

2. **如果 P ≠ NP（大多數人相信）**：
   → NP-完備問題沒有 P 演算法
   → 需要近似演算法或啟發式

3. **實務影響**：
   - 遇到 NP-完備問題 → 不太可能找到多項式演算法
   - 改用：近似演算法、隨機演算法、參數化演算法
   - 或接受指數時間（對小輸入）

## 參考資料

- Cook, S. A. (1971). [The complexity of theorem proving procedures](https://doi.org/10.1145/800157.805047). *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*, 151-158.
- Karp, R. M. (1972). Reducibility among combinatorial problems. In *Complexity of Computer Computations* (pp. 85-103). Plenum Press.
- Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.
