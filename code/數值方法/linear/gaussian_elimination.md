# 高斯消去法（Gaussian Elimination）

## 歷史背景

高斯消去法以德國數學家卡爾·弗里德里希·高斯（Carl Friedrich Gauss）命名，但這個方法早在公元前 200 年左右的中國數學著作《九章算術》中就已出現。當時稱為「方程術」，用於求解線性方程組。

高斯在 19 世紀初期將其系統化，並將其應用於天體力學中的軌道計算。現代的高斯消去法加入了部分選主元（partial pivoting）技術，由英國數學家約翰·馮·諾伊曼（John von Neumann）等人在 20 世紀中期完善，以提高數值穩定性。

## 核心原理

### 基本思想

高斯消去法將線性方程組 $Ax = b$ 的增廣矩陣 $[A|b]$ 通過初等行變換化為上三角形式，再通過回代求解。

### 演算法步驟

1. **前向消去**（Forward Elimination）：
   - 對每個列 $k = 0, 1, ..., n-2$：
     - （可選）部分選主元：在第 $k$ 列以下找絕對值最大的元素，交換行
     - 對每行 $i > k$，計算消去因子 $m_{ik} = a_{ik} / a_{kk}$
     - 更新第 $i$ 行：$a_{ij} \leftarrow a_{ij} - m_{ik} \cdot a_{kj}$（對 $j \geq k$）

2. **回代求解**（Back Substitution）：
   - 對 $i = n-1$ 到 $0$：
     $$
     x_i = \frac{b_i - \sum_{j=i+1}^{n-1} a_{ij} x_j}{a_{ii}}
$$

### 部分選主元

部分選主元是為了避免除以接近零的數值，提高數值穩定性。每次消去前，在第 $k$ 列以下選取絕對值最大的元素作為主元（pivot）。

交換行會使行列式符號改變，因此計算行列式時需要追蹤符號變化。

### 時間複雜度

- 前向消去：$O(n^3)$
- 回代：$O(n^2)$
- 總複雜度：$O(n^3)$

## 使用範例

```python
from code.數值方法.linear.gaussian_elimination import gaussian_elimination

# 求解 3×3 方程組
A = [
    [2.0, 1.0, -1.0],
    [-3.0, -1.0, 2.0],
    [-2.0, 1.0, 2.0]
]
b = [8.0, -11.0, -3.0]

x, det = gaussian_elimination(A, b)
print(f"解: {x}")
print(f"行列式: {det}")
```

## 優缺點

### 優點
- **通用性強**：可求解任意大小的線性方程組
- **可計算行列式**：順便得到矩陣行列式
- **直接法**：精確到機器精度（無迭代誤差）

### 缺點
- **不適合大型稀疏矩陣**：$O(n^3)$ 複雜度對大型矩陣太慢
- **數值不穩定**：若無選主元，可能因小主元導致大誤差
- **破壞稀疏性**：填滿（fill-in）問題

## 參考資料

1. [Gaussian Elimination - Wikipedia](https://en.wikipedia.org/wiki/Gaussian_elimination)
2. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.
3. Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM.
