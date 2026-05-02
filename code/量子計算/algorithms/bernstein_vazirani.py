"""
Bernstein-Vazirani 演算法 - 單次查詢找出隱藏字串
"""

from typing import List, Callable, Tuple
import math
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gates.quantum_gates import QubitState, H_GATE, apply_single_qubit_gate, apply_cnot
from gates.circuit import QuantumCircuit


def bernstein_vazirani_algorithm(s: str) -> str:
    """
    Bernstein-Vazirani 演算法：找出隱藏的位元字串 s
    
    Args:
        s: 隱藏的位元字串 (如 "101")
    
    Returns:
        找出的位元字串
    """
    n = len(s)  # 位元數
    
    # 建立電路: n 個資料位元 + 1 個目標位元
    circuit = QuantumCircuit(n + 1)
    
    # 初始化目標位元為 |1⟩
    circuit.x(0)  # 目標位元是 qubit 0
    
    # 對所有位元應用 Hadamard
    for i in range(n + 1):
        circuit.h(i)
    
    # 執行電路得到初始狀態
    circuit.run()
    state = circuit.state
    
    # 應用 Oracle U_f
    # f(x) = s·x (內積 mod 2)
    # Oracle: |x⟩|y⟩ -> |x⟩|y ⊕ s·x⟩
    # 相位 kickback: (-1)^(s·x) |x⟩|−⟩
    
    new_amplitudes = list(state.amplitudes)
    N = 2 ** (n + 1)
    
    # 對於每個基底 |x⟩|y⟩，如果 f(x)=1 則添加負號
    for x in range(2 ** n):
        # 計算 s·x
        s_dot_x = 0
        for i in range(n):
            s_bit = int(s[n - 1 - i])  # s 的最低位對應 qubit n-1
            x_bit = (x >> i) & 1
            s_dot_x ^= (s_bit & x_bit)
        
        if s_dot_x == 1:
            # 對所有 y ∈ {0,1} 添加負號
            for y in range(2):
                idx = (x << 1) | y  # x 在高 n 位，y 在最低位
                new_amplitudes[idx] *= -1
    
    state.amplitudes = new_amplitudes
    circuit.state = state
    
    # 對資料位元 (qubit n-1 downto 1) 應用 H
    for i in range(1, n + 1):
        state = apply_single_qubit_gate(state, H_GATE, i)
    circuit.state = state
    
    # 測量資料位元
    # 測量結果應該就是 s
    result_bits = []
    for i in range(n):  # 資料位元是 qubit 1 到 qubit n
        # 計算第 i 個資料位元的機率
        qubit_idx = i + 1  # qubit 索引 (跳過目標位元 0)
        prob_1 = 0.0
        for j, amp in enumerate(state.amplitudes):
            if ((j >> qubit_idx) & 1) == 1:
                prob_1 += abs(amp) ** 2
        result_bits.append('1' if prob_1 > 0.5 else '0')
    
    # 反轉順序（根據量子位元的排列）
    result = ''.join(reversed(result_bits))
    
    return result


def create_oracle_function(s: str) -> Callable[[int], int]:
    """
    建立 Oracle 函數 f(x) = s·x (mod 2)
    
    Args:
        s: 隱藏字串
    
    Returns:
        Oracle 函數
    """
    n = len(s)
    
    def f(x: int) -> int:
        """計算內積 s·x mod 2"""
        result = 0
        for i in range(n):
            s_bit = int(s[n - 1 - i])
            x_bit = (x >> i) & 1
            result ^= (s_bit & x_bit)
        return result
    
    return f


def bernstein_vazirani_with_measurement(s: str) -> str:
    """
    使用測量執行 Bernstein-Vazirani 演算法
    
    Args:
        s: 隱藏字串
    
    Returns:
        測量得到的字串
    """
    n = len(s)
    
    # 初始化: |0...0⟩|1⟩
    state = QubitState([0.0] * (2 ** (n + 1)))
    # 設置為 |0...01⟩ (目標位元為 1)
    state.amplitudes[1] = 1.0
    
    # H⊗(n+1)
    for i in range(n + 1):
        state = apply_single_qubit_gate(state, H_GATE, i)
    
    # Oracle: 相位 kickback
    # 對於每個 x，如果 s·x = 1，則 |x⟩ 乘以 -1
    new_amps = list(state.amplitudes)
    for x in range(2 ** n):
        s_dot_x = 0
        for i in range(n):
            s_bit = int(s[n - 1 - i])
            x_bit = (x >> i) & 1
            s_dot_x ^= (s_bit & x_bit)
        
        if s_dot_x == 1:
            for y in range(2):
                idx = (x << 1) | y
                new_amps[idx] *= -1
    
    state.amplitudes = new_amps
    
    # H⊗n 到資料位元
    for i in range(1, n + 1):
        state = apply_single_qubit_gate(state, H_GATE, i)
    
    # 測量資料位元
    result_bits = []
    for i in range(n):
        qubit_idx = i + 1
        prob_1 = sum(abs(state.amplitudes[j]) ** 2 
                     for j in range(len(state.amplitudes)) 
                     if ((j >> qubit_idx) & 1) == 1)
        result_bits.append('1' if prob_1 > 0.5 else '0')
    
    return ''.join(reversed(result_bits))


if __name__ == "__main__":
    print("=== Bernstein-Vazirani 演算法示範 ===\n")
    
    # 示範 1: s = "101"
    print("1. 隱藏字串 s = '101' (3 bits):")
    s = "101"
    result = bernstein_vazirani_with_measurement(s)
    print(f"   隱藏字串: {s}")
    print(f"   演算法結果: {result}")
    print(f"   成功: {result == s}")
    
    # 示範 2: s = "1101"
    print("\n2. 隱藏字串 s = '1101' (4 bits):")
    s = "1101"
    result = bernstein_vazirani_with_measurement(s)
    print(f"   隱藏字串: {s}")
    print(f"   演算法結果: {result}")
    print(f"   成功: {result == s}")
    
    # 示範 3: s = "1"
    print("\n3. 隱藏字串 s = '1' (1 bit):")
    s = "1"
    result = bernstein_vazirani_with_measurement(s)
    print(f"   隱藏字串: {s}")
    print(f"   演算法結果: {result}")
    print(f"   成功: {result == s}")
    
    # 示範 4: 比較古典與量子
    print("\n=== 量子優勢比較 ===")
    print("問題: 找出隱藏字串 s，其中 f(x) = s·x (mod 2)")
    print()
    print("古典演算法:")
    print("  - 需要 n 次查詢 (分別查詢 |100...0⟩, |010...0⟩, ...)")
    print("  - 或者 1 次查詢如果允許多次輸出 (但標準模型不允許)")
    print()
    print("Bernstein-Vazirani 量子演算法:")
    print("  - 只需要 1 次查詢!")
    print("  - 時間複雜度: O(n)")
    print()
    print("這是第一個展示指數級量子優勢的演算法")
