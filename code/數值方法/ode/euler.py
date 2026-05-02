"""
尤拉方法（Euler's Method）求解常微分方程

最簡單的數值 ODE 求解器，使用前向差分將微分方程離散化。
雖然精度不高（一階方法），但概念簡單，是理解更複雜方法
（如龍格-庫塔法）的基礎。
"""

from typing import Callable, List, Tuple


def euler(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    h: float,
    steps: int
) -> Tuple[List[float], List[float]]:
    """
    使用前向尤拉法求解一階 ODE：dy/dx = f(x, y)

    參數:
        f: 函數 f(x, y) = dy/dx
        x0: 初始 x
        y0: 初始 y (y(x0) = y0)
        h: 步長
        steps: 迭代步數

    回傳:
        (x_vals, y_vals): x 和 y 的數值解序列
    """
    x_vals = [x0]
    y_vals = [y0]

    x = x0
    y = y0

    for _ in range(steps):
        y_new = y + h * f(x, y)
        x_new = x + h

        x_vals.append(x_new)
        y_vals.append(y_new)

        x = x_new
        y = y_new

    return (x_vals, y_vals)


def euler_adaptive(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    h0: float,
    x_end: float,
    tol: float = 1e-6
) -> Tuple[List[float], List[float]]:
    """
    自適應步長的尤拉法（簡單版本）

    參數:
        f: 函數 f(x, y)
        x0, y0: 初始條件
        h0: 初始步長
        x_end: 終點
        tol: 容差

    回傳:
        (x_vals, y_vals)
    """
    x_vals = [x0]
    y_vals = [y0]

    x = x0
    y = y0
    h = h0

    while x < x_end:
        if x + h > x_end:
            h = x_end - x

        # 兩種步長計算
        y_half = y + h * f(x, y)
        y_double = y_half + h * f(x + h, y_half)

        y_full = y + 2 * h * f(x, y)

        # 誤差估計（簡化）
        error = abs(y_double - y_full) / 3.0

        if error < tol:
            x += h
            y = y_half
            x_vals.append(x)
            y_vals.append(y)

        # 調整步長
        if error > 0:
            h = h * min(2.0, max(0.5, 0.9 * (tol / error) ** 0.5))
        else:
            h = 2.0 * h

    return (x_vals, y_vals)


def demo_exponential_decay() -> None:
    """指數衰減：dy/dx = -ky, 解析解 y = y0 * exp(-kx)"""
    import math

    k = 0.5
    f = lambda x, y: -k * y
    x0, y0 = 0.0, 1.0
    h = 0.1
    steps = 20  # 積分到 x = 2.0

    x_vals, y_vals = euler(f, x0, y0, h, steps)

    print("指數衰減 dy/dx = -0.5y:")
    print(f"  初始條件: y(0) = 1")
    print(f"  步長: h = {h}")
    print(f"\n  {'x':>6} | {'數值解':>12} | {'解析解':>12} | {'誤差':>12}")
    print("  " + "-" * 50)

    for i, (x, y) in enumerate(zip(x_vals, y_vals)):
        y_exact = y0 * math.exp(-k * x)
        error = abs(y - y_exact)
        if i % 5 == 0:  # 每 5 步顯示一次
            print(f"  {x:6.2f} | {y:12.6f} | {y_exact:12.6f} | {error:12.2e}")


def demo_harmonic_oscillator() -> None:
    """簡諧振子：轉化為一二階系統，用尤拉法求解"""
    import math

    # d²x/dt² + ω²x = 0 → 令 v = dx/dt
    # dx/dt = v, dv/dt = -ω²x
    omega = 2.0 * math.pi  # 頻率

    def system(t: float, state: List[float]) -> List[float]:
        x, v = state
        return [v, -(omega**2) * x]

    # 使用簡單的尤拉法求解系統
    t0, t_end = 0.0, 2.0
    h = 0.001
    steps = int((t_end - t0) / h)

    t_vals = [t0]
    x_vals = [1.0]  # x(0) = 1
    v_vals = [0.0]  # v(0) = 0

    t = t0
    x = 1.0
    v = 0.0

    for _ in range(steps):
        derivs = system(t, [x, v])
        dxdt, dvdt = derivs[0], derivs[1]
        x_new = x + h * dxdt
        v_new = v + h * dvdt
        t_new = t + h

        t_vals.append(t_new)
        x_vals.append(x_new)
        v_vals.append(v_new)

        t, x, v = t_new, x_new, v_new

    print("\n\n簡諧振子 (ω = 2π):")
    print(f"  初始條件: x(0)=1, v(0)=0")
    print(f"  步長: h = {h}")
    print(f"\n  在 t = 0, 0.5, 1.0, 1.5, 2.0 處的 x 值:")
    for i, t in enumerate(t_vals):
        if abs(t - round(t, 1)) < h / 2 and t <= 2.0:
            x_exact = math.cos(omega * t)
            print(f"  t={t:.1f}: 數值={x_vals[i]:.6f}, 解析={x_exact:.6f}, 誤差={abs(x_vals[i]-x_exact):.2e}")


if __name__ == "__main__":
    print("=== 尤拉方法求解 ODE ===\n")
    demo_exponential_decay()
    demo_harmonic_oscillator()
