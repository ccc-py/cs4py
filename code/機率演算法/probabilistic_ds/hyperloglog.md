# HyperLogLog 演算法

## 歷史背景

HyperLogLog 由 Philippe Flajolet、Éric Fusy、Olivier Gandouet 和 Frédéric Meunier 在 2007 年提出。它是 LogLog 演算法的改進版本，進一步降低了估計的變異數。

這個演算法在需要估計大數據流中不重複元素數量（基數估計）的場景中極其重要，例如：
- Redis 的 PFCOUNT 命令
- 網頁瀏覽量的去重統計
- 大規模數據流的基數估計

## 核心原理

### 觀察

對於均勻雜湊函數，觀察雜湊值的前導零數量：
- 前導零越多，表示遇到的隨機數越大
- 如果觀察到最多 k 個前導零，估計基數約為 2^k

### 演算法步驟

1. **雜湊**: 將每個元素通過雜湊函數映射到 64 位元整數
2. **分桶**: 取前 p 位作為寄存器索引（產生 m = 2^p 個桶）
3. **前導零**: 對剩餘位元計算前導零數量 ρ
4. **更新**: 每個桶保留最大的 ρ 值
5. **估計**: 使用調和平均計算基數估計

### 估計公式

$$
\hat{n} = \alpha_m \cdot m^2 \cdot \left( \sum_{j=1}^{m} 2^{-M[j]} \right)^{-1}
$$

其中 $\alpha_m$ 是與 m 相關的常數，用於減少偏差。

### 誤差分析

標準誤差約為：

$$
\text{error} \approx \frac{1.04}{\sqrt{m}} = \frac{1.04}{\sqrt{2^p}}
$$

| p | m (桶數) | 誤差 |
|---|---------|------|
| 10 | 1024 | ~3.25% |
| 14 | 16384 | ~0.81% |
| 16 | 65536 | ~0.41% |

## 使用範例

```python
from probabilistic_ds.hyperloglog import HyperLogLog

# 建立 HyperLogLog，精度參數 p=14
hll = HyperLogLog(precision=14)

# 加入元素
for i in range(10000):
    hll.add(f"user_{i}")

# 估計不重複元素數量
count = hll.count()
print(f"估計基數: {count}")

# 合併兩個 HyperLogLog
hll2 = HyperLogLog(precision=14)
hll2.add("new_user")
hll.merge(hll2)
```

## 與其他方法的比較

| 方法 | 空間複雜度 | 誤差 | 支援合併 |
|------|-----------|------|---------|
| 精確集合 (set) | O(n) | 0% | 是 |
| Linear Counting | O(n) | 低 | 否 |
| LogLog | O(log log n) | ~1.30/√m | 是 |
| HyperLogLog | O(log log n) | ~1.04/√m | 是 |

## 參考資料

1. Flajolet, P., Fusy, É., Gandouet, O., & Meunier, F. (2007). HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm. *DMTCS Proceedings*, 1-10.
2. Flajolet, P., & Martin, G. N. (1985). Probabilistic counting algorithms for data base applications. *Journal of Computer and System Sciences*, 31(2), 182-209.
3. Heule, S., Nunkesser, M., & Hall, A. (2013). HyperLogLog in practice: Algorithmic engineering of a state-of-the-art cardinality estimation algorithm. *Proceedings of the 16th International Conference on Extending Database Technology*, 683-692.
