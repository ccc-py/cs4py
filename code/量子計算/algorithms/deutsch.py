"""
Deutsch 演算法 - 第一個展現量子優勢的演算法
"""

from typing import Callable, List
import math
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gates.quantum_gates import QubitState, H_GATE, apply_single_qubit_gate, apply_cnot
from gates.circuit import QuantumCircuit


def deutsch_algorithm(f: Callable[[int], int]) -> str:
    """
    Deutsch 演算法：判斷函數是常數函數還是平衡函數
    
    Args:
        f: 函數 f: {0,1} -> {0,1}，實際上只評估一次
    
    Returns:
        "constant" 或 "balanced"
    """
    # 建立 2-qubit 電路
    circuit = QuantumCircuit(2)
    
    # 初始狀態: |01⟩
    circuit.x(0)  # 將 qubit 0 設為 |1⟩
    
    # 應用 Hadamard 到兩個量子位元
    circuit.h(1)
    circuit.h(0)
    
    # 執行電路得到初始狀態
    circuit.run()
    
    # 應用 oracle (U_f)
    # U_f|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩
    state = circuit.state
    new_amplitudes = list(state.amplitudes)
    
    # 對於 2-qubit 系統: |00⟩, |01⟩, |10⟩, |11⟩
    # 索引: 0, 1, 2, 3
    # 如果 f(0)=1, 翻轉 |01⟩ 的目標位元 (但目標位元已經是 |1⟩)
    # 實際上只需要根據 f(0) 和 f(1) 來調整相位
    
    # 簡化實作：直接應用變換
    for x in range(2):
        fx = f(x)
        # |x⟩|1⟩ 變為 |x⟩|1⊕f(x)⟩
        # 對於 Deutsch 演算法，我們用相位 kickback
        if fx == 1:
            # 添加負號到 |x⟩|−⟩ 分量
            # 由於目標是 |1⟩，H|1⟩ = |−⟩
            # 實際操作：對應的基底乘以 (-1)^f(x)
            for i in range(4):
                if ((i >> 1) & 1) == x:  # 控制位元為 x
                    if (i & 1) == 1:  # 目標位元為 1
                        new_amplitudes[i] *= -1
    
    state.amplitudes = new_amplitudes
    circuit.state = state
    
    # 應用 Hadamard 到第一個量子位元
    state = apply_single_qubit_gate(state, H_GATE, 1)
    circuit.state = state
    
    # 測量第一個量子位元
    result = circuit.measure(1)
    
    return "constant" if result == 0 else "balanced"


def constant_function(x: int) -> int:
    """常數函數: f(x) = 0"""
    return 0


def constant_function_1(x: int) -> int:
    """常數函數: f(x) = 1"""
    return 1


def balanced_function_x(x: int) -> int:
    """平衡函數: f(x) = x (identity)"""
    return x


def balanced_function_not(x: int) -> int:
    """平衡函數: f(x) = NOT x"""
    return 1 - x


def deutsch_with_oracle(f: Callable[[int], int]) -> str:
    """
    使用標準 Deutsch 演算法實作
    
    Args:
        f: 函數 f: {0,1} -> {0,1}
    
    Returns:
        "constant" 或 "balanced"
    """
    # 初始化: |0⟩|1⟩
    # 使用狀態向量直接實作
    # |ψ₀⟩ = |01⟩
    state = QubitState([0.0, 1.0, 0.0, 0.0])
    
    # 應用 H⊗H
    state = apply_single_qubit_gate(state, H_GATE, 1)  # H on qubit 1
    state = apply_single_qubit_gate(state, H_GATE, 0)  # H on qubit 0
    
    # 應用 U_f (oracle)
    # U_f|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩
    # 對於 |−⟩ 目標，這會產生相位 kickback: (-1)^f(x) |x⟩|−⟩
    new_amps = list(state.amplitudes)
    
    # 檢查 f(0) 和 f(1)
    f0 = f(0)
    f1 = f(1)
    
    # 相位 kickback: 如果 f(x)=1，對應的 |x⟩ 基底乘以 -1
    # 基底: |00⟩=0, |01⟩=1, |10⟩=2, |11⟩=3
    # qubit 1 (控制) 在高位: 0=|0⟩, 2=|1⟩
    if f0 == 1:
        new_amps[0] *= -1  # |00⟩
        new_amps[1] *= -1  # |01⟩
    if f1 == 1:
        new_amps[2] *= -1  # |10⟩
        new_amps[3] *= -1  # |11⟩
    
    state.amplitudes = new_amps
    
    # 應用 H 到 qubit 1 (控制位元)
    state = apply_single_qubit_gate(state, H_GATE, 1)
    
    # 測量 qubit 1
    # 如果 constant: 測量結果為 0
    # 如果 balanced: 測量結果為 1
    prob_0 = abs(state.amplitudes[0]) ** 2 + abs(state.amplitudes[1]) ** 2
    
    # 實際測量（簡化：根據機率判斷）
    return "constant" if prob_0 > 0.5 else "balanced"


if __name__ == "__main__":
    print("=== Deutsch 演算法示範 ===\n")
    
    # 測試常數函數
    print("1. 測試常數函數 f(x) = 0:")
    result = deutsch_with_oracle(constant_function)
    print(f"   結果: {result}")
    
    print("\n2. 測試常數函數 f(x) = 1:")
    result = deutsch_with_oracle(constant_function_1)
    print(f"   結果: {result}")
    
    # 測試平衡函數
    print("\n3. 測試平衡函數 f(x) = x:")
    result = deutsch_with_oracle(balanced_function_x)
    print(f"   結果: {result}")
    
    print("\n4. 測試平衡函數 f(x) = NOT x:")
    result = deutsch_with_oracle(balanced_function_not)
    print(f"   結果: {result}")
    
    # 說明
    print("\n=== 說明 ===")
    print("Deutsch 演算法只需要一次 oracle 查詢")
    print("古典演算法需要兩次查詢才能判斷函數類型")
    print("這是第一個展現量子計算優勢的演算法")
