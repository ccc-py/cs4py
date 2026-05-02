"""
割線法（Secant Method）求根演算法

割線法是牛頓法的一種變體，利用兩個前一時刻的點來近似導數，
避免了需要計算或提供導數函數的需求。收斂速度為超線性收斂
（收斂階約為 1.618，即黃金比例）。
"""

from typing import Callable, Tuple


def secant(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-12,
    max_iter: int = 100
) -> Tuple[float, int, list]:
    """
    使用割線法尋找函數 f(x) = 0 的根

    參數:
        f: 目標函數
        x0: 第一個初始點
        x1: 第二個初始點（通常取 x0 附近的點）
        tol: 容差，當 |f(x)| < tol 時停止
        max_iter: 最大迭代次數

    回傳:
        (root, iterations, history)
        root: 找到的根
        iterations: 實際迭代次數
        history: 每次迭代的 (x, f(x)) 記錄
    """
    fx0 = f(x0)
    fx1 = f(x1)
    history = [(x0, fx0), (x1, fx1)]

    for i in range(max_iter):
        if abs(fx1) < tol:
            return x1, i + 1, history

        # 避免除以零（兩點過於接近）
        if abs(fx1 - fx0) < 1e-15:
            raise ValueError("f(x1) - f(x0) 過小，無法構造割線")

        # 割線法迭代公式
        x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

        fx_new = f(x_new)
        history.append((x_new, fx_new))

        x0, fx0 = x1, fx1
        x1, fx1 = x_new, fx_new

    return x1, max_iter, history


def find_sqrt2() -> None:
    """使用割線法求 sqrt(2)"""
    f = lambda x: x**2 - 2
    root, iters, _ = secant(f, 1.0, 2.0, tol=1e-12)
    print(f"sqrt(2) ≈ {root}")
    print(f"迭代次數: {iters}")
    print(f"誤差: {abs(root - 2**0.5)}")


def solve_cubic() -> None:
    """求解 x³ - x - 1 = 0"""
    f = lambda x: x**3 - x - 1
    root, iters, _ = secant(f, 1.0, 2.0, tol=1e-12)
    print(f"x³ - x - 1 = 0 的根 ≈ {root}")
    print(f"迭代次數: {iters}")
    print(f"驗算 f(root) = {f(root)}")


def compare_methods() -> None:
    """比較割線法、牛頓法、二分法的收斂速度"""
    f = lambda x: x**2 - 2
    f_prime = lambda x: 2 * x

    print("割線法 (x0=1.0, x1=2.0):")
    root_s, iters_s, _ = secant(f, 1.0, 2.0, tol=1e-12)
    print(f"  根 ≈ {root_s}, 迭代次數: {iters_s}")

    # 嘗試導入牛頓法
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from root_finding.newton import newton
        print("牛頓法 (x0=1.5):")
        root_n, iters_n, _ = newton(f, 1.5, f_prime, tol=1e-12)
        print(f"  根 ≈ {root_n}, 迭代次數: {iters_n}")
    except (ImportError, NameError):
        print("  (牛頓法比較已跳過)")

    # 嘗試導入二分法
    try:
        from root_finding.bisection import bisection
        print("二分法 ([1.0, 2.0]):")
        root_b, iters_b, _ = bisection(f, 1.0, 2.0, tol=1e-12)
        print(f"  根 ≈ {root_b}, 迭代次數: {iters_b}")
    except (ImportError, NameError):
        print("  (二分法比較已跳過)")


if __name__ == "__main__":
    print("=== 割線法求根 ===\n")

    print("問題 1: 求 sqrt(2)")
    find_sqrt2()

    print("\n問題 2: 求解 x³ - x - 1 = 0")
    solve_cubic()

    print("\n比較三種求根方法的收斂速度:")
    compare_methods()
