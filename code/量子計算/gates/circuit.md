# 量子電路模擬器 (Quantum Circuit Simulator)

## 歷史背景

量子電路模型由 David Deutsch 在 1989 年提出，將量子計算表示為一系列量子閘的序列應用。這種模型類似於古典電路的閘級表示，但具有量子力學特有的疊加和糾纏特性。

1996 年，Robert B. Griffiths 和 Chi-Sheng Niu 提出了量子電路的純狀態向量模擬方法，成為現代量子模擬器的基礎。當前主流的量子模擬框架（如 Qiskit、Cirq）都採用類似的電路模型。

## 核心原理

### 量子電路模型
量子電路由以下元素組成：
1. **量子暫存器**：初始狀態通常為 $|00...0\rangle$
2. **量子閘序列**：對量子位元進行么正操作
3. **測量**：將量子態轉換為古典資訊

### 狀態演化
電路的執行過程是將一系列么正變換應用於初始狀態：
$$|\psi_{final}\rangle = U_n \cdots U_2 U_1 |\psi_{initial}\rangle$$

### 測量與坍縮
測量會導致量子態坍縮：
- 測量第 $i$ 個量子位元得到結果 $b \in \{0, 1\}$
- 狀態坍縮到與測量結果相容的子空間
- 機率由 Born 規則給出：$P(b) = \langle\psi|P_b|\psi\rangle$

### 重要量子態
- **Bell 態**：$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$
- **GHZ 態**：$|\text{GHZ}\rangle = \frac{1}{\sqrt{2}}(|0...0\rangle + |1...1\rangle)$

## 使用範例

```python
from circuit import QuantumCircuit, create_bell_circuit, create_ghz_circuit

# 建立 Bell 態電路
circuit = create_bell_circuit()
circuit.run()
print(circuit.state)  # (0.707+0j)|00⟩ + (0.707+0j)|11⟩

# 測量
result = circuit.measure_all()
print(f"測量結果: {result:02b}")

# 建立 GHZ 態 (3 qubits)
ghz = create_ghz_circuit(3)
ghz.run()
print(ghz.state)
```

## 參考資料

1. Deutsch, D. (1989). "Quantum Computational Networks". *Proceedings of the Royal Society A*.
2. Griffiths, R. B., & Niu, C. S. (1996). "Semiclassical Fourier Transform for Quantum Computation". *Physical Review Letters*.
3. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
4. Qiskit Documentation: https://qiskit.org/documentation/
