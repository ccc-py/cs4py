"""
有限元素法 (Finite Element Method, FEM)

一維問題的 Galerkin 有限元素法，使用線性基底函數。
求解一維 Poisson 方程：-u'' = f(x)，搭配 Dirichlet 邊界條件。

歷史背景：
有限元素法的概念由 Courant 在 1940 年代初步提出，但真正成熟於 1960 年代。
Clough、Turner 等人在 1960 年發表的論文被視為現代有限元素法的開端。
此方法最初應用於結構力學，現已成為工程領域求解偏微分方程的主流方法。

核心原理：
1. 將定義域分割為有限個元素
2. 選擇基底函數（線性、三次等）
3. 使用 Galerkin 方法將 PDE 轉換為弱形式
4. 組裝剛度矩陣和載荷向量
5. 求解線性方程組

author: cs4py
"""


def linear_basis(i: int, x: float, nodes: list[float]) -> float:
    """
    線性基底函數 φ_i(x)

    在節點 i 處為 1，相鄰節點處為 0，其他區域為 0

    Args:
        i: 基底函數索引
        x: 評估點
        nodes: 節點位置陣列

    Returns:
        基底函數值
    """
    if i < 0 or i >= len(nodes):
        return 0.0

    x_i = nodes[i]

    if i == 0:
        x_ip1 = nodes[i + 1]
        if x_i <= x <= x_ip1:
            return (x_ip1 - x) / (x_ip1 - x_i)
        return 0.0
    elif i == len(nodes) - 1:
        x_im1 = nodes[i - 1]
        if x_im1 <= x <= x_i:
            return (x - x_im1) / (x_i - x_im1)
        return 0.0
    else:
        x_im1 = nodes[i - 1]
        x_ip1 = nodes[i + 1]
        if x_im1 <= x <= x_i:
            return (x - x_im1) / (x_i - x_im1)
        elif x_i <= x <= x_ip1:
            return (x_ip1 - x) / (x_ip1 - x_i)
        return 0.0


def basis_derivative(i: int, x: float, nodes: list[float]) -> float:
    """
    線性基底函數的導數 φ_i'(x)

    在內部節點為常數值

    Args:
        i: 基底函數索引
        x: 評估點
        nodes: 節點位置陣列

    Returns:
        基底函數導數值
    """
    if i < 0 or i >= len(nodes):
        return 0.0

    if i == 0:
        x_ip1 = nodes[i + 1]
        if nodes[i] <= x <= x_ip1:
            return -1.0 / (x_ip1 - nodes[i])
        return 0.0
    elif i == len(nodes) - 1:
        x_im1 = nodes[i - 1]
        if x_im1 <= x <= nodes[i]:
            return 1.0 / (nodes[i] - x_im1)
        return 0.0
    else:
        x_im1 = nodes[i - 1]
        x_ip1 = nodes[i + 1]
        if x_im1 <= x <= nodes[i]:
            return 1.0 / (nodes[i] - x_im1)
        elif nodes[i] <= x <= x_ip1:
            return -1.0 / (x_ip1 - nodes[i])
        return 0.0


def assemble_stiffness_matrix(nodes: list[float]) -> list[list[float]]:
    """
    組裝剛度矩陣 K_ij = ∫ φ_i' φ_j' dx

    對於線性基底函數，每個元素只影響相鄰的三個 entry

    Args:
        nodes: 節點位置陣列

    Returns:
        剛度矩陣（n x n）
    """
    n = len(nodes)
    K = [[0.0] * n for _ in range(n)]

    for i in range(n):
        K[i][i] = 2.0 / (nodes[i+1] - nodes[i-1]) if 0 < i < n-1 else 1.0 / (nodes[1] - nodes[0]) if i == 0 else 1.0 / (nodes[-1] - nodes[-2])

    for i in range(n - 1):
        h_i = nodes[i + 1] - nodes[i]
        K[i][i] += 1.0 / h_i
        K[i][i+1] = -1.0 / h_i
        K[i+1][i] = -1.0 / h_i
        K[i+1][i+1] += 1.0 / h_i

    return K


def assemble_load_vector(f, nodes: list[float]) -> list[float]:
    """
    組裝載荷向量 F_i = ∫ f(x) φ_i(x) dx

    使用數值積分（梯形法則）

    Args:
        f: 右端函數 f(x)
        nodes: 節點位置陣列

    Returns:
        載荷向量
    """
    n = len(nodes)
    F = [0.0] * n

    for i in range(n):
        if i == 0:
            h0 = nodes[1] - nodes[0]
            F[i] = f(nodes[0]) * h0 / 2 + f(nodes[1]) * h0 / 2
        elif i == n - 1:
            hnm1 = nodes[-1] - nodes[-2]
            F[i] = f(nodes[-2]) * hnm1 / 2 + f(nodes[-1]) * hnm1 / 2
        else:
            him1 = nodes[i] - nodes[i-1]
            hip1 = nodes[i+1] - nodes[i]
            F[i] = f(nodes[i-1]) * him1 / 2 + f(nodes[i]) * (him1 + hip1) / 2 + f(nodes[i+1]) * hip1 / 2

    return F


def apply_dirichlet_boundary(
    K: list[list[float]],
    F: list[float],
    u_left: float,
    u_right: float,
    nodes: list[float]
) -> tuple[list[list[float]], list[float]]:
    """
    套用 Dirichlet 邊界條件 u(0) = u_left, u(1) = u_right

    將第一個和最後一個未知數設為已知值，並調整方程組

    Args:
        K: 剛度矩陣
        F: 載荷向量
        u_left: 左端邊界值
        u_right: 右端邊界值
        nodes: 節點位置

    Returns:
        調整後的 K 和 F
    """
    n = len(nodes)
    K_mod = [row[:] for row in K]
    F_mod = F[:]

    K_mod[0][0] = 1.0
    for j in range(1, n):
        K_mod[0][j] = 0.0
    K_mod[n-1][n-1] = 1.0
    for j in range(n - 1):
        K_mod[n-1][j] = 0.0

    F_mod[0] = u_left
    F_mod[n-1] = u_right

    return K_mod, F_mod


def solve_linear_system(A: list[list[float]], b: list[float]) -> list[float]:
    """
    使用 Gaussian elimination 求解線性系統 Ax = b

    Args:
        A: 係數矩陣 (n x n)
        b: 右端向量 (n,)

    Returns:
        解向量 x
    """
    n = len(b)
    A_aug = [A[i][:] + [b[i]] for i in range(n)]

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A_aug[k][i]) > abs(A_aug[max_row][i]):
                max_row = k
        A_aug[i], A_aug[max_row] = A_aug[max_row], A_aug[i]

        pivot = A_aug[i][i]
        if abs(pivot) < 1e-12:
            continue
        for j in range(i, n + 1):
            A_aug[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = A_aug[k][i]
                for j in range(i, n + 1):
                    A_aug[k][j] -= factor * A_aug[i][j]

    x = [A_aug[i][n] for i in range(n)]
    return x


def solve_poisson_1d(
    f,
    left: float,
    right: float,
    u_left: float,
    u_right: float,
    num_elements: int
) -> tuple[list[float], list[float]]:
    """
    求解一維 Poisson 方程：-u'' = f(x)，u(left) = u_left，u(right) = u_right

    Args:
        f: 右端函數 f(x)
        left: 定義域左端
        right: 定義域右端
        u_left: 左端邊界值
        u_right: 右端邊界值
        num_elements: 元素數量

    Returns:
        (nodes, u) — 節點位置和解向量
    """
    nodes = [left + i * (right - left) / num_elements for i in range(num_elements + 1)]

    K = assemble_stiffness_matrix(nodes)
    F = assemble_load_vector(f, nodes)
    K_mod, F_mod = apply_dirichlet_boundary(K, F, u_left, u_right, nodes)
    u = solve_linear_system(K_mod, F_mod)

    return nodes, u


if __name__ == "__main__":
    print("=" * 50)
    print("有限元素法示範")
    print("=" * 50)

    print("\n--- 線性基底函數 ---")
    nodes = [0.0, 0.25, 0.5, 0.75, 1.0]
    x_test = 0.375

    print(f"節點位置: {nodes}")
    print(f"在 x = {x_test} 處的基底函數值:")
    for i in range(len(nodes)):
        val = linear_basis(i, x_test, nodes)
        print(f"  φ_{i}({x_test}) = {val:.4f}")

    print("\n--- 求解 Poisson 方程 ---")
    print("問題：-u'' = 1，u(0) = 0，u(1) = 0")
    print("精確解：u(x) = x(1-x)/2")

    f_const = lambda x: 1.0

    for num_elem in [4, 8, 16]:
        nodes, u = solve_poisson_1d(
            f_const, 0.0, 1.0, 0.0, 0.0, num_elem
        )
        exact = [x * (1 - x) / 2 for x in nodes]
        error = max(abs(u[i] - exact[i]) for i in range(len(nodes)))
        print(f"\n元素數 = {num_elem}，最大誤差 = {error:.6f}")

    print("\n--- 自定義右端函數 ---")
    print("問題：-u'' = sin(x)，u(0) = 0，u(π) = 0")
    print("精確解：u(x) = sin(x)")

    f_sin = lambda x: __import__('math').sin(x)

    nodes, u = solve_poisson_1d(
        f_sin, 0.0, 3.14159265358979, 0.0, 0.0, 20
    )
    exact_sin = [__import__('math').sin(x) for x in nodes]
    error_sin = max(abs(u[i] - exact_sin[i]) for i in range(len(nodes)))
    print(f"元素數 = 20，最大誤差 = {error_sin:.6f}")

    print("\n--- 顯示數值解與精確解比較 ---")
    print(f"{'x':>6} {'數值解':>12} {'精確解':>12} {'誤差':>12}")
    for i in range(0, len(nodes), 4):
        print(f"{nodes[i]:6.3f} {u[i]:12.6f} {exact_sin[i]:12.6f} {abs(u[i]-exact_sin[i]):12.6f}")

    print("\n" + "=" * 50)
    print("有限元素法求解完成")
    print("=" * 50)