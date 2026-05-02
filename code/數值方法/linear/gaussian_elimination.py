"""
高斯消去法（Gaussian Elimination）求解線性方程組

通過前向消去將增廣矩陣化為上三角形式，再通過回代求解。
使用部分選主元（partial pivoting）提高數值穩定性。
"""

from typing import List, Tuple, Optional


def gaussian_elimination(
    A: List[List[float]],
    b: List[float],
    pivot: bool = True
) -> Tuple[List[float], float]:
    """
    使用高斯消去法求解 Ax = b

    參數:
        A: n×n 係數矩陣
        b: n 維常數向量
        pivot: 是否使用部分選主元

    回傳:
        (x, det): 解向量 x 和矩陣行列式 det
    """
    n = len(A)
    # 建立增廣矩陣 [A|b]
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    det = 1.0

    # 前向消去
    for col in range(n):
        if pivot:
            # 部分選主元：找第 col 列以下絕對值最大的行
            max_row = col
            max_val = abs(M[col][col])
            for row in range(col + 1, n):
                if abs(M[row][col]) > max_val:
                    max_val = abs(M[row][col])
                    max_row = row
            if max_row != col:
                M[col], M[max_row] = M[max_row], M[col]
                det *= -1  # 交換行改變行列式符號

        pivot_val = M[col][col]
        if abs(pivot_val) < 1e-15:
            raise ValueError("矩陣奇異或接近奇異，無法求解")

        det *= pivot_val

        # 消去第 col 列以下的元素
        for row in range(col + 1, n):
            factor = M[row][col] / pivot_val
            for j in range(col, n + 1):
                M[row][j] -= factor * M[col][j]

    # 回代求解
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n]
        for j in range(i + 1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]

    return x, det


def solve_example1() -> None:
    """求解簡單的 3×3 線性方程組"""
    A = [
        [2.0, 1.0, -1.0],
        [-3.0, -1.0, 2.0],
        [-2.0, 1.0, 2.0]
    ]
    b = [8.0, -11.0, -3.0]

    x, det = gaussian_elimination(A, b)
    print("方程組 Ax = b:")
    print("A =", A)
    print("b =", b)
    print("解 x =", x)
    print("行列式 det(A) =", det)

    # 驗算
    print("\n驗算 Ax:")
    Ax = [sum(A[i][j] * x[j] for j in range(len(A))) for i in range(len(A))]
    print("Ax =", Ax)


def solve_example2() -> None:
    """求解更大的方程組"""
    A = [
        [4.0, -1.0, 0.0, -1.0],
        [-1.0, 4.0, -1.0, 0.0],
        [0.0, -1.0, 4.0, -1.0],
        [-1.0, 0.0, -1.0, 4.0]
    ]
    b = [3.0, 2.0, 2.0, 3.0]

    x, det = gaussian_elimination(A, b)
    print("\n4×4 方程組:")
    print("解 x =", x)
    print("行列式 det(A) =", det)


if __name__ == "__main__":
    print("=== 高斯消去法 ===\n")
    solve_example1()
    solve_example2()
