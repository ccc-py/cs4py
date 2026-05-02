"""
拉格朗日插值（Lagrange Interpolation）

給定 n+1 個插值點，構造通過所有點的 n 次多項式。
雖然概念簡單，但直接計算會出現數值不穩定（龍格現象）。
"""

from typing import List, Tuple, Callable


def lagrange_basis(
    x: float,
    points: List[Tuple[float, float]],
    j: int
) -> float:
    """
    計算第 j 個拉格朗日基函數在 x 處的值

    參數:
        x: 求值點
        points: 插值點列表 [(x0, y0), (x1, y1), ...]
        j: 基函數索引

    回傳:
        基函數值 L_j(x)
    """
    result = 1.0
    xj = points[j][0]
    for i, (xi, _) in enumerate(points):
        if i != j:
            result *= (x - xi) / (xj - xi)
    return result


def lagrange_interpolation(
    points: List[Tuple[float, float]]
) -> Callable[[float], float]:
    """
    構造拉格朗日插值多項式

    參數:
        points: 插值點列表 [(x0, y0), (x1, y1), ..., (xn, yn)]

    回傳:
        插值多項式函數 p(x)
    """
    n = len(points)

    def p(x: float) -> float:
        """插值多項式在 x 處的值"""
        result = 0.0
        for j in range(n):
            result += points[j][1] * lagrange_basis(x, points, j)
        return result

    return p


def runge_phenomenon() -> None:
    """演示龍格現象：在等距點上插值高次多項式會在邊緣震盪"""
    import math

    # 龍格函數: f(x) = 1 / (1 + 25x²), x ∈ [-1, 1]
    f = lambda x: 1.0 / (1.0 + 25.0 * x * x)

    print("龍格現象演示:")
    print("函數: f(x) = 1 / (1 + 25x²)")
    print()

    for n_points in [5, 9, 13]:
        # 等距插值點
        points = []
        for i in range(n_points):
            xi = -1.0 + 2.0 * i / (n_points - 1)
            points.append((xi, f(xi)))

        # 構造插值多項式
        p = lagrange_interpolation(points)

        # 在邊緣點（如 x=0.8）和中心點評估
        test_points = [-0.8, -0.4, 0.0, 0.4, 0.8]
        print(f"n = {n_points} 個插值點:")
        for x in test_points:
            true_val = f(x)
            interp_val = p(x)
            error = abs(interp_val - true_val)
            print(f"  x={x:5.1f}: 真值={true_val:.6f}, 插值={interp_val:.6f}, 誤差={error:.2e}")
        print()


def demo_simple() -> None:
    """簡單插值範例"""
    # 插值點 (0,1), (1,3), (2,7)
    points = [(0.0, 1.0), (1.0, 3.0), (2.0, 7.0)]
    p = lagrange_interpolation(points)

    print("簡單插值範例:")
    print("插值點:", points)
    print("多項式應通過這些點:")
    for x, y in points:
        print(f"  p({x}) = {p(x):.6f} (應為 {y})")


if __name__ == "__main__":
    print("=== 拉格朗日插值 ===\n")
    demo_simple()
    runge_phenomenon()
