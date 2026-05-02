"""
分散式演算法 - 三階段提交 (Three-Phase Commit, 3PC)

2PC 的非阻塞改進版，透過加入 PRE-COMMIT 階段避免阻塞。
"""

from typing import List, Dict, Tuple
from enum import Enum
import random


class Vote(Enum):
    """參與者的投票"""
    YES = "YES"
    NO = "NO"


class TransactionState(Enum):
    """交易狀態"""
    INIT = "INIT"
    VOTING = "VOTING"
    PRE_COMMITTED = "PRE_COMMITTED"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTTED"


class Participant3PC:
    """3PC 的參與者"""
    
    def __init__(self, pid: int, fail_rate: float = 0.0):
        """
        初始化參與者
        
        Args:
            pid: 參與者 ID
            fail_rate: 模擬失敗機率
        """
        self.id = pid
        self.state = TransactionState.INIT
        self.can_commit = True
        self.fail_rate = fail_rate
    
    def prepare(self) -> Vote:
        """第一階段：準備投票"""
        if random.random() < self.fail_rate:
            self.can_commit = False
        
        if self.can_commit:
            self.state = TransactionState.VOTING
            return Vote.YES
        else:
            self.state = TransactionState.VOTING
            return Vote.NO
    
    def pre_commit(self) -> bool:
        """第二階段：PRE-COMMIT"""
        if self.state == TransactionState.VOTING:
            self.state = TransactionState.PRE_COMMITTED
            return True
        return False
    
    def commit(self) -> bool:
        """第三階段：COMMIT"""
        if self.state == TransactionState.PRE_COMMITTED:
            self.state = TransactionState.COMMITTED
            return True
        return False
    
    def abort(self) -> bool:
        """中止交易"""
        if self.state in [TransactionState.VOTING, TransactionState.PRE_COMMITTED]:
            self.state = TransactionState.ABORTED
            return True
        return False


class Coordinator3PC:
    """3PC 的協調者"""
    
    def __init__(self, coordinator_id: int):
        """初始化協調者"""
        self.id = coordinator_id
        self.state = TransactionState.INIT
        self.votes: List[Vote] = []
    
    def phase1_prepare(self, participants: List[Participant3PC]) -> bool:
        """第一階段：收集投票"""
        self.state = TransactionState.VOTING
        self.votes = [p.prepare() for p in participants]
        return all(v == Vote.YES for v in self.votes)
    
    def phase2_pre_commit(self, participants: List[Participant3PC]) -> bool:
        """第二階段：發送 PRE-COMMIT"""
        if self.state != TransactionState.VOTING:
            return False
        
        self.state = TransactionState.PRE_COMMITTED
        for p in participants:
            p.pre_commit()
        return True
    
    def phase3_commit(self, participants: List[Participant3PC]) -> bool:
        """第三階段：發送 COMMIT"""
        if self.state != TransactionState.PRE_COMMITTED:
            return False
        
        self.state = TransactionState.COMMITTED
        for p in participants:
            p.commit()
        return True
    
    def abort(self, participants: List[Participant3PC]) -> bool:
        """中止交易"""
        self.state = TransactionState.ABORTED
        for p in participants:
            p.abort()
        return True


class ThreePhaseCommit:
    """3PC 協定的事件驅動模擬"""
    
    def __init__(self, coordinator_id: int, participant_ids: List[int]):
        """初始化 3PC 模擬"""
        self.coordinator = Coordinator3PC(coordinator_id)
        self.participants: Dict[int, Participant3PC] = {}
        for pid in participant_ids:
            self.participants[pid] = Participant3PC(pid)
        self.log: List[str] = []
    
    def execute_transaction(self) -> Tuple[bool, str]:
        """
        執行完整 3PC 交易
        
        Returns:
            (是否成功, 結果訊息)
        """
        participants = list(self.participants.values())
        
        # 第一階段
        self.log.append("=== 第一階段：PREPARE ===")
        all_yes = self.coordinator.phase1_prepare(participants)
        self.log.append(f"投票: {[v.value for v in self.coordinator.votes]}")
        
        if not all_yes:
            self.log.append("=== 中止交易 ===")
            self.coordinator.abort(participants)
            return False, "ABORTED"
        
        # 第二階段
        self.log.append("=== 第二階段：PRE-COMMIT ===")
        self.coordinator.phase2_pre_commit(participants)
        
        # 第三階段
        self.log.append("=== 第三階段：COMMIT ===")
        self.coordinator.phase3_commit(participants)
        
        for pid, p in self.participants.items():
            self.log.append(f"參與者 {pid}: {p.state.value}")
        
        return True, "COMMITTED"
    
    def get_log(self) -> List[str]:
        """取得日誌"""
        return self.log


if __name__ == "__main__":
    random.seed(42)
    
    print("=== 三階段提交 (3PC) 示範 ===")
    
    # 成功情況
    print("\n--- 情況 1：成功提交 ---")
    tpc = ThreePhaseCommit(coordinator_id=0, participant_ids=[1, 2, 3])
    success, msg = tpc.execute_transaction()
    print(f"結果: {msg}")
    for line in tpc.get_log():
        print(f"  {line}")
    
    # 失敗情況
    print("\n--- 情況 2：參與者拒絕 ---")
    tpc2 = ThreePhaseCommit(coordinator_id=0, participant_ids=[1, 2, 3])
    tpc2.participants[2].can_commit = False
    success, msg = tpc2.execute_transaction()
    print(f"結果: {msg}")
    
    print("\n3PC vs 2PC:")
    print("1. 加入 PRE-COMMIT 階段，避免阻塞")
    print("2. 協調者失效時，參與者可逾時後自行決定")
    print("3. 需要可靠的網路（無網路分區）")
