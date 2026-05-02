"""
布隆過濾器 (Bloom Filter)

空間效率極高的機率型資料結構，用於測試元素是否為集合的成員。
可能產生假陽性 (false positive)，但不會有假陰性 (false negative)。
"""

import hashlib
import math
from typing import List, Optional


class BloomFilter:
    """
    布隆過濾器
    
    使用多位元陣列和多個雜湊函數來表示集合。
    查詢時若返回 False，元素一定不在集合中；
    若返回 True，元素可能在集合中（有一定假陽性機率）。
    """
    
    def __init__(self, capacity: int, false_positive_rate: float = 0.01):
        """
        初始化布隆過濾器
        
        參數:
            capacity: 預期要儲存的元素數量
            false_positive_rate: 可接受的假陽性率
        """
        self.capacity = capacity
        self.false_positive_rate = false_positive_rate
        
        # 計算位元陣列大小和雜湊函數數量
        self.size = self._calculate_size(capacity, false_positive_rate)
        self.hash_count = self._calculate_hash_count(self.size, capacity)
        
        # 初始化位元陣列 (使用 bytearray)
        self.bit_array = bytearray((self.size + 7) // 8)
        self.count = 0
    
    @staticmethod
    def _calculate_size(n: int, p: float) -> int:
        """
        計算需要的位元數
        
        參數:
            n: 預期元素數量
            p: 假陽性率
        
        返回:
            需要的位元數
        """
        return int(-n * math.log(p) / (math.log(2) ** 2))
    
    @staticmethod
    def _calculate_hash_count(m: int, n: int) -> int:
        """
        計算最優雜湊函數數量
        
        參數:
            m: 位元陣列大小
            n: 預期元素數量
        
        返回:
            雜湊函數數量
        """
        return int(m / n * math.log(2))
    
    def _get_hash_indices(self, item: bytes) -> List[int]:
        """
        計算 item 的所有雜湊索引
        
        參數:
            item: 要雜湊的項目 (bytes)
        
        返回:
            雜湊索引列表
        """
        # 使用不同的雜湊種子來模擬多個雜湊函數
        indices = []
        for i in range(self.hash_count):
            # 使用 hashlib 產生雜湊值
            hash_input = str(i).encode() + item
            hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
            indices.append(hash_value % self.size)
        return indices
    
    def add(self, item: any) -> None:
        """
        加入元素
        
        參數:
            item: 要加入的元素
        """
        # 將元素轉為 bytes
        if isinstance(item, str):
            item_bytes = item.encode('utf-8')
        elif isinstance(item, bytes):
            item_bytes = item
        else:
            item_bytes = str(item).encode('utf-8')
        
        # 設定對應的位元
        indices = self._get_hash_indices(item_bytes)
        for idx in indices:
            byte_idx = idx // 8
            bit_idx = idx % 8
            self.bit_array[byte_idx] |= (1 << bit_idx)
        
        self.count += 1
    
    def contains(self, item: any) -> bool:
        """
        檢查元素是否可能在集合中
        
        參數:
            item: 要檢查的元素
        
        返回:
            False 表示一定不在；True 表示可能在
        """
        # 將元素轉為 bytes
        if isinstance(item, str):
            item_bytes = item.encode('utf-8')
        elif isinstance(item, bytes):
            item_bytes = item
        else:
            item_bytes = str(item).encode('utf-8')
        
        # 檢查所有對應的位元是否都為 1
        indices = self._get_hash_indices(item_bytes)
        for idx in indices:
            byte_idx = idx // 8
            bit_idx = idx % 8
            if not (self.bit_array[byte_idx] & (1 << bit_idx)):
                return False
        return True
    
    def __contains__(self, item: any) -> bool:
        """支援 'in' 運算子"""
        return self.contains(item)
    
    def clear(self) -> None:
        """清空布隆過濾器"""
        self.bit_array = bytearray((self.size + 7) // 8)
        self.count = 0
    
    def estimate_false_positive_rate(self) -> float:
        """
        估計當前的假陽性率
        
        返回:
            假陽性率的估計值
        """
        # 計算位元陣列中 1 的比例
        ones = sum(bin(byte).count('1') for byte in self.bit_array)
        zeros = self.size - ones
        if zeros <= 0:
            return 1.0
        
        # 假陽性率 = (1 - (1 - 1/m)^(k*n))^k ≈ (1 - e^(-k*n/m))^k
        m = self.size
        k = self.hash_count
        n = self.count
        return (1 - math.exp(-k * n / m)) ** k


def calculate_bloom_parameters(
    n: int, 
    p: float
) -> tuple[int, int]:
    """
    計算布隆過濾器的參數
    
    參數:
        n: 預期元素數量
        p: 目標假陽性率
    
    返回:
        (位元數, 雜湊函數數量)
    """
    m = int(-n * math.log(p) / (math.log(2) ** 2))
    k = int(m / n * math.log(2))
    return m, k


if __name__ == "__main__":
    print("=== 布隆過濾器測試 ===\n")
    
    # 測試 1: 基本功能
    print("1. 基本功能測試")
    bf = BloomFilter(capacity=1000, false_positive_rate=0.01)
    print(f"   位元數: {bf.size}, 雜湊函數數: {bf.hash_count}")
    
    bf.add("apple")
    bf.add("banana")
    bf.add("cherry")
    
    print(f"   'apple' in bf: {'apple' in bf}")
    print(f"   'banana' in bf: {'banana' in bf}")
    print(f"   'grape' in bf: {'grape' in bf}")
    
    # 測試 2: 假陽性率測試
    print(f"\n2. 假陽性率測試")
    bf2 = BloomFilter(capacity=1000, false_positive_rate=0.01)
    
    # 加入 1000 個元素
    for i in range(1000):
        bf2.add(f"item_{i}")
    
    # 測試不存在的元素
    false_positives = 0
    test_count = 10000
    for i in range(1000, 1000 + test_count):
        if f"item_{i}" in bf2:
            false_positives += 1
    
    actual_fp_rate = false_positives / test_count
    theoretical_fp = bf2.estimate_false_positive_rate()
    print(f"   加入元素數: {bf2.count}")
    print(f"   測試不存在元素: {test_count} 個")
    print(f"   假陽性數: {false_positives}")
    print(f"   實際假陽性率: {actual_fp_rate:.4f}")
    print(f"   理論假陽性率: {theoretical_fp:.4f}")
    print(f"   目標假陽性率: {bf2.false_positive_rate:.4f}")
    
    # 測試 3: 不同假陽性率的比較
    print(f"\n3. 不同假陽性率的比較")
    for fp_rate in [0.1, 0.01, 0.001]:
        m, k = calculate_bloom_parameters(1000, fp_rate)
        print(f"   FP={fp_rate}: 位元數={m}, 雜湊函數數={k}")
    
    # 測試 4: 空過濾器
    print(f"\n4. 空過濾器測試")
    bf3 = BloomFilter(capacity=100, false_positive_rate=0.01)
    print(f"   'test' in empty bf: {'test' in bf3}")
    bf3.add("test")
    print(f"   'test' in bf after add: {'test' in bf3}")
