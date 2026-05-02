"""
SHA-256 雜湊函數 (SHA-256 Hash Function)

歷史背景：
SHA-256 由美國國家標準與技術研究院（NIST）於2001年發布，屬於 SHA-2 家族。
它是目前廣泛使用的雜湊函數，應用於 SSL/TLS、比特幣、區塊鏈等眾多領域。

原理：
SHA-256 將任意長度輸入轉換為256位（32字節）的雜湊值。主要步驟：
1. 訊息填充：使長度為512位的倍數
2. 初始化雜湊值：8個32位常數（基於質數平方根的小數部分）
3. 處理每個512位塊：64輪壓縮函數
4. 輸出最終雜湊值

作者：cs4py 專案
"""

from typing import List


# SHA-256 常數（前64個質數的立方根的小數部分前32位）
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def rotr(x: int, n: int) -> int:
    """循環右移（rotate right）"""
    return (x >> n) | (x << (32 - n)) & 0xffffffff


def choose(x: int, y: int, z: int) -> int:
    """Ch 函數: (x AND y) XOR ((NOT x) AND z)"""
    return (x & y) ^ (~x & z)


def majority(x: int, y: int, z: int) -> int:
    """Maj 函數: (x AND y) XOR (x AND z) XOR (y AND z)"""
    return (x & y) ^ (x & z) ^ (y & z)


def sigma0(x: int) -> int:
    """Σ₀: ROTR(2, x) ⊕ ROTR(13, x) ⊕ ROTR(22, x)"""
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def sigma1(x: int) -> int:
    """Σ₁: ROTR(6, x) ⊕ ROTR(11, x) ⊕ ROTR(25, x)"""
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def gamma0(x: int) -> int:
    """σ₀: ROTR(7, x) ⊕ ROTR(18, x) ⊕ SHR(3, x)"""
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def gamma1(x: int) -> int:
    """σ₁: ROTR(17, x) ⊕ ROTR(19, x) ⊕ SHR(10, x)"""
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def pad_message(message: bytes) -> bytes:
    """填充訊息
    
    填充規則：
    1. 附加 bit '1'
    2. 附加 k 個 '0'，使 (長度 + 1 + k + 64) ≡ 0 (mod 512)
    3. 附加原始訊息長度的64位大端序表示
    
    Args:
        message: 原始訊息
    
    Returns:
        填充後的訊息
    """
    # 原始長度（位）
    original_length_bits = len(message) * 8
    
    # 附加 bit '1'（即 0x80）
    padded = message + b'\x80'
    
    # 計算需要填充的 '0' 數量
    # 當前長度 mod 64（字節），需要使最後64位元組（8字節）留給長度
    # 所以 (len + 1 + k) ≡ 56 (mod 64)
    padding_len = (56 - (len(padded) % 64)) % 64
    padded += b'\x00' * padding_len
    
    # 附加長度（64位大端序）
    padded += original_length_bits.to_bytes(8, 'big')
    
    return padded


def process_block(block: bytes, H: List[int]) -> List[int]:
    """處理單個512位塊
    
    Args:
        block: 512位（64字節）的塊
        H: 當前的8個雜湊值
    
    Returns:
        更新後的雜湊值
    """
    # 將塊分割為16個32位字（大端序）
    W = [int.from_bytes(block[i:i+4], 'big') for i in range(0, 64, 4)]
    
    # 擴展為64個字
    for i in range(16, 64):
        s0 = gamma0(W[i-15])
        s1 = gamma1(W[i-2])
        W.append((W[i-16] + s0 + W[i-7] + s1) & 0xffffffff)
    
    # 初始化工作變數
    a, b, c, d, e, f, g, h = H
    
    # 64輪壓縮
    for i in range(64):
        S1 = sigma1(e)
        ch = choose(e, f, g)
        temp1 = (h + S1 + ch + K[i] + W[i]) & 0xffffffff
        S0 = sigma0(a)
        maj = majority(a, b, c)
        temp2 = (S0 + maj) & 0xffffffff
        
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xffffffff
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xffffffff
    
    # 計算新的雜湊值
    return [
        (H[0] + a) & 0xffffffff,
        (H[1] + b) & 0xffffffff,
        (H[2] + c) & 0xffffffff,
        (H[3] + d) & 0xffffffff,
        (H[4] + e) & 0xffffffff,
        (H[5] + f) & 0xffffffff,
        (H[6] + g) & 0xffffffff,
        (H[7] + h) & 0xffffffff
    ]


def sha256(message: bytes) -> bytes:
    """計算 SHA-256 雜湊值
    
    Args:
        message: 輸入訊息（位元組）
    
    Returns:
        256位（32字節）的雜湊值
    """
    # 初始化雜湊值（前8個質數平方根的小數部分前32位）
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    # 填充訊息
    padded = pad_message(message)
    
    # 處理每個512位塊
    for i in range(0, len(padded), 64):
        block = padded[i:i+64]
        H = process_block(block, H)
    
    # 將8個32位整數轉換為32字節
    return b''.join(h.to_bytes(4, 'big') for h in H)


def sha256_hex(message: bytes) -> str:
    """計算 SHA-256 雜湊值並返回十六進制字串
    
    Args:
        message: 輸入訊息
    
    Returns:
        十六進制雜湊字串
    """
    return sha256(message).hex()


if __name__ == "__main__":
    print("=== SHA-256 雜湊函數演示 ===\n")
    
    # 演示1：基本雜湊
    print("演示1：基本雜湊")
    test_cases = [
        b"",
        b"abc",
        b"hello world",
        b"SHA-256 is widely used in blockchain technology."
    ]
    
    for msg in test_cases:
        hash_result = sha256_hex(msg)
        print(f"訊息: {msg[:30]}{'...' if len(msg) > 30 else ''}")
        print(f"雜湊: {hash_result}\n")
    
    # 演示2：與 hashlib 比較
    print("演示2：與 Python hashlib 比較")
    try:
        import hashlib
        msg = b"test message for comparison"
        our_hash = sha256_hex(msg)
        lib_hash = hashlib.sha256(msg).hexdigest()
        print(f"我們的實作: {our_hash}")
        print(f"hashlib:     {lib_hash}")
        print(f"結果相同: {our_hash == lib_hash}")
    except ImportError:
        print("hashlib 不可用")
    print()
    
    # 演示3：雜湊特性
    print("演示3：雜湊特性（雪崩效應）")
    msg1 = b"hello"
    msg2 = b"hellp"  # 只改一個字節
    hash1 = sha256_hex(msg1)
    hash2 = sha256_hex(msg2)
    print(f"訊息1: {msg1} -> {hash1[:16]}...")
    print(f"訊息2: {msg2} -> {hash2[:16]}...")
    print("注意：微小的輸入變化會導致完全不同的雜湊值")
