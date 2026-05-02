"""
ECDSA 類簽章驗證（簡化版）
模擬橢圓曲線數位簽章演算法
"""

import hashlib
import random
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class KeyPair:
    """金鑰對"""
    private_key: int
    public_key: Tuple[int, int]  # (x, y) 座標


class SimpleECDSA:
    """
    簡化版 ECDSA
    使用簡化的橢圓曲線運算來模擬簽章與驗證
    實際 ECDSA 使用 secp256k1 曲線
    """

    def __init__(self) -> None:
        # 簡化版曲線參數（非真實 secp256k1）
        self.p: int = 2**256 - 2**32 - 977  # 質數模數
        self.G: Tuple[int, int] = (2, 3)  # 生成點
        self.n: int = 2**256 - 2**32 - 981  # 曲線階（簡化）

    def generate_keypair(self) -> KeyPair:
        """生成金鑰對"""
        private_key: int = random.getrandbits(256) % self.n
        if private_key == 0:
            private_key = 1

        # 公鑰 = private_key * G（簡化版橢圓曲線乘法）
        public_key: Tuple[int, int] = self._point_multiply(private_key, self.G)
        return KeyPair(private_key, public_key)

    def sign(self, private_key: int, message: str) -> Tuple[int, int]:
        """
        簽署訊息
        返回 (r, s) 簽章
        """
        # 計算訊息雜湊
        message_hash: int = int(hashlib.sha256(message.encode()).hexdigest(), 16) % self.n

        # 生成隨機 k
        k: int = random.getrandbits(256) % (self.n - 1) + 1

        # 計算 R = k * G
        R: Tuple[int, int] = self._point_multiply(k, self.G)
        r: int = R[0] % self.n
        if r == 0:
            return self.sign(private_key, message)  # 重試

        # 計算 s = k^(-1) * (hash + r * private_key) mod n
        k_inv: int = self._mod_inverse(k, self.n)
        s: int = (k_inv * (message_hash + r * private_key)) % self.n
        if s == 0:
            return self.sign(private_key, message)  # 重試

        return r, s

    def verify(self, public_key: Tuple[int, int], message: str, signature: Tuple[int, int]) -> bool:
        """
        驗證簽章
        檢查是否 valid = (r, s) 是有效的簽章
        """
        r, s = signature

        # 檢查 r, s 是否在 [1, n-1] 範圍內
        if r < 1 or r >= self.n or s < 1 or s >= self.n:
            return False

        # 計算訊息雜湊
        message_hash: int = int(hashlib.sha256(message.encode()).hexdigest(), 16) % self.n

        # 計算 w = s^(-1) mod n
        w: int = self._mod_inverse(s, self.n)

        # 計算 u1 = hash * w mod n, u2 = r * w mod n
        u1: int = (message_hash * w) % self.n
        u2: int = (r * w) % self.n

        # 計算 P = u1 * G + u2 * public_key
        P1: Tuple[int, int] = self._point_multiply(u1, self.G)
        P2: Tuple[int, int] = self._point_multiply(u2, public_key)
        P: Tuple[int, int] = self._point_add(P1, P2)

        # 驗證 r == P.x mod n
        return r == P[0] % self.n

    def _point_add(self, P: Tuple[int, int], Q: Tuple[int, int]) -> Tuple[int, int]:
        """橢圓曲線點加法（簡化版）"""
        if P == Q:
            # 點加倍
            lam: int = (3 * P[0] * P[0]) * self._mod_inverse(2 * P[1], self.p) % self.p
        else:
            # 不同點相加
            lam: int = (Q[1] - P[1]) * self._mod_inverse(Q[0] - P[0], self.p) % self.p

        x: int = (lam * lam - P[0] - Q[0]) % self.p
        y: int = (lam * (P[0] - x) - P[1]) % self.p
        return (x, y)

    def _point_multiply(self, k: int, P: Tuple[int, int]) -> Tuple[int, int]:
        """橢圓曲線點乘法（倍數加法算法）"""
        result: Tuple[int, int] = P
        k -= 1
        while k > 0:
            if k & 1:
                result = self._point_add(result, P)
            P = self._point_add(P, P)
            k >>= 1
        return result

    def _mod_inverse(self, a: int, m: int) -> int:
        """模反元素（擴展歐幾里得算法）"""
        def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x: int = y1 - (b // a) * x1
            y: int = x1
            return gcd, x, y

        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m


class TransactionSigner:
    """交易簽章器，用於簽署區塊鏈交易"""

    def __init__(self) -> None:
        self.ecdsa: SimpleECDSA = SimpleECDSA()

    def sign_transaction(self, private_key: int, tx_data: str) -> Tuple[int, int]:
        """簽署交易資料"""
        return self.ecdsa.sign(private_key, tx_data)

    def verify_transaction(self, public_key: Tuple[int, int], tx_data: str, signature: Tuple[int, int]) -> bool:
        """驗證交易簽章"""
        return self.ecdsa.verify(public_key, tx_data, signature)


if __name__ == "__main__":
    # 建立 ECDSA 實例
    ecdsa: SimpleECDSA = SimpleECDSA()
    signer: TransactionSigner = TransactionSigner()

    print("=== ECDSA 簽章驗證模擬 ===\n")

    # 生成金鑰對
    keypair: KeyPair = ecdsa.generate_keypair()
    print(f"私鑰: {hex(keypair.private_key)[:20]}...")
    print(f"公鑰: ({hex(keypair.public_key[0])[:10]}..., {hex(keypair.public_key[1])[:10]}...)")

    # 簽署訊息
    message: str = "Alice sends 10 BTC to Bob"
    signature: Tuple[int, int] = signer.sign_transaction(keypair.private_key, message)
    print(f"\n簽署訊息: {message}")
    print(f"簽章 (r, s): ({signature[0]}, {signature[1]})")

    # 驗證簽章
    is_valid: bool = signer.verify_transaction(keypair.public_key, message, signature)
    print(f"\n簽章驗證: {'成功 ✓' if is_valid else '失敗 ✗'}")

    # 測試篡改
    tampered_message: str = "Alice sends 100 BTC to Bob"
    is_tampered: bool = signer.verify_transaction(keypair.public_key, tampered_message, signature)
    print(f"篡改後驗證: {'成功 ✓' if is_tampered else '失敗 ✗'} (應該失敗)")
