# 布隆過濾器 (Bloom Filter)

## 歷史背景

布隆過濾器由 Burton Howard Bloom 在 1970 年的論文《Space/Time Trade-offs in Hash Coding with Allowable Errors》中提出。這是一種空間效率極高的機率型資料結構。

主要應用場景包括：
- 資料庫系統（如 Cassandra、Bigtable）的記憶體查詢
- 網頁爬蟲的 URL 去重
- 密碼強度檢查（查詢常見弱密碼）
- 比特幣節點的快速交易驗證

## 核心原理

### 資料結構

布隆過濾器由兩部分組成：
1. **位元陣列 (Bit Array)**: 長度為 m 的二進位陣列
2. **k 個獨立的雜湊函數**: 每個函數將元素映射到 [0, m-1] 範圍

### 操作

**加入元素**:
1. 使用 k 個雜湊函數計算 k 個索引
2. 將位元陣列中對應的位置設為 1

**查詢元素**:
1. 使用相同的 k 個雜湊函數計算索引
2. 如果所有對應位元都是 1，返回 True（可能在）；否則返回 False（一定不在）

### 假陽性率

假陽性率 (False Positive Rate) 公式：

$$
p \approx \left(1 - e^{-kn/m}\right)^k
$$

其中：
- m: 位元陣列大小
- n: 已插入元素數量
- k: 雜湊函數數量

最優的 k 值為：

$$
k = \frac{m}{n} \ln 2
$$

### 特性

| 特性 | 說明 |
|------|------|
| 假陽性 (False Positive) | 可能發生 |
| 假陰性 (False Negative) | 不可能發生 |
| 刪除元素 | 不支援（除非使用計數布隆過濾器） |
| 空間複雜度 | O(m) |
| 時間複雜度 | O(k) |

## 使用範例

```python
from probabilistic_ds.bloom_filter import BloomFilter

# 建立布隆過濾器，預期儲存 1000 個元素，假陽性率 1%
bf = BloomFilter(capacity=1000, false_positive_rate=0.01)

# 加入元素
bf.add("apple")
bf.add("banana")

# 查詢
print("apple" in bf)    # True (可能在)
print("grape" in bf)    # False (一定不在)
```

## 參數選擇

| 假陽性率 | m/n (位元數/元素數) | k (雜湊函數數) |
|---------|-------------------|---------------|
| 1%      | ~9.6              | 7             |
| 0.1%    | ~14.4             | 10            |
| 0.01%   | ~19.2             | 14            |

## 參考資料

1. Bloom, B. H. (1970). Space/time trade-offs in hash coding with allowable errors. *Communications of the ACM*, 13(7), 422-426.
2. Broder, A., & Mitzenmacher, M. (2004). Network applications of Bloom filters: A survey. *Internet Mathematics*, 1(4), 485-509.
3. Tarkoma, S., Rothenberg, C. E., & Lagerspetz, E. (2012). Theory and practice of Bloom filters for distributed systems. *IEEE Communications Surveys & Tutorials*, 14(1), 131-155.
