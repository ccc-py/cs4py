"""
HyperLogLog 演算法

用於估計大數據集中的不重複元素數量（基數估計），
空間複雜度僅為 O(log log n)，極其節省記憶體。
"""

import math
import hashlib
from typing import List, Any, Optional


class HyperLogLog:
    """
    HyperLogLog 演算法實作
    
    使用隨機化的雜湊值前導零計數來估計基數。
    由 Philippe Flajolet 等人在 2007 年提出。
    """
    
    def __init__(self, precision: int = 14):
        """
        初始化 HyperLogLog
        
        參數:
            precision: 精度參數 (通常 4-16)
                       寄存器的數量 = 2^precision
        """
        if not 4 <= precision <= 16:
            raise ValueError("precision 必須在 4 到 16 之間")
        
        self.p = precision
        self.m = 1 << precision  # 寄存器數量 = 2^p
        self.registers = [0] * self.m
        
        # 預計算的 alpha 常數
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)
    
    def _hash(self, value: Any) -> int:
        """
        計算值的雜湊值
        
        參數:
            value: 要雜湊的值
        
        返回:
            64 位元雜湊值 (整數)
        """
        if isinstance(value, bytes):
            data = value
        elif isinstance(value, str):
            data = value.encode('utf-8')
        else:
            data = str(value).encode('utf-8')
        
        # 使用 MD5 產生 128 位元雜湊，取前 64 位元
        h = hashlib.md5(data).hexdigest()
        return int(h[:16], 16)
    
    def _leading_zeros(self, value: int, max_bits: int = 64) -> int:
        """
        計算二進位表示中前導零的數量
        
        參數:
            value: 要計算的值
            max_bits: 假設的位元數
        
        返回:
            前導零數量 + 1 (1 到 max_bits)
        """
        if value == 0:
            return max_bits
        # 計算前導零（從最高位開始）
        count = 0
        for i in range(max_bits - 1, -1, -1):
            if (value >> i) & 1:
                break
            count += 1
        return count + 1  # +1 因為可以觀察到 0 個前導零
    
    def add(self, value: Any) -> None:
        """
        加入一個元素到 HyperLogLog
        
        參數:
            value: 要加入的值
        """
        h = self._hash(value)
        
        # 取前 p 位作為寄存器索引
        index = h & (self.m - 1)
        
        # 剩餘位元用於計算前導零
        remaining = h >> self.p
        
        # 計算前導零數量 (+1)
        rho = self._leading_zeros(remaining, 64 - self.p)
        
        # 更新寄存器（取最大值）
        if rho > self.registers[index]:
            self.registers[index] = rho
    
    def count(self) -> int:
        """
        估計當前的不重複元素數量
        
        返回:
            基數的估計值
        """
        # 計算調和平均
        indicator = sum(2.0 ** (-r) for r in self.registers)
        estimate = self.alpha * self.m * self.m / indicator
        
        # 小範圍修正
        if estimate <= 2.5 * self.m:
            # 計算零寄存器的數量
            zeros = sum(1 for r in self.registers if r == 0)
            if zeros > 0:
                # 使用線性計數修正
                estimate = self.m * math.log(self.m / zeros)
        
        # 大範圍修正 (可選，當 estimate > 2^32/30 時)
        if estimate > (1 << 32) / 30:
            estimate = -(1 << 32) * math.log(1 - estimate / (1 << 32))
        
        return int(round(estimate))
    
    def merge(self, other: 'HyperLogLog') -> None:
        """
        合併另一個 HyperLogLog (必須有相同的精度)
        
        參數:
            other: 要合併的 HyperLogLog
        """
        if self.p != other.p:
            raise ValueError("兩個 HyperLogLog 必須有相同的精度")
        
        for i in range(self.m):
            if other.registers[i] > self.registers[i]:
                self.registers[i] = other.registers[i]
    
    def clear(self) -> None:
        """清空 HyperLogLog"""
        self.registers = [0] * self.m
    
    def __len__(self) -> int:
        """返回估計的基數"""
        return self.count()


def compute_error_rate(precision: int) -> float:
    """
    計算 HyperLogLog 的標準誤差
    
    參數:
        precision: 精度參數
    
    返回:
        標準誤差 (相對誤差)
    """
    m = 1 << precision
    return 1.04 / math.sqrt(m)


if __name__ == "__main__":
    print("=== HyperLogLog 測試 ===\n")
    
    # 測試 1: 基本功能
    print("1. 基本功能測試")
    hll = HyperLogLog(precision=10)
    
    # 加入一些元素
    for i in range(100):
        hll.add(f"user_{i}")
    
    print(f"   實際元素數: 100")
    print(f"   HyperLogLog 估計: {hll.count()}")
    print(f"   相對誤差: {abs(hll.count() - 100) / 100 * 100:.2f}%")
    
    # 測試 2: 不同基數的比較
    print(f"\n2. 不同基數的估計")
    for n in [100, 1000, 10000, 100000]:
        hll = HyperLogLog(precision=14)
        for i in range(n):
            hll.add(f"item_{i}")
        estimate = hll.count()
        error = abs(estimate - n) / n * 100
        print(f"   實際: {n:>6d}, 估計: {estimate:>6d}, 誤差: {error:.2f}%")
    
    # 測試 3: 精度對誤差的影響
    print(f"\n3. 精度對誤差的影響 (n=10000)")
    for p in [8, 10, 12, 14, 16]:
        hll = HyperLogLog(precision=p)
        for i in range(10000):
            hll.add(f"data_{i}")
        estimate = hll.count()
        error = abs(estimate - 10000) / 10000 * 100
        theoretical_error = compute_error_rate(p) * 100
        print(f"   p={p:>2d}, 寄存器數={1<<p:>5d}, 估計: {estimate:>6d}, "
              f"實際誤差: {error:.2f}%, 理論誤差: {theoretical_error:.2f}%")
    
    # 測試 4: 合併測試
    print(f"\n4. 合併測試")
    hll1 = HyperLogLog(precision=10)
    hll2 = HyperLogLog(precision=10)
    
    for i in range(50):
        hll1.add(f"item_{i}")
    for i in range(50, 100):
        hll2.add(f"item_{i}")
    
    print(f"   hll1 估計: {hll1.count()}")
    print(f"   hll2 估計: {hll2.count()}")
    
    hll1.merge(hll2)
    print(f"   合併後估計: {hll1.count()}")
    print(f"   實際應為: ~100")
    
    # 測試 5: 記憶體使用
    print(f"\n5. 記憶體使用比較 (n=10000, p=14)")
    import sys
    hll = HyperLogLog(precision=14)
    for i in range(10000):
        hll.add(f"element_{i}")
    
    hll_size = sys.getsizeof(hll.registers)
    # 精確集合的大小
    exact_set = set(f"element_{i}" for i in range(10000))
    exact_size = sys.getsizeof(exact_set)
    
    print(f"   HyperLogLog 大小: {hll_size} bytes")
    print(f"   精確集合大小: {exact_size} bytes")
    print(f"   節省空間: {exact_size/hll_size:.1f}x")
