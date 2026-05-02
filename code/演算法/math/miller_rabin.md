# Miller-Rabin 質數測試 (Miller-Rabin Primality Test)

## 歷史背景

Miller-Rabin 是實務上最重要的質數測試演算法之一。

### 發展歷程

- **1976 年**：Gary L. Miller 提出了基於廣義黎曼猜想（GRH）的確定性演算法
- **1980 年**：Michael O. Rabin 將其改進為概率性演算法，不依賴未證明的猜想
- **現代**：已成為密碼學中標準的質數測試方法

## 演算法原理

### 數學基礎

```
費馬小定理：若 p 是質數，則對於任意 a 使 gcd(a, p) = 1，
有 a^(p-1) ≡ 1 (mod p)

Miller-Rabin 加強了這個測試：
將 n-1 寫為 d * 2^s，其中 d 是奇數
對於質數 n，對於任意 a，以下至少一個成立：
1. a^d ≡ 1 (mod n)
2. 存在 0 ≤ r < s 使得 a^(d*2^r) ≡ -1 (mod n)
```

### 演算法步驟

```
輸入：奇數 n > 2，基底 a
1. 將 n-1 寫為 d * 2^s（d 是奇數）
2. 計算 x = a^d mod n
3. 如果 x == 1 或 x == n-1，則通過測試
4. 重複 s-1 次：
   x = x² mod n
   如果 x == n-1，通過測試
   如果 x == 1，失敗
5. 如果到這裡還沒通過，則 n 是合數
```

**時間複雜度**：O(k * log³ n)，k 是測試輪數
**空間複雜度**：O(1)

## Witness 與合數檢測

- **Witness（見證人）**：如果基底 a 能證明 n 是合數，則 a 稱為 n 的 witness
- **Strong Liar**：如果 n 是合數，但 a 誤判 n 為質數，則 a 稱為 strong liar

```
對於合數 n，最多有 1/4 的 a 是 strong liar
因此，k 輪測試都通過的錯誤機率 ≤ (1/4)^k
```

## 確定性版本（64 位元）

對於 n < 2^64，使用以下基底可以達到確定性：

```
基底集合：{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}
```

這意味著在 64 位元整數範圍內，Miller-Rabin 可以作為確定性測試。

## 程式碼說明

### 核心測試函數

```python
def miller_rabin_test(n, a):
    # 將 n-1 寫為 d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    x = modular_pow(a, d, n)
    if x == 1 or x == n - 1:
        return True

    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
        if x == 1:
            return False

    return False
```

### 確定性測試

```python
def is_prime_deterministic_64bit(n):
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n:
            break
        if not miller_rabin_test(n, a):
            return False
    return True
```

## 應用場景

### 1. RSA 金鑰生成

生成大質數 p 和 q（通常 1024-4096 位元）。

### 2. 密碼學協定

Diffie-Hellman、DSA 等都需要質數測試。

### 3. 數學研究

尋找大質數（如梅森質數）。

## 與其他質數測試比較

| 演算法 | 類型 | 時間複雜度 | 適用場景 |
|--------|------|-----------|---------|
| 試除法 | 確定性 | O(√n) | 小整數 |
| Fermat | 概率性 | O(log³ n) | 不推薦（有 Carmichael 數） |
| Miller-Rabin | 概率性 | O(k log³ n) | 實務標準 |
| AKS | 確定性 | O(log⁶ n) | 理論重要，實務慢 |

## 參考資料

- Miller, G. L. (1976). *Riemann's Hypothesis and tests for primality*. Journal of Computer and System Sciences, 13(3), 300-317.
- Rabin, M. O. (1980). *Probabilistic algorithm for testing primality*. Journal of Number Theory, 12(1), 128-138.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 31.8)
