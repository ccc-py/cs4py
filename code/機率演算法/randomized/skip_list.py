"""
跳躍表 (Skip List)

由 William Pugh 在 1989 年發明的隨機化資料結構，
提供類似平衡樹的 O(log n) 期望時間複雜度，但實作更簡單。
"""

import random
from typing import Optional, Any, Iterator, List


class SkipListNode:
    """跳躍表節點"""
    
    def __init__(self, key: Any, value: Any, level: int):
        """
        初始化節點
        
        參數:
            key: 鍵值
            value: 資料值
            level: 節點層數
        """
        self.key = key
        self.value = value
        self.forward: List[Optional['SkipListNode']] = [None] * (level + 1)
    
    def __repr__(self) -> str:
        return f"SkipListNode(key={self.key}, level={len(self.forward)-1})"


class SkipList:
    """
    跳躍表資料結構
    
    支援搜尋、插入、刪除操作，期望時間複雜度為 O(log n)。
    使用隨機化決定節點的層數。
    """
    
    def __init__(self, max_level: int = 16, p: float = 0.5):
        """
        初始化跳躍表
        
        參數:
            max_level: 最大層數
            p: 節點上升到下一層的機率
        """
        self.max_level = max_level
        self.p = p
        self.level = 0  # 當前最高層數
        self.header = SkipListNode(None, None, max_level)
        self.size = 0
    
    def _random_level(self) -> int:
        """
        隨機生成節點層數
        
        返回:
            層數 (0 到 max_level 之間)
        """
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level
    
    def search(self, key: Any) -> Optional[Any]:
        """
        搜尋鍵值對應的資料
        
        參數:
            key: 要搜尋的鍵
        
        返回:
            對應的資料值，若不存在則返回 None
        """
        current = self.header
        # 從最高層開始往下搜尋
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and 
                   current.forward[i].key < key):
                current = current.forward[i]
        
        # 到達最底層，檢查下一個節點
        current = current.forward[0]
        if current is not None and current.key == key:
            return current.value
        return None
    
    def insert(self, key: Any, value: Any) -> None:
        """
        插入鍵值對
        
        參數:
            key: 鍵值
            value: 資料值
        """
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # 找出每層需要更新的節點
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and 
                   current.forward[i].key < key):
                current = current.forward[i]
            update[i] = current
        
        # 到達最底層
        current = current.forward[0]
        
        if current is not None and current.key == key:
            # 鍵已存在，更新值
            current.value = value
        else:
            # 插入新節點
            new_level = self._random_level()
            
            # 更新跳躍表的最高層數
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level
            
            # 建立新節點
            new_node = SkipListNode(key, value, new_level)
            
            # 更新每層的指標
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node
            
            self.size += 1
    
    def delete(self, key: Any) -> bool:
        """
        刪除鍵值對
        
        參數:
            key: 要刪除的鍵
        
        返回:
            是否成功刪除
        """
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # 找出每層需要更新的節點
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and 
                   current.forward[i].key < key):
                current = current.forward[i]
            update[i] = current
        
        # 到達要刪除的節點
        current = current.forward[0]
        
        if current is None or current.key != key:
            return False  # 鍵不存在
        
        # 從每層刪除節點
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]
        
        # 更新最高層數
        while (self.level > 0 and 
               self.header.forward[self.level] is None):
            self.level -= 1
        
        self.size -= 1
        return True
    
    def contains(self, key: Any) -> bool:
        """
        檢查鍵是否存在
        
        參數:
            key: 要檢查的鍵
        
        返回:
            是否存在
        """
        return self.search(key) is not None
    
    def __contains__(self, key: Any) -> bool:
        """支援 'in' 運算子"""
        return self.contains(key)
    
    def __len__(self) -> int:
        """返回元素數量"""
        return self.size
    
    def __getitem__(self, key: Any) -> Any:
        """支援 dict 風格的存取"""
        value = self.search(key)
        if value is None:
            raise KeyError(f"Key {key} not found")
        return value
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """支援 dict 風格的賦值"""
        self.insert(key, value)
    
    def items(self) -> Iterator[tuple]:
        """返回所有鍵值對"""
        current = self.header.forward[0]
        while current is not None:
            yield (current.key, current.value)
            current = current.forward[0]
    
    def keys(self) -> Iterator[Any]:
        """返回所有鍵"""
        for key, _ in self.items():
            yield key
    
    def values(self) -> Iterator[Any]:
        """返回所有值"""
        for _, value in self.items():
            yield value
    
    def __repr__(self) -> str:
        return f"SkipList(size={self.size}, level={self.level})"


if __name__ == "__main__":
    print("=== 跳躍表測試 ===\n")
    
    # 測試 1: 基本插入和搜尋
    print("1. 基本插入和搜尋")
    sl = SkipList(max_level=4)
    sl.insert(3, "C")
    sl.insert(1, "A")
    sl.insert(2, "B")
    sl.insert(5, "E")
    sl.insert(4, "D")
    
    print(f"   跳躍表: {sl}")
    for key in [1, 2, 3, 4, 5]:
        print(f"   search({key}) = {sl.search(key)}")
    
    # 測試 2: 刪除
    print(f"\n2. 刪除測試")
    print(f"   刪除 key=3: {sl.delete(3)}")
    print(f"   search(3) after delete: {sl.search(3)}")
    print(f"   刪除不存在的 key=10: {sl.delete(10)}")
    print(f"   跳躍表大小: {len(sl)}")
    
    # 測試 3: 更新現有鍵
    print(f"\n3. 更新現有鍵")
    sl.insert(2, "B_updated")
    print(f"   search(2) after update: {sl.search(2)}")
    
    # 測試 4: 遍歷
    print(f"\n4. 遍歷所有元素")
    print(f"   所有鍵值對: {list(sl.items())}")
    print(f"   所有鍵: {list(sl.keys())}")
    print(f"   所有值: {list(sl.values())}")
    
    # 測試 5: dict 風格操作
    print(f"\n5. dict 風格操作")
    sl2 = SkipList()
    sl2[10] = "ten"
    sl2[20] = "twenty"
    sl2[30] = "thirty"
    print(f"   sl2[10] = {sl2[10]}")
    print(f"   20 in sl2: {20 in sl2}")
    print(f"   40 in sl2: {40 in sl2}")
    
    # 測試 6: 效能測試
    print(f"\n6. 插入效能測試")
    import time
    sl3 = SkipList(max_level=8)
    n = 10000
    
    start = time.time()
    for i in range(n):
        sl3.insert(i, f"value_{i}")
    insert_time = time.time() - start
    
    start = time.time()
    for i in range(n):
        _ = sl3.search(i)
    search_time = time.time() - start
    
    print(f"   插入 {n} 個元素: {insert_time:.6f} 秒")
    print(f"   搜尋 {n} 個元素: {search_time:.6f} 秒")
    print(f"   平均每個搜尋: {search_time/n*1000000:.2f} 微秒")
