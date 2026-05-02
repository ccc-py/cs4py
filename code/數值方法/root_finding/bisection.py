"""
二分法（Bisection Method）求根演算法

對於在區間 [a, b] 上連續的函數 f(x)，若 f(a) 與 f(b) 異號，
則區間內必存在至少一個根。二分法每次將區間對半切，根據中點
函數值的符號決定保留左半或右半區間，直到區間寬度小於容差。
"""

from typing import Callable, Tuple


def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 1000
) -> Tuple[float, int, list]:
    """
    使用二分法尋找函數 f(x) = 0 的根

    參數:
        f: 目標函數，接受 float 回傳 float
        a: 區間左端點
        b: 區間右端點
        tol: 容差，區間寬度小於此值時停止
        max_iter: 最大迭代次數

    回傳:
        (root, iterations, history)
        root: 找到的根
        iterations: 實際迭代次數
        history: 每次迭代的 (a, b, c, f(c)) 記錄
    """
    fa = f(a)
    fb = f(b)

    # 檢查端點是否為根
    if abs(fa) < tol:
        return a, 0, [(a, b, a, fa)]
    if abs(fb) < tol:
        return b, 0, [(a, b, b, fb)]

    # 檢查是否異號
    if fa * fb > 0:
        raise ValueError(f"區間 [{a}, {b}] 兩端點函數值同號，無法保證存在根")

    history = []
    for i in range(max_iter):
        c = (a + b) / 2.0
        fc = f(c)
        history.append((a, b, c, fc))

        if abs(fc) < tol or (b - a) / 2.0 < tol:
            return c, i + 1, history

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return (a + b) / 2.0, max_iter, history


def find_sqrt2() -> None:
    """使用二分法求 sqrt(2)"""
    f = lambda x: x**2 - 2
    root, iters, _ = bisection(f, 1.0, 2.0, tol=1e-12)
    print(f"sqrt(2) ≈ {root}")
    print(f"迭代次數: {iters}")
    print(f"誤差: {abs(root - 2**0.5)}")


def solve_cubic() -> None:
    """求解 x³ - x - 1 = 0"""
    f = lambda x: x**3 - x - 1
    # 觀察: f(1) = -1, f(2) = 5，根在 [1, 2]
    root, iters, _ = bisection(f, 1.0, 2.0, tol=1e-12)
    print(f"x³ - x - 1 = 0 的根 ≈ {root}")
    print(f"迭代次數: {iters}")
    print(f"驗算 f(root) = {f(root)}")


if __name__ == "__main__":
    print("=== 二分法求根 ===\n")

    print("問題 1: 求 sqrt(2)")
    find_sqrt2()

    print("\n問題 2: 求解 x³ - x - 1 = 0")
    solve_cubic()
