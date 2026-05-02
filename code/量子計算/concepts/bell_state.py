"""
Bell 態 - 最大糾纏態的示範
"""

from typing import List, Tuple
import math
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gates.quantum_gates import QubitState, H_GATE, Z_GATE, apply_single_qubit_gate, apply_cnot


def create_bell_state_phi_plus() -> QubitState:
    """
    建立 Bell 態 |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
    
    Returns:
        Bell 態 |Φ⁺⟩
    """
    state = QubitState([1.0, 0.0, 0.0, 0.0])
    state = apply_single_qubit_gate(state, H_GATE, 1)
    state = apply_cnot(state, 1, 0)
    return state


def create_bell_state_phi_minus() -> QubitState:
    """
    建立 Bell 態 |Φ⁻⟩ = (|00⟩ - |11⟩) / √2
    
    Returns:
        Bell 態 |Φ⁻⟩
    """
    state = QubitState([1.0, 0.0, 0.0, 0.0])
    state = apply_single_qubit_gate(state, H_GATE, 1)
    state = apply_single_qubit_gate(state, Z_GATE, 1)
    state = apply_cnot(state, 1, 0)
    return state


def create_bell_state_psi_plus() -> QubitState:
    """
    建立 Bell 態 |Ψ⁺⟩ = (|01⟩ + |10⟩) / √2
    
    Returns:
        Bell 態 |Ψ⁺⟩
    """
    state = QubitState([0.0, 1.0, 0.0, 0.0])
    state = apply_single_qubit_gate(state, H_GATE, 1)
    state = apply_cnot(state, 1, 0)
    return state


def create_bell_state_psi_minus() -> QubitState:
    """
    建立 Bell 態 |Ψ⁻⟩ = (|01⟩ - |10⟩) / √2
    
    Returns:
        Bell 態 |Ψ⁻⟩
    """
    state = QubitState([0.0, 1.0, 0.0, 0.0])
    state = apply_single_qubit_gate(state, H_GATE, 1)
    state = apply_single_qubit_gate(state, Z_GATE, 1)
    state = apply_cnot(state, 1, 0)
    return state


def get_all_bell_states() -> List[QubitState]:
    """
    取得所有四個 Bell 態
    
    Returns:
        Bell 態列表 [|Φ⁺⟩, |Φ⁻⟩, |Ψ⁺⟩, |Ψ⁻⟩]
    """
    return [
        create_bell_state_phi_plus(),
        create_bell_state_phi_minus(),
        create_bell_state_psi_plus(),
        create_bell_state_psi_minus()
    ]


def measure_in_basis(state: QubitState, basis: str = 'computational') -> Tuple[int, QubitState]:
    """
    在特定基底下測量
    
    Args:
        state: 2-qubit 狀態
        basis: 基底類型 ('computational', 'bell')
    
    Returns:
        (測量結果, 坍縮後的狀態)
    """
    if basis == 'computational':
        # 計算基底 |00⟩, |01⟩, |10⟩, |11⟩
        probs = [abs(amp) ** 2 for amp in state.amplitudes]
        r = math.random()
        cumulative = 0.0
        for i, p in enumerate(probs):
            cumulative += p
            if cumulative >= r:
                new_state = QubitState([0.0] * 4)
                new_state.amplitudes[i] = 1.0
                return i, new_state
    elif basis == 'bell':
        # Bell 基底
        bell_states = get_all_bell_states()
        # 計算在每個 Bell 態上的投影機率
        probs = []
        for bell in bell_states:
            # 內積絕對值平方
            prob = 0.0
            for i in range(4):
                prob += abs(state.amplitudes[i] * bell.amplitudes[i].conjugate()) ** 2
            probs.append(prob)
        
        r = math.random()
        cumulative = 0.0
        for i, p in enumerate(probs):
            cumulative += p
            if cumulative >= r:
                return i, bell_states[i]
    
    return 0, state


def chsh_expectation(theta: float) -> float:
    """
    計算 CHSH 不等式的期望值（簡化版）
    
    Args:
        theta: 測量角度
    
    Returns:
        期望值
    """
    # CHSH 不等式: |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2
    # 量子力學可以違反此不等式，最大值為 2√2
    
    # 使用 |Φ⁺⟩ 態
    bell = create_bell_state_phi_plus()
    
    # 簡化: 返回 cos(2θ) 作為期望值的一部分
    return math.cos(2 * theta)


def bell_inequality_test() -> float:
    """
    測試 CHSH 不等式
    
    Returns:
        S 值（若 > 2 則違反貝爾不等式）
    """
    # 選擇四個測量方向
    angles = [0, math.pi/4, math.pi/2, 3*math.pi/4]
    
    # 計算 CHSH 表達式
    # S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    E_00 = chsh_expectation(angles[0] - angles[0])
    E_01 = chsh_expectation(angles[0] - angles[1])
    E_10 = chsh_expectation(angles[2] - angles[0])
    E_11 = chsh_expectation(angles[2] - angles[3])
    
    S = E_00 - E_01 + E_10 + E_11
    return abs(S)


if __name__ == "__main__":
    print("=== Bell 態示範 ===\n")
    
    # 示範 1: 四個 Bell 態
    print("1. 四個 Bell 態:")
    bell_states = get_all_bell_states()
    names = ["|Φ⁺⟩", "|Φ⁻⟩", "|Ψ⁺⟩", "|Ψ⁻⟩"]
    for name, state in zip(names, bell_states):
        print(f"   {name}: {state}")
    
    # 示範 2: Bell 態的糾纏特性
    print("\n2. Bell 態 |Φ⁺⟩ 的測量:")
    phi_plus = create_bell_state_phi_plus()
    print(f"   狀態: {phi_plus}")
    print(f"   機率: |00⟩={abs(phi_plus.amplitudes[0])**2:.3f}, |11⟩={abs(phi_plus.amplitudes[3])**2:.3f}")
    
    # 示範 3: 測量一個量子位元對另一個的影響
    print("\n3. 測量 qubit 0 後的狀態:")
    import random
    phi_plus = create_bell_state_phi_plus()
    # 測量 qubit 0
    prob_0 = abs(phi_plus.amplitudes[0]) ** 2 + abs(phi_plus.amplitudes[1]) ** 2
    if random.random() < prob_0:
        result = 0
        # 坍縮到 |00⟩
        new_state = QubitState([1.0, 0.0, 0.0, 0.0])
    else:
        result = 1
        # 坍縮到 |11⟩
        new_state = QubitState([0.0, 0.0, 0.0, 1.0])
    print(f"   測量 qubit 0 = {result}")
    print(f"   坍縮後狀態: {new_state}")
    print(f"   Qubit 1 現在確定為 {result}")
    
    # 示範 4: CHSH 不等式
    print("\n4. CHSH 不等式測試:")
    S = bell_inequality_test()
    print(f"   S = {S:.3f}")
    print(f"   古典極限: S ≤ 2")
    print(f"   量子極限: S ≤ 2√2 ≈ {2*math.sqrt(2):.3f}")
    print(f"   違反貝爾不等式: {'是' if S > 2 else '否'}")
    
    # 說明
    print("\n=== 糾纏說明 ===")
    print("Bell 態是最大糾纏態:")
    print("- 單獨測量一個量子位元，結果隨機 (50/50)")
    print("- 但兩個量子位元的測量結果完全相關")
    print("- 這種關聯無法用古典物理解釋")
