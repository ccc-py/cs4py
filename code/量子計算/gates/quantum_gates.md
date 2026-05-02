# 量子閘 (Quantum Gates)

## 歷史背景

量子閘是量子計算的基本操作單元，類似於古典計算中的邏輯閘。1995 年，David Deutsch 提出了量子圖靈機的正式定義，奠定了量子電路的數學基礎。量子閘以么正矩陣（unitary matrix）表示，確保量子演化是可逆且保持機率總和為 1。

主要的量子閘包括：
- **Pauli 閘 (X, Y, Z)**：由 Wolfgang Pauli 的矩陣推廣而來
- **Hadamard 閘 (H)**：由 Jacques Hadamard 提出，用於創建疊加態
- **相位閘 (S, T)**：引入量子相位，對通用量子計算至關重要

## 核心原理

### 量子狀態表示
n 個量子位元的狀態可以用 $2^n$ 維複數向量表示：
$$|\psi\rangle = \sum_{i=0}^{2^n-1} \alpha_i |i\rangle$$

其中 $\sum |\alpha_i|^2 = 1$

### 量子閘的性質
1. **么正性**：$U^\dagger U = I$，確保可逆性
2. **線性**：量子閘對疊加態的作用等於對各基底分別作用後的疊加
3. **張量積**：多量子位元系統的閘是單量子位元閘的張量積

### 基本量子閘矩陣

| 閘 | 符號 | 矩陣表示 |
|---|---|---|
| 單位 | I | $\begin{bmatrix}1 & 0\\0 & 1\end{bmatrix}$ |
| Pauli-X | X | $\begin{bmatrix}0 & 1\\1 & 0\end{bmatrix}$ |
| Pauli-Y | Y | $\begin{bmatrix}0 & -i\\i & 0\end{bmatrix}$ |
| Pauli-Z | Z | $\begin{bmatrix}1 & 0\\0 & -1\end{bmatrix}$ |
| Hadamard | H | $\frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\1 & -1\end{bmatrix}$ |
| 相位 | S | $\begin{bmatrix}1 & 0\\0 & i\end{bmatrix}$ |
| T | T | $\begin{bmatrix}1 & 0\\0 & e^{i\pi/4}\end{bmatrix}$ |

### CNOT 閘
受控 NOT 閘是兩量子位元閘，當控制位元為 |1⟩ 時翻轉目標位元：
$$\text{CNOT} = |0\rangle\langle0| \otimes I + |1\rangle\langle1| \otimes X$$

## 使用範例

```python
from quantum_gates import QubitState, H_GATE, X_GATE, apply_single_qubit_gate, create_bell_state

# 建立 |0⟩ 狀態
state = QubitState([1.0, 0.0])
print(state)  # |0⟩

# 應用 Hadamard 閘
state_h = apply_single_qubit_gate(state, H_GATE, 0)
print(state_h)  # (0.7071+0j)|0⟩ + (0.7071+0j)|1⟩

# 建立 Bell 態
bell = create_bell_state()
print(bell)  # (0.7071+0j)|00⟩ + (0.7071+0j)|11⟩
```

## 參考資料

1. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
2. Deutsch, D. (1985). "Quantum Theory, the Church-Turing Principle and the Universal Quantum Computer". *Proceedings of the Royal Society A*.
3. Hadamard, J. (1893). *Resolution d'une question relative aux determinants*. Bulletin des Sciences Mathématiques.
4. Preskill, J. (1998). *Lecture Notes for Physics 229: Quantum Information and Computation*. California Institute of Technology.
