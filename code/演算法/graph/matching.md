# 一般圖匹配 (General Graph Matching - Blossom Algorithm)

## 歷史背景

一般圖的最大匹配問題是圖論中的經典問題。不同於二分圖匹配，一般圖可能包含奇環（odd cycle），使得問題變得更加複雜。

### 發展歷程

- **1957 年**：Claude Berge 提出一般圖匹配的理論基礎
- **1965 年**：Jack Edmonds 提出 Blossom Algorithm，這是一個突破性的成果
- **Edmonds 的貢獻**：證明了此問題可在多項式時間內解決，反駁了當時認為此問題可能是指數時間的猜測
- **後續發展**：Micali-Vazirani (1980) 提出 O(E√V) 的演算法

## 演算法原理

### 匹配（Matching）定義

```
匹配：圖中一組沒有公共端點的邊集合
最大匹配：邊數最多的匹配
完美匹配：所有節點都被匹配的匹配
```

### 為什麼一般圖比二分圖難？

```
二分圖：沒有奇環，可以用簡單的增廣路徑演算法
一般圖：可能存在奇環（如三角形、五邊形）

  1 --- 2
  |     |
  4 --- 3     這是一個 4 環（偶環），好處理

  1 --- 2
  | \   |
  |   \ |
  4 --- 3     這是一個 3 環（奇環/blossom），需要特殊處理
```

### Blossom（花）的概念

```
Blossom 是一個奇環，其中：
- 存在一個基底節點（base）
- 從基底出發，可以找到回到基底的奇數長度路徑

示例：三角形 1-2-3-1
  基底 = 1
  路徑 1-2-3 長度為 2（偶數），但加上 3-1 後形成奇環

Edmonds 的創新：將整個 blossom 收縮為一個「超級節點」，
在收縮後的圖上繼續搜尋，最後再展開。
```

### Edmonds' Blossom Algorithm

```
核心步驟：
1. 初始化匹配為空
2. 對每個未匹配節點 u：
   a. 使用 BFS 尋找交錯路徑（alternating path）
      交錯路徑：匹配邊和非匹配邊交替出現
   b. 遇到 blossom（奇環）時：
      - 將 blossom 收縮為一個節點
      - 繼續在收縮後的圖上搜尋
   c. 找到擴充路徑後，翻轉路徑上的匹配狀態
      （匹配的變成不匹配，不匹配的變成匹配）
3. 返回最大匹配

時間複雜度：O(V^3)
```

## 程式碼說明

### 資料結構

```python
class BlossomMatching:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]  # 鄰接表
        self.match = [-1] * n  # match[u] = v 表示 u 匹配到 v
```

### Blossom 收縮

```python
def _contract_blossom(self, base, parent, v, w, blossom_base):
    # 將發現 blossom 的兩個端點路徑收縮
    for node in [v, w]:
        curr = node
        while base[curr] != blossom_base:
            base[curr] = blossom_base
            curr = parent[curr]
```

### 路徑翻轉

```python
# 找到擴充路徑後，翻轉匹配
for i in range(0, len(path) - 1, 2):
    a, b = path[i], path[i + 1]
    self.match[a] = b
    self.match[b] = a
```

## 應用場景

### 1. 腎臟交換計畫

```
患者（有親友捐贈但血型不合）組成圖：
A 捐給 B，B 捐給 C，C 捐給 A
尋找最大匹配來最大化成功移植數
```

### 2. 學生選校配對

分配學生到學校，考慮雙向偏好，形成一般圖匹配問題。

### 3. 網路設計

在通訊網路中，配對發送端和接收端以最大化連線數。

## 圖例

```
示例：包含 Blossom 的圖

    0
    |
    1
    |
    2 --- 3
    |    /
    |   /
    6 /
    |
    4 --- 5

Blossom：2-3-6-2（三角形，奇環）
最大匹配包含：{(0,1), (2,6), (3,4)} 或其他組合
```

## 演算法比較

| 演算法 | 時間複雜度 | 適用圖形 |
|--------|-----------|---------|
| 匈牙利演算法 | O(V * E) | 僅二分圖 |
| Edmonds' Blossom | O(V^3) | 一般圖 |
| Micali-Vazirani | O(E√V) | 一般圖（最快） |

## 參考資料

- Edmonds, J. (1965). *Paths, trees, and flowers*. Canadian Journal of Mathematics, 17, 449-467.
- Lovász, L., & Plummer, M. D. (1986). *Matching Theory*. North-Holland.
- Schrijver, A. (2003). *Combinatorial Optimization: Polyhedra and Efficiency*. Springer.
