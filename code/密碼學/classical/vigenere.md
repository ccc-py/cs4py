# 維吉尼亞密碼 (Vigenère Cipher)

## 歷史背景
維吉尼亞密碼由16世紀法國外交官布萊斯·德·維吉尼亞（Blaise de Vigenère）於1586年發表，但實際上最早由意大利密碼學家萊昂·巴蒂斯塔·阿爾貝蒂（Leon Battista Alberti）構思。

在19世紀之前，維吉尼亞密碼被認為是「不可破解的密碼」（le chiffre indéchiffrable）。直到1863年，普魯士軍官弗里德里希·卡西斯基（Friedrich Kasiski）發表了破解方法，因此該方法被稱為「卡西斯基測試」。

## 核心原理
維吉尼亞密碼是一種多表替換密碼，使用關鍵字來決定每個字母的加密方式：

1. **密鑰擴展**：將關鍵字重複至與明文等長
2. **加密**：每個明文字母使用對應的密鑰字母進行凱薩移位
3. **數學表達**：`C_i = (P_i + K_(i mod m)) mod 26`

其中 m 為密鑰長度，K 為密鑰對應的數值（A=0, B=1, ...）。

## 使用範例
```python
from vigenere import encrypt, decrypt, crack, find_key_length

# 基本加密
plaintext = "ATTACK AT DAWN"
key = "LEMON"
ciphertext = encrypt(plaintext, key)  # "LXFOPV EF RNHR"
decrypted = decrypt(ciphertext, key)  # "ATTACK AT DAWN"

# 破解密鑰
ciphertext = "LXFOPVEFRNHR"
key_length = find_key_length(ciphertext, 10)
recovered_key = crack(ciphertext)
print(f"Recovered key: {recovered_key}")
```

## 參考資料
- [Vigenère Cipher - Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- Kasiski, F. W. (1863). *Die Geheimschriften und die Dechiffrir-Kunst*
- [Practical Cryptography](https://practicalcryptography.com/)
