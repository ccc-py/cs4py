"""
實用拜占庭容錯（Practical Byzantine Fault Tolerance, PBFT）實作
可容忍 f 個拜占庭節點，總節點數需 ≥ 3f+1
"""

from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class Phase(Enum):
    """PBFT 階段"""
    PRE_PREPARE = "pre-prepare"
    PREPARE = "prepare"
    COMMIT = "commit"
    REPLY = "reply"


class PBFTMessage:
    """PBFT 訊息類別"""

    def __init__(self, phase: Phase, sender: int, view: int, sequence: int, digest: str, data: Any = None) -> None:
        self.phase: Phase = phase
        self.sender: int = sender
        self.view: int = view
        self.sequence: int = sequence
        self.digest: str = digest
        self.data: Any = data

    def __repr__(self) -> str:
        return f"PBFTMessage({self.phase.value}, sender={self.sender})"


class PBFTNode:
    """PBFT 節點"""

    def __init__(self, node_id: int, is_byzantine: bool = False) -> None:
        self.node_id: int = node_id
        self.is_byzantine: bool = is_byzantine  # 拜占庭節點會亂發訊息
        self.view: int = 0
        self.sequence: int = 0
        self.logs: Dict[int, Dict[str, Any]] = {}  # sequence -> {pre_prepares, prepares, commits}
        self.prepared: Dict[int, bool] = {}
        self.committed: Dict[int, bool] = {}

    def init_log(self, sequence: int) -> None:
        """初始化日誌"""
        if sequence not in self.logs:
            self.logs[sequence] = {
                'pre_prepares': [],
                'prepares': [],
                'commits': []
            }

    def pre_prepare(self, primary_id: int, sequence: int, request: Any) -> Optional[PBFTMessage]:
        """主節點發送 pre-prepare 訊息"""
        if self.node_id != primary_id or self.is_byzantine:
            return None

        import hashlib
        digest: str = hashlib.sha256(str(request).encode()).hexdigest()
        msg: PBFTMessage = PBFTMessage(
            phase=Phase.PRE_PREPARE,
            sender=self.node_id,
            view=self.view,
            sequence=sequence,
            digest=digest,
            data=request
        )
        self.init_log(sequence)
        self.logs[sequence]['pre_prepares'].append(msg)
        return msg

    def prepare(self, msg: PBFTMessage) -> Optional[PBFTMessage]:
        """收到 pre-prepare 後發送 prepare 訊息"""
        if self.is_byzantine:
            return None

        self.init_log(msg.sequence)
        self.logs[msg.sequence]['pre_prepares'].append(msg)

        prepare_msg: PBFTMessage = PBFTMessage(
            phase=Phase.PREPARE,
            sender=self.node_id,
            view=msg.view,
            sequence=msg.sequence,
            digest=msg.digest
        )
        self.logs[msg.sequence]['prepares'].append(prepare_msg)
        return prepare_msg

    def commit(self, msg: PBFTMessage, prepare_count: int, total_nodes: int) -> Optional[PBFTMessage]:
        """收到足夠 prepare 後發送 commit 訊息"""
        if self.is_byzantine:
            return None

        f: int = (total_nodes - 1) // 3
        if prepare_count >= 2 * f:
            commit_msg: PBFTMessage = PBFTMessage(
                phase=Phase.COMMIT,
                sender=self.node_id,
                view=msg.view,
                sequence=msg.sequence,
                digest=msg.digest
            )
            self.logs[msg.sequence]['commits'].append(commit_msg)
            return commit_msg
        return None


class PBFT:
    """PBFT 共識系統"""

    def __init__(self, node_count: int, byzantine_nodes: List[int] = None) -> None:
        self.node_count: int = node_count
        self.f: int = (node_count - 1) // 3  # 可容忍的拜占庭節點數
        self.nodes: List[PBFTNode] = []
        self.primary_id: int = 0
        self.sequence: int = 0

        byzantine_set: set = set(byzantine_nodes or [])
        for i in range(node_count):
            self.nodes.append(PBFTNode(i, is_byzantine=(i in byzantine_set)))

    def run_consensus(self, request: Any) -> Tuple[bool, Dict[str, Any]]:
        """執行 PBFT 共識流程"""
        self.sequence += 1
        primary: PBFTNode = self.nodes[self.primary_id]

        # 階段 1: Pre-prepare
        pre_prepare_msg: Optional[PBFTMessage] = primary.pre_prepare(
            self.primary_id, self.sequence, request
        )

        if not pre_prepare_msg:
            return False, {"error": "Primary failed to pre-prepare"}

        # 階段 2: Prepare
        prepare_msgs: List[PBFTMessage] = []
        for node in self.nodes:
            if node.node_id != self.primary_id:
                msg: Optional[PBFTMessage] = node.prepare(pre_prepare_msg)
                if msg:
                    prepare_msgs.append(msg)

        # 檢查 prepare 數量
        prepare_count: int = len(prepare_msgs) + 1  # +1 包含 primary 的 pre-prepare

        # 階段 3: Commit
        commit_msgs: List[PBFTMessage] = []
        for node in self.nodes:
            msg: Optional[PBFTMessage] = node.commit(
                pre_prepare_msg, prepare_count, self.node_count
            )
            if msg:
                commit_msgs.append(msg)

        # 檢查 commit 數量
        commit_count: int = len(commit_msgs) + 1

        success: bool = commit_count > 2 * self.f
        return success, {
            "sequence": self.sequence,
            "prepare_count": prepare_count,
            "commit_count": commit_count,
            "required": 2 * self.f + 1,
            "success": success
        }


if __name__ == "__main__":
    # 建立 PBFT 系統：4 個節點，可容忍 1 個拜占庭節點
    pbft: PBFT = PBFT(node_count=4, byzantine_nodes=[3])
    print(f"PBFT 系統：{pbft.node_count} 個節點，可容忍 {pbft.f} 個拜占庭節點")

    # 執行共識
    request: str = "Transfer 10 BTC from Alice to Bob"
    success, result = pbft.run_consensus(request)

    print(f"\n共識請求: {request}")
    print(f"結果: {'成功' if success else '失敗'}")
    print(f"Prepare 數: {result['prepare_count']}/{pbft.node_count}")
    print(f"Commit 數: {result['commit_count']}/{pbft.node_count}")
    print(f"所需數量: {result['required']}")
