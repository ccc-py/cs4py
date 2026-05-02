"""使用分離鏈結（Separate Chaining）的雜湊表實作。

歷史背景：
分離鏈結是最早解決雜湊衝突的方法之一，由計算機科學家在20世紀50年代提出。當多個鍵映射到同一個索引時，將它們儲存在該索引的鏈結串列中。

核心概念：
- 雜湊函數：將鍵映射到陣列索引
- 鏈結串列：每個雜湊桶包含一個鏈結串列，儲存衝突的鍵值對
- 負載因子：元素數量 / 桶數量，超過閾值時重整（resize）
"""

from typing import Any, Optional, List


class HashTableChaining:
    """使用分離鏈結的雜湊表。"""
    def __init__(self, capacity: int = 8, load_factor_threshold: float = 0.7) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor_threshold: float = load_factor_threshold
        self.buckets: List[List[tuple]] = [[] for _ in range(capacity)]

    def _hash(self, key: Any) -> int:
        """自定義雜湊函數（基於Python內建hash，確保一致性）。"""
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        """插入或更新鍵值對。"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

    def get(self, key: Any) -> Optional[Any]:
        """獲取鍵對應的值，不存在返回None。"""
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        """刪除鍵值對，成功返回True。"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self) -> None:
        """擴容並重新雜湊所有元素。"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        items = []
        for i, bucket in enumerate(self.buckets):
            if bucket:
                items.append(f"桶{i}: {bucket}")
        return "\n".join(items) if items else "空雜湊表"


if __name__ == "__main__":
    print("=== 分離鏈結雜湊表測試 ===")
    ht = HashTableChaining(capacity=4)
    ht.put("apple", 1)
    ht.put("banana", 2)
    ht.put("orange", 3)
    print(f"雜湊表: {ht}")
    print(f"get('apple'): {ht.get('apple')}")
    print(f"get('grape'): {ht.get('grape')}")
    ht.put("apple", 10)
    print(f"更新apple後: {ht.get('apple')}")
    ht.delete("banana")
    print(f"刪除banana後: {ht}")
    print(f"大小: {len(ht)}")
    print(f"負載因子: {ht.size / ht.capacity:.2f}")
