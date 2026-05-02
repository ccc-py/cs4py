"""
MD5 雜湊函數 (MD5 Hash Function) - 簡化版

歷史背景：
MD5 由羅納德·李維斯特（Ronald Rivest）於1991年設計，用於取代 MD4。
雖然 MD5 曾被廣泛使用，但現在已被證明存在碰撞攻擊漏洞，不應用於
安全用途。本實作僅供教學和了解雜湊函數原理使用。

原理：
MD5 將任意長度輸入轉換為128位（16字節）的雜湊值。主要步驟：
1. 訊息填充：使長度為512位的倍數
2. 初始化4個32位狀態變數（A, B, C, D）
3. 處理每個512位塊：64輪（4輪×16次操作）
4. 輸出最終雜湊值

作者：cs4py 專案
"""

from typing import List


# MD5 常數表（正弦函數的絕對值）
# T[i] = floor(2^32 × |sin(i)|)，其中 i 從 1 開始
T = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]

# 每輪使用的移位數量
S = [
    # 第一輪
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    # 第二輪
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    # 第三輪
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    # 第四輪
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]


def left_rotate(x: int, n: int) -> int:
    """循環左移"""
    return ((x << n) | (x >> (32 - n))) & 0xffffffff


def pad_message(message: bytes) -> bytes:
    """填充訊息
    
    MD5 填充規則：
    1. 附加 bit '1'（0x80）
    2. 填充 '0' 直到長度 ≡ 448 (mod 512)
    3. 附加原始長度（64位小端序）
    
    Args:
        message: 原始訊息
    
    Returns:
        填充後的訊息
    """
    original_length_bits = len(message) * 8
    
    # 附加 0x80
    padded = message + b'\x80'
    
    # 填充 0 直到 (長度 % 64) == 56
    padding_len = (56 - (len(padded) % 64)) % 64
    padded += b'\x00' * padding_len
    
    # 附加長度（64位小端序）
    padded += original_length_bits.to_bytes(8, 'little')
    
    return padded


def process_block(block: bytes, state: List[int]) -> List[int]:
    """處理單個512位塊
    
    Args:
        block: 64字節的塊
        state: 當前狀態 [A, B, C, D]
    
    Returns:
        更新後的狀態
    """
    # 將塊分割為16個32位字（小端序）
    M = [int.from_bytes(block[i:i+4], 'little') for i in range(0, 64, 4)]
    
    A, B, C, D = state
    
    # 64輪壓縮
    for i in range(64):
        if i < 16:
            # 第一輪: F(B, C, D) = (B AND C) OR ((NOT B) AND D)
            F = (B & C) | ((~B) & D)
            g = i
        elif i < 32:
            # 第二輪: G(B, C, D) = (D AND B) OR ((NOT D) AND C)
            F = (D & B) | ((~D) & C)
            g = (5 * i + 1) % 16
        elif i < 48:
            # 第三輪: H(B, C, D) = B XOR C XOR D
            F = B ^ C ^ D
            g = (3 * i + 5) % 16
        else:
            # 第四輪: I(B, C, D) = C XOR (B OR (NOT D))
            F = C ^ (B | (~D))
            g = (7 * i) % 16
        
        F = (F + A + T[i] + M[g]) & 0xffffffff
        A = D
        D = C
        C = B
        B = (B + left_rotate(F, S[i])) & 0xffffffff
    
    # 更新狀態
    return [
        (state[0] + A) & 0xffffffff,
        (state[1] + B) & 0xffffffff,
        (state[2] + C) & 0xffffffff,
        (state[3] + D) & 0xffffffff
    ]


def md5(message: bytes) -> bytes:
    """計算 MD5 雜湊值
    
    Args:
        message: 輸入訊息
    
    Returns:
        128位（16字節）的雜湊值
    """
    # 初始化狀態（小端序）
    state = [
        0x67452301,
        0xefcdab89,
        0x98badcfe,
        0x10325476
    ]
    
    # 填充訊息
    padded = pad_message(message)
    
    # 處理每個512位塊
    for i in range(0, len(padded), 64):
        block = padded[i:i+64]
        state = process_block(block, state)
    
    # 將狀態轉換為16字節（小端序）
    return b''.join(s.to_bytes(4, 'little') for s in state)


def md5_hex(message: bytes) -> str:
    """計算 MD5 雜湊值並返回十六進制字串
    
    Args:
        message: 輸入訊息
    
    Returns:
        十六進制雜湊字串
    """
    return md5(message).hex()


if __name__ == "__main__":
    print("=== MD5 雜湊函數演示 ===\n")
    
    # 演示1：基本雜湊
    print("演示1：基本雜湊")
    test_cases = [
        b"",
        b"abc",
        b"hello world",
        b"MD5 is no longer secure for cryptographic purposes."
    ]
    
    for msg in test_cases:
        hash_result = md5_hex(msg)
        print(f"訊息: {msg[:30]}{'...' if len(msg) > 30 else ''}")
        print(f"MD5:   {hash_result}\n")
    
    # 演示2：與 hashlib 比較
    print("演示2：與 Python hashlib 比較")
    try:
        import hashlib
        msg = b"test message"
        our_hash = md5_hex(msg)
        lib_hash = hashlib.md5(msg).hexdigest()
        print(f"我們的實作: {our_hash}")
        print(f"hashlib:     {lib_hash}")
        print(f"結果相同: {our_hash == lib_hash}")
    except ImportError:
        print("hashlib 不可用")
    print()
    
    # 演示3：安全提醒
    print("演示3：安全提醒")
    print("⚠️  MD5 已被證明存在碰撞漏洞，不應用於：")
    print("   - 數位簽章")
    print("   - 密碼存儲")
    print("   - 完整性驗證（安全場景）")
    print("   請使用 SHA-256 或 SHA-3 等更安全的演算法。")
