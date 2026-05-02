# 區塊鏈錢包地址生成

## 歷史背景

比特幣地址生成方法由中本聰在比特幣白皮書中定義。錢包地址實質上是公鑰的雜湊值經過編碼後的表示，類似銀行帳號，用於接收加密貨幣。Base58 編碼由比特幣採用，去除了易混淆字元（0, O, I, l）。

## 核心原理

### 地址生成流程
1. **生成私鑰**：256 位隨機數（橢圓曲線的私鑰）
2. **推導公鑰**：透過橢圓曲線乘法（secp256k1）從私鑰計算公鑰
3. **公鑰雜湊**：SHA-256 → RIPEMD-160
4. **加入版本**：前面加上版本字節（主網為 0x00）
5. **計算校驗和**：雙重 SHA-256 的前 4 字節
6. **Base58 編碼**：將版本+雜湊+校驗和編碼為可讀字串

### Base58 編碼
Base58 是 Base64 的變體，去除了：
- 數字 0、字母 O（避免混淆）
- 字母 I、l（避免混淆）
剩下 58 個字元：123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz

## 使用範例

```python
from address import WalletAddress

# 建立錢包生成器
wallet = WalletAddress()

# 生成錢包
private_key, public_key, address = wallet.generate_wallet()

print(f"私鑰: {hex(private_key)}")
print(f"公鑰: {hex(public_key)}")
print(f"地址: {address}")

# 驗證地址生成
test_pub_key = wallet.private_key_to_public_key(private_key)
test_address = wallet.public_key_to_address(test_pub_key)
print(f"地址驗證: {test_address == address}")
```

## 參考資料

- [Bitcoin Address](https://en.bitcoin.it/wiki/Address)
- [secp256k1](https://en.bitcoin.it/wiki/Secp256k1)
- [Base58Check Encoding](https://en.bitcoin.it/wiki/Base58Check_encoding)
