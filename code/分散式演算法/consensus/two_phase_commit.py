"""
分散式演算法 - 兩階段提交 (Two-Phase Commit, 2PC)

分散式交易中的協調協定，確保所有參與者一致提交或中止。
"""

from typing import List, Dict, Optional, Tuple
from enum import Enum


class Vote(Enum):
    """參與者的投票"""
    YES = "YES"
    NO = "NO"


class TransactionState(Enum):
    """交易狀態"""
    INIT = "INIT"
    VOTING = "VOTING"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


class Participant:
    """2PC 的參與者"""
    
    def __init__(self, pid: int, fail_rate: float = 0.0):
        """
        初始化參與者
        
        Args:
            pid: 參與者 ID
            fail_rate: 模擬失敗機率（用於演示）
        """
        self.id = pid
        self.state = TransactionState.INIT
        self.can_commit = True
        self.fail_rate = fail_rate
    
    def prepare(self) -> Vote:
        """
        準備階段：決定是否同意提交
        
        Returns:
            YES 或 NO 投票
        """
        import random
        if random.random() < self.fail_rate:
            self.can_commit = False
        
        if self.can_commit:
            self.state = TransactionState.VOTING
            return Vote.YES
        else:
            self.state = TransactionState.VOTING
            return Vote.NO
    
    def commit(self) -> bool:
        """
        提交交易
        
        Returns:
            是否成功提交
        """
        if self.state == TransactionState.VOTING:
            self.state = TransactionState.COMMITTED
            return True
        return False
    
    def abort(self) -> bool:
        """
        中止交易
        
        Returns:
            是否成功中止
        """
        if self.state == TransactionState.VOTING:
            self.state = TransactionState.ABORTED
            return True
        return False


class Coordinator:
    """2PC 的協調者"""
    
    def __init__(self, coordinator_id: int):
        """
        初始化協調者
        
        Args:
            coordinator_id: 協調者 ID
        """
        self.id = coordinator_id
        self.state = TransactionState.INIT
        self.votes: List[Vote] = []
    
    def phase1_prepare(self, participants: List[Participant]) -> bool:
        """
        第一階段：發送 PREPARE，收集投票
        
        Args:
            participants: 所有參與者列表
            
        Returns:
            True 如果所有參與者都投票 YES
        """
        self.state = TransactionState.VOTING
        self.votes = []
        
        for p in participants:
            vote = p.prepare()
            self.votes.append(vote)
        
        return all(v == Vote.YES for v in self.votes)
    
    def phase2_decide(self, participants: List[Participant]) -> Tuple[bool, str]:
        """
        第二階段：根據投票決定 COMMIT 或 ABORT
        
        Args:
            participants: 所有參與者列表
            
        Returns:
            (是否提交, 狀態訊息)
        """
        all_yes = all(v == Vote.YES for v in self.votes)
        
        if all_yes:
            for p in participants:
                p.commit()
            self.state = TransactionState.COMMITTED
            return True, "COMMITTED"
        else:
            for p in participants:
                p.abort()
            self.state = TransactionState.ABORTED
            return False, "ABORTED"


class TwoPhaseCommit:
    """2PC 協定的事件驅動模擬"""
    
    def __init__(self, coordinator_id: int, participant_ids: List[int]):
        """
        初始化 2PC 模擬
        
        Args:
            coordinator_id: 協調者 ID
            participant_ids: 參與者 ID 列表
        """
        self.coordinator = Coordinator(coordinator_id)
        self.participants: Dict[int, Participant] = {}
        for pid in participant_ids:
            self.participants[pid] = Participant(pid)
        self.log: List[str] = []
    
    def execute_transaction(self) -> Tuple[bool, str]:
        """
        執行完整交易
        
        Returns:
            (是否成功, 結果訊息)
        """
        participants = list(self.participants.values())
        
        # 第一階段
        self.log.append("=== 第一階段：PREPARE ===")
        all_yes = self.coordinator.phase1_prepare(participants)
        self.log.append(f"投票結果: {[v.value for v in self.coordinator.votes]}")
        
        # 第二階段
        self.log.append("=== 第二階段：DECIDE ===")
        success, msg = self.coordinator.phase2_decide(participants)
        
        for pid, p in self.participants.items():
            self.log.append(f"參與者 {pid}: {p.state.value}")
        
        return success, msg
    
    def get_log(self) -> List[str]:
        """取得執行日誌"""
        return self.log


if __name__ == "__main__":
    import random
    random.seed(42)
    
    print("=== 兩階段提交 (2PC) 示範 ===")
    
    # 正常情況
    print("\n--- 情況 1：所有參與者同意 ---")
    tpc1 = TwoPhaseCommit(coordinator_id=0, participant_ids=[1, 2, 3])
    success, msg = tpc1.execute_transaction()
    print(f"結果: {msg}")
    for line in tpc1.get_log():
        print(f"  {line}")
    
    # 有參與者拒絕
    print("\n--- 情況 2：某參與者拒絕 ---")
    tpc2 = TwoPhaseCommit(coordinator_id=0, participant_ids=[1, 2, 3])
    tpc2.participants[2].can_commit = False
    success, msg = tpc2.execute_transaction()
    print(f"結果: {msg}")
    
    print("\n2PC 特點:")
    print("1. 阻塞式協定：等待所有參與者回應")
    print("2. 無逾時機制，協調者失效會導致阻塞")
    print("3. 保證原子性：全有或全無")
