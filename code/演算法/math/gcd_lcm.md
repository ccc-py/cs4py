# GCD（最大公因數）與 LCM（最小公倍數）

## 歷史背景

### 歐幾里得演算法（Euclidean Algorithm）

歐幾里得演算法是世界上最古老的演算法之一，出現在歐幾里得（Euclid）於約公元前 300 年撰寫的《幾何原本》（Elements）第七卷中。這個演算法基於一個簡單的原理：

> 若 a = bq + r，則 gcd(a, b) = gcd(b, r)

換句話說，兩個數的最大公因數等於其中較小數與兩數相除餘數的最大公因數。

歐幾里得演算法的高效性令人驚嘆：它的時間複雜度為 O(log min(a, b))，即使對於非常大的整數也能快速計算。

### 擴展歐幾里得演算法（Extended Euclidean Algorithm）

擴展歐幾里得演算法不僅計算最大公因數，還能找出整數 x 和 y，使得：

```
ax + by = gcd(a, b)
```

這個性質在數論和密碼學中有重要應用。

## 核心原理

### 歐幾里得演算法

**迭代版本：**
```python
while b != 0:
    a, b = b, a % b
return a
```

**數學基礎：**
- 假設 a = bq + r（其中 0 ≤ r < b）
- 如果 d 能同時整除 a 和 b，則 d 也能整除 r = a - bq
- 反之，如果 d 能同時整除 b 和 r，則 d 也能整除 a = bq + r
- 因此，gcd(a, b) = gcd(b, r)

### 擴展歐幾里得演算法

在計算 gcd 的同時，維護額外的資訊來找出係數 x 和 y。

**遞迴關係：**
```
gcd(a, b) = gcd(b, a mod b)
設: g, x1, y1 = extended_gcd(b, a mod b)
則: x = y1
    y = x1 - (a // b) * y1
```

### LCM 計算

最小公倍數可以透過 GCD 計算：

```
lcm(a, b) = |a × b| / gcd(a, b)
```

## 應用場景

### 1. 模反元素（Modular Inverse）

在模運算中，a 在模 m 下的反元素 x 滿足：

```
a × x ≡ 1 (mod m)
```

這等價於找出 x 使得 ax + my = 1，即 gcd(a, m) = 1 時的解。

**應用：** RSA 加密、橢圓曲線密碼學

### 2. 中國餘式定理（Chinese Remainder Theorem, CRT）

求解同餘方程組：

```
x ≡ a₁ (mod m₁)
x ≡ a₂ (mod m₂)
...
x ≡ aₙ (mod mₙ)
```

其中 m₁, m₂, ..., mₙ 兩兩互質。擴展歐幾里得演算法用於計算 CRT 中的係數。

### 3. 分數化簡

將分數 a/b 化簡為最簡分數：

```
分子 = a / gcd(a, b)
分母 = b / gcd(a, b)
```

## 使用範例

```python
from gcd_lcm import gcd, extended_gcd, lcm, mod_inverse

# GCD
print(gcd(48, 18))  # 6

# 擴展 GCD
g, x, y = extended_gcd(48, 18)
print(f"gcd={g}, x={x}, y={y}")  # gcd=6, x=-1, y=3
# 驗證: 48*(-1) + 18*3 = -48 + 54 = 6

# LCM
print(lcm(4, 6))  # 12

# 模反元素
inv = mod_inverse(3, 11)
print(inv)  # 4 (因為 3*4 = 12 ≡ 1 mod 11)
```

## 時間複雜度

| 操作 | 時間複雜度 | 空間複雜度 |
|------|-----------|-----------|
| GCD（迭代） | O(log min(a, b)) | O(1) |
| GCD（遞迴） | O(log min(a, b)) | O(log min(a, b)) |
| 擴展 GCD | O(log min(a, b)) | O(log min(a, b)) |
| LCM | O(log min(a, b)) | O(1) |

## 參考資料

1. Euclid. (c. 300 BC). *Elements* (7th Book).
2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 31)
3. Knuth, D. E. (1997). *The Art of Computer Programming, Vol. 2: Seminumerical Algorithms* (3rd ed.). Addison-Wesley.
4. [Euclidean algorithm - Wikipedia](https://en.wikipedia.org/wiki/Euclidean_algorithm)
5. [Extended Euclidean algorithm - Wikipedia](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)
