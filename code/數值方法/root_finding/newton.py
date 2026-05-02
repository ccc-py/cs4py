"""
牛頓法（Newton's Method / Newton-Raphson）求根演算法

牛頓法利用函數的導數資訊，從初始猜測值出發，沿切線方向迭代逼近根。
對於充分光滑的函數，在根附近具有二次收斂速度。
"""

from typing import Callable, Tuple, Optional


def derivative(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-9
) -> float:
    """
    數值計算函數在 x 處的導數（中心差分法）

    參數:
        f: 目標函數
        x: 計算點
        h: 微小增量

    回傳:
        導數近似值
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def newton(
    f: Callable[[float], float],
    x0: float,
    f_prime: Optional[Callable[[float], float]] = None,
    tol: float = 1e-12,
    max_iter: int = 100
) -> Tuple[float, int, list]:
    """
    使用牛頓法尋找函數 f(x) = 0 的根

    參數:
        f: 目標函數
        x0: 初始猜測值
        f_prime: 導數函數（若為 None 則使用數值微分）
        tol: 容差，當 |f(x)| < tol 時停止
        max_iter: 最大迭代次數

    回傳:
        (root, iterations, history)
        root: 找到的根
        iterations: 實際迭代次數
        history: 每次迭代的 (x, f(x), f'(x)) 記錄
    """
    if f_prime is None:
        f_prime = lambda x: derivative(f, x)

    x = x0
    history = []

    for i in range(max_iter):
        fx = f(x)
        fpx = f_prime(x)
        history.append((x, fx, fpx))

        if abs(fx) < tol:
            return x, i + 1, history

        if abs(fpx) < 1e-15:
            raise ValueError(f"在 x = {x} 處導數接近零，無法繼續迭代")

        x = x - fx / fpx

    return x, max_iter, history


def find_sqrt2() -> None:
    """使用牛頓法求 sqrt(2)"""
    f = lambda x: x**2 - 2
    f_prime = lambda x: 2 * x
    root, iters, _ = newton(f, 1.5, f_prime, tol=1e-12)
    print(f"sqrt(2) ≈ {root}")
    print(f"迭代次數: {iters}")
    print(f"誤差: {abs(root - 2**0.5)}")


def solve_cubic() -> None:
    """求解 x³ - x - 1 = 0，與二分法比較"""
    f = lambda x: x**3 - x - 1
    f_prime = lambda x: 3 * x**2 - 1
    root, iters, _ = newton(f, 1.5, f_prime, tol=1e-12)
    print(f"x³ - x - 1 = 0 的根 ≈ {root}")
    print(f"迭代次數: {iters}")
    print(f"驗算 f(root) = {f(root)}")


def compare_with_bisection() -> None:
    """比較牛頓法與二分法的收斂速度"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    try:
        from root_finding.bisection import bisection
    except ImportError:
        # Fallback: run as script
        import subprocess
        print("牛頓法:")
        f = lambda x: x**2 - 2
        f_prime = lambda x: 2 * x
        root_n, iters_n, _ = newton(f, 1.5, f_prime, tol=1e-12)
        print(f"  根 ≈ {root_n}, 迭代次數: {iters_n}")
        print("  (二分法比較已跳過，請直接執行 bisection.py 進行比較)")
        return

    f = lambda x: x**2 - 2
    f_prime = lambda x: 2 * x

    print("牛頓法:")
    root_n, iters_n, _ = newton(f, 1.5, f_prime, tol=1e-12)
    print(f"  根 ≈ {root_n}, 迭代次數: {iters_n}")

    print("二分法:")
    root_b, iters_b, _ = bisection(f, 1.0, 2.0, tol=1e-12)
    print(f"  根 ≈ {root_b}, 迭代次數: {iters_b}")


if __name__ == "__main__":
    print("=== 牛頓法求根 ===\n")

    print("問題 1: 求 sqrt(2)")
    find_sqrt2()

    print("\n問題 2: 求解 x³ - x - 1 = 0")
    solve_cubic()

    print("\n比較牛頓法與二分法的收斂速度:")
    compare_with_bisection()
