# Diffie-Hellman 金鑰交換 (Diffie-Hellman Key Exchange)

## 歷史背景
Diffie-Hellman 協議由惠特菲爾德·迪菲（Whitfield Diffie）和馬丁·赫爾曼（Martin Hellman）於1976年發表，是密碼學史上的里程碑。這是第一個公鑰密碼學協議，解決了「密鑰分發問題」——如何在不安全的通道上安全地協商共享密鑰。

拉爾夫·默克勒（Ralph Merkle）的貢獻也不能忽視，因此該協議有時稱為 Diffie-Hellman-Merkle 金鑰交換。

## 核心原理
Diffie-Hellman 基於離散對數問題的困難性：

1. Alice 和 Bob 約定公共參數：大質數 p 和生成元 g
2. Alice 選擇私鑰 a，計算公鑰 A = gᵃ mod p，發送給 Bob
3. Bob 選擇私鑰 b，計算公鑰 B = gᵇ mod p，發送給 Alice
4. Alice 計算共享秘密：s = Bᵃ mod p = gᵇᵃ mod p
5. Bob 計算共享秘密：s = Aᵇ mod p = gᵃᵇ mod p

攻擊者即使截獲 A 和 B，也無法在合理時間內計算出 a 或 b（離散對數問題）。

## 使用範例
```python
from diffie_hellman import generate_parameters, generate_keypair, compute_shared_secret

# 生成公共參數
p, g = generate_parameters(2048)

# Alice 生成密鑰對
alice_private, alice_public = generate_keypair(p, g)

# Bob 生成密鑰對
bob_private, bob_public = generate_keypair(p, g)

# 計算共享秘密
alice_shared = compute_shared_secret(bob_public, alice_private, p)
bob_shared = compute_shared_secret(alice_public, bob_private, p)

assert alice_shared == bob_shared
print(f"共享秘密: {alice_shared}")
```

## 參考資料
- [Diffie-Hellman - Wikipedia](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)
- Diffie, W., & Hellman, M. (1976). *New Directions in Cryptography*
- [RFC 3526 - Diffie-Hellman Group Parameters](https://www.rfc-editor.org/rfc/rfc3526)
