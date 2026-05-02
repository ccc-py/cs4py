"""
ElGamal 加密 (ElGamal Encryption)

歷史背景：
ElGamal 加密由塔希爾·蓋拉爾（Taher ElGamal）於1985年提出，是一種基於
Diffie-Hellman 金鑰交換的公鑰加密系統。它是許多密碼學系統的基礎，包括
GNU Privacy Guard（GPG）和數位簽章算法（DSA）。

原理：
與 Diffie-Hellman 類似，ElGamal 使用離散對數問題。加密時引入隨機數 k，
使得每次加密同一明文都會產生不同的密文（隨機化加密）。

作者：cs4py 專案
"""

from typing import Tuple, List
import random


def is_prime(n: int, k: int = 5) -> bool:
    """Miller-Rabin 質數測試"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def find_primitive_root(p: int) -> int:
    """尋找質數 p 的原根"""
    if not is_prime(p):
        raise ValueError("p 必須是質數")
    
    phi = p - 1
    factors = set()
    n = phi
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 1
    if n > 1:
        factors.add(n)
    
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in factors):
            return g
    return -1


def generate_keypair(bits: int = 256) -> Tuple[Tuple[int, int, int], int]:
    """生成 ElGamal 密鑰對
    
    Returns:
        (公鑰, 私鑰)，公鑰為 (p, g, h)，私鑰為 x
        其中 h = gˣ mod p
    """
    # 生成質數 p 和原根 g
    while True:
        q = random.getrandbits(bits - 1)
        q |= (1 << bits - 2) | 1
        if is_prime(q):
            p = 2 * q + 1
            if is_prime(p):
                break
    
    g = find_primitive_root(p)
    
    # 私鑰 x
    x = random.randrange(2, p - 1)
    
    # 公鑰 h = gˣ mod p
    h = pow(g, x, p)
    
    return (p, g, h), x


def encrypt(message: int, public_key: Tuple[int, int, int]) -> Tuple[int, int]:
    """使用 ElGamal 加密
    
    Args:
        message: 明文（整數，需小於 p）
        public_key: 公鑰 (p, g, h)
    
    Returns:
        密文 (c1, c2)
        c1 = gᵏ mod p
        c2 = m * hᵏ mod p
        其中 k 是隨機數
    """
    p, g, h = public_key
    if message >= p:
        raise ValueError("明文必須小於 p")
    
    # 隨機數 k
    k = random.randrange(2, p - 1)
    
    # 計算 c1 和 c2
    c1 = pow(g, k, p)
    c2 = (message * pow(h, k, p)) % p
    
    return c1, c2


def decrypt(ciphertext: Tuple[int, int], private_key: int, p: int) -> int:
    """解密 ElGamal 密文
    
    Args:
        ciphertext: 密文 (c1, c2)
        private_key: 私鑰 x
        p: 質數
    
    Returns:
        明文
    """
    c1, c2 = ciphertext
    
    # 計算 s = c1ˣ mod p
    s = pow(c1, private_key, p)
    
    # 計算 s 的模反元素
    # 因為 p 是質數，s^(p-2) ≡ s⁻¹ mod p（費馬小定理）
    s_inv = pow(s, p - 2, p)
    
    # 明文 m = c2 * s⁻¹ mod p
    message = (c2 * s_inv) % p
    
    return message


def encrypt_text(text: str, public_key: Tuple[int, int, int]) -> List[Tuple[int, int]]:
    """加密文本"""
    p = public_key[0]
    return [encrypt(ord(c), public_key) for c in text]


def decrypt_text(ciphertext: List[Tuple[int, int]], private_key: int, p: int) -> str:
    """解密文本"""
    return ''.join(chr(decrypt(c, private_key, p)) for c in ciphertext)


if __name__ == "__main__":
    print("=== ElGamal 加密演示 ===\n")
    
    # 演示1：使用小參數（教學用）
    print("演示1：小參數演示")
    p = 467  # 質數
    g = 2    # 原根
    
    # 私鑰
    x = 127
    # 公鑰 h = gˣ mod p
    h = pow(g, x, p)
    
    public_key = (p, g, h)
    private_key = x
    
    print(f"公鑰: p={p}, g={g}, h={h}")
    print(f"私鑰: x={x}")
    
    message = 123
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key, p)
    
    print(f"明文: {message}")
    print(f"密文: {ciphertext}")
    print(f"解密: {decrypted}")
    print()
    
    # 演示2：文本加密
    print("演示2：文本加密")
    text = "HELLO"
    encrypted = encrypt_text(text, public_key)
    decrypted_text = decrypt_text(encrypted, private_key, p)
    
    print(f"原文: {text}")
    print(f"密文: {encrypted}")
    print(f"解密: {decrypted_text}")
    print()
    
    # 演示3：使用生成的密鑰對
    print("演示3：自動生成密鑰對")
    public_key, private_key = generate_keypair(128)  # 128位（演示用）
    p, g, h = public_key
    print(f"生成公鑰: p={p}, g={g}, h={h}")
    print(f"生成私鑰: x={private_key}")
    
    message = 999
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key, p)
    print(f"明文: {message}, 解密: {decrypted}")
