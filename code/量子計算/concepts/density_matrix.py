"""
密度矩陣 - 純態與混合態的統一描述
"""

from typing import List, Optional
import math
import cmath
import sys
import os

# 添加上層目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DensityMatrix:
    """密度矩陣表示"""
    
    def __init__(self, state_or_matrix, is_pure_state: bool = True) -> None:
        """
        初始化密度矩陣
        
        Args:
            state_or_matrix: QubitState（純態）或矩陣（直接給定）
            is_pure_state: 是否為純態輸入
        """
        if is_pure_state:
            # 從純態建立密度矩陣: ρ = |ψ⟩⟨ψ|
            state = state_or_matrix
            n = len(state.amplitudes)
            self.matrix = [[0.0j for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    self.matrix[i][j] = state.amplitudes[i] * state.amplitudes[j].conjugate()
        else:
            # 直接給定矩陣
            self.matrix = state_or_matrix
    
    def __str__(self) -> str:
        """字串表示"""
        n = len(self.matrix)
        lines = []
        for i in range(n):
            row = []
            for j in range(n):
                val = self.matrix[i][j]
                if abs(val) < 1e-10:
                    row.append("0")
                else:
                    row.append(f"{val:.3f}")
            lines.append(" ".join(row))
        return "\n".join(lines)
    
    def trace(self) -> complex:
        """計算跡 Tr(ρ)"""
        n = len(self.matrix)
        return sum(self.matrix[i][i] for i in range(n))
    
    def is_valid(self) -> bool:
        """檢查是否為有效的密度矩陣"""
        # 1. 跡為 1
        if abs(self.trace() - 1.0) > 1e-10:
            return False
        # 2. Hermitian: ρ† = ρ
        n = len(self.matrix)
        for i in range(n):
            for j in range(n):
                if abs(self.matrix[i][j] - self.matrix[j][i].conjugate()) > 1e-10:
                    return False
        # 3. 半正定（簡化檢查：對角元非負）
        for i in range(n):
            if self.matrix[i][i].real < -1e-10:
                return False
        return True
    
    def purity(self) -> float:
        """
        計算純度 Tr(ρ²)
        
        Returns:
            純度值（純態為 1，混合態 < 1）
        """
        n = len(self.matrix)
        trace_sq = 0.0
        for i in range(n):
            for j in range(n):
                trace_sq += self.matrix[i][j] * self.matrix[j][i].conjugate()
        return trace_sq.real
    
    def is_pure(self) -> bool:
        """檢查是否為純態"""
        return abs(self.purity() - 1.0) < 1e-10
    
    def partial_trace(self, subsystem: int, num_qubits: int) -> 'DensityMatrix':
        """
        計算部分跡，追蹤掉一個子系統
        
        Args:
            subsystem: 要追蹤掉的子系統 (0 或 1)
            num_qubits: 總量子位元數
        
        Returns:
            約化密度矩陣
        """
        n = len(self.matrix)
        dim_sub = 2 ** (num_qubits - 1)
        reduced = [[0.0j for _ in range(dim_sub)] for _ in range(dim_sub)]
        
        if subsystem == 0:  # 追蹤掉第一個量子位元
            for i in range(dim_sub):
                for j in range(dim_sub):
                    for k in range(2):
                        idx_i = i | (k << (num_qubits - 1))
                        idx_j = j | (k << (num_qubits - 1))
                        reduced[i][j] += self.matrix[idx_i][idx_j]
        else:  # 追蹤掉第二個量子位元
            for i in range(dim_sub):
                for j in range(dim_sub):
                    for k in range(2):
                        idx_i = (i << 1) | k
                        idx_j = (j << 1) | k
                        reduced[i][j] += self.matrix[idx_i][idx_j]
        
        return DensityMatrix(reduced, is_pure_state=False)


def create_mixed_state(states: List, probabilities: List[float]) -> DensityMatrix:
    """
    從純態集合建立混合態
    
    Args:
        states: 純態列表 (QubitState)
        probabilities: 對應的機率
    
    Returns:
        混合態的密度矩陣
    """
    n = len(states[0].amplitudes)
    mixed = [[0.0j for _ in range(n)] for _ in range(n)]
    
    for state, prob in zip(states, probabilities):
        rho_pure = DensityMatrix(state)
        for i in range(n):
            for j in range(n):
                mixed[i][j] += prob * rho_pure.matrix[i][j]
    
    return DensityMatrix(mixed, is_pure_state=False)


def completely_mixed_state(num_qubits: int) -> DensityMatrix:
    """
    建立完全混合態 I / 2^n
    
    Args:
        num_qubits: 量子位元數
    
    Returns:
        完全混合態
    """
    n = 2 ** num_qubits
    matrix = [[0.0j for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1.0 / n
    return DensityMatrix(matrix, is_pure_state=False)


if __name__ == "__main__":
    print("=== 密度矩陣示範 ===\n")
    
    from gates.quantum_gates import QubitState, H_GATE, apply_single_qubit_gate
    
    # 示範 1: 純態的密度矩陣
    print("1. 純態 |0⟩ 的密度矩陣:")
    state_0 = QubitState([1.0, 0.0])
    rho_0 = DensityMatrix(state_0)
    print(rho_0)
    print(f"   純度: {rho_0.purity():.3f}")
    print(f"   是否為純態: {rho_0.is_pure()}")
    
    # 示範 2: 疊加態
    print("\n2. 純態 |+⟩ = H|0⟩ 的密度矩陣:")
    state_plus = apply_single_qubit_gate(state_0, H_GATE, 0)
    rho_plus = DensityMatrix(state_plus)
    print(rho_plus)
    print(f"   純度: {rho_plus.purity():.3f}")
    
    # 示範 3: 混合態
    print("\n3. 混合態: 50% |0⟩, 50% |1⟩:")
    states = [QubitState([1.0, 0.0]), QubitState([0.0, 1.0])]
    probs = [0.5, 0.5]
    rho_mixed = create_mixed_state(states, probs)
    print(rho_mixed)
    print(f"   純度: {rho_mixed.purity():.3f}")
    print(f"   是否為純態: {rho_mixed.is_pure()}")
    
    # 示範 4: Bell 態的部分跡
    print("\n4. Bell 態 |Φ⁺⟩ 的約化密度矩陣:")
    from bell_state import create_bell_state_phi_plus
    bell = create_bell_state_phi_plus()
    rho_bell = DensityMatrix(bell)
    print("   完整密度矩陣 (4x4):")
    print(f"   純度: {rho_bell.purity():.3f}")
    
    # 追蹤掉一個量子位元
    rho_reduced = rho_bell.partial_trace(0, 2)
    print("\n   約化密度矩陣 (追蹤掉 qubit 0, 2x2):")
    print(rho_reduced)
    print(f"   純度: {rho_reduced.purity():.3f}")
    print("   (糾纏態的約化密度矩陣是混合態!)")
    
    # 示範 5: 完全混合態
    print("\n5. 完全混合態 (1-qubit):")
    rho_completely_mixed = completely_mixed_state(1)
    print(rho_completely_mixed)
    print(f"   純度: {rho_completely_mixed.purity():.3f}")
    
    print("\n=== 純態 vs 混合態 ===")
    print("純態: 系統處於確定的量子態 (純度=1)")
    print("混合態: 系統以機率處於不同態 (純度<1)")
    print("混合態來源: 1) 不確定性 2) 糾纏+部分跡")
