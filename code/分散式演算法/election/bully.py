"""
分散式演算法 - Bully 演算法（霸道演算法）

在分散式系統中選舉領導者，優先權最高（ID 最大）的節點獲勝。
"""

from typing import List, Dict, Optional
import random


class Node:
    """分散式系統中的節點"""
    
    def __init__(self, node_id: int, total_nodes: int):
        """
        初始化節點
        
        Args:
            node_id: 節點 ID（越大優先權越高）
            total_nodes: 系統中總節點數
        """
        self.id = node_id
        self.total_nodes = total_nodes
        self.leader_id: Optional[int] = None
        self.active = True
        self.election_in_progress = False
        self.received_messages: List[str] = []
    
    def send_message(self, to_id: int, msg_type: str, 
                    nodes: Dict[int, 'Node']) -> None:
        """模擬發送訊息給其他節點"""
        if to_id in nodes and nodes[to_id].active:
            nodes[to_id].receive_message(self.id, msg_type)
    
    def receive_message(self, from_id: int, msg_type: str) -> None:
        """接收訊息"""
        if not self.active:
            return
        self.received_messages.append(f"{msg_type} from {from_id}")
        
        if msg_type == "ELECTION":
            self.handle_election(from_id)
        elif msg_type == "OK":
            self.handle_ok(from_id)
        elif msg_type == "COORDINATOR":
            self.handle_coordinator(from_id)
    
    def start_election(self, nodes: Dict[int, 'Node']) -> None:
        """啟動選舉"""
        if not self.active or self.election_in_progress:
            return
        
        self.election_in_progress = True
        self.received_messages = []
        
        # 向所有 ID 更大的節點發送 ELECTION 訊息
        higher_nodes = [nid for nid in range(self.id + 1, self.total_nodes) 
                       if nid in nodes and nodes[nid].active]
        
        if not higher_nodes:
            # 沒有更大 ID 的節點，自己當領導
            self.become_leader(nodes)
        else:
            for nid in higher_nodes:
                self.send_message(nid, "ELECTION", nodes)
    
    def handle_election(self, from_id: int) -> None:
        """處理 ELECTION 訊息"""
        if not self.active:
            return
        # 回覆 OK
        nodes = {}  # 簡化：實際應該有節點字典
        # 啟動自己的選舉（如果還沒開始）
        self.election_in_progress = True
    
    def become_leader(self, nodes: Dict[int, 'Node']) -> None:
        """成為領導者"""
        self.leader_id = self.id
        self.election_in_progress = False
        # 廣播 COORDINATOR 訊息
        for nid in range(self.total_nodes):
            if nid != self.id and nid in nodes and nodes[nid].active:
                self.send_message(nid, "COORDINATOR", nodes)
    
    def handle_coordinator(self, from_id: int) -> None:
        """處理 COORDINATOR 訊息"""
        self.leader_id = from_id
        self.election_in_progress = False


def simulate_bully_election(nodes: Dict[int, 'Node'], starter_id: int) -> int:
    """
    模擬 Bully 演算法選舉
    
    Args:
        nodes: 節點字典
        starter_id: 發起選舉的節點 ID
        
    Returns:
        選出的領導者 ID
    """
    if starter_id not in nodes or not nodes[starter_id].active:
        return -1
    
    nodes[starter_id].start_election(nodes)
    
    # 找出領導者（所有節點應該都有相同的 leader_id）
    for node in nodes.values():
        if node.active and node.leader_id is not None:
            return node.leader_id
    return -1


class EventDrivenBully:
    """事件驅動的 Bully 演算法模擬"""
    
    def __init__(self, node_ids: List[int]):
        """
        初始化模擬
        
        Args:
            node_ids: 節點 ID 列表（ID 越大優先權越高）
        """
        self.nodes: Dict[int, Node] = {}
        self.messages: List[tuple] = []  # (from, to, type)
        self.node_ids = sorted(node_ids)
        self.max_id = max(node_ids)
        
        for nid in node_ids:
            self.nodes[nid] = Node(nid, self.max_id + 1)
    
    def start_election(self, starter_id: int) -> None:
        """從指定節點開始選舉"""
        if starter_id not in self.nodes or not self.nodes[starter_id].active:
            return
        
        starter = self.nodes[starter_id]
        starter.election_in_progress = True
        
        # 向所有 ID 更大的活躍節點發送 ELECTION
        higher = [nid for nid in self.node_ids if nid > starter_id 
                  and nid in self.nodes and self.nodes[nid].active]
        
        if not higher:
            # 沒有更高 ID，自己當 leader
            self._become_leader(starter_id)
        else:
            for nid in higher:
                self.messages.append((starter_id, nid, "ELECTION"))
    
    def _become_leader(self, node_id: int) -> None:
        """節點成為 leader"""
        self.nodes[node_id].leader_id = node_id
        self.nodes[node_id].election_in_progress = False
        # 廣播給所有其他活躍節點
        for nid in self.node_ids:
            if nid != node_id and self.nodes[nid].active:
                self.messages.append((node_id, nid, "COORDINATOR"))
    
    def process_messages(self) -> None:
        """處理所有訊息"""
        while self.messages:
            from_id, to_id, msg_type = self.messages.pop(0)
            if not self.nodes[to_id].active:
                continue
            
            if msg_type == "ELECTION":
                # 較高 ID 節點收到 ELECTION
                # 回覆 OK（簡化省略）
                # 該節點也啟動自己的選舉
                if self.nodes[to_id].election_in_progress:
                    continue
                self.start_election(to_id)
            elif msg_type == "COORDINATOR":
                self.nodes[to_id].leader_id = from_id
                self.nodes[to_id].election_in_progress = False
    
    def get_leader(self) -> Optional[int]:
        """取得當前領導者"""
        for node in self.nodes.values():
            if node.active and node.leader_id is not None:
                return node.leader_id
        return None


if __name__ == "__main__":
    print("=== Bully 演算法示範 ===")
    
    # 創建 5 個節點，ID 0-4
    bully = EventDrivenBully([0, 1, 2, 3, 4])
    
    print("節點: [0, 1, 2, 3, 4] (4 優先權最高)")
    print("\n從節點 2 發起選舉...")
    bully.start_election(2)
    bully.process_messages()
    print(f"選出的領導者: {bully.get_leader()}")
    
    # 如果最高 ID 節點失效
    print("\n--- 節點 4 失效，重新選舉 ---")
    bully.nodes[4].active = False
    bully = EventDrivenBully([0, 1, 2, 3])  # 重新建立（簡化）
    bully.start_election(2)
    bully.process_messages()
    print(f"選出的領導者: {bully.get_leader()}")
    
    print("\nBully 演算法規則:")
    print("1. 發起選舉時，向所有 ID 更大的節點發送 ELECTION")
    print("2. 若有回應，等待該節點發起選舉")
    print("3. 若無更大 ID 節點，宣布自己為 leader")
    print("4. 收到 COORDINATOR 訊息的節點接受該 leader")
