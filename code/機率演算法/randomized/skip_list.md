# 跳躍表 (Skip List)

## 歷史背景

跳躍表由 William Pugh 在 1989 年發表於論文《Skip Lists: A Probabilistic Alternative to Balanced Trees》。Pugh 的動機是提供一個比平衡樹（如紅黑樹、AVL 樹）更簡單，但同樣高效的資料結構。

跳躍表在 Redis 等多個系統中都有應用，因為它的實作簡單且效能可預測。

## 核心原理

### 資料結構

跳躍表是多層鏈結串列的變體：

- **第 0 層**: 包含所有的元素（類似普通有序鏈表）
- **第 1 層**: 約一半的元素
- **第 2 層**: 約四分之一的元素
- ...

### 隨機化層數

每個節點的層數由隨機決定：

```
level = 0
while random() < p and level < max_level:
    level += 1
```

通常使用 p = 0.5，這確保了各層的分佈類似於二分搜尋樹的結構。

### 時間複雜度

- **搜尋**: O(log n) 期望值
- **插入**: O(log n) 期望值
- **刪除**: O(log n) 期望值

### 搜尋過程

1. 從最高層的 header 開始
2. 向右移動，直到下一個節點的鍵值大於等於目標鍵
3. 向下移動一層
4. 重複步驟 2-3，直到到達第 0 層

## 使用範例

```python
from randomized.skip_list import SkipList

# 建立跳躍表
sl = SkipList()

# 插入元素
sl.insert(3, "C")
sl.insert(1, "A")
sl.insert(2, "B")

# 搜尋
print(sl.search(2))  # 輸出: B

# dict 風格
sl[4] = "D"
print(sl[4])  # 輸出: D

# 檢查存在
print(2 in sl)  # 輸出: True

# 遍歷
for key, value in sl.items():
    print(f"{key}: {value}")
```

## 與其他資料結構比較

| 資料結構 | 搜尋 | 插入 | 刪除 | 實作難度 |
|---------|------|------|------|---------|
| 有序陣列 | O(log n) | O(n) | O(n) | 簡單 |
| 平衡樹 | O(log n) | O(log n) | O(log n) | 困難 |
| 跳躍表 | O(log n) | O(log n) | O(log n) | 中等 |
| 雜湊表 | O(1) | O(1) | O(1) | 簡單 |

## 參考資料

1. Pugh, W. (1989). Skip lists: a probabilistic alternative to balanced trees. *Communications of the ACM*, 33(6), 668-676.
2. Redis. (2023). *Redis Internals - Skip Lists*. https://redis.io/docs/reference/internals/
3. Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley. Chapter 3.4.
