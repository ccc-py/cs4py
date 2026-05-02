# PageRank 演算法

## 歷史背景

PageRank 由 Larry Page 和 Sergey Brin 在 1996 年於史丹佛大學提出，是 Google 搜尋引擎的核心技術之一。該演算法模擬使用者在網頁間隨機遊走的行為，將連結視為投票，透過遞迴方式計算網頁的重要性。

PageRank 的創新在於：
1. 將連結視為權威性投票
2. 來自重要頁面的連結權重更高
3. 使用馬可夫鏈的平穩分佈概念

## 核心原理

### PageRank 公式

```
PR(p) = (1-d)/N + d * Σ PR(q)/out_degree(q)
        q∈in_links(p)
```

其中：
- `PR(p)`：頁面 p 的 PageRank 分數
- `d`：阻尼因子（通常 0.85），表示使用者繼續點擊連結的機率
- `N`：總頁面數
- `in_links(p)`：指向 p 的所有頁面

### 冪迭代法

1. 初始化所有頁面為 1/N
2. 重複更新直到收斂：
   - 每個頁面的新分數 = 隨機跳轉 + 來自入鏈的貢獻
3. 收斂條件：分數變化小於容差

### 懸空節點

沒有出鏈的頁面（dangling nodes）會導致權重流失，需要將其貢獻均勻分配給所有頁面。

## 使用範例

```python
from ranking.pagerank import PageRank

links = [(1, 2), (2, 3), (3, 1)]
pr = PageRank(damping_factor=0.85)
pr.build_from_links(links)
scores = pr.compute()

for node, score in pr.get_ranking():
    print(f"頁面 {node}: {score:.6f}")
```

## 參考資料

- Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). The PageRank citation ranking: Bringing order to the web. *Stanford InfoLab*.
- Langville, A. N., & Meyer, C. D. (2006). *Google's PageRank and Beyond: The Science of Search Engine Rankings*. Princeton University Press.
- Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual web search engine. *Computer Networks*, 30(1-7), 107-117.
