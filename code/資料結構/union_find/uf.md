# 並查集（Union-Find / Disjoint Set）

## 歷史背景
並查集由Bernard A. Galler和Michael J. Fischer在1964年的論文中提出，是一種維護不相交集合的資料結構。它最重要的應用是在Kruskal最小生成樹演算法中檢測環，也可用於動態連通性問題、圖的連通分量計算等場景。

## 核心概念與原理
### 基本操作
1. **Find（查找）**：查找元素所在集合的根節點
2. **Union（合併）**：將兩個集合合併為一個集合

### 優化技術
1. **路徑壓縮（Path Compression）**：在find操作中，將查找路徑上的所有節點直接掛到根節點下，將樹壓平，使後續查找接近O(1)
2. **按秩合併（Union by Rank）**：合併時將高度較小的樹掛到高度較大的樹下，避免樹過深
3. **按大小合併（Union by Size）**：類似按秩合併，但比較集合大小而非高度

### 時間複雜度
使用路徑壓縮和按秩合併時，每個操作的平攤時間複雜度接近O(α(n))，其中α是反阿克曼函數，增長極慢，可視為常數。

## 使用範例
```python
from uf import UnionFind

uf = UnionFind([1,2,3,4])
uf.union(1,2)
print(uf.connected(1,2))
```

## 參考資料
- [Wikipedia: Disjoint Set](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)
- [GeeksforGeeks: Union-Find](https://www.geeksforgeeks.org/union-find/)
