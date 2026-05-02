# Hungarian 演算法（Kuhn-Munkres 演算法）

## 歷史背景

指派問題（Assignment Problem）是組合優化中的經典問題：

> 將 n 個任務分配給 n 個工作者，如何使總成本最小？

### 理論基礎

- **Kőnig's Theorem (1916)**：匈牙利數學家 Dénes Kőnig 奠定二分圖匹配理論
- **Egérvár-Hall Theorem**：Jenő Egérvár 進一步發展

### 演算法發展

1. **1955 年**：Harold Kuhn 提出 Hungarian Algorithm
   - 基於 Kőnig 和 Egérvár 的理論
   - 時間複雜度 O(n⁴)，後改進至 O(n³)

2. **1957 年**：James Munkres 推廣至：
   - 非方形矩陣
   - 最大化版本
   - 正式確立為 Kuhn-Munkres 演算法

3. **後續優化**：
   - Edmonds-Karp 類似的實現技巧
   - O(n³) 已是最優複雜度

## 核心原理

### 對偶變數

匈牙利演算法維護兩組對偶變數（潛在函數）：
- **u[i]**：行（工作者）的潛在值
- **v[j]**：列（任務）的潛在值

滿足對偶約束：
```
u[i] + v[j] ≤ cost[i][j]  對於所有 i, j
```

### 覆蓋線

演算法使用最少的水平或垂直線覆蓋成本矩陣中的所有零：
- 如果覆蓋線數量等於 n，則找到最優解
- 否則，繼續調整潛在值

### 標記法（Labeling）

當前未被完全分配的列會被標記，
用於尋找增廣路徑以增加匹配數量。

## 演算法步驟

```
Hungarian(cost_matrix):
  1. 初始化對偶變數為 0

  2. 對每一行，減去該行最小值
     對每一列，減去該列最小值

  3. 嘗試用最少線覆蓋所有 0
     如果需要 n 條線，則找到最優解
     否則，進行步驟 4

  4. 調整：
     - 找到未被覆蓋的最小元素 a
     - 所有未被覆蓋的行減去 a
     - 所有被覆蓋的列加上 a
     - 回到步驟 3

  5. 恢復原始成本，輸出指派
```

## 複雜度分析

| 步驟 | 時間複雜度 |
|------|----------|
| 初始化減法 | O(n²) |
| 主迴圈（n 次迭代）| O(n³) |
| **總時間** | **O(n³)** |

## 使用範例

### 最小化成本

```python
from hungarian import hungarian

cost_matrix = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
]

min_cost, assignment = hungarian(cost_matrix)
print(f"最小成本: {min_cost}")
print(f"指派: {assignment}")
# 輸出：最小成本: 11
# 指派：[1, 2, 0, 3]
```

### 最大化收益

```python
from hungarian import hungarian_maximize

profit_matrix = [
    [3, 8, 2, 9],
    [7, 2, 5, 1],
    [8, 4, 6, 3],
    [5, 7, 3, 6]
]

max_profit, assignment = hungarian_maximize(profit_matrix)
print(f"最大收益: {max_profit}")
```

## 應用場景

1. **人力資源調度**：最優員工-任務分配
2. **路徑規劃**：旅行商問題的鬆弛
3. **電腦視覺**：特徵匹配
4. **物流優化**：車輛-訂單分配
5. **航空調度**：機組人員排班

## 變體

### 非方形矩陣

當 m ≠ n 時，添加虛擬行或列使矩陣變為方形。

### 帶約束的指派

- 每個工作者多個任務
- 任務需要多個工作者
- 成本為無窮大表示不可行分配

## 參考資料

1. Kuhn, H.W. (1955). The Hungarian method for the assignment problem. Naval Research Logistics Quarterly.
2. Munkres, J. (1957). Algorithms for the Assignment and Transportation Problems. SIAM Journal on Applied Mathematics.
3. Burkard, R., & Cela, E. (1999). Linear Assignment and Scheduling Problems. Handbooks in Operations Research.
4. Papadimitriou, C.H., & Steiglitz, K. (1982). Combinatorial Optimization: Algorithms and Complexity. Prentice Hall.