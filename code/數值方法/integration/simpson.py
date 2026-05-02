"""
辛普森法則（Simpson's Rule）數值積分

使用二次多項式（拋物線）來近似每個子區間上的被積函數，
比梯形法則更精確。Simpson 1/3 法則的誤差為 O(h⁴)。
"""

from typing import Callable, Tuple


def simpson(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100
) -> float:
    """
    使用辛普森 1/3 法則計算定積分 ∫_a^b f(x) dx

    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n: 區間分割數（必須為偶數）

    回傳:
        積分近似值
    """
    if n % 2 != 0:
        n += 1  # 確保 n 為偶數

    h = (b - a) / n
    integral = f(a) + f(b)

    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            integral += 2 * f(x)  # 偶數點係數 2
        else:
            integral += 4 * f(x)  # 奇數點係數 4

    integral *= h / 3.0
    return integral


def composite_simpson(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int = 100
) -> Tuple[float, list]:
    """
    複合辛普森法則，記錄收斂過程

    參數:
        f: 被積函數
        a: 積分下限
        b: 積分上限
        n: 初始區間分割數

    回傳:
        (integral, history)
    """
    if n % 2 != 0:
        n += 1

    history = []
    current_n = n
    for _ in range(6):
        integral = simpson(f, a, b, current_n)
        history.append(integral)
        current_n *= 2
    return history[-1], history


def demo_polynomial() -> None:
    """積分多項式（Simpson 對三次以下多項式精確）"""
    # ∫₀¹ x³ dx = 1/4
    f = lambda x: x**3
    result = simpson(f, 0.0, 1.0, n=2)  # 只需 2 個區間就精確！
    exact = 0.25
    print(f"∫₀¹ x³ dx (n=2):")
    print(f"  近似值: {result}")
    print(f"  精確值: {exact}")
    print(f"  誤差: {abs(result - exact)}")


def demo_sine() -> None:
    """積分 sin(x) 從 0 到 π"""
    import math
    f = lambda x: math.sin(x)
    n = 10
    result = simpson(f, 0.0, math.pi, n)
    exact = 2.0
    print(f"\n∫₀^π sin(x) dx (n={n}):")
    print(f"  近似值: {result}")
    print(f"  精確值: {exact}")
    print(f"  誤差: {abs(result - exact)}")


def compare_with_trapezoidal() -> None:
    """比較 Simpson 法則與梯形法則的精度"""
    import math
    f = lambda x: math.exp(x)
    a, b = 0.0, 1.0
    exact = math.exp(1) - 1

    print("\n比較 Simpson 與梯形法則 (∫₀¹ e^x dx):")
    print(f"  精確值: {exact}")
    print("\n  區間數\tSimpson 誤差\t\t梯形法誤差")
    for k in range(1, 7):
        n = 2**k  # Simpson 需要偶數
        if n % 2 != 0:
            n += 1
        s_result = simpson(f, a, b, n)
        t_result = sum(f(a + i * (b - a) / n) * (b - a) / n for i in range(n))  # 簡單梯形
        # 嘗試使用梯形法
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from integration.trapezoidal import trapezoidal
            t_result = trapezoidal(f, a, b, n)
        except ImportError:
            pass  # 使用簡單梯形結果
        s_error = abs(s_result - exact)
        t_error = abs(t_result - exact)
        print(f"  {n}\t\t{s_error:.2e}\t\t{t_error:.2e}")


if __name__ == "__main__":
    print("=== 辛普森法則數值積分 ===\n")
    demo_polynomial()
    demo_sine()
    compare_with_trapezoidal()
