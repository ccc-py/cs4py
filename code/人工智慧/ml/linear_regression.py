"""
線性迴歸 (Linear Regression)

歷史背景：
- 1805 年由法國數學家勒讓德 (Adrien-Marie Legendre) 首次提出最小平方法
- 1809 年高斯 (Carl Friedrich Gauss) 獨立發展並聲稱更早發明
- 高斯將此方法應用於天文學的軌道預測，成功預測穀神星位置
- 現代機器學習中，線性迴歸是最基礎的迴歸方法
- 梯度下降法由 Cauchy 於 1847 年提出，後成為神經網路訓練的核心

核心概念：
- 模型：y = w₀ + w₁x₁ + w₂x₂ + ... + wₙxₙ = w · x + b
- 目標：最小化均方誤差 MSE = (1/N) Σ (y_pred - y_true)²
- 正規方程：w = (XᵀX)⁻¹Xᵀy（解析解）
- 梯度下降：迭代更新 w = w - η × ∇L(w)
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
    rows, cols = len(A), len(A[0]) if A else 0
    return [[A[i][j] for i in range(rows)] for j in range(cols)]


def matrix_inverse_2x2(A: List[List[float]]) -> List[List[float]]:
    """計算 2x2 矩陣的逆矩陣"""
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]

    det = a * d - b * c
    if abs(det) < 1e-12:
        raise ValueError("矩陣不可逆（行列式為零）")

    inv_det = 1.0 / det
    return [
        [d * inv_det, -b * inv_det],
        [-c * inv_det, a * inv_det]
    ]


def solve_normal_equation(
    X: List[List[float]], y: List[float]
) -> List[float]:
    """
    使用正規方程求解線性迴歸
    w = (XᵀX)⁻¹ Xᵀ y

    適用於小型資料集，當特徵數量不多時效率佳
    """
    n_samples = len(X)
    n_features = len(X[0])

    # 構建 X 矩陣（已包含截距項時）
    # 計算 XᵀX
    XT = matrix_transpose(X)
    XTX = matrix_multiply(XT, X)

    # 計算 Xᵀy
    XTy = [sum(XT[i][j] * y[j] for j in range(n_samples)) for i in range(n_features)]

    # 解 (XᵀX)w = Xᵀy 使用高斯消去法
    # 構建增廣矩陣 [XᵀX | Xᵀy]
    aug = [XTX[i] + [XTy[i]] for i in range(n_features)]

    # 高斯消去法
    n = n_features
    for col in range(n):
        # 找主元
        max_row = col
        for row in range(col + 1, n):
            if abs(aug[row][col]) > abs(aug[max_row][col]):
                max_row = row
        aug[col], aug[max_row] = aug[max_row], aug[col]

        pivot = aug[col][col]
        if abs(pivot) < 1e-12:
            raise ValueError("矩陣奇異，無法求解")

        # 正規化該行
        for j in range(n + 1):
            aug[col][j] /= pivot

        # 消去其他行
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                for j in range(n + 1):
                    aug[row][j] -= factor * aug[col][j]

    # 最後一列即為解
    return [aug[i][n] for i in range(n)]


class LinearRegression:
    """線性迴歸模型"""

    def __init__(self, fit_intercept: bool = True):
        """
        初始化線性迴歸模型

        參數：
            fit_intercept: 是否擬合截距項（偏置）
        """
        self.fit_intercept = fit_intercept
        self.weights: List[float] = []
        self.bias: float = 0.0
        self.n_features: int = 0

    def _add_intercept(self, X: List[List[float]]) -> List[List[float]]:
        """為特徵矩陣添加截距項（全 1 列）"""
        return [[1.0] + row for row in X]

    def fit_normal_equation(self, X: List[List[float]], y: List[float]) -> None:
        """
        使用正規方程擬合模型（解析解）

        參數：
            X: 特徵矩陣，每行為一個樣本
            y: 目標值列表
        """
        self.n_features = len(X[0])

        if self.fit_intercept:
            X_aug = self._add_intercept(X)
        else:
            X_aug = X

        # 使用正規方程求解
        coeffs = solve_normal_equation(X_aug, y)

        if self.fit_intercept:
            self.bias = coeffs[0]
            self.weights = coeffs[1:]
        else:
            self.bias = 0.0
            self.weights = coeffs

    def fit_gradient_descent(
        self,
        X: List[List[float]],
        y: List[float],
        learning_rate: float = 0.01,
        epochs: int = 1000,
        verbose: bool = False,
    ) -> None:
        """
        使用梯度下降擬合模型

        參數：
            X: 特徵矩陣
            y: 目標值列表
            learning_rate: 學習率 η
            epochs: 訓練回合數
            verbose: 是否輸出損失
        """
        n_samples = len(X)
        n_features = len(X[0])
        self.n_features = n_features

        # 初始化權重和偏置
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for epoch in range(epochs):
            # 計算預測值
            predictions = self._predict_batch(X)

            # 計算誤差
            errors = [predictions[i] - y[i] for i in range(n_samples)]

            # 計算梯度
            # ∂L/∂w_j = (2/N) Σ (y_pred - y_true) * x_j
            # ∂L/∂b = (2/N) Σ (y_pred - y_true)
            grad_w = [0.0] * n_features
            grad_b = 0.0

            for i in range(n_samples):
                grad_b += errors[i] / n_samples
                for j in range(n_features):
                    grad_w[j] += errors[i] * X[i][j] / n_samples

            # 更新參數
            for j in range(n_features):
                self.weights[j] -= learning_rate * grad_w[j]
            self.bias -= learning_rate * grad_b

            if verbose and epoch % 100 == 0:
                loss = self._mean_squared_error(predictions, y)
                print(f"  Epoch {epoch}: MSE = {loss:.6f}")

    def _predict_batch(self, X: List[List[float]]) -> List[float]:
        """批量預測"""
        return [self._predict_one(x) for x in X]

    def _predict_one(self, x: List[float]) -> float:
        """預測單一樣本"""
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def predict(self, X: List[List[float]]) -> List[float]:
        """
        預測

        參數：
            X: 特徵矩陣

        返回：預測值列表
        """
        return self._predict_batch(X)

    def _mean_squared_error(self, y_pred: List[float], y_true: List[float]) -> float:
        """計算均方誤差"""
        n = len(y_true)
        return sum((y_pred[i] - y_true[i]) ** 2 for i in range(n)) / n

    def score(self, X: List[List[float]], y: List[float]) -> float:
        """
        計算 R² 決定係數

        R² = 1 - SS_res / SS_tot
        """
        y_pred = self.predict(X)
        y_mean = sum(y) / len(y)

        ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(len(y)))
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)

        if ss_tot == 0:
            return 0.0
        return 1.0 - ss_res / ss_tot


def generate_synthetic_data(
    n_samples: int, n_features: int, noise_std: float = 0.5
) -> Tuple[List[List[float]], List[float]]:
    """
    生成合成線性資料

    參數：
        n_samples: 樣本數
        n_features: 特徵數
        noise_std: 雜訊標準差

    返回：(X, y)
    """
    random.seed(42)

    # 隨機生成真實權重
    true_weights = [random.uniform(-2, 2) for _ in range(n_features)]
    true_bias = random.uniform(-1, 1)

    X = []
    y = []

    for _ in range(n_samples):
        x = [random.uniform(-5, 5) for _ in range(n_features)]
        y_val = sum(w * xi for w, xi in zip(true_weights, x)) + true_bias
        # 加入高斯雜訊
        y_val += random.gauss(0, noise_std)
        X.append(x)
        y.append(y_val)

    return X, y


def demo_simple_regression() -> None:
    """簡單線性迴歸示範 (一維)"""
    print("=== 簡單線性迴歸示範 (一維) ===\n")

    # 生成資料：y = 2x + 1 + noise
    random.seed(42)
    X = [[x] for x in range(-10, 11)]
    y = [2 * x[0] + 1 + random.gauss(0, 1.0) for x in X]

    print(f"樣本數: {len(X)}")
    print(f"真實模型: y = 2.0 * x + 1.0 (+ 雜訊)")

    # 使用正規方程
    model_ne = LinearRegression(fit_intercept=True)
    model_ne.fit_normal_equation(X, y)
    print(f"\n正規方程結果:")
    print(f"  權重 w = {model_ne.weights[0]:.4f} (真實值: 2.0)")
    print(f"  偏置 b = {model_ne.bias:.4f} (真實值: 1.0)")
    print(f"  R² = {model_ne.score(X, y):.4f}")

    # 使用梯度下降
    model_gd = LinearRegression(fit_intercept=True)
    model_gd.fit_gradient_descent(X, y, learning_rate=0.01, epochs=2000)
    print(f"\n梯度下降結果:")
    print(f"  權重 w = {model_gd.weights[0]:.4f}")
    print(f"  偏置 b = {model_gd.bias:.4f}")
    print(f"  R² = {model_gd.score(X, y):.4f}")


def demo_multiple_regression() -> None:
    """多元線性迴歸示範"""
    print("\n=== 多元線性迴歸示範 (三維) ===\n")

    # 生成三維資料：y = 1.5x₁ - 0.8x₂ + 2.0x₃ + 3.0
    random.seed(42)
    X = [[random.uniform(-5, 5) for _ in range(3)] for _ in range(50)]
    y = [
        1.5 * x[0] - 0.8 * x[1] + 2.0 * x[2] + 3.0 + random.gauss(0, 1.0)
        for x in X
    ]

    print(f"樣本數: {len(X)}, 特徵數: {len(X[0])}")
    print("真實模型: y = 1.5*x₁ - 0.8*x₂ + 2.0*x₃ + 3.0")

    # 使用正規方程
    model = LinearRegression(fit_intercept=True)
    model.fit_normal_equation(X, y)

    print(f"\n擬合結果:")
    print(f"  偏置 b = {model.bias:.4f} (真實值: 3.0)")
    for i, w in enumerate(model.weights):
        true_w = [1.5, -0.8, 2.0][i]
        print(f"  權重 w{i+1} = {w:.4f} (真實值: {true_w})")
    print(f"  R² = {model.score(X, y):.4f}")


def demo_gradient_descent_convergence() -> None:
    """梯度下降收斂示範"""
    print("\n=== 梯度下降收斂示範 ===\n")

    # 簡單資料
    X = [[x] for x in range(-5, 6)]
    y = [3 * x[0] - 2 for x in X]  # 無雜訊，完美線性關係

    model = LinearRegression(fit_intercept=True)
    model.fit_gradient_descent(
        X, y, learning_rate=0.05, epochs=500, verbose=True
    )

    print(f"\n最終結果: w = {model.weights[0]:.4f}, b = {model.bias:.4f}")
    print(f"目標值:   w = 3.0000, b = -2.0000")


if __name__ == "__main__":
    demo_simple_regression()
    demo_multiple_regression()
    demo_gradient_descent_convergence()
