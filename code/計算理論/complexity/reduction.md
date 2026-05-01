# 歸約 (Reduction)

## 歷史背景

歸約是計算複雜度理論中最核心的概念之一，用於建立問題之間的難度關係。

### 重要里程碑

- **1971 年**：Stephen Cook 定義多項式時間歸約
- **1972 年**：Richard Karp 使用歸約證明 21 個問題的 NP-Complete 性
- **1974 年**：Levin 的通用搜尋問題理論
- 此後：歸約成為證明問題難度的標準工具

## 核心定義

### 歸約的本質

歸約是將一個問題的實例轉換為另一個問題的實例。

```
如果我們能將問題 A 歸約到問題 B：
- 解決 B → 解決 A
- B 容易 → A 容易
- A 困難 → B 困難
```

### 形式定義

```
語言 L₁ 可歸約到 L₂：存在多項式時間可計算函數 f
使得：x ∈ L₁ ⟺ f(x) ∈ L₂

記作：L₁ ≤ₚ L₂
```

### 多項式時間歸約

歸約轉換必須在多項式時間內完成：
- 轉換代價：O(nᵏ)
- 確保不會因為轉換本身太複雜而隱藏問題難度

## 歸約的類型

### 庫克歸約 (Cook Reduction)

通用型歸約：使用黑盒子求解 L₂ 來求解 L₁

```
L₁ ≤ᴛ L₂：Oracle 機器可以在多項式時間內用 L₂ 作為子程序求解 L₁
```

### 卡普歸約 (Karp Reduction)

多項式時間變換：經典的 mapping reduction

```
L₁ ≤ₚ L₂：存在多項式時間可計算函數 f，x ∈ L₁ ⟺ f(x) ∈ L₂
```

### 對數空間歸約 (Logspace Reduction)

使用對數空間歸約，表達能力更強

```
L₁ ≤ₗ L₂
```

## 經典歸約鏈

### SAT → 3-SAT → CLIQUE

```
SAT (Cook 1971)
    │ 經典填充歸約
    ▼
3-SAT
    │ 建圖歸約
    ▼
CLIQUE ────────────→ VERTEX-COVER
    │                    │
    │ (互補圖)            │ (互補)
    │                    │
    └────────────────────┘
```

### HAM-CYCLE → TSP

```
HAM-CYCLE (哈密爾頓圈)
    │
    │ 加入城市間距離
    │
    ▼
TSP (旅行推銷員)
```

## 實用歸約範例

### SAT → 3-SAT 歸約

**目的**：證明 3-SAT 是 NP-Complete

**方法**：將任意子句轉換為 3-子句

```python
def reduce_sat_to_3sat(clauses):
    result = []
    for clause in clauses:
        if len(clause) <= 3:
            result.append(clause + ['x'] * (3 - len(clause)))
        else:
            # 引入新變數，逐步拆分
            new_vars = []
            while len(clause) > 3:
                y = new_variable()
                result.append([clause[0], clause[1], y])
                clause = clause[2:] + [y]
            result.append(clause)
    return result
```

### 3-SAT → CLIQUE 歸約

**目的**：證明 CLIQUE 是 NP-Complete

**建圖方法**：
1. 每個子句建立一個三頂點的團
2. 不同子句的頂點可連接，除非是正反文字衝突

```python
def reduce_3sat_to_clique(clauses):
    # 建圖
    vertices = []
    for i, clause in enumerate(clauses):
        for j, lit in enumerate(clause):
            vertices.append((i, j, lit))

    # 建邊：同子句全連；不同子句看文字衝突
    edges = []
    for (i, j1, lit1), (k, j2, lit2) in pairs(vertices):
        if i == k:  # 同子句
            edges.append(((i,j1), (i,j2)))
        elif not conflict(lit1, lit2):
            edges.append(((i,j1), (k,j2)))

    # 存在大小 k 的團 ⟺ 3-SAT 可滿足
    return vertices, edges, len(clauses)
```

### CLIQUE → VERTEX-COVER 歸約

**互補關係**：圖 G 的團 = 補圖 Ḡ 的頂點覆蓋

```
C 是 G 的 k-團
⟺ G - C 的每條邊都至少有一個端點在 C 中
⟺ V - C 是 Ḡ 的 k-頂點覆蓋
```

## 歸約的複雜度含義

| 歸約結果 | 含義 |
|---------|------|
| A ≤ₚ B 且 B ∈ P | A ∈ P |
| A ≤ₚ B 且 A ∉ P | B ∉ P |
| A 是 NP-Complete 且 A ≤ₚ B | B 是 NP-Hard |
| A 是 NP-Complete 且 A ≤ₚ B 且 B ∈ NP | B 是 NP-Complete |

## 證明問題是 NP-Complete 的步驟

```
1. 證明 B ∈ NP
   - 給定候選解
   - 多項式時間驗證

2. 證明 B 是 NP-Hard
   - 取已知 NP-Complete 問題 A
   - 建構多項式時間歸約 f：A → B
   - 證明：x ∈ A ⟺ f(x) ∈ B

3. 結論：B 是 NP-Complete
```

## 歸約的實際應用

### 密碼學

- **NP 困難問題**用於建立密碼系統安全性
- 例：背包問題、RSA 問題

### 演算法設計

- **將新問題歸約到已知問題**：使用現有演算法求解
- **將困難問題歸約到更難問題**：證明難度

### 复杂性分類

```
           NP
          ╱  ╲
    P  ╱──────╲  NP-Complete
      ╱        ╲
    ╱            ╲
   ────────────────
     NPC
```

## 各種歸約的包含關係

```
L ≤ₚ L'  ⊆  L ≤ₗ L'  ⊆  L ≤ᴛ L'
 (Karp)      (Logspace)    (Cook)

逆轉不成立：
  L ≤ₚ L' 不意味著 L' ≤ₚ L
```

## 著名的歸約問題

| 歸約 | 意義 |
|------|------|
| SAT → 3-SAT | 3-SAT 的 NP-Complete 性 |
| 3-SAT → CLIQUE | CLIQUE 的 NP-Complete 性 |
| CLIQUE → VERTEX-COVER | VERTEX-COVER 的 NP-Complete 性 |
| VERTEX-COVER → SET-COVER | SET-COVER 的 NP-Complete 性 |
| HAM-CYCLE → TSP | TSP 的 NP-Complete 性 |
| SUBSET-SUM → KNAPSACK | KNAPSACK 的 NP-Complete 性 |

## 參考資料

- Cook, S. A. (1971). [The complexity of theorem proving procedures](https://doi.org/10.1145/800157.805047).
- Karp, R. M. (1972). [Reducibility Among Combinatorial Problems](https://doi.org/10.1007/978-1-4684-2001-2_9).
- Ladner, R. E. (1975). [On the Structure of Polynomial Time Reducibility](https://doi.org/10.1145/321864.321877). *JACM*, 22(1), 155-171.