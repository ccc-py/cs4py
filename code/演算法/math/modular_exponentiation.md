# 模冪運算 (Modular Exponentiation)

## 歷史背景

模冪運算是數論和密碼學中的基礎運算，用於計算 (base^exponent) mod modulus。

### 應用領域

- **RSA 加密**：需要計算大數的模冪
- **Diffie-Hellman 金鑰交換**：離散對數問題的基礎
- **數位簽章**：DSA、ECDSA 等演算法
- **質數測試**：Miller-Rabin 等演算法

## 演算法原理

### 暴力法問題

直接計算 `base^exponent` 再取模會有問題：
- 當 exponent 很大時（如 2^1000），中間結果會超出電腦表示範圍
- 計算時間過長

### Square-and-Multiply（平方乘）

利用指數的二進位表示，將時間複雜度降到 O(log exponent)。

```
原理：
假設 exponent 的二進位為 b_k b_{k-1} ... b_0

base^exponent = Π (base^(2^i))^b_i

例如：計算 3^13 mod 7
13 的二進位：1101 (8 + 4 + 0 + 1)

步驟：
result = 1, base = 3
13 是奇數：result = 1 * 3 = 3, base = 3² = 9 ≡ 2 (mod 7), exp = 6
6 是偶數：result = 3, base = 2² = 4, exp = 3
3 是奇數：result = 3 * 4 = 12 ≡ 5, base = 4² = 16 ≡ 2, exp = 1
1 是奇數：result = 5 * 2 = 10 ≡ 3, base = 2² = 4, exp = 0

結果：3^13 ≡ 3 (mod 7)
```

**時間複雜度**：O(log exponent)
**空間複雜度**：O(1)（迭代版）

## 程式碼說明

### 迭代版核心

```python
def modular_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    exp = exponent

    while exp > 0:
        if exp & 1:  # 奇數
            result = (result * base) % modulus
        base = (base * base) % modulus
        exp >>= 1  # 除以 2

    return result
```

### 遞迴版核心

```python
def modular_pow_rec(base, exp, mod):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        temp = modular_pow_rec(base, exp // 2, mod)
        return (temp * temp) % mod
    else:
        temp = modular_pow_rec(base, (exp - 1) // 2, mod)
        return (base * temp * temp) % mod
```

## 費馬小定理

```
若 p 是質數，a 是任意整數且 gcd(a, p) = 1，
則 a^(p-1) ≡ 1 (mod p)
```

這可以用來進行質數測試，但注意：
- 通過測試的不一定是質數（ Carmichael 數）
- 這只是必要條件，不是充分條件

## 應用場景

### 1. RSA 加密

```
加密：ciphertext = plaintext^e mod n
解密：plaintext = ciphertext^d mod n
```

### 2. Diffie-Hellman 金鑰交換

```
Alice: A = g^a mod p
Bob: B = g^b mod p
共享金鑰: B^a = A^b = g^(ab) mod p
```

### 3. 質數測試

在 Miller-Rabin 等演算法中，需要計算大數的模冪。

## 與 Python 內建 pow 比較

Python 的內建 `pow(base, exp, mod)` 已經實現了高效的模冪運算：

```python
# 三者等價
pow(3, 13, 7)  # 內建，最快
modular_pow_iterative(3, 13, 7)  # 我們的實現
(3 ** 13) % 7  # 不建議，中間結果可能很大
```

## 參考資料

- Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3rd ed.). Addison-Wesley.
- Rivest, R. L., Shamir, A., & Adleman, L. (1978). *A method for obtaining digital signatures and public-key cryptosystems*. Communications of the ACM, 21(2), 120-126.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. (Chapter 31.6)
