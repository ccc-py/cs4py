# 數位簽章 (Digital Signature)

## 歷史背景
數位簽章的概念由惠特菲爾德·迪菲（Whitfield Diffie）和馬丁·赫爾曼（Martin Hellman）於1976年首次提出。第一個實用的數位簽章算法是 RSA 簽章，由 Rivest、Shamir 和 Adleman 於1977年提出。

數位簽章提供三個重要的安全保證：
1. **認證（Authentication）**：確認簽署者身份
2. **完整性（Integrity）**：確認訊息未被竄改
3. **不可否認性（Non-repudiation）**：簽署者不能否認簽署行為

## 核心原理
數位簽章結合雜湊函數和非對稱加密：

1. **簽署過程**：
   - 計算訊息的雜湊值：h = hash(message)
   - 使用私鑰加密雜湊值：signature = hᵈ mod n
   - 發送訊息和簽章

2. **驗證過程**：
   - 使用公鑰解密簽章：h' = signatureᵉ mod n
   - 重新計算訊息雜湊：h = hash(message)
   - 比較 h' 和 h 是否相等

## 使用範例
```python
from digital_signature import generate_keys, sign, verify

# 生成密鑰對
public_key, private_key = generate_keys(2048)

# 簽署訊息
message = "重要合約內容"
signature = sign(message, private_key)

# 驗證簽章
is_valid = verify(message, signature, public_key)
print(f"簽章有效: {is_valid}")

# 竄改檢測
tampered = "被竄改的合約"
is_valid_tampered = verify(tampered, signature, public_key)
print(f"竄改後驗證: {is_valid_tampered}")
```

## 參考資料
- [Digital Signature - Wikipedia](https://en.wikipedia.org/wiki/Digital_signature)
- Diffie, W., & Hellman, M. (1976). *New Directions in Cryptography*
- Rivest, R., Shamir, A., & Adleman, L. (1978). *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*
- [FIPS 186-4 - Digital Signature Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)
