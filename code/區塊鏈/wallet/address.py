"""
區塊鏈錢包地址生成
從公鑰推導地址，包含 Base58 編碼
"""

import hashlib
from typing import Tuple


class WalletAddress:
    """錢包地址生成器"""

    def __init__(self) -> None:
        pass

    def generate_private_key(self) -> int:
        """生成私鑰（簡化版，實際應使用密碼學安全的隨機數）"""
        import random
        return random.getrandbits(256)

    def private_key_to_public_key(self, private_key: int) -> int:
        """
        從私鑰推導公鑰（簡化版橢圓曲線）
        實際比特幣使用 secp256k1 曲線
        """
        # 簡化：使用簡單的橢圓曲線乘法模擬
        # 實際實作應使用 ecdsa 函式庫
        g: int = 2  # 生成點（簡化）
        return pow(g, private_key, 2**256 - 2**32 - 977)  # 簡化模數

    def public_key_to_address(self, public_key: int) -> str:
        """
        從公鑰推導地址
        步驟：公鑰 → SHA-256 → RIPEMD-160 → 加入版本字節 → 雙重 SHA-256 → Base58
        """
        # 1. SHA-256 雜湊
        pub_key_bytes: bytes = public_key.to_bytes(32, byteorder='big')
        sha256_hash: bytes = hashlib.sha256(pub_key_bytes).digest()

        # 2. RIPEMD-160 雜湊（簡化版，實際應使用 ripemd160）
        # 這裡使用另一輪 SHA-256 的前 20 字節模擬
        ripemd160_hash: bytes = hashlib.sha256(sha256_hash).digest()[:20]

        # 3. 加入版本字節（比特幣主網為 0x00）
        version: bytes = b'\x00'
        versioned_hash: bytes = version + ripemd160_hash

        # 4. 計算校驗和（雙重 SHA-256 的前 4 字節）
        checksum: bytes = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]

        # 5. Base58 編碼
        address_bytes: bytes = versioned_hash + checksum
        address: str = self.base58_encode(address_bytes)

        return address

    def base58_encode(self, data: bytes) -> str:
        """Base58 編碼（比特幣使用的編碼方式）"""
        alphabet: str = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

        # 計算前導零的數量
        leading_zeros: int = 0
        for byte in data:
            if byte == 0:
                leading_zeros += 1
            else:
                break

        # 將 bytes 轉為整數
        num: int = int.from_bytes(data, byteorder='big')

        # 轉為 Base58
        encoded: str = ""
        base: int = 58
        while num > 0:
            num, remainder = divmod(num, base)
            encoded = alphabet[remainder] + encoded

        # 加入前導 '1'（代表零）
        return '1' * leading_zeros + encoded

    def base58_decode(self, address: str) -> bytes:
        """Base58 解碼"""
        alphabet: str = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

        # 計算前導 '1' 的數量
        leading_ones: int = 0
        for char in address:
            if char == '1':
                leading_ones += 1
            else:
                break

        # 將 Base58 轉為整數
        num: int = 0
        base: int = 58
        for char in address:
            num = num * base + alphabet.index(char)

        # 轉回 bytes
        if num == 0:
            return b'\x00' * leading_ones

        result: bytes = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
        return b'\x00' * leading_ones + result

    def generate_wallet(self) -> Tuple[int, int, str]:
        """生成完整錢包（私鑰、公鑰、地址）"""
        private_key: int = self.generate_private_key()
        public_key: int = self.private_key_to_public_key(private_key)
        address: str = self.public_key_to_address(public_key)
        return private_key, public_key, address


if __name__ == "__main__":
    wallet: WalletAddress = WalletAddress()

    # 生成錢包
    private_key, public_key, address = wallet.generate_wallet()

    print("錢包資訊：")
    print(f"私鑰: {hex(private_key)[:20]}...")
    print(f"公鑰: {hex(public_key)[:20]}...")
    print(f"地址: {address}")
    print(f"地址長度: {len(address)} 字元")

    # 測試 Base58
    test_data: bytes = b'\x00\x01\x02\x03\x04'
    encoded: str = wallet.base58_encode(test_data)
    decoded: bytes = wallet.base58_decode(encoded)
    print(f"\nBase58 測試:")
    print(f"原始: {test_data}")
    print(f"編碼: {encoded}")
    print(f"解碼: {decoded}")
    print(f"驗證: {test_data == decoded}")
