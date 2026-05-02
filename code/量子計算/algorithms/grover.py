"""
Grover 演算法 - 非結構化搜尋的量子演算法
"""

from typing import List, Callable, Tuple
import math
import random
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gates.quantum_gates import QubitState, H_GATE, Z_GATE, apply_single_qubit_gate, apply_cnot
from gates.circuit import QuantumCircuit


def initialize_superposition(num_qubits: int) -> QubitState:
    """
    初始化為均勻疊加態
    
    Args:
        num_qubits: 量子位元數量
    
    Returns:
        均勻疊加態 |+⟩⊗n
    """
    n = num_qubits
    state = QubitState([0.0] * (2 ** n))
    state.amplitudes[0] = 1.0
    
    # 對所有量子位元應用 Hadamard
    for i in range(n):
        new_amplitudes = [0.0] * (2 ** n)
        for j in range(2 ** n):
            bit = (j >> i) & 1
            base = j & ~(1 << i)
            for b in range(2):
                new_idx = base | (b << i)
                new_amplitudes[new_idx] += H_GATE[b][bit] * state.amplitudes[j]
        state.amplitudes = new_amplitudes
    
    return state


def create_oracle(target: int, num_qubits: int) -> List[complex]:
    """
    建立 Oracle 算子，標記目標狀態
    
    Args:
        target: 要搜尋的目標（基底索引）
        num_qubits: 量子位元數量
    
    Returns:
        應用 Oracle 後的狀態（修改原狀態）
    """
    # Oracle: 對目標狀態添加負號
    # U_ω|x⟩ = (-1)^f(x)|x⟩，其中 f(x)=1 若 x=ω
    def apply_oracle(state: QubitState) -> QubitState:
        new_amps = list(state.amplitudes)
        new_amps[target] *= -1
        return QubitState(new_amps)
    
    return apply_oracle


def diffusion_operator(state: QubitState, num_qubits: int) -> QubitState:
    """
    擴散算子（inversion about average）
    
    Args:
        state: 當前量子狀態
        num_qubits: 量子位元數量
    
    Returns:
        應用擴散算子後的狀態
    """
    # 擴散算子: 2|s⟩⟨s| - I，其中 |s⟩ 是均勻疊加態
    n = num_qubits
    N = 2 ** n
    
    # 步驟:
    # 1. 應用 H⊗n
    # 2. 對 |0⟩ 施加相位翻轉（除了 |0⟩ 外全部加負號）
    # 3. 應用 H⊗n
    
    # 實作: 2|s⟩⟨s| - I 作用於 |ψ⟩
    # 計算 ⟨s|ψ⟩ = (1/√N) * Σ ψ_i
    s_dot_psi = sum(state.amplitudes) / math.sqrt(N)
    
    # 新狀態: 2 * s_dot_psi * |s⟩ - |ψ⟩
    # |s⟩ 的振幅都是 1/√N
    new_amplitudes = []
    for i in range(N):
        new_amp = 2 * s_dot_psi * (1.0 / math.sqrt(N)) - state.amplitudes[i]
        new_amplitudes.append(new_amp)
    
    return QubitState(new_amplitudes)


def grover_search(target: int, num_qubits: int, iterations: int = None) -> Tuple[int, QubitState]:
    """
    Grover 搜尋演算法
    
    Args:
        target: 要搜尋的目標索引
        num_qubits: 量子位元數量
        iterations: 迭代次數（若 None 則自動計算）
    
    Returns:
        (測量結果, 最終狀態)
    """
    n = num_qubits
    N = 2 ** n
    
    # 計算最優迭代次數
    if iterations is None:
        iterations = int(math.pi / 4 * math.sqrt(N))
    
    # 初始化均勻疊加態
    state = initialize_superposition(n)
    
    # Grover 迭代
    for _ in range(iterations):
        # Oracle: 標記目標
        state.amplitudes[target] *= -1
        
        # 擴散算子
        state = diffusion_operator(state, n)
    
    # 測量
    probabilities = [abs(amp) ** 2 for amp in state.amplitudes]
    result = max(range(N), key=lambda i: probabilities[i])
    
    return result, state


def grover_search_with_circuit(target: int, num_qubits: int) -> int:
    """
    使用 QuantumCircuit 實作的 Grover 搜尋
    
    Args:
        target: 要搜尋的目標
        num_qubits: 量子位元數量
    
    Returns:
        測量結果
    """
    n = num_qubits
    N = 2 ** n
    
    # 最優迭代次數
    iterations = int(math.pi / 4 * math.sqrt(N))
    
    # 建立電路
    circuit = QuantumCircuit(n)
    
    # 初始化: H⊗n
    for i in range(n):
        circuit.h(i)
    
    # Grover 迭代
    for _ in range(iterations):
        # Oracle: 標記目標狀態
        # 需要對目標狀態添加負號
        # 使用多控制 Z 閘的簡化版
        circuit.run()
        state = circuit.state
        state.amplitudes[target] *= -1
        circuit.state = state
        
        # 擴散算子: H⊗n (2|0⟩⟨0| - I) H⊗n
        for i in range(n):
            circuit.h(i)
        
        # 對 |0...0⟩ 外的所有狀態加負號
        circuit.run()
        state = circuit.state
        for i in range(1, N):
            state.amplitudes[i] *= -1
        circuit.state = state
        
        # 再次 H⊗n
        for i in range(n):
            circuit.h(i)
    
    circuit.run()
    
    # 測量
    return circuit.measure_all()


if __name__ == "__main__":
    print("=== Grover 搜尋演算法示範 ===\n")
    
    # 示範 1: 2-qubit 搜尋 (搜尋 4 個項目中的 1 個)
    print("1. 2-qubit Grover 搜尋 (搜尋目標=3, 即 |11⟩):")
    target = 3
    result, final_state = grover_search(target, 2)
    print(f"   目標: {target} ({target:02b})")
    print(f"   搜尋結果: {result} ({result:02b})")
    print(f"   成功: {result == target}")
    print(f"   最終狀態機率: {[f'{abs(amp)**2:.3f}' for amp in final_state.amplitudes]}")
    
    # 示範 2: 3-qubit 搜尋
    print("\n2. 3-qubit Grover 搜尋 (搜尋目標=5, 即 |101⟩):")
    target = 5
    result, final_state = grover_search(target, 3)
    print(f"   目標: {target} ({target:03b})")
    print(f"   搜尋結果: {result} ({result:03b})")
    print(f"   成功: {result == target}")
    
    # 示範 3: 統計成功率
    print("\n3. Grover 演算法成功率統計 (2-qubit, 搜尋目標=2):")
    target = 2
    successes = 0
    trials = 100
    for _ in range(trials):
        result, _ = grover_search(target, 2)
        if result == target:
            successes += 1
    print(f"   {trials} 次試驗中成功 {successes} 次 ({successes}%)")
    
    # 示範 4: 比較古典與量子
    print("\n4. 時間複雜度比較:")
    print("   古典線性搜尋: O(N) = O(2ⁿ)")
    print("   Grover 量子搜尋: O(√N) = O(2ⁿ/²)")
    print("   例如 N=1024 (10 qubits):")
    print("   古典最壞情況: 1024 次查詢")
    print("   量子: ~32 次迭代")
