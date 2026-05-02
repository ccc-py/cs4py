# ElGamal 加密 (ElGamal Encryption)

## 歷史背景
ElGamal 加密由埃及裔美國密碼學家塔希爾·蓋拉爾（Taher ElGamal）於1985年提出，發表於《密碼學新方向》（A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms）論文中。

ElGamal 是許多現代密碼系統的基礎，包括 GNU Privacy Guard（GPG）使用的加密標準，以及數位簽章算法（DSA）的基礎。

## 核心原理
ElGamal 基於 Diffie-Hellman 協議，提供隨機化加密：

1. **密鑰生成**：
   - 選擇大質數 p 和原根 g
   - 選擇私鑰 x，計算公鑰 h = gˣ mod p
   - 公鑰：(p, g, h)，私鑰：x

2. **加密**（引入隨機數 k）：
   - c1 = gᵏ mod p
   - c2 = m × hᵏ mod p
   - 密文：(c1, c2)

3. **解密**：
   - 計算 s = c1ˣ mod p
   - 計算 s⁻¹ mod p
   - m = c2 × s⁻¹ mod p

由於每次加密使用不同的 k，同一明文會產生不同的密文，這是語義安全的重要特性。

## 使用範例
```python
from elgamal import generate_keypair, encrypt, decrypt

# 生成密鑰對
public_key, private_key = generate_keypair(2048)

# 加密
message = 123456
ciphertext = encrypt(message, public_key)
print(f"密文: {ciphertext}")

# 解密
decrypted = decrypt(ciphertext, private_key, public_key[0])
print(f"解密: {decrypted}")
```

## 參考資料
- [ElGamal Encryption - Wikipedia](https://en.wikipedia.org/wiki/ElGamal_encryption)
- ElGamal, T. (1985). *A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms*
- [RFC 6979 - Deterministic DSA](https://www.rfc-editor.org/rfc/rfc6979)
