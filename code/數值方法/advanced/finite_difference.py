"""
有限差分法 (Finite Difference Method)

使用有限差分近似偏導數，將偏微分方程離散化為代數方程組求解。
支援前向差分、後向差分和中央差分，並示範熱傳導方程的數值解。

歷史背景：
有限差分法的概念可追溯至牛頓和萊布尼茲時期，但作為偏微分方程的系統性
數值方法，在 20 世紀隨著電腦發展而成熟。各種差分格式（顯式、隱式、
Crank-Nicolson 等）陸續被提出，廣泛應用於流體力學、熱傳導、金融模型等領域。

核心原理：
1. 將連續 domain 離散化為有限個格點
2. 用差商近似導數：f'(x) ≈ (f(x+h) - f(x))/h
3. 將偏微分方程轉換為每個格點上的代數關係
4. 求解得到的線性或非線性方程組

author: cs4py
"""


def forward_difference(f, x: float, h: float = 1e-5) -> float:
    """
    前向差分：f'(x) ≈ (f(x+h) - f(x)) / h

    Args:
        f: 單變數函數
        x: 求導點
        h: 步長

    Returns:
        近似導數值
    """
    return (f(x + h) - f(x)) / h


def backward_difference(f, x: float, h: float = 1e-5) -> float:
    """
    後向差分：f'(x) ≈ (f(x) - f(x-h)) / h

    Args:
        f: 單變數函數
        x: 求導點
        h: 步長

    Returns:
        近似導數值
    """
    return (f(x) - f(x - h)) / h


def central_difference(f, x: float, h: float = 1e-5) -> float:
    """
    中央差分：f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
    精度較前向/後向差分更高，為二階精度

    Args:
        f: 單變數函數
        x: 求導點
        h: 步長

    Returns:
        近似導數值
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def second_central_difference(f, x: float, h: float = 1e-5) -> float:
    """
    二階中央差分：f''(x) ≈ (f(x+h) - 2f(x) + f(x-h)) / h^2

    Args:
        f: 單變數函數
        x: 求導點
        h: 步長

    Returns:
        近似二階導數值
    """
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


def solve_heat_equation(
    u0: list[float],
    alpha: float,
    dx: float,
    dt: float,
    nt: int
) -> list[list[float]]:
    """
    求解一維熱傳導方程：∂u/∂t = α ∂²u/∂x²

    使用顯式有限差分格式（穩定性條件：α*dt/dx² ≤ 0.5）

    Args:
        u0: 初始溫度分佈（陣列）
        alpha: 熱擴散係數
        dx: 空間步長
        dt: 時間步長
        nt: 時間步數

    Returns:
        每個時間步的溫度分佈（nt+1 個陣列）
    """
    nx = len(u0)
    u = [u0.copy()]
    current = u0.copy()

    r = alpha * dt / (dx ** 2)

    for _ in range(nt):
        next_u = current.copy()
        for i in range(1, nx - 1):
            next_u[i] = current[i] + r * (current[i+1] - 2*current[i] + current[i-1])
        current = next_u
        u.append(current.copy())

    return u


def solve_heat_implicit(
    u0: list[float],
    alpha: float,
    dx: float,
    dt: float,
    nt: int
) -> list[list[float]]:
    """
    求解一維熱傳導方程（隱式格式）

    使用隱式有限差分格式，穩定但需要求解三對角線性系統
    ∂u/∂t = α ∂²u/∂x² → (I - r*L)u^{n+1} = u^n

    Args:
        u0: 初始溫度分佈
        alpha: 熱擴散係數
        dx: 空間步長
        dt: 時間步長
        nt: 時間步數

    Returns:
        每個時間步的溫度分佈
    """
    from math import sqrt

    nx = len(u0)
    u = [u0.copy()]
    current = u0.copy()

    r = alpha * dt / (dx ** 2)

    def solve_tridiag(a, b, c, d):
        n = len(d)
        cp = [0.0] * n
        dp = [0.0] * n
        x = [0.0] * n

        cp[0] = c[0] / b[0]
        dp[0] = d[0] / b[0]

        for i in range(1, n):
            denom = b[i] - a[i] * cp[i-1]
            cp[i] = c[i] / denom if i < n-1 else 0
            dp[i] = (d[i] - a[i] * dp[i-1]) / denom

        x[n-1] = dp[n-1]
        for i in range(n-2, -1, -1):
            x[i] = dp[i] - cp[i] * x[i+1]

        return x

    for _ in range(nt):
        a = [-r] * nx
        b = [1 + 2*r] * nx
        c = [-r] * nx
        a[0] = 0
        c[-1] = 0
        current = solve_tridiag(a, b, c, current)
        u.append(current.copy())

    return u


if __name__ == "__main__":
    import math

    print("=" * 50)
    print("有限差分法示範")
    print("=" * 50)

    print("\n--- 導數近似比較 ---")
    f = math.sin
    x = 1.0
    h = 0.001

    exact = math.cos(x)
    fd = forward_difference(f, x, h)
    bd = backward_difference(f, x, h)
    cd = central_difference(f, x, h)

    print(f"f(x) = sin(x), x = {x}")
    print(f"準確值 f'(x) = cos({x}) = {exact:.10f}")
    print(f"前向差分: {fd:.10f}, 誤差 = {abs(fd - exact):.2e}")
    print(f"後向差分: {bd:.10f}, 誤差 = {abs(bd - exact):.2e}")
    print(f"中央差分: {cd:.10f}, 誤差 = {abs(cd - exact):.2e}")

    print("\n--- 二階導數近似 ---")
    f2 = lambda x: x ** 3
    x2 = 2.0
    exact2 = 6 * x2
    cd2 = second_central_difference(f2, x2, h)
    print(f"f(x) = x^3, x = {x2}")
    print(f"準確值 f''(x) = 6x = {exact2:.10f}")
    print(f"二階中央差分: {cd2:.10f}, 誤差 = {abs(cd2 - exact2):.2e}")

    print("\n--- 熱傳導方程求解（顯式格式）---")
    nx = 50
    u0 = [0.0] * nx
    for i in range(nx):
        if 20 <= i <= 30:
            u0[i] = 100.0
        else:
            u0[i] = 0.0

    alpha = 0.01
    dx = 0.1
    dt = 0.001
    r = alpha * dt / (dx ** 2)
    print(f"穩定性參數 r = α*dt/dx² = {r:.4f} (需 < 0.5)")

    nt = 100
    u_result = solve_heat_equation(u0, alpha, dx, dt, nt)

    print(f"初始條件：中央區段 100°C，其餘 0°C")
    print(f"模擬 {nt} 步後，溫度分佈（前10個格點）:")
    for i in range(10):
        print(f"  x = {i*dx:.1f}: u = {u_result[-1][i]:.2f}°C")

    print("\n--- 熱傳導方程求解（隱式格式）---")
    u0_implicit = [0.0] * nx
    for i in range(nx):
        if 20 <= i <= 30:
            u0_implicit[i] = 100.0

    dt_implicit = 0.01
    u_result_implicit = solve_heat_implicit(u0_implicit, alpha, dx, dt_implicit, 50)

    print(f"隱式格式（可使用更大的時間步長）")
    print(f"模擬 50 步後，溫度分佈（前10個格點）:")
    for i in range(10):
        print(f"  x = {i*dx:.1f}: u = {u_result_implicit[-1][i]:.2f}°C")

    print("\n" + "=" * 50)
    print("熱傳導模擬完成")
    print("=" * 50)