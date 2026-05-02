"""
工作量證明（Proof of Work, PoW）實作
模擬挖礦過程，透過調整 nonce 找到符合難度的雜湊值
"""

import hashlib
import json
from typing import Tuple


class ProofOfWork:
    """工作量證明類別，實作挖礦演算法"""

    def __init__(self, difficulty: int = 4) -> None:
        self.difficulty: int = difficulty
        self.target: str = "0" * difficulty

    def calculate_hash(self, index: int, timestamp: str, data: str, prev_hash: str, nonce: int) -> str:
        """計算區塊雜湊值"""
        block_string: str = json.dumps({
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'prev_hash': prev_hash,
            'nonce': nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, index: int, timestamp: str, data: str, prev_hash: str) -> Tuple[str, int]:
        """
        挖礦：尋找符合難度要求的 nonce
        返回 (hash, nonce)
        """
        nonce: int = 0
        while True:
            hash_result: str = self.calculate_hash(index, timestamp, data, prev_hash, nonce)
            if hash_result.startswith(self.target):
                return hash_result, nonce
            nonce += 1

    def validate(self, index: int, timestamp: str, data: str, prev_hash: str, nonce: int) -> bool:
        """驗證雜湊值是否符合難度要求"""
        hash_result: str = self.calculate_hash(index, timestamp, data, prev_hash, nonce)
        return hash_result.startswith(self.target)

    def adjust_difficulty(self, mining_time: float) -> int:
        """
        根據挖礦時間調整難度
        如果挖礦時間太短，增加難度；太長則降低難度
        """
        target_time: float = 60.0  # 目標 60 秒
        if mining_time < target_time / 2:
            self.difficulty += 1
        elif mining_time > target_time * 2 and self.difficulty > 1:
            self.difficulty -= 1
        self.target = "0" * self.difficulty
        return self.difficulty


if __name__ == "__main__":
    import time
    from datetime import datetime

    # 建立 PoW 實例
    pow_algorithm: ProofOfWork = ProofOfWork(difficulty=4)
    print("當前難度:", pow_algorithm.difficulty)
    print("目標前綴:", pow_algorithm.target)

    # 模擬挖礦
    index: int = 1
    timestamp: str = str(datetime.now())
    data: str = "Alice sends 10 BTC to Bob"
    prev_hash: str = "0" * 64

    print("\n開始挖礦...")
    start_time: float = time.time()
    hash_result, nonce = pow_algorithm.mine(index, timestamp, data, prev_hash)
    end_time: float = time.time()

    print(f"挖礦成功！")
    print(f"Nonce: {nonce}")
    print(f"Hash: {hash_result}")
    print(f"耗時: {end_time - start_time:.2f} 秒")

    # 驗證
    is_valid: bool = pow_algorithm.validate(index, timestamp, data, prev_hash, nonce)
    print(f"驗證結果: {is_valid}")
