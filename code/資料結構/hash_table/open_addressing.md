# 開放定址雜湊表（Hash Table with Open Addressing）

## 歷史背景
開放定址法由計算機科學家在20世紀50年代提出，與分離鏈結不同，它不使用額外的鏈結結構，而是當發生衝突時，按照某種探測策略在雜湊表中尋找下一個可用位置。

## 核心概念與原理
### 探測策略
1. **線性探測**：依次檢查下一個位置，`h(k,i) = (h(k) + i) % m`
   - 優點：實作簡單，快取友好
   - 缺點：容易產生群集（clustering）效應
2. **二次探測**：按平方數跳躍，`h(k,i) = (h(k) + i²) % m`
   - 優點：減少群集效應
   - 缺點：可能無法探測到所有位置
3. **雙重雜湊**：使用第二個雜湊函數，`h(k,i) = (h1(k) + i*h2(k)) % m`
   - 優點：探測序列更均勻，效能最佳
   - 缺點：需要設計兩個雜湊函數

### 墓碑標記
刪除元素時，不能直接置為空（會中斷探測鏈），而是標記為墓碑（tombstone），探測時可跳過墓碑但插入時可覆蓋。

## 使用範例
```python
from open_addressing import HashTableOpenAddressing, ProbingType

ht = HashTableOpenAddressing(probing_type=ProbingType.DOUBLE_HASH)
ht.put("key", "value")
print(ht.get("key"))
```

## 參考資料
- [Wikipedia: Open Addressing](https://en.wikipedia.org/wiki/Open_addressing)
- [GeeksforGeeks: Open Addressing](https://www.geeksforgeeks.org/hashing-set-3-open-addressing/)
