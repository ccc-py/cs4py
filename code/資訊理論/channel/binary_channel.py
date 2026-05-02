"""
資訊理論 - 二元通道模擬

實作二元對稱通道 (BSC) 和二元擦除通道 (BEC) 的模擬。
"""

from typing import List, Tuple
import random


class BinarySymmetricChannel:
    """二元對稱通道 (BSC)"""
    
    def __init__(self, error_prob: float):
        """
        初始化 BSC
        
        Args:
            error_prob: 翻轉機率 p (0 ≤ p ≤ 1)
        """
        self.p = error_prob
    
    def transmit(self, bit: int) -> int:
        """
        傳輸一個位元
        
        Args:
            bit: 輸入位元 (0 或 1)
            
        Returns:
            輸出位元（可能翻轉）
        """
        if random.random() < self.p:
            return 1 - bit  # 翻轉
        return bit
    
    def transmit_sequence(self, bits: List[int]) -> List[int]:
        """傳輸位元序列"""
        return [self.transmit(b) for b in bits]
    
    def error_rate(self, n_trials: int = 10000) -> float:
        """估算錯誤率"""
        errors = 0
        for _ in range(n_trials):
            b = random.randint(0, 1)
            if self.transmit(b) != b:
                errors += 1
        return errors / n_trials


class BinaryErasureChannel:
    """二元擦除通道 (BEC)"""
    
    def __init__(self, erase_prob: float):
        """
        初始化 BEC
        
        Args:
            erase_prob: 擦除機率 p (0 ≤ p ≤ 1)
        """
        self.p = erase_prob
    
    def transmit(self, bit: int) -> int:
        """
        傳輸一個位元
        
        Args:
            bit: 輸入位元 (0 或 1)
            
        Returns:
            輸出位元，或 -1 表示擦除
        """
        if random.random() < self.p:
            return -1  # 擦除
        return bit
    
    def transmit_sequence(self, bits: List[int]) -> List[int]:
        """傳輸位元序列"""
        return [self.transmit(b) for b in bits]
    
    def erasure_rate(self, n_trials: int = 10000) -> float:
        """估算擦除率"""
        erasures = 0
        for _ in range(n_trials):
            b = random.randint(0, 1)
            if self.transmit(b) == -1:
                erasures += 1
        return erasures / n_trials


def analyze_bsc(p: float, n_bits: int = 1000) -> Tuple[float, float]:
    """
    分析 BSC 的錯誤特性
    
    Args:
        p: 錯誤機率
        n_bits: 測試位元數
        
    Returns:
        (理論錯誤率, 實際錯誤率)
    """
    bsc = BinarySymmetricChannel(p)
    bits = [random.randint(0, 1) for _ in range(n_bits)]
    received = bsc.transmit_sequence(bits)
    errors = sum(1 for i in range(n_bits) if bits[i] != received[i])
    return p, errors / n_bits


def analyze_bec(p: float, n_bits: int = 1000) -> Tuple[float, float]:
    """
    分析 BEC 的擦除特性
    
    Args:
        p: 擦除機率
        n_bits: 測試位元數
        
    Returns:
        (理論擦除率, 實際擦除率)
    """
    bec = BinaryErasureChannel(p)
    bits = [random.randint(0, 1) for _ in range(n_bits)]
    received = bec.transmit_sequence(bits)
    erasures = sum(1 for r in received if r == -1)
    return p, erasures / n_bits


if __name__ == "__main__":
    random.seed(42)
    
    # 示範：BSC
    print("=== BSC 模擬 ===")
    bsc = BinarySymmetricChannel(0.1)
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    received = bsc.transmit_sequence(bits)
    print(f"輸入: {bits}")
    print(f"輸出: {received}")
    print(f"理論錯誤率: {bsc.p:.4f}")
    print(f"實際錯誤率: {bsc.error_rate(5000):.4f}")
    
    # 示範：BEC
    print("\n=== BEC 模擬 ===")
    bec = BinaryErasureChannel(0.2)
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    received = bec.transmit_sequence(bits)
    print(f"輸入: {bits}")
    print(f"輸出: {received} (-1 表示擦除)")
    print(f"理論擦除率: {bec.p:.4f}")
    print(f"實際擦除率: {bec.erasure_rate(5000):.4f}")
    
    # 示範：錯誤分析
    print("\n=== 錯誤率分析 ===")
    for p in [0.01, 0.05, 0.1, 0.2]:
        theory, actual = analyze_bsc(p, 5000)
        print(f"BSC p={p:.2f}: 理論={theory:.4f}, 實際={actual:.4f}")
