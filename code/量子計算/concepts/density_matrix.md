# 密度矩陣 (Density Matrix)

## 歷史背景

密度矩陣（或密度算子）由 John von Neumann 在 1927 年引入，用於描述統計混合的量子態。這個形式主義對於量子統計力學、開放量子系統、以及量子資訊理論至關重要。

密度矩陣提供了一種統一描述純態（pure states）和混合態（mixed states）的方法，是現代量子物理不可或缺的數學工具。

## 核心原理

### 定義
對於純態 $|\psi\rangle$，密度矩陣為：
$$\rho = |\psi\rangle\langle\psi|$$

對於混合態（以機率 $p_i$ 處於態 $|\psi_i\rangle$）：
$$\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$$

### 性質
有效的密度矩陣必須滿足：
1. **Hermitian**：$\rho^\dagger = \rho$
2. **跡為 1**：$\text{Tr}(\rho) = 1$
3. **半正定**：$\langle v|\rho|v\rangle \geq 0$ 對所有 $|v\rangle$

### 純度 (Purity)
$$\text{Tr}(\rho^2) = \begin{cases} 1 & \text{純態} \\ < 1 & \text{混合態} \end{cases}$$

### 部分跡 (Partial Trace)
對於複合系統 $AB$，約化密度矩陣：
$$\rho_A = \text{Tr}_B(\rho_{AB})$$

這描述了子系統 A 的狀態，即使整體是純態，約化態也可能是混合態（糾纏的結果）。

## 使用範例

```python
from density_matrix import DensityMatrix, create_mixed_state, completely_mixed_state
from gates.quantum_gates import QubitState

# 純態 |0⟩
state = QubitState([1.0, 0.0])
rho = DensityMatrix(state)
print(f"純度: {rho.purity()}")  # 1.0

# 混合態: 50% |0⟩, 50% |1⟩
states = [QubitState([1.0, 0.0]), QubitState([0.0, 1.0])]
rho_mixed = create_mixed_state(states, [0.5, 0.5])
print(f"純度: {rho_mixed.purity()}")  # 0.5
```

## 比較

| 特性 | 純態 | 混合態 |
|---|---|---|
| 表示 | $|\psi\rangle$ | $\rho = \sum p_i|\psi_i\rangle\langle\psi_i|$ |
| 純度 | 1 | < 1 |
| 來源 | 確定的量子態 | 經典不確定性或糾纏 |
| 可分離性 | 可能糾纏 | 一定可分離 |

## 參考資料

1. Von Neumann, J. (1927). "Thermodynamik quantenmechanischer Gesamtheiten". *Göttinger Nachrichten*, 273-291.
2. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
3. Preskill, J. (1998). *Lecture Notes for Physics 229: Quantum Information and Computation*. Caltech.
4. Breuer, H. P., & Petruccione, F. (2002). *The Theory of Open Quantum Systems*. Oxford University Press.
