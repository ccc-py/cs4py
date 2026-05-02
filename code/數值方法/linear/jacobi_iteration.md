# 雅可比迭代法（Jacobi Iteration Method）

## 歷史背景

雅可比迭代法以德國數學家卡爾·古斯塔夫·雅可比（Carl Gustav Jacob Jacobi）命名。雅可比在 19 世紀對行列式理論和數值分析做出了重要貢獻。雅可比迭代法是第一個被系統研究的迭代法，為後續的高斯-賽德爾法（Gauss-Seidel method）和共軛梯度法（Conjugate Gradient method）奠定了基礎。

在 20 世紀中期，隨著大型稀疏矩陣問題（如電力網絡分析、有限差分法）的出現，迭代法因其記憶體效率高而受到重視。現代科學計算中，對於百萬維以上的線性系統，直接法（如高斯消去法）因記憶體限制而不可行，迭代法成為唯一選擇。

## 核心原理

### 演算法思想

對於線性方程組 $Ax = b$，將 $A$ 拆分為對角部分 $D$ 和非對角部分 $R$：

$$
A = D + R
$$

其中 $D$ 是對角矩陣，$R$ 是非對角部分。雅可比法的迭代公式為：

$$
x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)
$$

等價地，矩陣形式為：

$$
x^{(k+1)} = D^{-1}(b - Rx^{(k)})
$$

### 收斂條件

雅可比法收斂的充分條件是矩陣 $A$ **嚴格對角占優**（strictly diagonally dominant）：

$$
|a_{ii}| > \sum_{j \neq i} |a_{ij}|, \quad \forall i
$$

另一個充分條件是 $A$ 是對稱正定矩陣。

### 收斂速度

收斂速度取決於譜半徑 $\rho(T)$，其中 $T = D^{-1}R$ 是迭代矩陣。收斂速度為線性收斂，誤差約以 $\rho(T)^k$ 的速度衰減。

## 使用範例

```python
from code.數值方法.linear.jacobi_iteration import jacobi_iteration

# 對角占優矩陣
A = [
    [4.0, -1.0, 0.0, -1.0],
    [-1.0, 4.0, -1.0, 0.0],
    [0.0, -1.0, 4.0, -1.0],
    [-1.0, 0.0, -1.0, 4.0]
]
b = [3.0, 2.0, 2.0, 3.0]

x, iters, _ = jacobi_iteration(A, b, tol=1e-10)
print(f"解: {x}, 迭代次數: {iters}")
```

## 優缺點

### 優點
- **記憶體效率高**：只需存儲矩陣的非零元素（稀疏矩陣）
- **實作簡單**：邏輯直觀
- **易於平行化**：每次迭代的更新彼此獨立

### 缺點
- **收斂速度慢**：線性收斂，可能需要很多次迭代
- **需要收斂條件**：矩陣需對角占優或對稱正定
- **不利用最新資訊**：每次迭代只用上一次的完整解，不用當次已更新的分量

## 與直接法比較

| 特性 | 雅可比迭代 | 高斯消去法 |
|------|-----------|-----------|
| 適用問題 | 大型稀疏矩陣 | 中小型稠密矩陣 |
| 記憶體 | $O(\text{nnz})$ | $O(n^2)$ |
| 時間 | 取決於收斂速度 | $O(n^3)$ |
| 精度 | 近似解 | 直接得到精確解 |
| 收斂保證 | 需滿足條件 | 總是可行 |

## 參考資料

1. [Jacobi Method - Wikipedia](https://en.wikipedia.org/wiki/Jacobi_method)
2. Saad, Y. (2003). *Iterative Methods for Sparse Linear Systems* (2nd ed.). SIAM.
3. Varga, R. S. (2000). *Matrix Iterative Analysis* (2nd ed.). Springer.
