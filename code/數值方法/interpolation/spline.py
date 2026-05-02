"""
三次樣條插值（Cubic Spline Interpolation）

將每個子區間用三次多項式插值，並要求函數值、一階導數、二階導數
在內部節點連續（C² 連續）。自然樣條在端點處二階導數為零。
"""

from typing import List, Tuple, Callable


def cubic_spline(
    points: List[Tuple[float, float]],
    boundary: str = "natural"
) -> Callable[[float], float]:
    """
    構造三次樣條插值

    參數:
        points: 插值點列表，按 x 升序排列 [(x0, y0), (x1, y1), ...]
        boundary: 邊界條件，"natural"（自然樣條，二階導數為零）

    回傳:
        樣條函數 s(x)
    """
    n = len(points) - 1  # 區間數
    if n < 1:
        raise ValueError("至少需要兩個點")

    # 排序點（以防未排序）
    points = sorted(points, key=lambda p: p[0])

    # 提取 x 和 y
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    # 計算區間長度 h
    h = [x[i+1] - x[i] for i in range(n)]

    # 構造三對角方程組求二階導數 M
    # 對於自然樣條：M[0] = M[n] = 0
    # 對於內部點 i=1..n-1:
    #   h[i-1]*M[i-1] + 2*(h[i-1]+h[i])*M[i] + h[i]*M[i+1]
    #     = 6 * ((y[i+1]-y[i])/h[i] - (y[i]-y[i-1])/h[i-1])

    if boundary == "natural":
        # 建立三對角系統（去除已知的 M[0] 和 M[n]）
        size = n - 1  # 內部點數
        if size <= 0:
            # 只有兩個點，退化為線性插值
            return linear_interpolation(points)

        # 對角線
        diag = [2.0 * (h[i-1] + h[i]) for i in range(1, n)]
        # 下對角線
        lower = [h[i] for i in range(1, n-1)]
        # 上對角線
        upper = [h[i-1] for i in range(2, n)]
        # 右端項
        rhs = [6.0 * ((y[i+1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])
               for i in range(1, n)]

        # 使用 Thomas 算法求解 M[1..n-1]
        M_internal = thomas_solve(diag, lower, upper, rhs)

        # 組合完整的 M 陣列
        M = [0.0] * (n + 1)
        for i in range(1, n):
            M[i] = M_internal[i-1]
        # M[0] = M[n] = 0 已經是自然樣條的設定

    else:
        raise ValueError(f"不支援的邊界條件: {boundary}")

    def s(x_val: float) -> float:
        """計算樣條在 x_val 處的值"""
        # 找到所在區間
        i = find_interval(x, x_val, n)

        hi = h[i]
        xi = x[i]
        xi1 = x[i+1]
        yi = y[i]
        yi1 = y[i+1]
        Mi = M[i]
        Mi1 = M[i+1]

        t = x_val - xi

        # 三次多項式：S_i(x) = a_i + b_i*t + c_i*t² + d_i*t³
        a = yi
        b = (yi1 - yi) / hi - hi * (2*Mi + Mi1) / 6.0
        c = Mi / 2.0
        d = (Mi1 - Mi) / (6.0 * hi)

        return a + b*t + c*t*t + d*t*t*t

    return s


def linear_interpolation(points: List[Tuple[float, float]]) -> Callable[[float], float]:
    """兩個點時的線性插值"""
    x0, y0 = points[0]
    x1, y1 = points[1]

    def linear(x_val: float) -> float:
        if x1 == x0:
            return y0
        return y0 + (y1 - y0) * (x_val - x0) / (x1 - x0)

    return linear


def thomas_solve(
    diag: List[float],
    lower: List[float],
    upper: List[float],
    rhs: List[float]
) -> List[float]:
    """
    Thomas 算法（特種高斯消去）求解三對角方程組

    參數:
        diag: 對角線元素 [d0, d1, ..., dn-1]
        lower: 下對角線元素 [l1, l2, ..., ln-1]（第一個元素對應第二行）
        upper: 上對角線元素 [u0, u1, ..., un-2]（最後一個元素對應第 n-2 行）
        rhs: 右端項

    回傳:
        解向量
    """
    n = len(diag)
    if n == 0:
        return []

    # 前向消去
    d = diag[:]
    r = rhs[:]

    for i in range(1, n):
        factor = lower[i-1] / d[i-1]
        d[i] -= factor * upper[i-1]
        r[i] -= factor * r[i-1]

    # 回代
    x = [0.0] * n
    x[n-1] = r[n-1] / d[n-1]
    for i in range(n-2, -1, -1):
        x[i] = (r[i] - upper[i] * x[i+1]) / d[i]

    return x


def find_interval(x: List[float], x_val: float, n: int) -> int:
    """找到 x_val 所在的區間索引"""
    if x_val <= x[0]:
        return 0
    if x_val >= x[n]:
        return n - 1
    for i in range(n):
        if x[i] <= x_val < x[i+1]:
            return i
    return n - 1


def demo_simple() -> None:
    """簡單樣條插值範例"""
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0)]

    print("三次樣條插值範例:")
    print("插值點:", points)

    s = cubic_spline(points, boundary="natural")

    # 在每個區間內取點評估
    print("\n樣條函數值:")
    for x_val in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        print(f"  s({x_val}) = {s(x_val):.6f}")


def demo_smoothness() -> None:
    """展示樣條的平滑性：與高次多項式插值比較"""
    import math

    # 使用 5 個點
    points = [(-1.0, 1.0/(1+25*(-1)**2)), (-0.5, 1.0/(1+25*(-0.5)**2)),
              (0.0, 1.0), (0.5, 1.0/(1+25*0.5**2)), (1.0, 1.0/(1+25*1**2))]

    print("\n對比樣條與拉格朗日插值（龍格函數）:")
    print("樣條插值避免了邊緣震盪問題")


if __name__ == "__main__":
    print("=== 三次樣條插值 ===\n")
    demo_simple()
    demo_smoothness()
