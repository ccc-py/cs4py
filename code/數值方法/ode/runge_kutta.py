"""
龍格-庫塔法（Runge-Kutta Methods）求解常微分方程

RK4（四階龍格-庫塔法）是最廣泛使用的 ODE 求解器之一，
通過四個斜率的加權平均來達到四階精度。
"""

from typing import Callable, List, Tuple


def runge_kutta_4(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    h: float,
    steps: int
) -> Tuple[List[float], List[float]]:
    """
    使用四階龍格-庫塔法（RK4）求解一階 ODE：dy/dx = f(x, y)

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
        k1 = h * f(x, y)
        k2 = h * f(x + h/2.0, y + k1/2.0)
        k3 = h * f(x + h/2.0, y + k2/2.0)
        k4 = h * f(x + h, y + k3)

        y_new = y + (k1 + 2*k2 + 2*k3 + k4) / 6.0
        x_new = x + h

        x_vals.append(x_new)
        y_vals.append(y_new)

        x = x_new
        y = y_new

    return (x_vals, y_vals)


def runge_kutta_system(
    f: Callable[[float, List[float]], List[float]],
    x0: float,
    y0: List[float],
    h: float,
    steps: int
) -> Tuple[List[float], List[List[float]]]:
    """
    使用 RK4 求解一階 ODE 系統

    參數:
        f: 函數 f(x, y) 回傳導數向量
        x0: 初始 x
        y0: 初始 y 向量
        h: 步長
        steps: 迭代步數

    回傳:
        (x_vals, y_vals): x 和 y 向量序列
    """
    n = len(y0)
    x_vals = [x0]
    y_vals = [y0[:]]

    x = x0
    y = y0[:]

    for _ in range(steps):
        k1 = [h * fi for fi in f(x, y)]
        y_temp = [y[i] + k1[i]/2.0 for i in range(n)]
        k2 = [h * fi for fi in f(x + h/2.0, y_temp)]
        y_temp = [y[i] + k2[i]/2.0 for i in range(n)]
        k3 = [h * fi for fi in f(x + h/2.0, y_temp)]
        y_temp = [y[i] + k3[i] for i in range(n)]
        k4 = [h * fi for fi in f(x + h, y_temp)]

        y_new = [y[i] + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6.0 for i in range(n)]
        x_new = x + h

        x_vals.append(x_new)
        y_vals.append(y_new)

        x = x_new
        y = y_new

    return (x_vals, y_vals)


def demo_exponential_decay() -> None:
    """指數衰減：dy/dx = -ky, 解析解 y = y0 * exp(-kx)"""
    import math

    k = 0.5
    f = lambda x, y: -k * y
    x0, y0 = 0.0, 1.0
    h = 0.1
    steps = 20  # 積分到 x = 2.0

    x_vals, y_vals = runge_kutta_4(f, x0, y0, h, steps)

    print("指數衰減 dy/dx = -0.5y (RK4):")
    print(f"  初始條件: y(0) = 1")
    print(f"  步長: h = {h}")
    print(f"\n  {'x':>6} | {'數值解':>12} | {'解析解':>12} | {'誤差':>12}")
    print("  " + "-" * 50)

    for i, (x, y) in enumerate(zip(x_vals, y_vals)):
        y_exact = y0 * math.exp(-k * x)
        error = abs(y - y_exact)
        if i % 5 == 0:
            print(f"  {x:6.2f} | {y:12.6f} | {y_exact:12.6f} | {error:12.2e}")


def demo_logistic_equation() -> None:
    """邏輯方程（Logistic Equation）：dy/dt = ry(1 - y/K)"""
    import math

    r = 1.0  # 增長率
    K = 10.0  # 承載容量

    f = lambda t, y: r * y * (1 - y / K)
    t0, y0 = 0.0, 1.0
    h = 0.1
    steps = 50  # 積分到 t = 5.0

    t_vals, y_vals = runge_kutta_4(f, t0, y0, h, steps)

    print("\n\n邏輯方程 dy/dt = y(1 - y/10) (RK4):")
    print(f"  初始條件: y(0) = 1")
    print(f"  步長: h = {h}")
    print(f"\n  在 t = 0, 1, 2, 3, 4, 5 處的 y 值:")
    for i, (t, y) in enumerate(zip(t_vals, y_vals)):
        if abs(t - round(t)) < h / 2 and t <= 5.0:
            print(f"  t={t:.1f}: y = {y:.6f}")


def demo_harmonic_oscillator() -> None:
    """簡諧振子：d²x/dt² + ω²x = 0"""
    import math

    omega = 2.0 * math.pi

    def system(t: float, state: List[float]) -> List[float]:
        x, v = state
        return [v, -(omega**2) * x]

    t0, t_end = 0.0, 2.0
    h = 0.01
    steps = int((t_end - t0) / h)

    t_vals, state_vals = runge_kutta_system(system, t0, [1.0, 0.0], h, steps)
    x_vals = [s[0] for s in state_vals]

    print("\n\n簡諧振子 (ω = 2π) 使用 RK4:")
    print(f"  初始條件: x(0)=1, v(0)=0")
    print(f"  步長: h = {h}")
    print(f"\n  在 t = 0, 0.5, 1.0, 1.5, 2.0 處的 x 值:")
    for i, t in enumerate(t_vals):
        if abs(t - round(t, 1)) < h / 2 and t <= 2.0:
            x_exact = math.cos(omega * t)
            print(f"  t={t:.1f}: 數值={x_vals[i]:.6f}, 解析={x_exact:.6f}, 誤差={abs(x_vals[i]-x_exact):.2e}")


def compare_with_euler() -> None:
    """比較 RK4 與尤拉法的精度"""
    import math

    f = lambda x, y: -0.5 * y
    x0, y0 = 0.0, 1.0
    x_end = 2.0

    print("\n\n比較 RK4 與尤拉法的精度 (∫₀² e^(-0.5x) dx):")
    print(f"  解析解: y(2) = {math.exp(-1.0):.8f}")
    print()

    for h in [0.1, 0.05, 0.025]:
        steps = int(x_end / h)

        # RK4
        _, y_rk4 = runge_kutta_4(f, x0, y0, h, steps)
        err_rk4 = abs(y_rk4[-1] - math.exp(-1.0))

        # Euler
        from code.數值方法.ode.euler import euler
        _, y_euler = euler(f, x0, y0, h, steps)
        err_euler = abs(y_euler[-1] - math.exp(-1.0))

        print(f"  h={h}: RK4 誤差={err_rk4:.2e}, 尤拉誤差={err_euler:.2e}")


if __name__ == "__main__":
    print("=== 四階龍格-庫塔法 (RK4) ===\n")
    demo_exponential_decay()
    demo_logistic_equation()
    demo_harmonic_oscillator()
    compare_with_euler()
