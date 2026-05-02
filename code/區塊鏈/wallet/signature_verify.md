# ECDSA 簽章驗證（簡化版）

## 歷史背景

ECDSA（Elliptic Curve Digital Signature Algorithm）於 1992 年由 Scott Vanstone 提出，結合橢圓曲線密碼學（ECC）與數位簽章演算法。比特幣和以太坊都採用 ECDSA 配合 secp256k1 曲線來簽署交易，確保只有私鑰持有者能花費其資金。

## 核心原理

### 橢圓曲線密碼學
- 基於橢圓曲線離散對數問題的困難性
- 私鑰是隨機數，公鑰是橢圓曲線上的點（私鑰 × 生成點）
- secp256k1 是比特幣專用的曲線（y² = x³ + 7 mod p）

### ECDSA 簽章流程
1. 選擇隨機數 k，計算 R = k × G
2. 取 r = R.x mod n
3. 計算 s = k⁻¹ × (hash + r × private_key) mod n
4. 簽章為 (r, s)

### 驗證流程
1. 計算 w = s⁻¹ mod n
2. 計算 u1 = hash × w mod n, u2 = r × w mod n
3. 計算 P = u1 × G + u2 × public_key
4. 驗證 r == P.x mod n

## 使用範例

```python
from signature_verify import SimpleECDSA, TransactionSigner

# 生成金鑰對
ecdsa = SimpleECDSA()
keypair = ecdsa.generate_keypair()

# 簽署交易
signer = TransactionSigner()
message = "Alice sends 10 BTC to Bob"
signature = signer.sign_transaction(keypair.private_key, message)

# 驗證
is_valid = signer.verify_transaction(keypair.public_key, message, signature)
print(f"驗證結果: {is_valid}")
```

## 參考資料

- [ECDSA - Wikipedia](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
- [secp256k1](https://en.bitcoin.it/wiki/Secp256k1)
- [Bitcoin Developer Guide - Transactions](https://bitcoin.org/en/developer-guide#transactions)
