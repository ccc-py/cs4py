"""
權益證明（Proof of Stake, PoS）實作
基於持幣權重隨機選擇驗證者
"""

import random
from typing import List, Dict, Optional


class Validator:
    """驗證者類別，包含權益資訊"""

    def __init__(self, address: str, stake: float) -> None:
        self.address: str = address
        self.stake: float = stake
        self.is_active: bool = True

    def __repr__(self) -> str:
        return f"Validator({self.address}, stake={self.stake})"


class ProofOfStake:
    """權益證明共識機制"""

    def __init__(self) -> None:
        self.validators: List[Validator] = []
        self.total_stake: float = 0.0

    def add_validator(self, address: str, stake: float) -> None:
        """新增驗證者"""
        validator: Validator = Validator(address, stake)
        self.validators.append(validator)
        self.total_stake += stake

    def remove_validator(self, address: str) -> None:
        """移除驗證者"""
        for v in self.validators:
            if v.address == address:
                self.total_stake -= v.stake
                self.validators.remove(v)
                break

    def select_validator(self) -> Optional[Validator]:
        """
        根據權益權重隨機選擇驗證者
        權益越高，被選中的機率越大
        """
        if not self.validators or self.total_stake == 0:
            return None

        # 產生一個隨機數
        r: float = random.uniform(0, self.total_stake)
        cumulative: float = 0.0

        for validator in self.validators:
            cumulative += validator.stake
            if cumulative >= r:
                return validator

        return self.validators[-1]  # 保底

    def get_validator_probability(self, address: str) -> float:
        """計算驗證者被選中的機率"""
        for v in self.validators:
            if v.address == address:
                return v.stake / self.total_stake if self.total_stake > 0 else 0
        return 0.0


if __name__ == "__main__":
    # 建立 PoS 系統
    pos: ProofOfStake = ProofOfStake()

    # 新增驗證者
    pos.add_validator("Alice", 100.0)
    pos.add_validator("Bob", 200.0)
    pos.add_validator("Charlie", 700.0)

    print("驗證者列表:")
    for v in pos.validators:
        prob: float = pos.get_validator_probability(v.address)
        print(f"  {v.address}: stake={v.stake}, 選中機率={prob:.2%}")

    # 模擬多次選擇
    print("\n模擬 10 次驗證者選擇:")
    selection_count: Dict[str, int] = {"Alice": 0, "Bob": 0, "Charlie": 0}
    for _ in range(1000):
        selected: Optional[Validator] = pos.select_validator()
        if selected:
            selection_count[selected.address] += 1

    for addr, count in selection_count.items():
        print(f"  {addr}: 被選中 {count} 次 ({count/10:.1f}%)")
