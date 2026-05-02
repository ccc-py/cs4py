"""
數位簽章 (Digital Signature) - 基於 RSA

歷史背景：
數位簽章的概念由惠特菲爾德·迪菲（Whitfield Diffie）和馬丁·赫爾曼（Martin Hellman）
於1976年提出。第一個實用的數位簽章算法是 Ronald Rivest、Adi Shamir 和
Leonard Adleman 於1977年提出的 RSA 簽章。

原理：
數位簽章使用非對稱加密實現：
1. 簽署：使用私鑰對訊息的雜湊值進行加密
2. 驗證：使用公鑰解密簽章，並與重新計算的雜湊值比較
3. 結合雜湊函數確保簽章固定長度且不可逆

作者：cs4py 專案
"""

from typing import Tuple, List
import random


# 簡單的雜湊函數（教學用，實際應使用 SHA-256）
def simple_hash(message: str) -> int:
    """簡單的雜湊函數（教學用）
    
    Args:
        message: 訊息字串
    
    Returns:
        雜湊值（整數）
    """
    h = 0x811C9DC5  # FNV 偏移基礎
    for c in message.encode('utf-8'):
        h = ((h ^ c) * 0x01000193) & 0xFFFFFFFF
    return h


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


def generate_prime(bits: int) -> int:
    """生成質數"""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1
        if is_prime(n):
            return n


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """擴展歐幾里得算法"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e: int, phi: int) -> int:
    """計算模反元素"""
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("模反元素不存在")
    return x % phi


def generate_keys(bits: int = 512) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """生成 RSA 密鑰對（用於簽章）
    
    Returns:
        (公鑰, 私鑰) = ((e, n), (d, n))
    """
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    while __import__('math').gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)


def sign(message: str, private_key: Tuple[int, int]) -> int:
    """簽署訊息
    
    使用私鑰對訊息雜湊值進行加密（即簽章）
    
    Args:
        message: 要簽署的訊息
        private_key: 私鑰 (d, n)
    
    Returns:
        簽章（整數）
    """
    d, n = private_key
    h = simple_hash(message)
    # 簽章 = hashᵈ mod n
    signature = pow(h, d, n)
    return signature


def verify(message: str, signature: int, public_key: Tuple[int, int]) -> bool:
    """驗證簽章
    
    使用公鑰解密簽章，並與重新計算的雜湊值比較
    
    Args:
        message: 原始訊息
        signature: 簽章
        public_key: 公鑰 (e, n)
    
    Returns:
        簽章是否有效
    """
    e, n = public_key
    # 解密簽章 = signatureᵉ mod n
    decrypted_hash = pow(signature, e, n)
    # 計算訊息雜湊值
    message_hash = simple_hash(message)
    return decrypted_hash == message_hash


def sign_with_hash(message: str, private_key: Tuple[int, int], 
                   hash_func=None) -> int:
    """使用指定雜湊函數簽署訊息
    
    Args:
        message: 訊息
        private_key: 私鑰
        hash_func: 雜湊函數（預設使用 simple_hash）
    
    Returns:
        簽章
    """
    if hash_func is None:
        hash_func = simple_hash
    
    d, n = private_key
    h = hash_func(message)
    return pow(h, d, n)


def verify_with_hash(message: str, signature: int, 
                     public_key: Tuple[int, int], hash_func=None) -> bool:
    """使用指定雜湊函數驗證簽章"""
    if hash_func is None:
        hash_func = simple_hash
    
    e, n = public_key
    decrypted_hash = pow(signature, e, n)
    message_hash = hash_func(message)
    return decrypted_hash == message_hash


if __name__ == "__main__":
    print("=== 數位簽章演示 ===\n")
    
    # 演示1：基本簽章與驗證
    print("演示1：基本簽章與驗證")
    public_key, private_key = generate_keys(512)
    print(f"公鑰 (e, n): e={public_key[0]}, n={public_key[1]}")
    print(f"私鑰 (d, n): d={private_key[0]}, n={private_key[1]}")
    
    message = "這是一條重要的訊息"
    print(f"\n訊息: {message}")
    
    # 簽署
    signature = sign(message, private_key)
    print(f"簽章: {signature}")
    
    # 驗證
    is_valid = verify(message, signature, public_key)
    print(f"驗證結果: {is_valid}")
    print()
    
    # 演示2：竄改檢測
    print("演示2：竄改檢測")
    tampered_message = "這是一條被竄改的訊息"
    is_valid_tampered = verify(tampered_message, signature, public_key)
    print(f"原始訊息: {message}")
    print(f"竄改訊息: {tampered_message}")
    print(f"原始簽章驗證竄改訊息: {is_valid_tampered}")
    print()
    
    # 演示3：不同訊息產生不同簽章
    print("演示3：不同訊息的簽章")
    msg1 = "Message 1"
    msg2 = "Message 2"
    sig1 = sign(msg1, private_key)
    sig2 = sign(msg2, private_key)
    print(f"訊息1: {msg1}")
    print(f"簽章1: {sig1}")
    print(f"訊息2: {msg2}")
    print(f"簽章2: {sig2}")
    print(f"簽章是否不同: {sig1 != sig2}")
    print()
    
    # 演示4：使用 SHA-256 風格的雜湊
    print("演示4：使用更好的雜湊函數")
    
    def simple_sha256_style(message: str) -> int:
        """模擬 SHA-256 風格的雜湊（簡化版）"""
        h = 0x6a09e667
        for c in message.encode('utf-8'):
            h = ((h << 5) + h + c) & 0xFFFFFFFF  # h * 33 + c
        return h
    
    signature2 = sign_with_hash(message, private_key, simple_sha256_style)
    is_valid2 = verify_with_hash(message, signature2, public_key, simple_sha256_style)
    print(f"使用改進雜湊的簽章驗證: {is_valid2}")
