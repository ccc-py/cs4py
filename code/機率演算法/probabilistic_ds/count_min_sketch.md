# Count-Min Sketch

## 歷史背景

Count-Min Sketch 由 Graham Cormode 和 S. Muthukrishnan 在 2005 年的論文《An Improved Data Stream Summary: The Count-Min Sketch and its Applications》中提出。

這個資料結構專門用於資料流（data stream）場景，其中：
- 資料量太大，無法全部儲存
- 只能進行一次掃描
- 需要即時查詢元素的頻率

應用場景包括：
- 網路流量監控
- 資料庫查詢最佳化
- 自然語言處理中的 n-gram 頻率估計

## 核心原理

### 資料結構

Count-Min Sketch 是一個 d × w 的計數表，其中：
- d (depth): 雜湊函數的數量
- w (width): 每個雜湊表的寬度

### 操作

**加入元素**:
1. 對每個雜湊函數 i (0 ≤ i < d)，計算 h_i(x)
2. 將表中第 i 行、第 h_i(x) 列的值加 1

**查詢頻率**:
1. 對每個雜湊函數 i，計算 h_i(x)
2. 返回所有 table[i][h_i(x)] 中的最小值

### 誤差保證

對於任何元素 x：

$$
\hat{f}[x] \geq f[x]
$$

且以機率 1 - δ：

$$
\hat{f}[x] \leq f[x] + \epsilon \cdot N
$$

其中 N 是流中元素總數。

### 參數選擇

建議參數：
- w = ⌈e/ε⌉ ≈ 2.718/ε
- d = ⌈ln(1/δ)⌉

| ε (誤差) | δ (失敗機率) | w | d |
|---------|-----------|---|---|
| 0.01 | 0.01 | 272 | 5 |
| 0.001 | 0.001 | 2718 | 7 |

## 使用範例

```python
from probabilistic_ds.count_min_sketch import CountMinSketch

# 建立 Count-Min Sketch
cms = CountMinSketch(epsilon=0.01, delta=0.01)

# 加入元素
cms.add("apple", 5)
cms.add("banana", 3)

# 查詢頻率
print(cms.estimate("apple"))  # 至少 5
print(cms.estimate("grape"))  # 0 或很小的值
```

## 與其他方法的比較

| 方法 | 空間 | 支援更新 | 誤差保證 |
|------|------|---------|---------|
| 精確計數 (dict) | O(n) | 是 | 無誤差 |
| Bloom Filter | O(n) | 否 | 只支援存在性 |
| Count-Min Sketch | O(1/ε · log(1/δ)) | 是 | 有界誤差 |
| Count Sketch | O(1/ε² · log n) | 是 | 有界誤差 |

## 參考資料

1. Cormode, G., & Muthukrishnan, S. (2005). An improved data stream summary: the count-min sketch and its applications. *Journal of Algorithms*, 55(1), 58-75.
2. Cormode, G. (2014). Misra-Gries, Space-Saving, and Frequent Sketch. *Encyclopedia of Algorithms*, 1-6.
3. Muthukrishnan, S. (2005). *Data Streams: Algorithms and Applications*. Now Publishers Inc.
