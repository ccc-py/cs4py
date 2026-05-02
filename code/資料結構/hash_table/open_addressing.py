"""使用開放定址（Open Addressing）的雜湊表實作。

歷史背景：
開放定址法由計算機科學家在20世紀50年代提出，當發生衝突時，按某種探測策略在陣列中尋找下一個可用位置，無需額外的鏈結結構。

核心概念：
- 線性探測：依次檢查下一個位置（h(k,i) = (h(k) + i) % m）
- 二次探測：按平方數跳躍（h(k,i) = (h(k) + i²) % m）
- 雙重雜湊：使用第二個雜湊函數（h(k,i) = (h1(k) + i*h2(k)) % m）
- 墓碑標記：刪除時標記為墓碑，避免中斷探測鏈
"""

from typing import Any, Optional, List, Tuple
from enum import Enum


class ProbingType(Enum):
    """探測策略類型。"""
    LINEAR = "linear"
    QUADRATIC = "quadratic"
    DOUBLE_HASH = "double_hash"


class HashTableOpenAddressing:
    """使用開放定址的雜湊表。"""
    def __init__(self, capacity: int = 8, probing_type: ProbingType = ProbingType.LINEAR,
                 load_factor_threshold: float = 0.7) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.probing_type: ProbingType = probing_type
        self.load_factor_threshold: float = load_factor_threshold
        self.table: List[Tuple[Any, Any, bool]] = [(None, None, False)] * capacity
        self.tombstone = (None, None, True)

    def _hash1(self, key: Any) -> int:
        """主雜湊函數。"""
        return hash(key) % self.capacity

    def _hash2(self, key: Any) -> int:
        """第二個雜湊函數（用於雙重雜湊）。"""
        return 1 + (hash(key) % (self.capacity - 1))

    def _probe(self, key: Any, i: int) -> int:
        """根據探測策略計算第i次探測的位置。"""
        if self.probing_type == ProbingType.LINEAR:
            return (self._hash1(key) + i) % self.capacity
        elif self.probing_type == ProbingType.QUADRATIC:
            return (self._hash1(key) + i * i) % self.capacity
        else:
            return (self._hash1(key) + i * self._hash2(key)) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        """插入或更新鍵值對。"""
        for i in range(self.capacity):
            index = self._probe(key, i)
            if self.table[index] == self.tombstone or self.table[index][0] is None:
                self.table[index] = (key, value, False)
                self.size += 1
                if self.size / self.capacity > self.load_factor_threshold:
                    self._resize()
                return
            elif self.table[index][0] == key:
                self.table[index] = (key, value, False)
                return
        raise OverflowError("雜湊表已滿")

    def get(self, key: Any) -> Optional[Any]:
        """獲取鍵對應的值，不存在返回None。"""
        for i in range(self.capacity):
            index = self._probe(key, i)
            if self.table[index][0] == key:
                return self.table[index][1]
            if self.table[index][0] is None and self.table[index] != self.tombstone:
                return None
        return None

    def delete(self, key: Any) -> bool:
        """刪除鍵值對，成功返回True（使用墓碑標記）。"""
        for i in range(self.capacity):
            index = self._probe(key, i)
            if self.table[index][0] == key:
                self.table[index] = self.tombstone
                self.size -= 1
                return True
            if self.table[index][0] is None and self.table[index] != self.tombstone:
                return False
        return False

    def _resize(self) -> None:
        """擴容並重新插入所有有效元素。"""
        old_table = self.table
        self.capacity *= 2
        self.table = [(None, None, False)] * self.capacity
        self.size = 0
        for item in old_table:
            if item[0] is not None and not item[2]:
                self.put(item[0], item[1])

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        items = []
        for i, (k, v, tomb) in enumerate(self.table):
            if k is not None and not tomb:
                items.append(f"位置{i}: {k} -> {v}")
        return "\n".join(items) if items else "空雜湊表"


if __name__ == "__main__":
    print("=== 開放定址雜湊表測試（線性探測） ===")
    ht = HashTableOpenAddressing(probing_type=ProbingType.LINEAR, capacity=4)
    ht.put("a", 1)
    ht.put("b", 2)
    ht.put("c", 3)
    print(f"雜湊表: {ht}")
    print(f"get('b'): {ht.get('b')}")
    ht.delete("b")
    print(f"刪除b後: {ht}")

    print("\n=== 比較不同探測策略 ===")
    for ptype in [ProbingType.LINEAR, ProbingType.QUADRATIC, ProbingType.DOUBLE_HASH]:
        ht = HashTableOpenAddressing(probing_type=ptype, capacity=8)
        for i in range(6):
            ht.put(f"key{i}", i)
        print(f"{ptype.value}: 大小={len(ht)}, 負載因子={ht.size/ht.capacity:.2f}")
