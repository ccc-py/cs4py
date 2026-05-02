"""
區塊鏈核心：區塊與鏈結構
實作基本區塊結構與區塊鏈驗證
"""

import hashlib
import json
from datetime import datetime
from typing import List, Optional, Dict, Any


class Block:
    """區塊類別，包含區塊基本資訊與雜湊計算"""

    def __init__(self, index: int, timestamp: str, data: Any, prev_hash: str, nonce: int = 0) -> None:
        self.index: int = index
        self.timestamp: str = timestamp
        self.data: Any = data
        self.prev_hash: str = prev_hash
        self.nonce: int = nonce
        self.hash: str = self.calculate_hash()

    def calculate_hash(self) -> str:
        """計算區塊的 SHA-256 雜湊值"""
        block_string: str = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash[:10]}...)"


class Blockchain:
    """區塊鏈類別，管理區塊的創建與驗證"""

    def __init__(self) -> None:
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """創建創世區塊"""
        return Block(0, str(datetime.now()), "創世區塊", "0")

    def get_latest_block(self) -> Block:
        """取得最新區塊"""
        return self.chain[-1]

    def add_block(self, new_data: Any) -> Block:
        """新增區塊到鏈中"""
        prev_block: Block = self.get_latest_block()
        new_block: Block = Block(
            index=prev_block.index + 1,
            timestamp=str(datetime.now()),
            data=new_data,
            prev_hash=prev_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """驗證整條區塊鏈的完整性"""
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            prev_block: Block = self.chain[i - 1]

            # 檢查當前區塊的雜湊值是否正確
            if current_block.hash != current_block.calculate_hash():
                return False

            # 檢查前後區塊的關聯性
            if current_block.prev_hash != prev_block.hash:
                return False

        return True


if __name__ == "__main__":
    # 創建區塊鏈並測試
    my_blockchain: Blockchain = Blockchain()
    print("創建創世區塊:", my_blockchain.get_latest_block())

    # 新增幾個區塊
    my_blockchain.add_block({"amount": 10, "sender": "Alice", "receiver": "Bob"})
    my_blockchain.add_block({"amount": 20, "sender": "Bob", "receiver": "Charlie"})

    print("區塊鏈長度:", len(my_blockchain.chain))
    print("區塊鏈是否有效:", my_blockchain.is_chain_valid())

    # 篡改測試
    my_blockchain.chain[1].data = {"amount": 100, "sender": "Alice", "receiver": "Bob"}
    print("篡改後區塊鏈是否有效:", my_blockchain.is_chain_valid())
