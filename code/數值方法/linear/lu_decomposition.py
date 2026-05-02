"""
LU 分解（LU Decomposition）求解線性方程組

將矩陣 A 分解為下三角矩陣 L 和上三角矩陣 U 的乘積（PA = LU），
其中 P 是置換矩陣。LU 分解可高效求解多個右端項的線性方程組，
也可用於計算矩陣的逆和行列式。
"""

from typing import List, Tuple, Optional


def lu_decomposition(
    A: List[List[float]]
) -> Tuple[List[List[float]], List[List[float]], List[int]]:
    """
    對矩陣 A 進行 LU 分解（帶部分選主元）

    參數:
        A: n×n 矩陣

    回傳:
        (L, U, P): L 為下三角，U 為上三角，P 為置換向量
                   P[i] 表示第 i 行來自原矩陣的第 P[i] 行
    """
    n = len(A)
    # 複製 A 以避免修改原矩陣
    U = [row[:] for row in A]
    L = [[0.0] * n for _ in range(n)]
    P = list(range(n))  # 置換向量

    for col in range(n):
        # 部分選主元
        max_row = col
        max_val = abs(U[col][col])
        for row in range(col + 1, n):
            if abs(U[row][col]) > max_val:
                max_val = abs(U[row][col])
                max_row = row

        if max_row != col:
            # 交換 U 的行
            U[col], U[max_row] = U[max_row], U[col]
            # 交換 L 的已計算部分
            for j in range(col):
                L[col][j], L[max_row][j] = L[max_row][j], L[col][j]
            # 更新置換向量
            P[col], P[max_row] = P[max_row], P[col]

        pivot_val = U[col][col]
        if abs(pivot_val) < 1e-15:
            raise ValueError("矩陣奇異或接近奇異")

        # 計算 L 的元素併消去 U 的下三角部分
        for row in range(col + 1, n):
            L[row][col] = U[row][col] / pivot_val
            for j in range(col, n):
                U[row][j] -= L[row][col] * U[col][j]

    # 設置 L 的對角線為 1
    for i in range(n):
        L[i][i] = 1.0

    return L, U, P


def solve_with_lu(
    L: List[List[float]],
    U: List[List[float]],
    P: List[int],
    b: List[float]
) -> List[float]:
    """
    利用 LU 分解求解 Ax = b

    參數:
        L: 下三角矩陣
        U: 上三角矩陣
        P: 置換向量
        b: 右端項

    回傳:
        解向量 x
    """
    n = len(b)
    # 應用置換：Pb
    b_perm = [b[P[i]] for i in range(n)]

    # 前向代入：Ly = Pb
    y = [0.0] * n
    for i in range(n):
        y[i] = b_perm[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]

    # 回代：Ux = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i]
        for j in range(i + 1, n):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]

    return x


def matrix_inverse(
    L: List[List[float]],
    U: List[List[float]],
    P: List[int]
) -> List[List[float]]:
    """
    利用 LU 分解計算矩陣的逆

    參數:
        L, U, P: LU 分解結果

    回傳:
        逆矩陣 A⁻¹
    """
    n = len(L)
    inv = [[0.0] * n for _ in range(n)]

    for j in range(n):
        # 第 j 個單位向量
        e = [0.0] * n
        e[j] = 1.0
        # 求解 A * x = e
        col = solve_with_lu(L, U, P, e)
        for i in range(n):
            inv[i][j] = col[i]

    return inv


def determinant(L: List[List[float]], U: List[List[float]], P: List[int]) -> float:
    """
    計算矩陣行列式

    參數:
        L, U, P: LU 分解結果

    回傳:
        行列式值
    """
    n = len(U)
    det = 1.0
    for i in range(n):
        det *= U[i][i]
    # 置換的次數影響符號
    swaps = sum(1 for i in range(n) if P[i] != i)
    if swaps % 2 == 1:
        det *= -1
    return det


def demo() -> None:
    """展示 LU 分解的應用"""
    A = [
        [2.0, 1.0, -1.0],
        [-3.0, -1.0, 2.0],
        [-2.0, 1.0, 2.0]
    ]

    print("矩陣 A:")
    for row in A:
        print("  ", row)

    L, U, P = lu_decomposition(A)
    print("\nL (下三角):")
    for row in L:
        print("  ", row)
    print("\nU (上三角):")
    for row in U:
        print("  ", row)
    print("\n置換向量 P:", P)

    # 驗算 PA = LU
    print("\n驗算 PA = LU:")
    n = len(A)
    PA = [[A[P[i]][j] for j in range(n)] for i in range(n)]
    LU = [[sum(L[i][k] * U[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    print("PA:")
    for row in PA:
        print("  ", row)
    print("LU:")
    for row in LU:
        print("  ", row)

    # 求解 Ax = b
    b = [8.0, -11.0, -3.0]
    x = solve_with_lu(L, U, P, b)
    print("\n求解 Ax = b, b =", b)
    print("解 x =", x)

    # 計算行列式
    det = determinant(L, U, P)
    print(f"\n行列式 det(A) = {det}")

    # 計算逆矩陣
    inv = matrix_inverse(L, U, P)
    print("\n逆矩陣 A⁻¹:")
    for row in inv:
        print("  ", row)


if __name__ == "__main__":
    print("=== LU 分解 ===\n")
    demo()
