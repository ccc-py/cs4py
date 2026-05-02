# 頂點覆蓋近似演算法 (Vertex Cover Approximation)

## 歷史背景

頂點覆蓋是圖論中的經典 NP-完全問題，尋找最小的頂點集合來覆蓋所有邊。

### 發展歷程

- **1972 年**：Richard Karp 將頂點覆蓋列為 21 個 NP-完全問題之一
- **1970 年代**：Gavril 和 Yannakakis 提出基於最大匹配的 2-近似演算法
- **1990 年代**：證明除非 P=NP，否則不存在 (2-ε)-近似演算法
- **現代應用**：網路監控、生物資訊、感測器佈局

## 演算法原理

### 問題定義

```
頂點覆蓋（Vertex Cover）：
給定圖 G = (V, E)，找出最小的頂點子集 C ⊆ V，
使得每一條邊 (u,v) ∈ E 至少有一端點在 C 中。

最優解大小記為 OPT。
```

### 2-近似演算法（基於最大匹配）

```
核心思想：
1. 找出圖的一個最大匹配 M
   （匹配：沒有公共端點的邊集合）
2. 將 M 中每條邊的兩個端點都加入覆蓋集

為什麼是 2-近似？
- 設 M 是最大匹配，則 |M| <= OPT（每條匹配的邊需要不同頂點覆蓋）
- 我們的覆蓋集大小 = 2|M| <= 2 * OPT
- 因此近似比為 2

時間複雜度：O(V * E)
```

### 貪婪演算法（無近似保證）

```
貪婪策略：
while 還有未覆蓋的邊：
    選擇度數最大的節點加入覆蓋
    移除所有與該節點相連的邊

注意：此演算法沒有近似比保證，在最壞情況下可能很差。
```

### 線性規劃鬆弛（LP Relaxation）

```
整數規劃形式：
  minimize: Σ x_v (v ∈ V)
  subject to: x_u + x_v >= 1, ∀(u,v) ∈ E
              x_v ∈ {0, 1}

鬆弛為線性規劃（允許 0 <= x_v <= 1）：
  求解 LP 得到分數解
  取整：若 x_v >= 0.5，則將 v 加入覆蓋

這也是一個 2-近似演算法。
```

## 程式碼說明

### 基於匹配的 2-近似

```python
def matching_2approx(self):
    matched = set()
    matching = []

    # 貪婪找匹配
    for u, v in self.edges:
        if u not in matched and v not in matched:
            matched.add(u)
            matched.add(v)
            matching.append((u, v))

    # 將匹配邊的兩端點加入覆蓋
    cover = set()
    for u, v in matching:
        cover.add(u)
        cover.add(v)

    return cover, len(cover)
```

## 應用場景

### 1. 網路安全監控

```
在網路中選擇少量關鍵節點安裝監控設備，
使得所有連線（邊）都被監控到。
```

### 2. 感測器覆蓋

```
在感測器網路中，選擇最少的感測器進行數據收集，
使得所有通訊鏈路都被覆蓋。
```

### 3. 生物資訊

```
蛋白質交互網路中，找出最少的蛋白質來解釋所有觀察到的交互。
```

## 圖例

```
示例：路徑圖 0-1-2-3

  0 --- 1 --- 2 --- 3

最優頂點覆蓋：{1, 2}，大小 = 2

2-近似演算法：
  最大匹配：{(0,1), (2,3)} 或 {(1,2)}
  覆蓋集：{0, 1, 2, 3}（大小 4）或 {1, 2}（大小 2）
```

## 近似比比較

| 演算法 | 近似比 | 時間複雜度 | 說明 |
|--------|--------|-----------|------|
| 貪婪（度數最大） | 無保證 | O(V * E) | 實務可能不錯 |
| 基於匹配 | 2 | O(V * E) | 有保證 |
| LP 鬆弛取整 | 2 | 取決於 LP 求解器 | 理論最優 |

## 參考資料

- Karp, R. M. (1972). *Reducibility among combinatorial problems*. In Complexity of Computer Computations (pp. 85-103).
- Gavril, F. (1974). *Algorithms for minimum coloring, maximum clique, minimum covering by cliques, and maximum independent set of a chordal graph*. Networks, 4(2), 151-162.
- Vazirani, V. V. (2001). *Approximation Algorithms*. Springer.
