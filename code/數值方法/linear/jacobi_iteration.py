"""
雅可比迭代法（Jacobi Iteration Method）求解線性方程組

雅可比法是求解大型稀疏線性方程組的古典迭代法之一。
要求矩陣對角占優（diagonally dominant）以保證收斂。
每次迭代使用上一次的所有分量來更新當前解。
"""

from typing import List, Tuple, Optional


def jacobi_iteration(
    A: List[List[float]],
    b: List[float],
    x0: Optional[List[float]] = None,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> Tuple[List[float], int, List[List[float]]]:
    """
    使用雅可比迭代法求解 Ax = b

    參數:
        A: n×n 係數矩陣（最好對角占優）
        b: n 維常數向量
        x0: 初始猜測（預設為零向量）
        tol: 容差，當 ||x_new - x_old|| < tol 時停止
        max_iter: 最大迭代次數

    回傳:
        (x, iterations, history)
        x: 解向量
        iterations: 實際迭代次數
        history: 每次迭代的解向量記錄
    """
    n = len(A)

    if x0 is None:
        x0 = [0.0] * n

    x_old = x0[:]
    x_new = [0.0] * n
    history = [x0[:]]

    for iteration in range(max_iter):
        for i in range(n):
            # 計算 sigma = sum(A[i][j] * x_old[j] for j != i)
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x_old[j]
            x_new[i] = (b[i] - sigma) / A[i][i]

        history.append(x_new[:])

        # 檢查收斂
        diff = max(abs(x_new[i] - x_old[i]) for i in range(n))
        if diff < tol:
            return x_new, iteration + 1, history

        # 更新
        x_old, x_new = x_new, x_old
        # 重置 x_new（因為現在 x_old 持有最新值，x_new 要被覆寫）
        x_new = [0.0] * n

    return x_old, max_iter, history


def is_diagonally_dominant(A: List[List[float]]) -> bool:
    """
    檢查矩陣是否對角占優

    參數:
        A: n×n 矩陣

    回傳:
        是否嚴格對角占優
    """
    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= off_diag_sum:
            return False
    return True


def demo_diagonally_dominant() -> None:
    """對角占優矩陣的求解範例"""
    A = [
        [4.0, -1.0, 0.0, -1.0],
        [-1.0, 4.0, -1.0, 0.0],
        [0.0, -1.0, 4.0, -1.0],
        [-1.0, 0.0, -1.0, 4.0]
    ]
    b = [3.0, 2.0, 2.0, 3.0]

    print("矩陣 A:")
    for row in A:
        print("  ", row)
    print("b =", b)
    print("對角占優:", is_diagonally_dominant(A))

    x, iters, _ = jacobi_iteration(A, b, tol=1e-12)
    print(f"\n雅可比法解 (迭代 {iters} 次):")
    print("x =", x)

    # 與直接法比較
    try:
        from linear.gaussian_elimination import gaussian_elimination
        x_direct, _ = gaussian_elimination(A, b)
        print("\n高斯消去法解:")
        print("x =", x_direct)

        # 誤差
        error = max(abs(x[i] - x_direct[i]) for i in range(len(x)))
        print(f"\n兩方法誤差: {error}")
    except ImportError:
        print("  (高斯消去法比較已跳過)")


def demo_spd_matrix() -> None:
    """對稱正定矩陣的求解"""
    A = [
        [4.0, 1.0, 1.0, 0.0],
        [1.0, 3.0, 1.0, 1.0],
        [1.0, 1.0, 5.0, 1.0],
        [0.0, 1.0, 1.0, 4.0]
    ]
    b = [7.0, 6.0, 8.0, 6.0]

    print("\n\n對稱正定矩陣:")
    print("對角占優:", is_diagonally_dominant(A))

    x, iters, _ = jacobi_iteration(A, b, tol=1e-12)
    print(f"解 (迭代 {iters} 次): x = {x}")


if __name__ == "__main__":
    print("=== 雅可比迭代法 ===\n")
    demo_diagonally_dominant()
    demo_spd_matrix()
