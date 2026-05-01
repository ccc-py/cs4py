# P vs NP 問題

## 歷史背景

P vs NP 是理論計算機科學中最重要的未解問題之一。

### 重要里程碑

- **1971 年**：Stephen Cook 在 "The Complexity of Theorem Proving Procedures" 論文中正式提出 P vs NP 問題
- **1972 年**：Richard Karp 發表 "Reducibility Among Combinatorial Problems"，證明 21 個經典問題是 NP-Complete
- **1974 年**：Levin's 獨立工作
- **2000 年**：Clay 數學研究所將 P vs NP 列為千禧年七大難題之一，獎金 100 萬美元
- **至今未解**

## 核心定義

### P 類（多項式時間可求解）

```
P = { L | L 可在多項式時間內由確定性圖靈機決定 }
```

**特點**：
- 可以在「合理時間」內解決
- 時間複雜度：O(n^k)，其中 k 是常數
- 例子：排序、圖遍歷、線性規劃、矩陣乘法

### NP 類（多項式時間可驗證）

```
NP = { L | L 可在多項式時間內由非確定性圖靈機決定 }
```

**等價定義**：
```
NP = { L | 存在多項式時間驗證器 V }
```

**特點**：
- 如果給定候選解，可以在多項式時間驗證
- 時間複雜度：O(n^k) 驗證
- 例子：子集合問題（Subset Sum）、哈密頓圈、TSP 近似驗證

## 核心問題

```
         P ⊆ NP
    問題：P = NP 還是 P ≠ NP？
```

### 為什麼重要？

| 如果 P = NP | 如果 P ≠ NP |
|-------------|-------------|
| 所有 NP 問題都易解 | 有些問題本質上困難 |
| 密碼學崩潰 | 公開金鑰密碼學安全 |
| 優化問題易解 | 需要近似演算法 |
| AI 飛躍發展 | 密碼學實用 |

## 類比理解

```
【P 問題】
你：老師，我找到了演算法！
老師：多快？
你：O(n²)，很快！

【NP 問題】
你：老師，我找到答案了！
老師：給我看看。
你：（給出解答）
老師：（快速檢查）對的，很好！
```

## 複雜度類別階層

```
L ⊆ NL ⊆ P ⊆ NP ⊆ PSPACE ⊆ EXPTIME ⊆ NEXPTIME ⊆ ...
```

**已知包含關係**：
- L ⊊ NL（空間階層定理）
- NL ⊊ PSPACE（空間階層定理）
- PSPACE ⊊ EXPTIME（時間階層定理）

**未解問題**：
- P vs NP
- NP vs PSPACE
- P vs PSPACE

## NP-Complete 問題

### 第一個 NP-Complete 問題

**Cook-Levin 定理 (1971)**：
> SAT（布林可滿足性問題）是 NP-Complete 的

證明思路：
1. 任何 NP 問題都可以被非確定性圖靈機在多項式時間內計算
2. 圖靈機可以轉換為布林公式
3. 求解 SAT 就等於求解原問題

### Karp 的 21 個 NP-Complete 問題 (1972)

| 問題 | 描述 |
|------|------|
| SAT | 布林公式可滿足性 |
| 3-SAT | 3-CNF 可滿足性 |
| CLIQUE | 最大團問題 |
| VERTEX COVER | 最小頂點覆蓋 |
| HAM-CYCLE | 哈密頓圈 |
| TSP | 旅行推銷員問題 |
| SUBSET-SUM | 子集合問題 |
| KNAPSACK | 背包問題 |

### 意義

如果任何一個 NP-Complete 問題在 P 中，則 P = NP。

## 為什麼相信 P ≠ NP？

1. **直覺**：驗證答案比找到答案容易
2. **歷史**：數十年研究未能找到多項式時間演算法
3. **密碼學**：基於困難假設的密碼系統廣泛使用
4. **數學**：很多證明依賴於某些問題的困難性

## 參考資料

- Cook, S. A. (1971). [The complexity of theorem proving procedures](https://doi.org/10.1145/800157.805047). *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*, 151-158.
- Karp, R. M. (1972). [Reducibility Among Combinatorial Problems](https://doi.org/10.1007/978-1-4684-2001-2_9). *Complexity of Computer Computations*, 85-103.
- Fortnow, L. J. (2013). *The Golden Ticket: P, NP, and the Search for the Impossible*. Princeton University Press.
- Aaronson, S. (2017). P ?= NP. *Communications of the ACM*, 60(2), 50-59.
- Clay Mathematics Institute. [P vs NP](https://www.claymath.org/millennium-problems/p-vs-np)