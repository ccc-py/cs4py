"""
Paxos 共識演算法實作
含提議者、接受者、學習者三種角色
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PaxosRole(Enum):
    """Paxos 角色"""
    PROPOSER = "proposer"
    ACCEPTOR = "acceptor"
    LEARNER = "learner"


@dataclass
class PaxosValue:
    """Paxos 值"""
    value: str
    proposer_id: int


class PaxosMessage:
    """Paxos 訊息"""

    def __init__(self, msg_type: str, proposal_number: Tuple[int, int], value: Optional[str] = None, accepted_by: List[int] = None) -> None:
        self.msg_type: str = msg_type  # prepare, promise, accept, accepted
        self.proposal_number: Tuple[int, int] = proposal_number  # (round, proposer_id)
        self.value: Optional[str] = value
        self.accepted_by: List[int] = accepted_by or []


class Acceptor:
    """接受者，負責接受提議"""

    def __init__(self, acceptor_id: int) -> None:
        self.acceptor_id: int = acceptor_id
        self.promised_number: Optional[Tuple[int, int]] = None
        self.accepted_number: Optional[Tuple[int, int]] = None
        self.accepted_value: Optional[str] = None

    def handle_prepare(self, proposal_number: Tuple[int, int]) -> Optional[PaxosMessage]:
        """處理 prepare 請求，返回 promise 或拒絕"""
        if self.promised_number is None or proposal_number > self.promised_number:
            self.promised_number = proposal_number
            return PaxosMessage(
                msg_type="promise",
                proposal_number=proposal_number,
                value=self.accepted_value
            )
        return None  # 拒絕

    def handle_accept(self, proposal_number: Tuple[int, int], value: str) -> Optional[PaxosMessage]:
        """處理 accept 請求，返回 accepted"""
        if self.promised_number is None or proposal_number >= self.promised_number:
            self.promised_number = proposal_number
            self.accepted_number = proposal_number
            self.accepted_value = value
            return PaxosMessage(
                msg_type="accepted",
                proposal_number=proposal_number,
                value=value,
                accepted_by=[self.acceptor_id]
            )
        return None


class Proposer:
    """提議者，提出值並推動共識"""

    def __init__(self, proposer_id: int) -> None:
        self.proposer_id: int = proposer_id
        self.proposal_number: Tuple[int, int] = (0, proposer_id)
        self.value: Optional[str] = None

    def prepare(self, round_num: int) -> PaxosMessage:
        """發送 prepare 請求"""
        self.proposal_number = (round_num, self.proposer_id)
        return PaxosMessage(
            msg_type="prepare",
            proposal_number=self.proposal_number
        )

    def handle_promise(self, promises: List[PaxosMessage], proposers: List['Proposer']) -> Optional[PaxosMessage]:
        """處理 promise 回應，決定要提議的值"""
        if len(promises) <= len(proposers) // 2:
            return None  # 未獲得多數

        # 找出已接受的最高編號提議的值
        max_number: Tuple[int, int] = (-1, -1)
        chosen_value: Optional[str] = None

        for promise in promises:
            if promise.value and promise.proposal_number and promise.proposal_number > max_number:
                max_number = promise.proposal_number
                chosen_value = promise.value

        # 如果沒有已接受的值，使用自己的值
        if chosen_value is None:
            chosen_value = self.value

        return PaxosMessage(
            msg_type="accept",
            proposal_number=self.proposal_number,
            value=chosen_value
        )

    def handle_accepted(self, accepted_msgs: List[PaxosMessage]) -> Optional[str]:
        """處理 accepted 回應，確認共識達成"""
        if len(accepted_msgs) > len(accepted_msgs) // 2:
            return accepted_msgs[0].value
        return None


class Learner:
    """學習者，學習已達成共識的值"""

    def __init__(self, learner_id: int) -> None:
        self.learner_id: int = learner_id
        self.learned_value: Optional[str] = None

    def learn(self, accepted_msgs: List[PaxosMessage]) -> Optional[str]:
        """從 accepted 訊息中學習值"""
        value_count: Dict[str, int] = {}
        for msg in accepted_msgs:
            if msg.value:
                value_count[msg.value] = value_count.get(msg.value, 0) + 1

        # 找出最多人接受的值
        for value, count in value_count.items():
            if count > len(accepted_msgs) // 2:
                self.learned_value = value
                return value
        return None


class Paxos:
    """Paxos 共識系統"""

    def __init__(self, proposer_count: int, acceptor_count: int, learner_count: int) -> None:
        self.proposers: List[Proposer] = [Proposer(i) for i in range(proposer_count)]
        self.acceptors: List[Acceptor] = [Acceptor(i) for i in range(acceptor_count)]
        self.learners: List[Learner] = [Learner(i) for i in range(learner_count)]

    def run_paxos(self, proposer: Proposer, value: str, round_num: int) -> Tuple[bool, Optional[str]]:
        """執行一次 Paxos 共識流程"""
        proposer.value = value

        # 階段 1: Prepare
        prepare_msg: PaxosMessage = proposer.prepare(round_num)
        promises: List[PaxosMessage] = []

        for acceptor in self.acceptors:
            promise: Optional[PaxosMessage] = acceptor.handle_prepare(prepare_msg.proposal_number)
            if promise:
                promises.append(promise)

        # 階段 2: Accept
        accept_msg: Optional[PaxosMessage] = proposer.handle_promise(promises, self.proposers)
        if not accept_msg:
            return False, None

        accepted_msgs: List[PaxosMessage] = []
        for acceptor in self.acceptors:
            accepted: Optional[PaxosMessage] = acceptor.handle_accept(accept_msg.proposal_number, accept_msg.value)
            if accepted:
                accepted_msgs.append(accepted)

        # 學習結果
        learner: Learner = self.learners[0]
        result: Optional[str] = learner.learn(accepted_msgs)

        return result is not None, result


if __name__ == "__main__":
    # 建立 Paxos 系統
    paxos: Paxos = Paxos(proposer_count=1, acceptor_count=3, learner_count=1)
    print(f"Paxos 系統：{len(paxos.proposers)} 個提議者，{len(paxos.acceptors)} 個接受者")

    # 執行共識
    proposer: Proposer = paxos.proposers[0]
    value: str = "SET x = 100"

    success, result = paxos.run_paxos(proposer, value, round_num=1)

    print(f"\n提議值: {value}")
    print(f"共識結果: {'成功' if success else '失敗'}")
    print(f"達成共識的值: {result}")
