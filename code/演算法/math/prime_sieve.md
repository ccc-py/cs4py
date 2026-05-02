# 質數篩選演算法

## 歷史背景

### 埃拉托斯特尼篩法（Sieve of Eratosthenes）

埃拉托斯特尼（Eratosthenes of Cyrene，公元前 276–194 年）是古希臘的數學家、地理學家和天文學家，曾任亞歷山大圖書館館長。他最著名的成就之一是計算出地球的周長，誤差僅約 10%。

埃拉托斯特尼篩法是他提出的用於找出所有小於等於 n 的質數的演算法，距今已有超過 2200 年的歷史，至今仍是最常用的質數篩選方法之一。

### 現代發展

- **Sieve of Sundaram**（1934）：另一種質數篩選方法
- **Sieve of Atkin**（2003）：由 Atkin 和 Bernstein 提出，理論複雜度更低 O(n / log log n)
- **分段篩法（Segmented Sieve）**：解決大範圍篩選的記憶體問題

## 核心原理

### 埃拉托斯特尼篩法

**演算法步驟：**

1. 建立一個從 2 到 n 的列表，初始全部標記為「質數」
2. 從最小的質數 2 開始：
   - 將當前質數的所有倍數標記為「合數」
   - 移到下一個未被標記的數（即下一個質數）
3. 重複步驟 2，直到處理完所有 ≤ √n 的數
4. 剩餘未被標記的數即為質數

**優化：**

- 只需篩選到 √n，因為任何合數 n 必定有一個 ≤ √n 的質因數
- 從 p² 開始標記 p 的倍數（因為小於 p² 的倍數已被更小的質數標記過）

**視覺化範例（n=30）：**

```
初始: 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
篩2:  2  3  5  7  9  11 13 15 17 19 21 23 25 27 29
篩3:  2  3  5  7  11 13 17 19 23 25 29
篩5:  2  3  5  7  11 13 17 19 23 29
```

### 分段篩法（Segmented Sieve）

當 n 非常大時（如 10¹²），無法分配大小為 n+1 的陣列。分段篩法將範圍 [2, n] 分成多個小段，每次只處理一個段：

**步驟：**

1. 先使用普通篩法找出 √n 內的所有質數（基礎質數）
2. 將 [2, n] 分成大小為 segment_size 的段
3. 對每個段，使用基礎質數進行篩選

**優點：** 空間複雜度從 O(n) 降至 O(√n + segment_size)

### 質因數分解（SPF 方法）

預先計算每個數的最小質因數（Smallest Prime Factor, SPF）：

1. 使用篩法計算 spf[i]（i 的最小質因數）
2. 分解時，不斷除以 spf[n]，即可得到所有質因數

**時間複雜度：** 預計算 O(n log log n)，每次分解 O(log n)

## 時間與空間複雜度

### 埃拉托斯特尼篩法

| 操作 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 篩選質數 | O(n log log n) | O(n) |

### 分段篩法

| 操作 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 篩選質數 | O(n log log n) | O(√n + segment_size) |

### SPF 質因數分解

| 操作 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| 預計算 SPF | O(n log log n) | O(n) |
| 分解單個數 | O(log n) | O(1) |

## 使用範例

```python
from prime_sieve import sieve_of_eratosthenes, segmented_sieve, prime_factorization

# 埃拉托斯特尼篩法
primes = sieve_of_eratosthenes(50)
print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# 分段篩法
primes_seg = segmented_sieve(100, segment_size=20)
print(len(primes_seg))  # 25

# 質因數分解
factors = prime_factorization(360)
print(factors)  # {2: 3, 3: 2, 5: 1}
# 即 360 = 2³ × 3² × 5¹
```

## 應用場景

1. **密碼學**：RSA 需要大質數，質數篩選用於生成或驗證質數
2. **數論研究**：研究質數分佈、孿生質數等
3. **競賽程式設計**：快速預計算質數表或質因數
4. **哈希函數**：某些哈希函數使用質數作為參數

## 參考資料

1. Eratosthenes of Cyrene. (c. 240 BC). *Sieve of Eratosthenes*.
2. Crandall, R., & Pomerance, C. (2005). *Prime Numbers: A Computational Perspective* (2nd ed.). Springer.
3. Atkin, A. O. L., & Bernstein, D. J. (2004). *Prime sieves using binary quadratic forms*. Mathematics of Computation, 73(246), 1023-1030.
4. [Sieve of Eratosthenes - Wikipedia](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
5. [Segmented Sieve - GeeksforGeeks](https://www.geeksforgeeks.org/segmented-sieve/)
