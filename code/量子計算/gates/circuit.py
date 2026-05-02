"""
量子電路模擬器 - 支援閘序列組合與狀態演化
"""

from typing import List, Tuple, Optional
import math
import cmath
import sys
import os

# 添加當前目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quantum_gates import (
    QubitState, H_GATE, X_GATE, Y_GATE, Z_GATE, S_GATE, T_GATE, I_GATE,
    apply_single_qubit_gate, apply_cnot, tensor_product, mat_mul
)


class QuantumGate:
    """表示電路中的一個量子閘操作"""
    
    def __init__(self, gate_type: str, targets: List[int], 
                 controls: Optional[List[int]] = None, 
                 matrix: Optional[List[List[complex]]] = None) -> None:
        """
        初始化量子閘
        
        Args:
            gate_type: 閘類型 ('X', 'Y', 'Z', 'H', 'S', 'T', 'CNOT')
            targets: 目標量子位元索引列表
            controls: 控制量子位元索引列表（僅 CNOT 使用）
            matrix: 自定義閘矩陣
        """
        self.gate_type = gate_type
        self.targets = targets
        self.controls = controls or []
        self.matrix = matrix
    
    def get_matrix(self) -> List[List[complex]]:
        """取得閘矩陣"""
        gate_matrices = {
            'X': X_GATE, 'Y': Y_GATE, 'Z': Z_GATE,
            'H': H_GATE, 'S': S_GATE, 'T': T_GATE, 'I': I_GATE
        }
        return self.matrix or gate_matrices.get(self.gate_type, I_GATE)


class QuantumCircuit:
    """量子電路模擬器"""
    
    def __init__(self, num_qubits: int) -> None:
        """
        初始化量子電路
        
        Args:
            num_qubits: 量子位元數量
        """
        self.num_qubits = num_qubits
        self.gates: List[QuantumGate] = []
        # 初始狀態 |00...0⟩
        self.state = QubitState([1.0] + [0.0] * (2 ** num_qubits - 1))
    
    def add_gate(self, gate: QuantumGate) -> None:
        """添加閘到電路"""
        self.gates.append(gate)
    
    def h(self, target: int) -> None:
        """添加 Hadamard 閘"""
        self.add_gate(QuantumGate('H', [target]))
    
    def x(self, target: int) -> None:
        """添加 Pauli-X 閘"""
        self.add_gate(QuantumGate('X', [target]))
    
    def z(self, target: int) -> None:
        """添加 Pauli-Z 閘"""
        self.add_gate(QuantumGate('Z', [target]))
    
    def cnot(self, control: int, target: int) -> None:
        """添加 CNOT 閘"""
        self.add_gate(QuantumGate('CNOT', [target], [control]))
    
    def run(self) -> QubitState:
        """
        執行電路，返回最終狀態
        
        Returns:
            最終量子狀態
        """
        state = QubitState([1.0] + [0.0] * (2 ** self.num_qubits - 1))
        
        for gate in self.gates:
            if gate.gate_type == 'CNOT':
                state = apply_cnot(state, gate.controls[0], gate.targets[0])
            else:
                # 處理多目標位元
                for target in gate.targets:
                    state = apply_single_qubit_gate(state, gate.get_matrix(), target)
        
        self.state = state
        return state
    
    def measure(self, qubit: int) -> int:
        """
        測量特定量子位元
        
        Args:
            qubit: 要測量的量子位元索引
        
        Returns:
            測量結果 (0 或 1)
        """
        # 計算該位元為 0 或 1 的機率
        prob_0 = 0.0
        prob_1 = 0.0
        
        for i, amp in enumerate(self.state.amplitudes):
            if ((i >> qubit) & 1) == 0:
                prob_0 += abs(amp) ** 2
            else:
                prob_1 += abs(amp) ** 2
        
        # 根據機率隨機測量
        import random
        if random.random() < prob_1:
            result = 1
        else:
            result = 0
        
        # 坍縮狀態
        new_amplitudes = [0.0] * len(self.state.amplitudes)
        norm = math.sqrt(prob_1 if result == 1 else prob_0)
        
        for i, amp in enumerate(self.state.amplitudes):
            bit = (i >> qubit) & 1
            if bit == result:
                new_amplitudes[i] = amp / norm
        
        self.state = QubitState(new_amplitudes)
        return result
    
    def measure_all(self) -> int:
        """
        測量所有量子位元
        
        Returns:
            測量結果的整數表示
        """
        probabilities = [abs(amp) ** 2 for amp in self.state.amplitudes]
        import random
        r = random.random()
        cumulative = 0.0
        for i, p in enumerate(probabilities):
            cumulative += p
            if cumulative >= r:
                self.state = QubitState([1.0 if j == i else 0.0 for j in range(len(self.state.amplitudes))])
                return i
        return len(self.state.amplitudes) - 1
    
    def get_probabilities(self) -> List[float]:
        """取得各基底的測量機率"""
        return [abs(amp) ** 2 for amp in self.state.amplitudes]
    
    def __str__(self) -> str:
        """字串表示"""
        return f"QuantumCircuit({self.num_qubits} qubits)\n狀態: {self.state}"


def create_bell_circuit() -> QuantumCircuit:
    """
    建立產生 Bell 態的電路
    
    Returns:
        配置好的量子電路
    """
    circuit = QuantumCircuit(2)
    circuit.h(1)      # 對量子位元 1 應用 Hadamard
    circuit.cnot(1, 0)  # CNOT: 控制=1, 目標=0
    return circuit


def create_ghz_circuit(num_qubits: int = 3) -> QuantumCircuit:
    """
    建立 GHZ 態的電路
    
    Args:
        num_qubits: 量子位元數量
    
    Returns:
        配置好的量子電路
    """
    circuit = QuantumCircuit(num_qubits)
    circuit.h(num_qubits - 1)  # 對最高位元應用 Hadamard
    for i in range(num_qubits - 1, 0, -1):
        circuit.cnot(i, i - 1)
    return circuit


if __name__ == "__main__":
    print("=== 量子電路模擬器示範 ===\n")
    
    # 示範 1: Bell 態電路
    print("1. Bell 態電路 (|Φ⁺⟩ = (|00⟩ + |11⟩)/√2):")
    bell_circuit = create_bell_circuit()
    bell_circuit.run()
    print(f"   電路: {bell_circuit}")
    print(f"   機率分布: {bell_circuit.get_probabilities()}")
    
    # 測量多次觀察統計
    print("\n   測量 1000 次統計:")
    counts = {0: 0, 3: 0}
    for _ in range(1000):
        bell_circuit.run()
        result = bell_circuit.measure_all()
        counts[result] = counts.get(result, 0) + 1
    print(f"   |00⟩: {counts[0]} 次, |11⟩: {counts[3]} 次")
    
    # 示範 2: GHZ 態電路
    print("\n2. GHZ 態電路 (3 qubits):")
    ghz_circuit = create_ghz_circuit(3)
    ghz_circuit.run()
    print(f"   狀態: {ghz_circuit.state}")
    print(f"   機率分布: {ghz_circuit.get_probabilities()}")
    
    # 示範 3: 量子傅立葉變換 (3-qubit 簡化版)
    print("\n3. 簡單量子電路 - 疊加態:")
    circuit = QuantumCircuit(3)
    circuit.h(2)
    circuit.h(1)
    circuit.h(0)
    circuit.run()
    print(f"   H⊗H⊗H|000⟩ 狀態:")
    print(f"   機率分布 (前 8 個): {circuit.get_probabilities()[:8]}")
    
    # 示範 4: 測量特定位元
    print("\n4. 測量特定量子位元:")
    circuit = QuantumCircuit(2)
    circuit.h(1)
    circuit.cnot(1, 0)
    circuit.run()
    print(f"   電路狀態: {circuit}")
    result_0 = circuit.measure(0)
    print(f"   測量 qubit 0: {result_0}")
    print(f"   測量後狀態: {circuit.state}")
