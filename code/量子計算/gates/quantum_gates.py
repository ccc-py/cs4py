"""
量子閘模組 - 實作基本的量子閘與矩陣表示
"""

from typing import List, Tuple
import cmath
import math


class QubitState:
    """表示量子位元的狀態向量"""
    
    def __init__(self, amplitudes: List[complex]) -> None:
        """
        初始化量子狀態
        
        Args:
            amplitudes: 複數振幅列表，長度必須是 2 的冪次
        """
        self.amplitudes: List[complex] = amplitudes
        self.num_qubits: int = int(math.log2(len(amplitudes)))
        if 2 ** self.num_qubits != len(amplitudes):
            raise ValueError("狀態向量長度必須是 2 的冪次")
    
    def __str__(self) -> str:
        """字串表示"""
        terms = []
        for i, amp in enumerate(self.amplitudes):
            if abs(amp) > 1e-10:
                basis = format(i, f'0{self.num_qubits}b')
                terms.append(f"{amp:.4f}|{basis}⟩")
        return " + ".join(terms) if terms else "|0⟩"
    
    def measure(self) -> int:
        """
        測量量子狀態，回傳測量結果（基底索引）
        
        Returns:
            測量得到的基底索引
        """
        probabilities = [abs(amp) ** 2 for amp in self.amplitudes]
        r = math.random()
        cumulative = 0.0
        for i, p in enumerate(probabilities):
            cumulative += p
            if cumulative >= r:
                # 測量後坍縮到該狀態
                self.amplitudes = [1.0 if j == i else 0.0 for j in range(len(self.amplitudes))]
                return i
        return len(self.amplitudes) - 1


# 單量子位元閘矩陣
I_GATE: List[List[complex]] = [[1.0, 0.0], [0.0, 1.0]]  # 單位閘
X_GATE: List[List[complex]] = [[0.0, 1.0], [1.0, 0.0]]  # Pauli-X (NOT)
Y_GATE: List[List[complex]] = [[0.0, complex(0, -1)], [complex(0, 1), 0.0]]  # Pauli-Y
Z_GATE: List[List[complex]] = [[1.0, 0.0], [0.0, -1.0]]  # Pauli-Z
H_GATE: List[List[complex]] = [[1/math.sqrt(2), 1/math.sqrt(2)], 
                                [1/math.sqrt(2), -1/math.sqrt(2)]]  # Hadamard
S_GATE: List[List[complex]] = [[1.0, 0.0], [0.0, complex(0, 1)]]  # 相位閘 S
T_GATE: List[List[complex]] = [[1.0, 0.0], 
                                [0.0, complex(math.cos(math.pi/4), math.sin(math.pi/4))]]  # T 閘


def mat_mul(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
    """
    矩陣乘法
    
    Args:
        A: 第一個矩陣
        B: 第二個矩陣
    
    Returns:
        相乘後的矩陣
    """
    n, m = len(A), len(A[0])
    m2, p = len(B), len(B[0])
    if m != m2:
        raise ValueError("矩陣維度不匹配")
    
    result = [[0.0 for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    return result


def tensor_product(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
    """
    張量積 (Kronecker product)
    
    Args:
        A: 第一個矩陣
        B: 第二個矩陣
    
    Returns:
        張量積結果
    """
    n_a, m_a = len(A), len(A[0])
    n_b, m_b = len(B), len(B[0])
    
    result = [[0.0 for _ in range(m_a * m_b)] for _ in range(n_a * n_b)]
    for i in range(n_a):
        for j in range(m_a):
            for k in range(n_b):
                for l in range(m_b):
                    result[i * n_b + k][j * m_b + l] = A[i][j] * B[k][l]
    return result


def apply_single_qubit_gate(state: QubitState, gate: List[List[complex]], target: int) -> QubitState:
    """
    對單一量子位元應用量子閘
    
    Args:
        state: 原始量子狀態
        gate: 量子閘矩陣 (2x2)
        target: 目標量子位元索引（從 0 開始，0 為最低有效位元）
    
    Returns:
        新的量子狀態
    """
    n = state.num_qubits
    new_amplitudes = [0.0] * (2 ** n)
    
    for i in range(2 ** n):
        # 取得目標位元的值
        bit = (i >> target) & 1
        # 取得其他位元的遮罩
        mask = ~(1 << target)
        base = i & mask
        
        # 應用量子閘
        for b in range(2):
            new_index = base | (b << target)
            new_amplitudes[new_index] += gate[b][bit] * state.amplitudes[i]
    
    return QubitState(new_amplitudes)


def apply_cnot(state: QubitState, control: int, target: int) -> QubitState:
    """
    應用 CNOT 閘（受控 NOT）
    
    Args:
        state: 原始量子狀態
        control: 控制位元索引
        target: 目標位元索引
    
    Returns:
        新的量子狀態
    """
    n = state.num_qubits
    new_amplitudes = [0.0] * (2 ** n)
    
    for i in range(2 ** n):
        control_bit = (i >> control) & 1
        if control_bit == 1:
            # 翻轉目標位元
            mask = 1 << target
            new_index = i ^ mask
            new_amplitudes[new_index] = state.amplitudes[i]
        else:
            new_amplitudes[i] = state.amplitudes[i]
    
    return QubitState(new_amplitudes)


def create_bell_state() -> QubitState:
    """
    建立 Bell 態 |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
    
    Returns:
        Bell 態
    """
    # 初始狀態 |00⟩
    state = QubitState([1.0, 0.0, 0.0, 0.0])
    # 對第一個量子位元應用 Hadamard
    state = apply_single_qubit_gate(state, H_GATE, 1)
    # 應用 CNOT (控制=1, 目標=0)
    state = apply_cnot(state, 1, 0)
    return state


def get_gate_matrix(name: str) -> List[List[complex]]:
    """
    根據名稱取得量子閘矩陣
    
    Args:
        name: 閘名稱 ('X', 'Y', 'Z', 'H', 'S', 'T', 'I')
    
    Returns:
        對應的矩陣
    """
    gates = {
        'X': X_GATE, 'Y': Y_GATE, 'Z': Z_GATE,
        'H': H_GATE, 'S': S_GATE, 'T': T_GATE, 'I': I_GATE
    }
    return gates.get(name, I_GATE)


if __name__ == "__main__":
    print("=== 量子閘示範 ===\n")
    
    # 示範 1: 對 |0⟩ 應用 Hadamard
    print("1. Hadamard 閘應用於 |0⟩:")
    state0 = QubitState([1.0, 0.0])
    print(f"   初始: {state0}")
    state_h = apply_single_qubit_gate(state0, H_GATE, 0)
    print(f"   H|0⟩: {state_h}")
    
    # 示範 2: 對 |1⟩ 應用 Hadamard
    print("\n2. Hadamard 閘應用於 |1⟩:")
    state1 = QubitState([0.0, 1.0])
    print(f"   初始: {state1}")
    state_h1 = apply_single_qubit_gate(state1, H_GATE, 0)
    print(f"   H|1⟩: {state_h1}")
    
    # 示範 3: 建立 Bell 態
    print("\n3. 建立 Bell 態 |Φ⁺⟩:")
    bell = create_bell_state()
    print(f"   {bell}")
    print(f"   測量機率: |00⟩={abs(bell.amplitudes[0])**2:.3f}, |11⟩={abs(bell.amplitudes[3])**2:.3f}")
    
    # 示範 4: 應用 Pauli-X (NOT)
    print("\n4. Pauli-X 閘 (NOT):")
    state_x = apply_single_qubit_gate(state0, X_GATE, 0)
    print(f"   X|0⟩ = |1⟩: {state_x}")
    
    # 示範 5: 應用 Pauli-Z
    print("\n5. Pauli-Z 閘:")
    state_z = apply_single_qubit_gate(state_h, Z_GATE, 0)
    print(f"   Z(H|0⟩): {state_z}")
    
    print("\n=== 量子閘矩陣 ===")
    print(f"I (單位): {I_GATE}")
    print(f"X (NOT): {X_GATE}")
    print(f"H (Hadamard): {H_GATE}")
