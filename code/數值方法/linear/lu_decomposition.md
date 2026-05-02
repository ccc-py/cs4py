# LU 分解（LU Decomposition）

## 歷史背景

LU 分解的歷史可追溯到 20 世紀初，由數學家 Alan Turing 和 John von Neumann 等人在發展現代數值線性代數時系統化。其概念本質上與高斯消去法相同，只是將消去過程中的乘數記錄下來，形成下三角矩陣 L。

這個分解在計算機出現後變得極為重要，因為它讓我們可以預先分解矩陣，然後高效地求解多個不同右端項的方程組。在有限元素法（FEM）、電路模擬等領域中，LU 分解是核心運算之一。

## 核心原理

### 分解形式

對於非奇異方陣 $A$，LU 分解將其表示為：

$$
PA = LU
$$

其中：
- $P$ 是置換矩陣（permutation matrix），來自部分選主元
- $L$ 是下三角矩陣，對角線元素為 1
- $U$ 是上三角矩陣

若無需選主元，則 $P = I$（單位矩陣），即 $A = LU$。

### 與高斯消去法的關係

高斯消去法中的消去乘數（elimination multipliers）直接構成了 L 矩陣的非零元素。具體來說，若消去過程中 $a_{ik}$ 被 $a_{kk}$ 除得到 $m_{ik}$，則 $L_{ik} = m_{ik}$。

### 求解多個右端項

有了 LU 分解後，求解 $Ax = b_j$ 對於不同的 $b_j$ 變得非常高效：

1. 先解 $Ly = Pb$（前向代入，$O(n^2)$）
2. 再解 $Ux = y$（回代，$O(n^2)$）

相比於每次重新做高斯消去（$O(n^3)$），這節省了大量運算。

### 計算行列式

$$
\det(A) = \det(P) \cdot \det(L) \cdot \det(U) = (-1)^s \cdot \prod_{i} U_{ii}
$$

其中 $s$ 是置換的次數。

### 計算逆矩陣

通過求解 $AX = I$（每列求解一個單位向量），可以得到逆矩陣。

## 使用範例

```python
from code.數值方法.linear.lu_decomposition import lu_decomposition, solve_with_lu

A = [
    [2.0, 1.0, -1.0],
    [-3.0, -1.0, 2.0],
    [-2.0, 1.0, 2.0]
]

L, U, P = lu_decomposition(A)

# 求解 Ax = b
b = [8.0, -11.0, -3.0]
x = solve_with_lu(L, U, P, b)
print(f"解: {x}")
```

## 優缺點

### 優點
- **高效求解多組 RHS**：分解只需一次 $O(n^3)$，之後每次求解 $O(n^2)$
- **可計算行列式和逆矩陣**：一個分解多用
- **數值穩定**：配合部分選主元可保證穩定性

### 缺點
- **不適合稀疏矩陣**：與高斯消去法一樣存在填滿問題
- **需要存儲 L 和 U**：對大型矩陣記憶體消耗大
- **僅適用方陣**：非方陣需要 QR 等其他分解

## 參考資料

1. [LU Decomposition - Wikipedia](https://en.wikipedia.org/wiki/LU_decomposition)
2. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.
3. Davis, T. A. (2006). *Direct Methods for Sparse Linear Systems*. SIAM.
