"""
RSA 公鑰加密 (RSA Public Key Cryptography)

歷史背景：
RSA 由羅納德·李維斯特（Ron Rivest）、阿迪·薩莫爾（Adi Shamir）和倫納德·阿德曼
（Leonard Adleman）於1977年提出，是首個實用的公鑰加密算法。RSA 的名字來自
三位發明人的姓氏首字母。

原理：
基於大整數分解的困難性。選擇兩個大質數 p 和 q，計算 n = p×q 和 φ(n) = (p-1)(q-1)。
選擇 e 使得 gcd(e, φ(n)) = 1，計算 d ≡ e⁻¹ mod φ(n)。
公鑰為 (e, n)，私鑰為 (d, n)。
加密：c ≡ mᵉ mod n
解密：m ≡ cᵈ mod n

作者：cs4py 專案
"""

from typing import Tuple, List
import random


def is_prime(n: int, k: int = 5) -> bool:
    """使用 Miller-Rabin 測試檢測質數（簡化版）
    
    Args:
        n: 待檢測數
        k: 測試次數
    
    Returns:
        是否為質數
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    
    # 寫成 n-1 = d × 2ʳ
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Miller-Rabin 測試
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


def generate_prime(bits: int) -> int:
    """生成指定位數的質數
    
    Args:
        bits: 質數的位數
    
    Returns:
        質數
    """
    while True:
        # 生成隨機奇數
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # 確保最高位為1且為奇數
        if is_prime(n):
            return n


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """擴展歐幾里得算法
    
    返回 (gcd, x, y) 使得 ax + by = gcd(a, b)
    
    Args:
        a: 整數
        b: 整數
    
    Returns:
        (gcd, x, y)
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e: int, phi: int) -> int:
    """計算模反元素
    
    找到 d 使得 e × d ≡ 1 mod phi
    
    Args:
        e: 公鑰指數
        phi: 歐拉函數值
    
    Returns:
        模反元素 d
    """
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("模反元素不存在")
    return x % phi


def generate_keypair(bits: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """生成 RSA 密鑰對
    
    Args:
        bits: 質數位數（實際使用需2048+位，演示用1024或更小）
    
    Returns:
        (公鑰, 私鑰)，公鑰為 (e, n)，私鑰為 (d, n)
    """
    # 生成兩個大質數
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    # 計算 n 和 φ(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # 選擇公鑰指數 e（通常為65537）
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    # 計算私鑰指數 d
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)


def gcd(a: int, b: int) -> int:
    """計算最大公約數"""
    while b:
        a, b = b, a % b
    return a


def encrypt(message: int, public_key: Tuple[int, int]) -> int:
    """使用公鑰加密
    
    Args:
        message: 明文（整數，需小於 n）
        public_key: 公鑰 (e, n)
    
    Returns:
        密文（整數）
    """
    e, n = public_key
    if message >= n:
        raise ValueError("明文必須小於 n")
    return pow(message, e, n)


def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> int:
    """使用私鑰解密
    
    Args:
        ciphertext: 密文（整數）
        private_key: 私鑰 (d, n)
    
    Returns:
        明文（整數）
    """
    d, n = private_key
    return pow(ciphertext, d, n)


def encrypt_text(text: str, public_key: Tuple[int, int]) -> List[int]:
    """加密文本（將每個字符轉為整數）"""
    e, n = public_key
    return [encrypt(ord(c), (e, n)) for c in text]


def decrypt_text(ciphertext: List[int], private_key: Tuple[int, int]) -> str:
    """解密文本"""
    return ''.join(chr(decrypt(c, private_key)) for c in ciphertext)


if __name__ == "__main__":
    print("=== RSA 公鑰加密演示 ===\n")
    
    # 演示1：使用小質數（教學用）
    print("演示1：小質數演示")
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi)
    
    public_key = (e, n)
    private_key = (d, n)
    
    print(f"p = {p}, q = {q}")
    print(f"n = {n}, φ(n) = {phi}")
    print(f"公鑰 (e, n) = {public_key}")
    print(f"私鑰 (d, n) = {private_key}")
    
    message = 65  # 'A'
    ciphertext = encrypt(message, public_key)
    decrypted = decrypt(ciphertext, private_key)
    print(f"明文: {message} ('{chr(message)}')")
    print(f"密文: {ciphertext}")
    print(f"解密: {decrypted} ('{chr(decrypted)}')")
    print()
    
    # 演示2：文本加密
    print("演示2：文本加密")
    text = "HELLO"
    encrypted = encrypt_text(text, public_key)
    decrypted_text = decrypt_text(encrypted, private_key)
    print(f"原文: {text}")
    print(f"密文: {encrypted}")
    print(f"解密: {decrypted_text}")
    print()
    
    # 演示3：數位簽章概念
    print("演示3：數位簽章概念")
    # 簽章：用私鑰加密（作為簽章）
    message = ord('X')
    signature = encrypt(message, private_key)  # 注意：這裡用私鑰加密
    # 驗證：用公鑰解密
    verified = decrypt(signature, public_key)
    print(f"訊息: {chr(message)}")
    print(f"簽章: {signature}")
    print(f"驗證: {chr(verified)}")
