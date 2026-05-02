"""
梯形法則（Trapezoidal Rule）數值積分

將積分區間分割為多個小區間，在每個小區間上用梯形面積近似積分值。
是複合積分中最基礎的方法，具有線性收斂速度。
"""

from typing import Callable, List, Tuple


def trapezoidal(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100
) -> float:
    """
    使用梯形法則計算定積分 ∫_a^b f(x) dx

    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n: 區間分割數

    回傳:
        積分近似值
    """
    h = (b - a) / n
    x = a
    # 端點貢獻 (f(a) + f(b)) / 2
    integral = 0.5 * (f(a) + f(b))

    # 中間點貢獻
    for i in range(1, n):
        x = a + i * h
        integral += f(x)

    integral *= h
    return integral


def composite_trapezoidal(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100
) -> Tuple[float, List[float]]:
    """
    複合梯形法則，並記錄每次加倍區間的結果（用於 Richardson 外推）

    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n: 初始區間分割數（會逐次加倍）

    回傳:
        (integral, history): 最終積分值與歷史記錄
    """
    history = []
    current_n = n
    for _ in range(6):  # 記錄 6 次（n, 2n, 4n, ...）
        integral = trapezoidal(f, a, b, current_n)
        history.append(integral)
        current_n *= 2
    return history[-1], history


def error_estimate(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100
) -> Tuple[float, float]:
    """
    使用 Richardson 外推估計誤差

    參數:
        f: 被積函數
        a, b: 積分上下限
        n: 區間分割數

    回傳:
        (integral, error_estimate)
    """
    I_n = trapezoidal(f, a, b, n)
    I_2n = trapezoidal(f, a, b, 2 * n)
    # 梯形法則的誤差約為 O(h²)，因此 I_true ≈ (4*I_2n - I_n) / 3
    I_richardson = (4 * I_2n - I_n) / 3
    error = abs(I_2n - I_n) / 3  # Richardson 誤差估計
    return I_richardson, error


def demo_quadratic() -> None:
    """積分 x² 從 0 到 1"""
    f = lambda x: x**2
    n = 10
    result = trapezoidal(f, 0.0, 1.0, n)
    exact = 1.0 / 3.0
    print(f"∫₀¹ x² dx (n={n}):")
    print(f"  近似值: {result}")
    print(f"  精確值: {exact}")
    print(f"  誤差: {abs(result - exact)}")


def demo_sine() -> None:
    """積分 sin(x) 從 0 到 π"""
    import math
    f = lambda x: math.sin(x)
    n = 100
    result = trapezoidal(f, 0.0, math.pi, n)
    exact = 2.0
    print(f"\n∫₀^π sin(x) dx (n={n}):")
    print(f"  近似值: {result}")
    print(f"  精確值: {exact}")
    print(f"  誤差: {abs(result - exact)}")


def demo_error_convergence() -> None:
    """觀察誤差隨 n 增加的收斂情況"""
    import math
    f = lambda x: math.exp(x)
    exact = math.exp(1) - 1  # ∫₀¹ e^x dx

    print("\n誤差收斂觀察 (∫₀¹ e^x dx):")
    print(f"  精確值: {exact}")
    print("\n  n\t近似値\t\t誤差\t\t收斂階")
    prev_error = None
    for k in range(1, 8):
        n = 2**k
        result = trapezoidal(f, 0.0, 1.0, n)
        error = abs(result - exact)
        if prev_error is not None and prev_error > 0:
            order = math.log2(prev_error / error)
        else:
            order = float('nan')
        print(f"  {n}\t{result:.10f}\t{error:.2e}\t{order:.2f}")
        prev_error = error


if __name__ == "__main__":
    print("=== 梯形法則數值積分 ===\n")
    demo_quadratic()
    demo_sine()
    demo_error_convergence()
