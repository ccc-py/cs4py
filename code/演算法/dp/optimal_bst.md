# 最優二叉搜尋樹 (Optimal Binary Search Tree)

## 歷史背景

最優二叉搜尋樹問題由 Donald Knuth 在 1971 年深入研究，他證明了對於給定的鍵值和搜尋頻率，存在一個最優的 BST 結構使得期望搜尋成本最小。Knuth 還提出了一個重要的優化性質，將演算法的時間複雜度從 O(n³) 降到了 O(n²)。

這個問題在編譯器設計（符號表組織）和資料庫索引結構中有重要應用。

## 核心原理

### 問題定義

給定 n 個已排序的鍵值 `k1 < k2 < ... < kn` 和它們的搜尋頻率（或機率）`p1, p2, ..., pn`，建構一棵 BST，使得**期望搜尋成本**最小。

**期望搜尋成本** = Σ `pi` × (depth(i) + 1)

其中 depth(i) 是鍵值 ki 在樹中的深度。

### 動態規劃解法

定義 `dp[i][j]` 為鍵值 `i..j` 構成的最優 BST 的最小期望成本。

**狀態轉移方程**：
```
dp[i][j] = min_{k=i..j} (dp[i][k-1] + dp[k+1][j] + sum(pi..pj))
```

其中 k 是根節點的選擇。

**基本情況**：
```
dp[i][i] = pi  （單個節點）
```

### Knuth 優化

Knuth 證明了最優 BST 滿足以下性質：
```
root[i][j-1] ≤ root[i][j] ≤ root[i+1][j]
```

利用這個性質，可以在搜尋根節點時縮小範圍，從而將時間複雜度從 O(n³) 降到 O(n²)。

## 時間與空間複雜度

| 方法 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 普通 DP | O(n³) | O(n²) |
| Knuth 優化 | O(n²) | O(n²) |

## 使用範例

```python
from optimal_bst import optimal_bst_dp, reconstruct_tree

# 鍵值和搜尋頻率
keys = [10, 20, 30, 40, 50]
freq = [4, 2, 6, 3, 1]

# 計算最優 BST
min_cost, root_table = optimal_bst_dp(keys, freq)
print(f"最小期望成本: {min_cost:.2f}")

# 重建樹結構
tree = reconstruct_tree(root_table, keys, 0, len(keys) - 1)
print(f"根節點: {tree['key']}")
```

## 應用場景

- **編譯器符號表**：根據識別字使用頻率組織符號表
- **資料庫索引**：優化查詢效能
- **網路路由表**：根據路由頻率優化路由查找
- ** Huffman 編碼類似**：但維持 BST 的排序性質

## 參考資料

1. [Optimal Binary Search Tree - Wikipedia](https://en.wikipedia.org/wiki/Optimal_binary_search_tree)
2. Knuth, D. E. (1971). "Optimum binary search trees". *Acta Informatica*, 1(1), 14-25.
3. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. pp. 397-404.
4. Yao, A. C. (1980). "On the complexity of maintaining a binary search tree". *Proceedings of the 22nd Annual Symposium on Foundations of Computer Science*.
