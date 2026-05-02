# RSA 公鑰加密 (RSA Public Key Cryptography)

## 歷史背景
RSA 算法由麻省理工學院（MIT）的羅納德·李維斯特（Ron Rivest）、阿迪·薩莫爾（Adi Shamir）和倫納德·阿德曼（Leonard Adleman）於1977年提出，是首個實用的公鑰加密系統。RSA 的安全性基於大整數分解問題的困難性。

1976年，惠特菲爾德·迪菲（Whitfield Diffie）和馬丁·赫爾曼（Martin Hellman）提出了公鑰密碼學的概念，但未能提出具體實現。RSA 是第一個可用的公鑰加密算法，徹底改變了密碼學領域。

## 核心原理
RSA 基於以下數學原理：
1. 選擇兩個大質數 p 和 q，計算 n = p × q
2. 計算歐拉函數 φ(n) = (p-1)(q-1)
3. 選擇公鑰指數 e，使得 gcd(e, φ(n)) = 1
4. 計算私鑰指數 d ≡ e⁻¹ (mod φ(n))
5. 公鑰：(e, n)，私鑰：(d, n)

加密：c ≡ mᵉ (mod n)
解密：m ≡ cᵈ (mod n)

根據歐拉定理，當 m 與 n 互質時，m^(ed) ≡ m (mod n)。

## 使用範例
```python
from rsa import generate_keypair, encrypt, decrypt

# 生成密鑰對
public_key, private_key = generate_keypair(1024)

# 加密
message = 123456789
ciphertext = encrypt(message, public_key)
print(f"密文: {ciphertext}")

# 解密
decrypted = decrypt(ciphertext, private_key)
print(f"解密: {decrypted}")
```

## 參考資料
- [RSA - Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- Rivest, R., Shamir, A., & Adleman, L. (1978). *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*
- [PKCS #1 Standard](https://www.rfc-editor.org/rfc/rfc8017)
