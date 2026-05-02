"""
Raft 共識演算法實作
實作領導者選舉與日誌複製
"""

from typing import List, Dict, Optional, Tuple
from enum import Enum
import random


class NodeState(Enum):
    """Raft 節點狀態"""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class RaftLog:
    """Raft 日誌條目"""

    def __init__(self, term: int, command: str) -> None:
        self.term: int = term
        self.command: str = command

    def __repr__(self) -> str:
        return f"Log(term={self.term}, cmd={self.command})"


class RaftNode:
    """Raft 節點"""

    def __init__(self, node_id: int) -> None:
        self.node_id: int = node_id
        self.state: NodeState = NodeState.FOLLOWER
        self.current_term: int = 0
        self.voted_for: Optional[int] = None
        self.log: List[RaftLog] = []
        self.commit_index: int = 0
        self.last_applied: int = 0

        # 領導者相關
        self.leader_id: Optional[int] = None
        self.next_index: Dict[int, int] = {}
        self.match_index: Dict[int, int] = {}

    def start_election(self, nodes: List['RaftNode']) -> bool:
        """開始選舉，請求其他節點投票"""
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        votes: int = 1  # 自己投給自己

        for node in nodes:
            if node.node_id != self.node_id:
                # 模擬請求投票
                if node.handle_vote_request(self.current_term, self.node_id, len(self.log), self.get_last_log_term()):
                    votes += 1

        # 取得多數票則成為領導者
        if votes > len(nodes) // 2:
            self.state = NodeState.LEADER
            self.leader_id = self.node_id
            # 初始化 next_index 和 match_index
            for node in nodes:
                if node.node_id != self.node_id:
                    self.next_index[node.node_id] = len(self.log) + 1
                    self.match_index[node.node_id] = 0
            return True
        else:
            self.state = NodeState.FOLLOWER
            return False

    def handle_vote_request(self, term: int, candidate_id: int, last_log_index: int, last_log_term: int) -> bool:
        """處理投票請求"""
        if term < self.current_term:
            return False

        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.state = NodeState.FOLLOWER

        if self.voted_for is None or self.voted_for == candidate_id:
            # 檢查日誌是否至少一樣新
            my_last_term: int = self.get_last_log_term()
            if last_log_term > my_last_term or (last_log_term == my_last_term and last_log_index >= len(self.log)):
                self.voted_for = candidate_id
                return True

        return False

    def append_log(self, term: int, command: str) -> bool:
        """附加日誌條目（僅領導者調用）"""
        if self.state != NodeState.LEADER:
            return False
        self.log.append(RaftLog(term, command))
        return True

    def replicate_log(self, nodes: List['RaftNode'], entry: RaftLog) -> int:
        """複製日誌到其他節點，返回成功複製的節點數"""
        success_count: int = 1  # 自己

        for node in nodes:
            if node.node_id != self.node_id:
                # 模擬日誌複製
                if node.handle_append_entries(self.current_term, self.node_id, len(self.log) - 1, self.get_last_log_term(), [entry]):
                    success_count += 1
                    self.match_index[node.node_id] = len(node.log)
                    self.next_index[node.node_id] = len(node.log) + 1

        # 如果多數節點複製成功，則提交
        if success_count > len(nodes) // 2:
            self.commit_index = len(self.log)

        return success_count

    def handle_append_entries(self, term: int, leader_id: int, prev_log_index: int, prev_log_term: int, entries: List[RaftLog]) -> bool:
        """處理附加日誌請求"""
        if term < self.current_term:
            return False

        self.state = NodeState.FOLLOWER
        self.leader_id = leader_id
        self.current_term = term

        # 檢查前一個日誌是否匹配
        if prev_log_index >= 0:
            if prev_log_index >= len(self.log) or self.log[prev_log_index].term != prev_log_term:
                return False

        # 附加新日誌
        for entry in entries:
            self.log.append(entry)

        return True

    def get_last_log_term(self) -> int:
        """取得最後一條日誌的任期"""
        if not self.log:
            return 0
        return self.log[-1].term


class Raft:
    """Raft 共識系統"""

    def __init__(self, node_count: int) -> None:
        self.nodes: List[RaftNode] = [RaftNode(i) for i in range(node_count)]
        self.node_count: int = node_count

    def run_election(self) -> Optional[RaftNode]:
        """執行選舉，返回新的領導者"""
        # 隨機選一個節點發起選舉
        starter: RaftNode = random.choice(self.nodes)
        if starter.start_election(self.nodes):
            return starter
        return None

    def replicate_command(self, leader: RaftNode, command: str) -> Tuple[bool, int]:
        """透過領導者複製命令"""
        term: int = leader.current_term
        entry: RaftLog = RaftLog(term, command)
        leader.append_log(term, command)
        success_count: int = leader.replicate_log(self.nodes, entry)
        return success_count > self.node_count // 2, success_count


if __name__ == "__main__":
    # 建立 Raft 系統
    raft: Raft = Raft(node_count=5)
    print(f"Raft 系統：{raft.node_count} 個節點")

    # 執行選舉
    leader: Optional[RaftNode] = raft.run_election()
    if leader:
        print(f"選舉成功！領導者: Node {leader.node_id}, 任期: {leader.current_term}")
    else:
        print("選舉失敗！")

    # 複製命令
    if leader:
        command: str = "SET x = 100"
        success, count = raft.replicate_command(leader, command)
        print(f"\n複製命令: {command}")
        print(f"結果: {'成功' if success else '失敗'}")
        print(f"成功節點數: {count}/{raft.node_count}")

        # 查看領導者的日誌
        print(f"\n領導者日誌: {leader.log}")
