# 分離鏈結雜湊表（Hash Table with Separate Chaining）

## 歷史背景
分離鏈結是解決雜湊衝突的最早方法之一，由計算機科學家在20世紀50年代提出。當多個鍵通過雜湊函數映射到同一個索引時，將這些鍵值對儲存在該索引的鏈結串列中，從而解決衝突問題。

## 核心概念與原理
### 雜湊表基礎
- **雜湊函數**：將任意大小的鍵映射到固定大小的索引（如陣列下標）
- **衝突**：不同鍵映射到相同索引的情況
- **分離鏈結**：每個雜湊桶（bucket）是一個鏈結串列，衝突的鍵值對追加到串列中

### 操作時間複雜度
- 平均情況：O(1)（假設雜湊函數分佈均勻）
- 最壞情況：O(n)（所有鍵衝突到同一個桶）

### 負載因子與重整
- 負載因子 = 元素數量 / 桶數量
- 當負載因子超過閾值（通常0.7~0.75）時，擴容並重新雜湊所有元素

## 使用範例
```python
from chaining import HashTableChaining

ht = HashTableChaining()
ht.put("key1", "value1")
print(ht.get("key1"))
```

## 參考資料
- [Wikipedia: Hash Table](https://en.wikipedia.org/wiki/Hash_table)
- [GeeksforGeeks: Separate Chaining](https://www.geeksforgeeks.org/hashing-set-2-separate-chaining/)
