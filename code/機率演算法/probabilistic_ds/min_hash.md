# MinHash

## 歷史背景

MinHash（Minimum Hash）由 Andrei Broder 在 1997 年的論文《On the resemblance and containment of documents》中提出，最初用於檢測網頁之間的相似度（避免搜尋引擎索引重複內容）。

MinHash 是局部敏感雜湊（Locality-Sensitive Hashing, LSH）的一個經典範例，屬於「相似性搜尋」領域的重要技術。

## 核心原理

### Jaccard 相似度

兩個集合 A 和 B 的 Jaccard 相似度定義為：

$$
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$

### MinHash 原理

對於一個雜湊函數 h，MinHash 的定義為：

$$
\text{minhash}(S) = \min_{x \in S} h(x)
$$

**關鍵性質**：對於兩個集合 A 和 B，

$$
P(\text{minhash}(A) = \text{minhash}(B)) = J(A, B)
$$

即兩個集合的 MinHash 值相同的概率等於它們的 Jaccard 相似度。

### 演算法步驟

1. **選擇 k 個不同的雜湊函數** h₁, h₂, ..., hₖ
2. **計算簽章**: 對於集合 S，計算簽章 σ(S) = [min(h₁(S)), min(h₂(S)), ..., min(hₖ(S))]
3. **估計相似度**: 對於兩個簽章，計算相同位置的比例

### 誤差分析

使用 k 個雜湊函數，估計的標準誤差約為：

$$
\text{SE} \approx \sqrt{\frac{J(A, B)(1 - J(A, B))}{k}}
$$

## 使用範例

```python
from probabilistic_ds.min_hash import MinHash

# 建立 MinHash
mh = MinHash(num_hashes=128, seed=42)

# 兩個集合
set1 = {"apple", "banana", "cherry"}
set2 = {"banana", "cherry", "date"}

# 估計 Jaccard 相似度
similarity = mh.jaccard_similarity(set1, set2)
print(f"估計 Jaccard: {similarity:.4f}")

# 精確值比較
exact = len(set1 & set2) / len(set1 | set2)
print(f"精確 Jaccard: {exact:.4f}")
```

## MinHash LSH

結合局部敏感雜湊，可以高效地找到相似集合：

```python
from probabilistic_ds.min_hash import MinHashLSH

# 建立 LSH 索引
lsh = MinHashLSH(num_hashes=128, num_bands=32)

# 加入文件
lsh.add(0, {"apple", "banana"})
lsh.add(1, {"banana", "cherry"})

# 查詢相似文檔
candidates = lsh.query({"apple", "banana"})
```

## 與其他方法的比較

| 方法 | 時間複雜度 | 空間複雜度 | 精確度 |
|------|-----------|-----------|--------|
| 精確 Jaccard | O(n + m) | O(n + m) | 100% |
| MinHash | O(k) | O(k) | 有誤差 |
| SimHash | O(n) | O(1) | 有誤差 |
| LSH + MinHash | O(k/b) 查詢 | O(nk) | 有誤差 |

## 參考資料

1. Broder, A. Z. (1997). On the resemblance and containment of documents. *Compression and Complexity of Sequences*, 21-29.
2. Broder, A. Z., Charikar, M., Frieze, A. M., & Mitzenmacher, M. (2000). Min-wise independent permutations. *Journal of Computer and System Sciences*, 60(3), 630-659.
3. Leskovec, J., Rajaraman, A., & Ullman, J. D. (2020). *Mining of Massive Datasets* (3rd ed.). Cambridge University Press. Chapter 3.
