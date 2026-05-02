"""
資訊理論 - 通道編碼定理示範

透過模擬展示香農通道編碼定理：當傳輸速率 R < C 時，
存在編碼使錯誤機率趨近 0。
"""

from typing import List, Tuple
import random
import math


def repetition_code_encode(bit: int, n: int) -> List[int]:
    """
    重複碼編碼：將 1 位元重複 n 次
    
    Args:
        bit: 輸入位元 (0 或 1)
        n: 重複次數
        
    Returns:
        n 位元碼字
    """
    return [bit] * n


def repetition_code_decode(received: List[int]) -> int:
    """
    多數決解碼
    
    Args:
        received: 接收到的碼字
        
    Returns:
        解碼位元 (0 或 1)
    """
    ones = sum(received)
    return 1 if ones > len(received) / 2 else 0


def simulate_transmission(bits: List[int], channel_p: float, 
                         repeat_n: int, n_trials: int = 1000) -> Tuple[float, float]:
    """
    模擬 BSC 通道傳輸（使用重複碼）
    
    Args:
        bits: 原始資料位元
        channel_p: 通道錯誤機率
        repeat_n: 重複次數
        n_trials: 試驗次數
        
    Returns:
        (位元錯誤率, 碼字錯誤率)
    """
    bit_errors = 0
    codeword_errors = 0
    
    for _ in range(n_trials):
        # 編碼
        encoded = []
        for b in bits:
            encoded.extend(repetition_code_encode(b, repeat_n))
        
        # 通過 BSC 通道
        received = [1 - b if random.random() < channel_p else b for b in encoded]
        
        # 解碼
        decoded = []
        for i in range(0, len(received), repeat_n):
            decoded.append(repetition_code_decode(received[i:i+repeat_n]))
        
        # 計算錯誤
        for i in range(len(bits)):
            if decoded[i] != bits[i]:
                bit_errors += 1
                codeword_errors += 1
                break  # 只計碼字錯誤一次
    
    return bit_errors / (n_trials * len(bits)), codeword_errors / n_trials


def channel_capacity_bsc(p: float) -> float:
    """BSC 通道容量"""
    if p == 0 or p == 1:
        return 1.0
    h = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    return 1.0 - h


def shannon_limit_demo() -> None:
    """
    示範香農極限：當 R < C 時，增加重複次數可降低錯誤率
    """
    print("=== 通道編碼定理示範 ===")
    print("(使用重複碼，R = 1/n)")
    
    p = 0.1  # 通道錯誤機率
    c = channel_capacity_bsc(p)
    print(f"\nBSC p={p}, 通道容量 C={c:.4f} bits/symbol")
    
    test_bits = [random.randint(0, 1) for _ in range(10)]
    
    for n in [3, 5, 7, 9, 11]:
        rate = 1.0 / n
        ber, cer = simulate_transmission(test_bits, p, n, 500)
        print(f"n={n}, R={rate:.4f}, BER={ber:.6f}, CER={cer:.6f}, R<C: {rate<c}")
    
    print("\n當 R < C 時，增加 n 可降低錯誤率")
    print("當 R > C 時，錯誤率有正的下界")


def error_probability_vs_rate() -> None:
    """
    展示錯誤機率與傳輸速率的關係
    """
    print("\n=== 錯誤機率 vs 速率 ===")
    p = 0.05
    c = channel_capacity_bsc(p)
    
    print(f"通道: BSC p={p}, C={c:.4f}")
    print(f"{'重複次數':<10} {'速率 R':<10} {'錯誤率':<15} {'是否 < C'}")
    print("-" * 50)
    
    for n in [3, 5, 7, 9, 15, 31]:
        rate = 1.0 / n
        _, cer = simulate_transmission([1, 0, 1, 0], p, n, 300)
        below = "是" if rate < c else "否"
        print(f"{n:<10} {rate:<10.4f} {cer:<15.6f} {below}")


if __name__ == "__main__":
    random.seed(42)
    shannon_limit_demo()
    error_probability_vs_rate()
