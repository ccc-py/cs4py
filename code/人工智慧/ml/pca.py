"""
主成分分析 (Principal Component Analysis, PCA)

歷史背景：
- 1901 年由卡爾·皮爾森 (Karl Pearson) 首次提出，稱為「主軸定理」
- 1933 年哈羅德·霍特林 (Harold Hotelling) 發展為多變量統計方法
- 現代機器學習中，PCA 是最常用的無監督降維技術
- 廣泛應用於資料壓縮、視覺化、雜訊過濾等領域
- 與奇異值分解 (SVD) 有密切關係，可用 SVD 實現

核心概念：
- 將相關的特徵轉換為不相關的主成分 (Principal Components)
- 第一主成分指向資料變異最大的方向
- 第二主成分與第一主成分正交，指向剩餘變異最大的方向
- 透過保留前 k 個主成分，實現降維同時保留大部分資訊
"""

from typing import List, Tuple, Optional
import random
import math


def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """矩陣乘法 C = A × B"""
    rows_A, cols_A = len(A), len(A[0]) if A else 0
    rows_B, cols_B = len(B), len(B[0]) if B else 0

    if cols_A != rows_B:
        raise ValueError(f"矩陣維度不匹配: {cols_A} != {rows_B}")

    result = [[0.0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result


def matrix_transpose(A: List[List[float]]) -> List[List[float]]:
    """矩陣轉置 Aᵀ"""
    if not A:
        return []
    rows, cols = len(A), len(A[0])
    return [[A[i][j] for i in range(rows)] for j in range(cols)]


def matrix_subtract(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """矩陣相減 A - B"""
    rows, cols = len(A), len(A[0])
    return [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]


def vector_dot(a: List[float], b: List[float]) -> float:
    """向量內積"""
    return sum(ai * bi for ai, bi in zip(a, b))


def vector_norm(v: List[float]) -> float:
    """向量 2-範數 (歐幾里得長度)"""
    return math.sqrt(sum(x * x for x in v))


def vector_normalize(v: List[float]) -> List[float]:
    """將向量正規化為單位向量"""
    norm = vector_norm(v)
    if norm < 1e-12:
        return v[:]
    return [x / norm for x in v]


def matrix_vector_multiply(A: List[List[float]], v: List[float]) -> List[float]:
    """矩陣乘向量 A × v"""
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def compute_mean_vector(X: List[List[float]]) -> List[float]:
    """計算每個特徵的均值"""
    if not X:
        return []
    n_samples = len(X)
    n_features = len(X[0])
    return [sum(X[i][j] for i in range(n_samples)) / n_samples
            for j in range(n_features)]


def center_data(X: List[List[float]]) -> Tuple[List[List[float]], List[float]]:
    """
    將資料中心化（減去均值）

    返回：(X_centered, mean_vector)
    """
    mean = compute_mean_vector(X)
    n_samples = len(X)
    n_features = len(X[0])

    X_centered = [
        [X[i][j] - mean[j] for j in range(n_features)]
        for i in range(n_samples)
    ]
    return X_centered, mean


def compute_covariance_matrix(X_centered: List[List[float]]) -> List[List[float]]:
    """
    計算共變異數矩陣 C = (1/(n-1)) × XᵀX

    參數：
        X_centered: 已中心化的資料矩陣 (n_samples × n_features)

    返回：共變異數矩陣 (n_features × n_features)
    """
    n_samples = len(X_centered)
    n_features = len(X_centered[0])

    # 計算 XᵀX
    XT = matrix_transpose(X_centered)
    XTX = matrix_multiply(XT, X_centered)

    # 除以 (n-1) 得到無偏估計
    factor = 1.0 / (n_samples - 1) if n_samples > 1 else 1.0
    return [[XTX[i][j] * factor for j in range(n_features)]
            for i in range(n_features)]


def power_iteration(
    A: List[List[float]], max_iters: int = 100, tol: float = 1e-10
) -> Tuple[List[float], float]:
    """
    冪迭代法 (Power Iteration) 求矩陣的主特徵向量和特徵值

    參數：
        A: 對稱矩陣
        max_iters: 最大迭代次數
        tol: 收斂容忍度

    返回：(eigenvector, eigenvalue)
    """
    n = len(A)
    # 隨機初始化向量
    random.seed(42)
    v = [random.gauss(0, 1) for _ in range(n)]
    v = vector_normalize(v)

    for _ in range(max_iters):
        # v_new = A × v
        v_new = matrix_vector_multiply(A, v)
        # 瑞利商計算特徵值
        lambda_new = vector_dot(v, v_new)
        v_new = vector_normalize(v_new)

        # 檢查收斂
        diff = vector_norm([v_new[i] - v[i] for i in range(n)])
        v = v_new
        if diff < tol:
            break

    # 重新計算特徵值
    Av = matrix_vector_multiply(A, v)
    eigenvalue = vector_dot(v, Av)
    return v, eigenvalue


def gram_schmidt_orthogonalize(v: List[float], basis: List[List[float]]) -> List[float]:
    """
    使用 Gram-Schmidt 過程將向量 v 正交化於已有一組向量 basis
    """
    result = v[:]
    for b in basis:
        # 投影係數
        coeff = vector_dot(result, b)
        result = [result[i] - coeff * b[i] for i in range(len(v))]
    return vector_normalize(result)


def compute_eigen_decomposition(
    C: List[List[float]], n_components: int
) -> Tuple[List[List[float]], List[float]]:
    """
    計算共變異數矩陣的特徵向量和特徵值（使用冪迭代法）

    參數：
        C: 共變異數矩陣 (n_features × n_features)
        n_components: 需要的主成分數量

    返回：(eigenvectors, eigenvalues)
            eigenvectors 每行為一個主成分（特徵向量）
            eigenvalues 為對應的特徵值，由大到小排序
    """
    n_features = len(C)
    n_components = min(n_components, n_features)

    eigenvectors = []
    eigenvalues = []

    # 依序找出每個主成分
    C_work = [row[:] for row in C]  # 複製矩陣

    for k in range(n_components):
        # 使用冪迭代找出當前矩陣的主特徵向量
        v, lambda_val = power_iteration(C_work)
        eigenvectors.append(v)
        eigenvalues.append(lambda_val)

        # 從矩陣中移除該方向（deflation）
        # C_new = C - λvvᵀ
        for i in range(n_features):
            for j in range(n_features):
                C_work[i][j] -= lambda_val * v[i] * v[j]

    # 按照特徵值由大到小排序（冪迭代已經是這個順序）
    return eigenvectors, eigenvalues


def sort_by_eigenvalues(
    eigenvectors: List[List[float]], eigenvalues: List[float]
) -> Tuple[List[List[float]], List[float]]:
    """按照特徵值由大到小排序"""
    paired = sorted(zip(eigenvalues, eigenvectors), key=lambda x: -x[0])
    eigenvalues = [p[0] for p in paired]
    eigenvectors = [p[1] for p in paired]
    return eigenvectors, eigenvalues


class PCA:
    """主成分分析"""

    def __init__(self, n_components: Optional[int] = None):
        """
        初始化 PCA

        參數：
            n_components: 要保留的主成分數量，None 表示保留全部
        """
        self.n_components = n_components
        self.components_: List[List[float]] = []  # 主成分（特徵向量）
        self.explained_variance_: List[float] = []  # 解釋變異（特徵值）
        self.mean_: List[float] = []  # 訓練資料的均值
        self.n_features_: int = 0

    def fit(self, X: List[List[float]]) -> None:
        """
        擬合 PCA 模型

        參數：
            X: 訓練資料 (n_samples × n_features)
        """
        self.n_features_ = len(X[0])

        # 決定主成分數量
        if self.n_components is None:
            n_comp = self.n_features_
        else:
            n_comp = min(self.n_components, self.n_features_)

        # 中心化資料
        X_centered, self.mean_ = center_data(X)

        # 計算共變異數矩陣
        C = compute_covariance_matrix(X_centered)

        # 特徵分解
        eigenvectors, eigenvalues = compute_eigen_decomposition(C, n_comp)

        # 排序（應該已經排序，但保險起見）
        self.components_, self.explained_variance_ = sort_by_eigenvalues(
            eigenvectors, eigenvalues
        )

    def transform(self, X: List[List[float]]) -> List[List[float]]:
        """
        將資料投影到主成分上

        參數：
            X: 資料矩陣

        返回：降維後的資料
        """
        # 中心化
        X_centered = [
            [X[i][j] - self.mean_[j] for j in range(self.n_features_)]
            for i in range(len(X))
        ]

        # 投影到主成分上
        # 每個主成分是一個特徵向量，投影即為 X_centered × component
        n_samples = len(X)
        n_comp = len(self.components_)

        result = [[0.0] * n_comp for _ in range(n_samples)]
        for i in range(n_samples):
            for j in range(n_comp):
                result[i][j] = vector_dot(X_centered[i], self.components_[j])

        return result

    def fit_transform(self, X: List[List[float]]) -> List[List[float]]:
        """擬合模型並轉換資料"""
        self.fit(X)
        return self.transform(X)

    def explained_variance_ratio(self) -> List[float]:
        """
        每個主成分解釋的變異比例

        返回：各主成分的變異解釋比例列表
        """
        total = sum(self.explained_variance_)
        if total == 0:
            return [0.0] * len(self.explained_variance_)
        return [v / total for v in self.explained_variance_]


def demo_2d_to_1d() -> None:
    """2D 到 1D 降維示範"""
    print("=== PCA 2D → 1D 降維示範 ===\n")

    # 生成相關的 2D 資料（沿著對角線分佈）
    random.seed(42)
    n_samples = 50
    X = []
    for _ in range(n_samples):
        t = random.gauss(0, 1)
        x1 = t + random.gauss(0, 0.2)  # 主要方向
        x2 = t + random.gauss(0, 0.2)  # 主要方向（稍有雜訊）
        X.append([x1, x2])

    print(f"原始資料: {len(X)} 個樣本, {len(X[0])} 個特徵")

    # 擬合 PCA
    pca = PCA(n_components=1)
    X_transformed = pca.fit_transform(X)

    print(f"\n主成分 1:")
    print(f"  方向 (特徵向量): [{pca.components_[0][0]:.4f}, {pca.components_[0][1]:.4f}]")
    print(f"  解釋變異: {pca.explained_variance_[0]:.4f}")

    variance_ratio = pca.explained_variance_ratio()
    print(f"  變異解釋比例: {variance_ratio[0]:.2%}")

    print(f"\n降維後資料（前 5 筆）:")
    for i in range(min(5, len(X_transformed))):
        print(f"  {X[i]} -> [{X_transformed[i][0]:.4f}]")


def demo_3d_to_2d() -> None:
    """3D 到 2D 降維示範"""
    print("\n=== PCA 3D → 2D 降維示範 ===\n")

    # 生成 3D 資料，但主要分佈在 2D 平面上
    random.seed(42)
    n_samples = 100
    X = []
    for _ in range(n_samples):
        t1 = random.gauss(0, 1)
        t2 = random.gauss(0, 1)
        x1 = t1 + 0.1 * random.gauss(0, 1)
        x2 = t2 + 0.1 * random.gauss(0, 1)
        x3 = 0.5 * t1 + 0.5 * t2 + 0.1 * random.gauss(0, 1)  # 與 x1, x2 相關
        X.append([x1, x2, x3])

    print(f"原始資料: {len(X)} 個樣本, {len(X[0])} 個特徵")

    # 擬合 PCA
    pca = PCA(n_components=2)
    X_transformed = pca.fit_transform(X)

    print(f"\n主成分:")
    for i in range(2):
        comp = pca.components_[i]
        print(f"  PC{i+1} 方向: [{comp[0]:.4f}, {comp[1]:.4f}, {comp[2]:.4f}]")
        print(f"  解釋變異: {pca.explained_variance_[i]:.4f}")

    variance_ratio = pca.explained_variance_ratio()
    total_var = sum(variance_ratio)
    print(f"\n前 2 個主成分解釋了 {total_var:.2%} 的變異")

    print(f"\n降維後資料（前 5 筆）:")
    for i in range(min(5, len(X_transformed))):
        print(f"  {[f'{x:.2f}' for x in X[i]]} -> {[f'{x:.4f}' for x in X_transformed[i]]}")


def demo_variance_explained() -> None:
    """變異解釋比例示範"""
    print("\n=== 變異解釋比例示範 ===\n")

    # 生成 4D 資料
    random.seed(42)
    n_samples = 200
    X = []
    for _ in range(n_samples):
        t1 = random.gauss(0, 2.0)  # 最大變異方向
        t2 = random.gauss(0, 1.5)  # 第二大
        t3 = random.gauss(0, 0.5)  # 第三大
        t4 = random.gauss(0, 0.1)  # 最小（雜訊為主）
        X.append([t1, t2, t3, t4])

    # 擬合 PCA（保留全部）
    pca = PCA(n_components=4)
    pca.fit(X)

    variance_ratio = pca.explained_variance_ratio()

    print("各主成分解釋變異比例:")
    cumulative = 0.0
    for i, (var, ratio) in enumerate(zip(pca.explained_variance_, variance_ratio)):
        cumulative += ratio
        print(f"  PC{i+1}: 變異 = {var:.4f}, 比例 = {ratio:.2%}, "
              f"累積 = {cumulative:.2%}")

    # 找出解釋 95% 變異所需的主成分數
    cumulative = 0.0
    for i, ratio in enumerate(variance_ratio):
        cumulative += ratio
        if cumulative >= 0.95:
            print(f"\n保留前 {i+1} 個主成分即可解釋 95% 的變異")
            break


if __name__ == "__main__":
    demo_2d_to_1d()
    demo_3d_to_2d()
    demo_variance_explained()
