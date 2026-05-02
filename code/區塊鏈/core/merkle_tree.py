"""
Merkle Tree（默克爾樹）實作
用於高效驗證區塊中交易的完整性
"""

import hashlib
from typing import List, Optional, Tuple


class MerkleTree:
    """默克爾樹類別，建構雜湊樹並提供包含證明"""

    def __init__(self, data_blocks: List[str]) -> None:
        self.data_blocks: List[str] = data_blocks
        self.leaves: List[str] = [self._hash(block) for block in data_blocks]
        self.root: str = self._build_tree(self.leaves)

    def _hash(self, data: str) -> str:
        """計算資料的 SHA-256 雜湊值"""
        return hashlib.sha256(data.encode()).hexdigest()

    def _build_tree(self, leaves: List[str]) -> str:
        """遞迴建構默克爾樹，返回根雜湊值"""
        if not leaves:
            return self._hash("")
        
        if len(leaves) == 1:
            return leaves[0]

        # 如果節點數為奇數，複製最後一個節點
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])

        # 計算父節點
        parent_level: List[str] = []
        for i in range(0, len(leaves), 2):
            combined: str = leaves[i] + leaves[i + 1]
            parent_level.append(self._hash(combined))

        return self._build_tree(parent_level)

    def get_root(self) -> str:
        """取得默克爾樹根雜湊"""
        return self.root

    def get_proof(self, data: str) -> List[Tuple[str, bool]]:
        """
        取得資料在默克爾樹中的包含證明
        返回 [(hash, is_left), ...] 的列表
        """
        target_hash: str = self._hash(data)
        if target_hash not in self.leaves:
            return []

        proof: List[Tuple[str, bool]] = []
        level: List[str] = self.leaves[:]
        index: int = level.index(target_hash)

        while len(level) > 1:
            is_left: bool = index % 2 == 0
            sibling_index: int = index + 1 if is_left else index - 1

            if sibling_index < len(level):
                sibling_hash: str = level[sibling_index]
                proof.append((sibling_hash, is_left))

            # 計算下一層
            next_level: List[str] = []
            for i in range(0, len(level), 2):
                if i + 1 < len(level):
                    combined: str = level[i] + level[i + 1]
                    next_level.append(self._hash(combined))
                else:
                    next_level.append(level[i])
            
            index //= 2
            level = next_level

        return proof

    def verify_proof(self, data: str, proof: List[Tuple[str, bool]], root: str) -> bool:
        """驗證包含證明是否正確"""
        hash_value: str = self._hash(data)

        for sibling_hash, is_left in proof:
            if is_left:
                combined: str = hash_value + sibling_hash
            else:
                combined: str = sibling_hash + hash_value
            hash_value = self._hash(combined)

        return hash_value == root


if __name__ == "__main__":
    # 測試默克爾樹
    transactions: List[str] = ["tx1", "tx2", "tx3", "tx4"]
    merkle_tree: MerkleTree = MerkleTree(transactions)

    print("默克爾根:", merkle_tree.get_root())

    # 取得並驗證證明
    proof: List[Tuple[str, bool]] = merkle_tree.get_proof("tx2")
    print("tx2 的證明:", proof)
    print("驗證 tx2:", merkle_tree.verify_proof("tx2", proof, merkle_tree.get_root()))

    # 驗證不存在的交易
    print("驗證 tx5:", merkle_tree.verify_proof("tx5", proof, merkle_tree.get_root()))
