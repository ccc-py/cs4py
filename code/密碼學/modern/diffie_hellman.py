"""
Diffie-Hellman 金鑰交換 (Diffie-Hellman Key Exchange)

歷史背景：
1976年，惠特菲爾德·迪菲（Whitfield Diffie）和馬丁·赫爾曼（Martin Hellman）發表了
Diffie-Hellman 金鑰交換協議，這是首個公鑰密碼學協議，允許雙方在不安全的通道上
協商共享秘密。拉爾夫·默克勒（Ralph Merkle）也對此有貢獻，因此也稱為
Diffie-Hellman-Merkle 金鑰交換。

原理：
基於離散對數問題的困難性。雙方約定一個大質數 p 和生成元 g。
Alice 選擇私鑰 a，發送 A = gᵃ mod p
Bob 選擇私鑰 b，發送 B = gᵇ mod p
雙方計算共享秘密：s = Aᵇ mod p = Bᵃ mod p = gᵃᵇ mod p

作者：cs4py 專案
"""

from typing import Tuple
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
    """尋找質數 p 的一個原根
    
    原根 g 滿足：g 的冪次 mod p 可以生成 1 到 p-1 的所有數
    
    Args:
        p: 質數
    
    Returns:
        原根
    """
    if not is_prime(p):
        raise ValueError("p 必須是質數")
    
    # 分解 p-1
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
    
    # 測試每個數是否為原根
    for g in range(2, p):
        if all(pow(g, phi // f, p) != 1 for f in factors):
            return g
    return -1


def generate_parameters(bits: int = 256) -> Tuple[int, int]:
    """生成 Diffie-Hellman 參數
    
    Args:
        bits: 質數 p 的位數
    
    Returns:
        (p, g) 其中 p 是大質數，g 是原根
    """
    # 生成安全質數 p（p = 2q + 1，其中 q 也是質數）
    while True:
        q = random.getrandbits(bits - 1)
        q |= (1 << bits - 2) | 1
        if is_prime(q):
            p = 2 * q + 1
            if is_prime(p):
                break
    
    g = find_primitive_root(p)
    return p, g


def generate_keypair(p: int, g: int) -> Tuple[int, int]:
    """生成密鑰對
    
    Args:
        p: 大質數
        g: 原根
    
    Returns:
        (私鑰, 公鑰) = (a, A = gᵃ mod p)
    """
    private_key = random.randrange(2, p - 1)
    public_key = pow(g, private_key, p)
    return private_key, public_key


def compute_shared_secret(their_public: int, my_private: int, p: int) -> int:
    """計算共享秘密
    
    Args:
        their_public: 對方的公鑰
        my_private: 自己的私鑰
        p: 大質數
    
    Returns:
        共享秘密
    """
    return pow(their_public, my_private, p)


def man_in_the_middle_demo(p: int, g: int) -> None:
    """演示中間人攻擊
    
    中間人 Mallory 攔截 Alice 和 Bob 的公鑰，分別與雙方建立共享秘密。
    
    Args:
        p: 大質數
        g: 原根
    """
    print("\n=== 中間人攻擊演示 ===\n")
    
    # Alice 生成密鑰對
    alice_private, alice_public = generate_keypair(p, g)
    
    # Bob 生成密鑰對
    bob_private, bob_public = generate_keypair(p, g)
    
    # Mallory 攔截並替換公鑰
    mallory_private_a, mallory_public_a = generate_keypair(p, g)
    mallory_private_b, mallory_public_b = generate_keypair(p, g)
    
    # Alice 以為她收到 Bob 的公鑰，實際是 Mallory 的
    alice_shared = compute_shared_secret(mallory_public_a, alice_private, p)
    
    # Bob 以為他收到 Alice 的公鑰，實際是 Mallory 的
    bob_shared = compute_shared_secret(mallory_public_b, bob_private, p)
    
    # Mallory 可以計算出兩個共享秘密
    mallory_with_alice = compute_shared_secret(alice_public, mallory_private_a, p)
    mallory_with_bob = compute_shared_secret(bob_public, mallory_private_b, p)
    
    print(f"Alice 認為的共享秘密: {alice_shared}")
    print(f"Bob 認為的共享秘密: {bob_shared}")
    print(f"Mallory 與 Alice 的共享秘密: {mallory_with_alice}")
    print(f"Mallory 與 Bob 的共享秘密: {mallory_with_bob}")
    print("Mallory 可以解密並修改雙方的通信！")


if __name__ == "__main__":
    print("=== Diffie-Hellman 金鑰交換演示 ===\n")
    
    # 使用小參數演示（實際使用需要大質數）
    print("演示1：使用小參數（教學用）")
    p = 23  # 質數
    g = 5   # 原根
    
    print(f"公共參數: p = {p}, g = {g}")
    
    # Alice
    alice_private = 6
    alice_public = pow(g, alice_private, p)
    print(f"Alice 私鑰: {alice_private}, 公鑰: {alice_public}")
    
    # Bob
    bob_private = 15
    bob_public = pow(g, bob_private, p)
    print(f"Bob 私鑰: {bob_private}, 公鑰: {bob_public}")
    
    # 計算共享秘密
    alice_shared = compute_shared_secret(bob_public, alice_private, p)
    bob_shared = compute_shared_secret(alice_public, bob_private, p)
    
    print(f"Alice 計算的共享秘密: {alice_shared}")
    print(f"Bob 計算的共享秘密: {bob_shared}")
    print(f"共享秘密是否相同: {alice_shared == bob_shared}")
    print()
    
    # 演示2：使用較大參數
    print("演示2：使用較大參數")
    p, g = generate_parameters(128)  # 128位質數（演示用，實際需2048+）
    print(f"生成參數: p = {p}, g = {g}")
    
    alice_private, alice_public = generate_keypair(p, g)
    bob_private, bob_public = generate_keypair(p, g)
    
    alice_shared = compute_shared_secret(bob_public, alice_private, p)
    bob_shared = compute_shared_secret(alice_public, bob_private, p)
    
    print(f"共享秘密相同: {alice_shared == bob_shared}")
    print()
    
    # 演示3：中間人攻擊
    man_in_the_middle_demo(p, g)
