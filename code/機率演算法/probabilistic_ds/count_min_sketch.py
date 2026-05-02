"""
Count-Min Sketch

用於資料流中的頻率估計，由 Graham Cormode 和 S. Muthukrishnan 在 2005 年提出。
提供有界誤差的頻率估計，空間效率極高。
"""

import hashlib
import math
from typing import List, Any, Optional, Tuple


class CountMinSketch:
    """
    Count-Min Sketch 資料結構
    
    使用多個雜湊函數和計數表來估計元素在資料流中出現的頻率。
    估計值可能偏大（有正偏差），但不會偏小。
    """
    
    def __init__(self, epsilon: float = 0.01, delta: float = 0.01):
        """
        初始化 Count-Min Sketch
        
        參數:
            epsilon: 誤差參數 (估計誤差 < epsilon * total_count)
            delta: 機率參數 (估計錯誤的機率 < delta)
        """
        self.epsilon = epsilon
        self.delta = delta
        
        # 計算表的維度
        self.width = int(math.ceil(math.e / epsilon))  # w = ⌈e/ε⌉
        self.depth = int(math.ceil(math.log(1 / delta)))  # d = ⌈ln(1/δ)⌉
        
        # 初始化計數表
        self.table = [[0] * self.width for _ in range(self.depth)]
        
        # 總計數
        self.total_count = 0
    
    def _hash(self, item: Any, seed: int) -> int:
        """
        使用種子產生雜湊值
        
        參數:
            item: 要雜湊的項目
            seed: 雜湊種子
        
        返回:
            雜湊索引 (0 到 width-1)
        """
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        # 使用不同的種子產生不同的雜湊值
        h = hashlib.md5(str(seed).encode() + data).hexdigest()
        return int(h, 16) % self.width
    
    def add(self, item: Any, count: int = 1) -> None:
        """
        增加元素的計數
        
        參數:
            item: 要加入的元素
            count: 增加的數量 (預設 1)
        """
        for i in range(self.depth):
            index = self._hash(item, i)
            self.table[i][index] += count
        self.total_count += count
    
    def estimate(self, item: Any) -> int:
        """
        估計元素的頻率
        
        參數:
            item: 要查詢的元素
        
        返回:
            頻率的估計值（可能偏大）
        """
        min_count = float('inf')
        for i in range(self.depth):
            index = self._hash(item, i)
            count = self.table[i][index]
            if count < min_count:
                min_count = count
        return min_count
    
    def estimate_frequency(self, item: Any) -> float:
        """
        估計元素的相對頻率（佔總數的比例）
        
        參數:
            item: 要查詢的元素
        
        返回:
            相對頻率的估計值
        """
        if self.total_count == 0:
            return 0.0
        return self.estimate(item) / self.total_count
    
    def heavy_hitters(self, threshold: float) -> List[Any]:
        """
        找出重負載元素（出現頻率超過閾值的元素）
        
        注意: Count-Min Sketch 本身不儲存元素，需要外部維護候選列表
        
        參數:
            threshold: 頻率閾值 (0 到 1)
        
        返回:
            重負載元素列表（需要額外的追蹤機制）
        """
        # 注意: 標準 Count-Min Sketch 無法直接列出所有元素
        # 這只是一個介面說明
        raise NotImplementedError(
            "Count-Min Sketch 需要額外的資料結構來追蹤元素"
        )
    
    def clear(self) -> None:
        """清空 Count-Min Sketch"""
        self.table = [[0] * self.width for _ in range(self.depth)]
        self.total_count = 0
    
    def get_parameters(self) -> Tuple[int, int, float, float]:
        """
        返回當前參數
        
        返回:
            (width, depth, epsilon, delta)
        """
        return self.width, self.depth, self.epsilon, self.delta
    
    def __contains__(self, item: Any) -> bool:
        """檢查元素是否出現過（估計頻率 > 0）"""
        return self.estimate(item) > 0


class CountMinSketchWithItems(CountMinSketch):
    """
    擴展的 Count-Min Sketch，追蹤出現過的元素
    
    注意: 這會增加空間使用，但允許查詢重負載元素
    """
    
    def __init__(self, epsilon: float = 0.01, delta: float = 0.01):
        super().__init__(epsilon, delta)
        self.items: List[Any] = []
        self.item_set = set()
    
    def add(self, item: Any, count: int = 1) -> None:
        super().add(item, count)
        if item not in self.item_set:
            self.item_set.add(item)
            self.items.append(item)
    
    def heavy_hitters(self, threshold: float) -> List[Any]:
        """
        找出重負載元素
        
        參數:
            threshold: 頻率閾值
        
        返回:
            頻率超過閾值的元素列表
        """
        result = []
        for item in self.items:
            freq = self.estimate_frequency(item)
            if freq >= threshold:
                result.append((item, self.estimate(item), freq))
        return result
    
    def clear(self) -> None:
        super().clear()
        self.items = []
        self.item_set = set()


if __name__ == "__main__":
    print("=== Count-Min Sketch 測試 ===\n")
    
    # 測試 1: 基本功能
    print("1. 基本功能測試")
    cms = CountMinSketch(epsilon=0.01, delta=0.01)
    print(f"   表大小: {cms.depth} x {cms.width}")
    print(f"   參數: epsilon={cms.epsilon}, delta={cms.delta}")
    
    cms.add("apple", 5)
    cms.add("banana", 3)
    cms.add("apple", 2)  # 再次加入 apple
    
    print(f"   apple 估計頻率: {cms.estimate('apple')}")
    print(f"   banana 估計頻率: {cms.estimate('banana')}")
    print(f"   grape 估計頻率: {cms.estimate('grape')}")
    
    # 測試 2: 與真實頻率比較
    print(f"\n2. 與真實頻率比較")
    import random
    cms2 = CountMinSketch(epsilon=0.01, delta=0.01)
    true_counts = {}
    
    # 產生隨機資料流
    items = ['A', 'B', 'C', 'D', 'E']
    for _ in range(10000):
        item = random.choice(items)
        true_counts[item] = true_counts.get(item, 0) + 1
        cms2.add(item)
    
    print(f"   {'元素':>5} {'真實頻率':>10} {'CMS估計':>10} {'誤差':>10}")
    print(f"   {'-'*40}")
    for item in items:
        true = true_counts[item]
        est = cms2.estimate(item)
        error = est - true
        print(f"   {item:>5} {true:>10d} {est:>10d} {error:>+10d}")
    
    # 測試 3: 誤差界線驗證
    print(f"\n3. 誤差界線驗證")
    epsilon = 0.01
    cms3 = CountMinSketch(epsilon=epsilon, delta=0.01)
    total = 0
    
    for i in range(1000):
        item = f"item_{i % 10}"  # 10 個不同元素
        cms3.add(item)
        total += 1
    
    print(f"   總計數: {total}")
    print(f"   理論誤差界線: {epsilon * total:.1f}")
    for i in range(10):
        item = f"item_{i}"
        true = total // 10
        est = cms3.estimate(item)
        error = est - true
        print(f"   {item}: 真實={true}, 估計={est}, 誤差={error}")
    
    # 測試 4: 重負載元素
    print(f"\n4. 重負載元素測試")
    cms4 = CountMinSketchWithItems(epsilon=0.01, delta=0.01)
    
    # 加入資料，讓 A 和 B 成為重負載
    for _ in range(1000):
        cms4.add("A")
    for _ in range(500):
        cms4.add("B")
    for _ in range(100):
        cms4.add("C")
    for _ in range(10):
        cms4.add("D")
    
    heavy = cms4.heavy_hitters(threshold=0.2)
    print(f"   頻率 > 20% 的元素:")
    for item, count, freq in heavy:
        print(f"   {item}: 計數={count}, 頻率={freq:.2%}")
