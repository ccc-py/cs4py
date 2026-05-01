# NP-Complete 問題

## 歷史背景

NP-Complete 問題是計算複雜度理論中最重要的概念之一。

### 重要里程碑

- **1971 年**：Stephen Cook 證明 SAT 是第一個 NP-Complete 問題
- **1972 年**：Richard Karp 發表經典論文，證明 21 個組合問題是 NP-Complete
- **1974 年**：Leonid Levin 獨立提出類似概念
- 此後：數千個問題被證明是 NP-Complete

## 核心定義

### NP-Complete 的定義

```
NP-Complete = { L ∈ NP | 所有 NP 問題都可以多項式時間歸約到 L }
```

### 等價定義

一個問題 L 是 NP-Complete 當且僅當：
1. L ∈ NP（可以在多項式時間驗證）
2. 任何 NP 問題都可以歸約到 L

### 重要性質

```
如果任何一個 NP-Complete 問題在 P 中
⟺ P = NP
⟺ 所有 NP 問題都在 P 中
```

## NP-Complete 問題列表

### Cook-Levin 定理 (1971)

| 問題 | 全名 | 證明 |
|------|------|------|
| **SAT** | Boolean Satisfiability | 第一個 NP-Complete 問題 |

### Karp 的 21 個問題 (1972)

| 問題 | 輸入 | 問題描述 |
|------|------|----------|
| **3-SAT** | 3-CNF 公式 | 是否可滿足？ |
| **CLIQUE** | 圖 G, 整數 k | 是否存在大小 ≥k 的團？ |
| **VERTEX-COVER** | 圖 G, 整數 k | 是否存在大小 ≤k 的頂點覆蓋？ |
| **HAM-CYCLE** | 圖 G | 是否存在哈密爾頓圈？ |
| **TSP** | 完全圖 G, 預算 B | 是否存在長度 ≤B 的哈密爾頓圈？ |
| **SUBSET-SUM** | 集合 S, 目標 t | 是否存在和為 t 的子集合？ |
| **KNAPSACK** | 物品, 容量, 價值 | 是否能填滿背包？ |
| **GRAPH-PARTITION** | 圖 | 能否將頂點分成相等權重的集合？ |

## 問題間的歸約關係

```
                    SAT (Cook 1971)
                        │
                        ▼
    ┌──────────┬────────┼────────┬──────────┐
    │          │        │        │          │
    ▼          ▼        ▼        ▼          ▼
3-SAT      CLIQUE    HAM     SUBSET    GRAPH
              │      -CYCLE    -SUM     -COLORING
              │        │        │          │
              ▼        ▼        ▼          ▼
      VERTEX-COVER   TSP    KNAPSACK       ...
```

## 驗證器模式

NP-Complete 問題的關鍵特點：**容易驗證，不容易求解**

```python
def verify_clique(graph, vertices, k):
    """驗證是否為大小 k 的團 - O(k²)"""
    if len(vertices) < k:
        return False
    for each pair (u, v) in vertices:
        if (u, v) not in edges:
            return False
    return True

def find_clique(graph, k):
    """找大小 k 的團 - NP-Hard"""
    # 需要枚舉所有可能的組合
    for each subset of k vertices:
        if verify_clique(...):
            return True
    return False
```

## 實際影響

### 為什麼 NP-Complete 問題重要？

1. **密碼學**：許多加密系統基於某些問題的困難性
2. **排程**：工作分配、航線規劃
3. **晶片設計**：電路布局、測試向量生成
4. **網路**：路由、流量優化

### 面對 NP-Complete 問題的策略

| 策略 | 說明 |
|------|------|
| **精確演算法** | 指數時間，如回溯、分支限界 |
| **近似演算法** | 保證接近最優解 |
| **啟發式演算法** | 可能找到好解但不保證 |
| **參數化演算法** | 按某個參數 k 設計演算法 |
| **隨機演算法** | 機率上表現良好 |

## 經典問題：旅行推銷員問題 (TSP)

### 問題定義

```
輸入：n 個城市之間的距離矩陣 d[i][j]，預算 B
問題：是否存在長度 ≤ B 的哈密爾頓圈？
```

### 複雜度

- 暴力枚舉：O(n!)
- 動態規劃：O(n² · 2ⁿ)
- 近似演算法（度量 TSP）：O(n log n) 但解可能偏離 50%

### 應用

- 電路板鑽孔
- 物流配送
- 蛋白質結構預測

## 證明一個問題是 NP-Complete

步驟：
1. 證明問題在 NP 中（有快速驗證器）
2. 從已知 NP-Complete 問題歸約到該問題

```
證明 L 是 NP-Complete：

1. L ∈ NP：
   - 給定候選解
   - 在多項式時間內驗證
   - 返回正確/錯誤

2. L 是 NP-Hard：
   - 取已知 NP-Complete 問題 L'
   - 建構多項式時間變換 f
   - x ∈ L' ⟺ f(x) ∈ L
   - 由於 L' 可歸約到 L，且 L' 是 NP-Complete
   - 所以所有 NP 問題都可歸約到 L
```

## 著名的 NP-Complete 問題愛好者

> "如果有人宣稱他們設計的多項式時間演算法解決了 TSP，99% 的情況下他們是錯的。" — 匿名

> "NP-Complete 問題是資訊科學中最有趣的智慧挑戰之一。" — 所有研究人員

## 參考資料

- Cook, S. A. (1971). [The complexity of theorem proving procedures](https://doi.org/10.1145/800157.805047). *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*.
- Karp, R. M. (1972). [Reducibility Among Combinatorial Problems](https://doi.org/10.1007/978-1-4684-2001-2_9). *Complexity of Computer Computations*, 85-103.
- Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W.H. Freeman.