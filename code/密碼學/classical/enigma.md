# 恩尼格瑪密碼機 (Enigma Machine)

## 歷史背景
恩尼格瑪密碼機由德國工程師亞瑟·謝爾比烏斯（Arthur Scherbius）於1918年發明，二戰期間被德國軍方廣泛使用於軍事通信加密。其加密強度極高，盟軍花費大量精力破解。

波蘭數學家馬里安·雷耶夫斯基（Marian Rejewski）首先破解了早期恩尼格瑪，而英國布萊切利園（Bletchley Park）的艾倫·圖靈（Alan Turing）等人設計了「炸彈機」（Bombe）進一步加速破解，對盟軍勝利有重要貢獻。

## 核心原理
恩尼格瑪機使用以下組件加密：
1. **插線板（Plugboard）**：交換字母對（如A↔B）
2. **三個轉子（Rotor）**：每個轉子內部有26個字母的替換映射，轉子會在每次按鍵後步進
3. **反射板（Reflector）**：將信號反射回轉子，確保加密和解密過程相同

每個字母的加密路徑：鍵盤 → 插線板 → 轉子3 → 轉子2 → 轉子1 → 反射板 → 轉子1 → 轉子2 → 轉子3 → 插線板 → 燈管

## 使用範例
```python
from enigma import create_default_enigma

# 創建恩尼格瑪機
enigma = create_default_enigma()
enigma.set_rotor_positions([0, 0, 0])  # A, A, A

# 加密
plaintext = "HELLO"
ciphertext = enigma.encrypt(plaintext)
print(f"密文: {ciphertext}")

# 解密（需要相同初始位置）
enigma.set_rotor_positions([0, 0, 0])
decrypted = enigma.decrypt(ciphertext)
print(f"解密: {decrypted}")
```

## 參考資料
- [Enigma Machine - Wikipedia](https://en.wikipedia.org/wiki/Enigma_machine)
- Singh, S. (1999). *The Code Book*
- [Bletchley Park](https://bletchleypark.org.uk/)
