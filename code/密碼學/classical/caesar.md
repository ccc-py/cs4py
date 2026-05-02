# 凱薩密碼 (Caesar Cipher)

## 歷史背景
凱薩密碼是歷史上最著名的加密方法之一，由羅馬共和國的軍事統帥凱薩大帝（Julius Caesar）在公元前約100-44年間用於軍事通信。根據蘇維托尼烏斯（Suetonius）的記載，凱薩使用移位3的方式加密私人信件。

這是最簡單的替換密碼，雖然加密強度極弱，但作為密碼學的入門經典，展示了替換加密的基本概念。

## 核心原理
凱薩密碼是一種單表替換密碼，將字母表中的每個字母按照固定數量進行移位：

- **加密**：`E(x) = (x + k) mod 26`，其中 k 為密鑰（移位值）
- **解密**：`D(y) = (y - k) mod 26`

例如，當 k=3 時：
- A → D, B → E, C → F, ..., X → A, Y → B, Z → C

由於只有25種可能的密鑰（移位0等同於不加密），凱薩密碼極易受到暴力破解攻擊。

## 使用範例
```python
from caesar import encrypt, decrypt, brute_force, crack

# 基本加密解密
plaintext = "HELLO"
ciphertext = encrypt(plaintext, 3)  # "KHOOR"
decrypted = decrypt(ciphertext, 3)   # "HELLO"

# 暴力破解
results = brute_force("KHOOR")
for shift, text in results:
    print(f"Shift {shift}: {text}")

# 頻率分析自動破解
shift, plaintext = crack("XLMW MW E GEIWEV GMTLIV")
print(f"Detected shift: {shift}")
print(f"Plaintext: {plaintext}")
```

## 參考資料
- [Caesar Cipher - Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- Suetonius《羅馬十二帝王傳》
- [Classical Cryptography Course](https://www.cryptool.org/en/cto/)
