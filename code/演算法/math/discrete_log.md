# 離散對數問題 (Discrete Logarithm Problem)

## 歷史背景

離散對數問題是公鑰密碼學的基礎之一。1976 年，Diffie 和 Hellman 在他們的開創性論文《New Directions in Cryptography》中首次提出了基於離散對數的密鑰交換協議，標誌著公鑰密碼學的誕生。

離散對數問題的困難性是許多密碼系統安全性的基礎，包括 Diffie-Hellman 密鑰交換、ElGamal 加密、DSA 數位簽章等。

## 核心原理

### 問題定義

給定一個循環群 G（通常為乘法群 Z_p^*），生成元 g，和群中的一個元素 h，找到整數 x 使得：

```
g^x ≡ h (mod p)
```

這個 x 稱為 h 以 g 為底的離散對數，記作 x = log_g(h)。

### Baby-step Giant-step 演算法

由 Daniel Shanks 提出，是對窮舉法（O(n)）的改進。

**演算法步驟**：
1. 計算 m = ⌈√n⌉，其中 n 是群的階
2. **Baby steps**：計算並存儲 g^j mod p 對於 j = 0, 1, ..., m-1
3. **Giant steps**：計算 h·(g^(-m))^i 對於 i = 0, 1, ..., m，檢查是否在 Baby steps 中

**時間複雜度**：O(√n)
**空間複雜度**：O(√n)

### Pohlig-Hellman 演算法

當群的階（p-1）是合數時，可以將問題分解：

1. 對 p-1 進行質因子分解：p-1 = q₁^e₁ × q₂^e₂ × ... × q_k^e_k
2. 在每個質因子冪次的子群中求解離散對數
3. 使用中国餘式定理組合結果

如果 p-1 有小的質因子，這個演算法非常有效。

## 時間複雜度比較

| 方法 | 時間複雜度 | 空間複雜度 | 適用場景 |
|------|-----------|-----------|----------|
| 窮舉法 | O(n) | O(1) | 很小的群 |
| Baby-step Giant-step | O(√n) | O(√n) | 中等大小的群 |
| Pohlig-Hellman | O(Σ e_i × √q_i) | O(√max(q_i)) | p-1 有小的質因子 |
| Index Calculus | L_p[1/3, c] | - | 非常大的質數（最先進） |

## 使用範例

```python
from discrete_log import baby_step_giant_step, pohlig_hellman

# Baby-step Giant-step
g, h, p = 2, 9, 11
x = baby_step_giant_step(g, h, p)
print(f"解: x = {x}")  # x = 6 (因為 2^6 = 64 ≡ 9 mod 11)

# Pohlig-Hellman
p = 101  # p-1 = 100 = 2^2 * 5^2
g = 2
h = 57
factors = {2: 2, 5: 2}  # p-1 的質因子分解
x = pohlig_hellman(g, h, p, factors)
print(f"解: x = {x}")
```

## 密碼學應用

- **Diffie-Hellman 密鑰交換**：基於離散對數的困難性
- **ElGamal 加密**：使用離散對數的公鑰加密
- **DSA 數位簽章**：基於離散對數的簽章算法

## 安全性注意

- 為了抵抗 BSGS 攻擊，質數 p 應該足夠大（至少 2048 位）
- 為了抵抗 Pohlig-Hellman 攻擊，p-1 應該有一個大的質因子
- 實際應用中應使用橢圓曲群上的離散對數問題（ECDLP）

## 參考資料

1. [Discrete Logarithm - Wikipedia](https://en.wikipedia.org/wiki/Discrete_logarithm)
2. Shanks, D. (1971). "Class number, a theory of factorization, and genera". *Proceedings of Symposia in Pure Mathematics*, 20, 415-440.
3. Pohlig, S., & Hellman, M. (1978). "An improved algorithm for computing logarithms over GF(p) and its cryptographic significance". *IEEE Transactions on Information Theory*, 24(1), 106-110.
4. Diffie, W., & Hellman, M. (1976). "New directions in cryptography". *IEEE Transactions on Information Theory*, 22(6), 644-654.
