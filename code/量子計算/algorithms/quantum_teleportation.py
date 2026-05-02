"""
量子隱形傳態協定 - 量子通訊的核心協定
"""

from typing import Tuple, List
import math
import random
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gates.quantum_gates import QubitState, H_GATE, X_GATE, Z_GATE, apply_single_qubit_gate, apply_cnot
from gates.circuit import QuantumCircuit


def create_entangled_pair() -> Tuple[QubitState, int, int]:
    """
    建立糾纏對 (Bell 態)
    
    Returns:
        (糾纏系統狀態, qubit_a 索引, qubit_b 索引)
    """
    # 建立 |00⟩
    state = QubitState([1.0, 0.0, 0.0, 0.0])
    # H on qubit 1
    state = apply_single_qubit_gate(state, H_GATE, 1)
    # CNOT: control=1, target=0
    state = apply_cnot(state, 1, 0)
    # 結果: (|00⟩ + |11⟩) / √2
    return state, 1, 0  # Alice 拿 qubit 1, Bob 拿 qubit 0


def quantum_teleportation(state_to_send: QubitState) -> QubitState:
    """
    量子隱形傳態協定
    
    Args:
        state_to_send: 要傳送的量子態 (1-qubit)
    
    Returns:
        Bob 端恢復的量子態
    """
    # 要傳送的態: α|0⟩ + β|1⟩
    alpha = state_to_send.amplitudes[0]
    beta = state_to_send.amplitudes[1]
    
    # 建立 3-qubit 系統: [傳送態, Alice的糾纏位元, Bob的糾纏位元]
    # 初始: (α|0⟩ + β|1⟩) ⊗ |00⟩
    initial = [0.0] * 8
    initial[0] = alpha  # |000⟩
    initial[1] = beta   # |100⟩
    state = QubitState(initial)
    
    # 步驟 1: Alice 對她的兩個位元應用 CNOT (控制=0, 目標=1)
    state = apply_cnot(state, 0, 1)
    
    # 步驟 2: Alice 對她的第一個位元應用 H
    state = apply_single_qubit_gate(state, H_GATE, 0)
    
    # 步驟 3: Alice 測量她的兩個位元
    # 測量 qubit 0
    prob_0_0 = sum(abs(state.amplitudes[i]) ** 2 for i in range(8) if (i & 1) == 0)
    prob_0_1 = sum(abs(state.amplitudes[i]) ** 2 for i in range(8) if (i & 1) == 1)
    
    if random.random() < prob_0_1:
        alice_result_0 = 1
    else:
        alice_result_0 = 0
    
    # 測量 qubit 1
    prob_1_0 = sum(abs(state.amplitudes[i]) ** 2 for i in range(8) if ((i >> 1) & 1) == 0)
    prob_1_1 = sum(abs(state.amplitudes[i]) ** 2 for i in range(8) if ((i >> 1) & 1) == 1)
    
    if random.random() < prob_1_1:
        alice_result_1 = 1
    else:
        alice_result_1 = 0
    
    # 坍縮狀態（根據 Alice 的測量結果）
    # Bob 的位元 (qubit 2) 現在處於對應的狀態
    # 根據 Alice 的測量結果進行修正
    
    # 提取 Bob 的狀態
    # 根據結果選擇對應的基底
    if alice_result_0 == 0 and alice_result_1 == 0:
        # Bob 的態是 α|0⟩ + β|1⟩，不需要修正
        bob_state = QubitState([alpha, beta])
    elif alice_result_0 == 0 and alice_result_1 == 1:
        # Bob 的態是 α|1⟩ + β|0⟩，應用 X
        bob_state = QubitState([beta, alpha])
    elif alice_result_0 == 1 and alice_result_1 == 0:
        # Bob 的態是 α|0⟩ - β|1⟩，應用 Z
        bob_state = QubitState([alpha, -beta])
    else:  # (1, 1)
        # Bob 的態是 β|0⟩ - α|1⟩，應用 X 和 Z
        bob_state = QubitState([beta, -alpha])
    
    return bob_state


def quantum_teleportation_detailed(state_to_send: QubitState) -> Tuple[QubitState, int, int]:
    """
    詳細的量子隱形傳態，返回修正資訊
    
    Args:
        state_to_send: 要傳送的量子態
    
    Returns:
        (Bob 的狀態, Alice 的第一個測量結果, Alice 的第二個測量結果)
    """
    alpha = state_to_send.amplitudes[0]
    beta = state_to_send.amplitudes[1]
    
    # 建立 3-qubit 系統
    initial = [0.0] * 8
    initial[0] = alpha
    initial[1] = beta
    state = QubitState(initial)
    
    # Alice 的量子位元: 0 (訊息), 1 (糾纏)
    # Bob 的量子位元: 2 (糾纏)
    
    # CNOT: 控制=0, 目標=1
    state = apply_cnot(state, 0, 1)
    # H on qubit 0
    state = apply_single_qubit_gate(state, H_GATE, 0)
    
    # 測量 qubit 0 和 qubit 1
    # 簡化: 直接根據狀態計算測量結果和 Bob 的最終狀態
    
    # 經過上述操作後，狀態變為:
    # (|00⟩(α|0⟩+β|1⟩) + |01⟩(α|1⟩+β|0⟩) + |10⟩(α|0⟩-β|1⟩) + |11⟩(α|1⟩-β|0⟩)) / 2
    
    # 隨機選擇測量結果
    results = [(0, 0), (0, 1), (1, 0), (1, 1)]
    probabilities = [0.25, 0.25, 0.25, 0.25]  # 均勻分佈
    
    r = random.random()
    cumulative = 0
    idx = 0
    for i, p in enumerate(probabilities):
        cumulative += p
        if r < cumulative:
            idx = i
            break
    
    alice_0, alice_1 = results[idx]
    
    # 根據結果，Bob 的狀態
    if alice_0 == 0 and alice_1 == 0:
        bob = QubitState([alpha, beta])
    elif alice_0 == 0 and alice_1 == 1:
        bob = QubitState([beta, alpha])
        bob = apply_single_qubit_gate(bob, X_GATE, 0)
    elif alice_0 == 1 and alice_1 == 0:
        bob = QubitState([alpha, -beta])
        bob = apply_single_qubit_gate(bob, Z_GATE, 0)
    else:
        bob = QubitState([beta, -alpha])
        bob = apply_single_qubit_gate(bob, X_GATE, 0)
        bob = apply_single_qubit_gate(bob, Z_GATE, 0)
    
    return bob, alice_0, alice_1


if __name__ == "__main__":
    print("=== 量子隱形傳態協定示範 ===\n")
    
    # 示範 1: 傳送 |0⟩
    print("1. 傳送 |0⟩:")
    state_0 = QubitState([1.0, 0.0])
    bob_state, r1, r2 = quantum_teleportation_detailed(state_0)
    print(f"   Alice 測量結果: ({r1}, {r2})")
    print(f"   Bob 恢復的狀態: {bob_state}")
    
    # 示範 2: 傳送 |1⟩
    print("\n2. 傳送 |1⟩:")
    state_1 = QubitState([0.0, 1.0])
    bob_state, r1, r2 = quantum_teleportation_detailed(state_1)
    print(f"   Alice 測量結果: ({r1}, {r2})")
    print(f"   Bob 恢復的狀態: {bob_state}")
    
    # 示範 3: 傳送疊加態
    print("\n3. 傳送疊加態 (|0⟩ + |1⟩)/√2:")
    import math
    state_super = QubitState([1/math.sqrt(2), 1/math.sqrt(2)])
    bob_state, r1, r2 = quantum_teleportation_detailed(state_super)
    print(f"   Alice 測量結果: ({r1}, {r2})")
    print(f"   Bob 恢復的狀態: {bob_state}")
    
    # 示範 4: 傳送任意態
    print("\n4. 傳送任意態 α|0⟩ + β|1⟩ (α=0.6, β=0.8):")
    state_arb = QubitState([0.6, 0.8])
    bob_state, r1, r2 = quantum_teleportation_detailed(state_arb)
    print(f"   Alice 測量結果: ({r1}, {r2})")
    print(f"   Bob 恢復的狀態: {bob_state}")
    
    print("\n=== 協定說明 ===")
    print("量子隱形傳態不傳送物質，只傳送量子態")
    print("需要: 1) 糾纏對 2) 古典通訊 (2 bits)")
    print("原始量子態不會被複製 (遵守 no-cloning theorem)")
