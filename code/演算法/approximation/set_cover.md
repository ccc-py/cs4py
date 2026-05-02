# 集合覆蓋近似演算法 (Set Cover Approximation)

## 歷史背景

集合覆蓋是組合優化中的經典 NP-完全問題，在資源選擇和特徵選擇等領域有廣泛應用。

### 發展歷程

- **1972 年**：Karp 將集合覆蓋列為 21 個 NP-完全問題之一
- **1974 年**：Johnson 證明貪婪演算法的 O(log n) 近似比
- **1975 年**：Lovász 獨立證明相同的近似比
- **1990 年代**：證明除非 NP ⊆ DTIME(n^O(log log n))，否則無法改進

## 演算法原理

### 問題定義

```
給定：
- 全域集合 U = {e1, e2, ..., en}
- 一組集合 S = {S1, S2, ..., Sm}，其中 Si ⊆ U

目標：選擇最少的集合，使得它們的聯集 = U

集合覆蓋數記為 OPT。
```

### 貪婪演算法

```
核心思想（每次選覆蓋最多未覆蓋元素的集合）：
1. 初始化 uncovered = U, chosen = []
2. while uncovered 非空：
   a. 找覆蓋最多 uncovered 元素的集合 S
   b. chosen.append(S)
   c. uncovered -= S
3. 返回 chosen

近似比：O(log n)
```

### 加權集合覆蓋

```
每個集合 Si 有權重 w(Si)（成本）。
目標：最小化總權重。

貪婪策略（cost-effectiveness）：
選擇 min(w(S) / |S ∩ uncovered|) 的集合

近似比：O(log n)
```

### 為什麼是 O(log n) 近似？

```
關鍵觀察：
每次選擇至少覆蓋剩餘元素的 1/k（k 為最優解大小）
因此每次至少減少 (1 - 1/k) 的比例
經過 O(k log n) 次選擇後，所有元素被覆蓋

因此近似比 = O(log n) * OPT
```

## 程式碼說明

### 貪婪選擇

```python
while uncovered:
    best_idx = -1
    best_new = 0
    for i in range(len(sets)):
        new_covered = len(sets[i] & uncovered)
        if new_covered > best_new:
            best_new = new_covered
            best_idx = i

    chosen.append(best_idx)
    uncovered -= sets[best_idx]
```

### 加權版本

```python
for i in range(len(sets)):
    new_covered = len(sets[i] & uncovered)
    if new_covered == 0:
        continue
    ratio = weights[i] / new_covered
    if ratio < best_ratio:
        best_ratio = ratio
        best_idx = i
```

## 應用場景

### 1. 設施選址

```
在城市中選擇最少的消防局位置，
使得每個區域都在某個消防局的服務範圍內。
```

### 2. 機器學習特徵選擇

```
從大量特徵中選擇最少子集，
使得保留足夠的資訊（覆蓋所有「概念」）。
```

### 3. 文獻檢索

```
給定一組關鍵詞，選擇最少的文件，
使得所有關鍵詞都出現在選中的文件中。
```

## 圖例

```
示例：
U = {1, 2, 3, 4, 5, 6}

S0 = {1, 2, 3, 4, 5}
S1 = {4, 5, 6}
S2 = {1, 2, 6}

貪婪過程：
1. 選 S0（覆蓋 5 個元素）
   uncovered = {6}
2. 選 S1 或 S2（覆蓋 1 個元素）
   uncovered = {}

結果：{S0, S1}，大小 = 2
```

## 演算法比較

| 演算法 | 近似比 | 時間複雜度 | 說明 |
|--------|--------|-----------|------|
| 貪婪（無權重） | O(log n) | O(U * S) | 標準方法 |
| 加權貪婪 | O(log n) | O(U * S) | 考慮成本 |
| LP 鬆弛取整 | O(log n) | 取決於 LP | 理論最優 |

## 參考資料

- Johnson, D. S. (1974). *Approximation algorithms for combinatorial problems*. Journal of Computer and System Sciences, 9(3), 256-278.
- Lovász, L. (1975). *On the ratio of optimal integral and fractional covers*. Discrete Mathematics, 13(4), 383-390.
- Vazirani, V. V. (2001). *Approximation Algorithms*. Springer.
