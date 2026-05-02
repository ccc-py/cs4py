# 最大割近似演算法 (MAX-CUT Approximation)

## 歷史背景

MAX-CUT 是圖論中的經典 NP-完全問題，目標是將圖的節點分成兩組，使得連接兩組的邊數最多。

### 發展歷程

- **1972 年**：Karp 將 MAX-CUT 列為 21 個 NP-完全問題之一
- **1995 年**：Goemans 和 Williamson 提出基於 SDP 的 0.878-近似
- **隨機演算法**：簡單的隨機割可達到 0.5-近似
- **現代應用**：電路設計、社群發現、統計物理

## 演算法原理

### 問題定義

```
給定無向圖 G = (V, E)，每條邊 (u,v) 有權重 w(u,v)。

目標：將 V 分割成兩個不相交的子集 S 和 T = V \ S，
使得跨越 S 和 T 的邊權重和最大。

max Σ w(u,v) for all (u,v) where u in S, v in T
```

### 隨機 0.5-近似

```
核心思想：每個節點獨立地以 1/2 機率分配到 S 或 T。

對於任意邊 (u,v)：
  Pr[此邊是割邊] = Pr[u∈S, v∈T] + Pr[u∈T, v∈S] = 1/4 + 1/4 = 1/2

因此：
  E[割大小] = Σ w(u,v) * 1/2 = (總權重) / 2

因為 OPT <= 總權重，所以 E[割大小] >= OPT / 2
這是一個 0.5-近似演算法。
```

### 貪婪局部搜尋

```
從初始割開始，反覆：
  對每個節點，計算將其移到另一側的增益
  若增益 > 0，則執行移動

這可以改進初始解，但可能陷入局部最優。
```

### Goemans-Williamson (概念)

```
基於半正定規劃（SDP）：
1. 將節點表示為單位球面上的向量
2. 每個邊對應向量內積的損失
3. 求解 SDP 得到向量配置
4. 隨機超平面分割球體得到割

近似比：0.878（最佳的已知多項式時間近似比）
```

## 程式碼說明

### 隨機割

```python
def random_cut(self):
    S = set()
    T = set()
    for v in range(n):
        if random.random() < 0.5:
            S.add(v)
        else:
            T.add(v)
    cut_size = compute_cut_size(S)
    return S, T, cut_size
```

### 計算割大小

```python
def _compute_cut_size(self, S):
    cut = 0.0
    for u in S:
        for v, w in graph[u]:
            if v not in S:  # v 在 T 中
                cut += w
    return cut
```

## 應用場景

### 1. 電路佈局

```
將電路元件分成兩組，最小化連接兩組的線路數。
```

### 2. 社群發現

```
將社交網路分成兩個社群，最大化跨社群的連結（發現對立群體）。
```

### 3. 統計物理

```
Ising 模型中的自旋配置，對應於 MAX-CUT 問題。
```

## 圖例

```
正方形（4 環）：

  0 ---- 1
  |      |
  |      |
  3 ---- 2

最大割：S={0,2}, T={1,3}
割邊：(0,1), (0,3), (1,2), (2,3) = 4 條邊
但 4 環只有 4 條邊，全部都是割邊！
```

## 演算法比較

| 演算法 | 近似比 | 時間複雜度 | 說明 |
|--------|--------|-----------|------|
| 隨機割 | 0.5 | O(E) | 簡單快速 |
| 貪婪局部搜尋 | 無保證 | O(V * E) | 改進隨機解 |
| Goemans-Williamson | 0.878 | O(V^3.5) | SDP 基礎 |
| 最優解 | 1 | O(2^V) | 指數時間 |

## 參考資料

- Karp, R. M. (1972). *Reducibility among combinatorial problems*. In Complexity of Computer Computations (pp. 85-103).
- Goemans, M. X., & Williamson, D. P. (1995). *Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming*. Journal of the ACM, 42(6), 1115-1145.
- Vazirani, V. V. (2001). *Approximation Algorithms*. Springer.
