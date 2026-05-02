"""
分散式演算法 - 環狀選舉演算法 (Ring Election Algorithm)

在邏輯環狀拓撲中選舉領導者，使用令牌傳遞方式。
"""

from typing import List, Dict, Optional


class RingNode:
    """環狀拓撲中的節點"""
    
    def __init__(self, node_id: int, next_node_id: int):
        """
        初始化節點
        
        Args:
            node_id: 節點 ID
            next_node_id: 環中下一個節點的 ID
        """
        self.id = node_id
        self.next_id = next_node_id
        self.active = True
        self.leader_id: Optional[int] = None
        self.election_in_progress = False
        self.received_election_ids: List[int] = []
    
    def initiate_election(self, nodes: Dict[int, 'RingNode']) -> None:
        """發起選舉：發送包含自己 ID 的 ELECTION 訊息"""
        if not self.active:
            return
        self.election_in_progress = True
        self.received_election_ids = [self.id]
        self._send_election_message(self.id, nodes)
    
    def _send_election_message(self, candidate_id: int, 
                               nodes: Dict[int, 'RingNode']) -> None:
        """發送 ELECTION 訊息給下一個節點"""
        if self.next_id in nodes and nodes[self.next_id].active:
            nodes[self.next_id].receive_election(candidate_id, nodes)
    
    def receive_election(self, candidate_id: int, 
                         nodes: Dict[int, 'RingNode']) -> None:
        """接收 ELECTION 訊息"""
        if not self.active:
            return
        
        if not self.election_in_progress:
            # 第一次收到選舉訊息
            self.election_in_progress = True
            self.received_election_ids = [candidate_id]
            # 轉發給下一個節點
            if self.next_id in nodes and nodes[self.next_id].active:
                nodes[self.next_id].receive_election(candidate_id, nodes)
        else:
            # 已經在選舉中
            if candidate_id not in self.received_election_ids:
                self.received_election_ids.append(candidate_id)
                # 檢查是否完成一輪
                if len(self.received_election_ids) == len([n for n in nodes.values() if n.active]):
                    # 選舉完成，選出 ID 最大的
                    leader = max(self.received_election_ids)
                    self._send_coordinator(leader, nodes)
                else:
                    # 繼續轉發
                    if self.next_id in nodes and nodes[self.next_id].active:
                        nodes[self.next_id].receive_election(candidate_id, nodes)
    
    def _send_coordinator(self, leader_id: int, 
                          nodes: Dict[int, 'RingNode']) -> None:
        """發送 COORDINATOR 訊息"""
        self.leader_id = leader_id
        self.election_in_progress = False
        if self.next_id in nodes and nodes[self.next_id].active:
            nodes[self.next_id].receive_coordinator(leader_id, nodes)
    
    def receive_coordinator(self, leader_id: int, 
                            nodes: Dict[int, 'RingNode']) -> None:
        """接收 COORDINATOR 訊息"""
        if not self.active:
            return
        self.leader_id = leader_id
        self.election_in_progress = False
        # 轉發給下一個節點（直到回到起點）
        if self.next_id in nodes and nodes[self.next_id].active:
            if nodes[self.next_id].leader_id != leader_id:
                nodes[self.next_id].receive_coordinator(leader_id, nodes)


class RingElection:
    """環狀選舉演算法的事件驅動模擬"""
    
    def __init__(self, node_ids: List[int]):
        """
        初始化邏輯環
        
        Args:
            node_ids: 節點 ID 列表（按順序形成環）
        """
        self.node_ids = sorted(node_ids)
        self.nodes: Dict[int, RingNode] = {}
        
        # 建立環：每個節點指向下一個
        n = len(self.node_ids)
        for i, nid in enumerate(self.node_ids):
            next_id = self.node_ids[(i + 1) % n]
            self.nodes[nid] = RingNode(nid, next_id)
    
    def start_election(self, starter_id: int) -> None:
        """從指定節點開始選舉"""
        if starter_id not in self.nodes or not self.nodes[starter_id].active:
            return
        self.nodes[starter_id].initiate_election(self.nodes)
    
    def get_leader(self) -> Optional[int]:
        """取得當前領導者"""
        for node in self.nodes.values():
            if node.active and node.leader_id is not None:
                return node.leader_id
        return None
    
    def simulate_full_election(self, starter_id: int) -> int:
        """
        模擬完整選舉過程（簡化版）
        
        Args:
            starter_id: 發起選舉的節點
            
        Returns:
            選出的領導者 ID
        """
        if starter_id not in self.nodes or not self.nodes[starter_id].active:
            return -1
        
        # 收集所有活躍節點 ID
        active_ids = sorted([nid for nid in self.node_ids 
                            if nid in self.nodes and self.nodes[nid].active])
        
        # 選出最大 ID
        leader = max(active_ids)
        
        # 通知所有節點
        for nid in active_ids:
            self.nodes[nid].leader_id = leader
            self.nodes[nid].election_in_progress = False
        
        return leader


if __name__ == "__main__":
    print("=== 環狀選舉演算法示範 ===")
    
    # 創建環: 0 → 1 → 2 → 3 → 4 → 0
    ring = RingElection([0, 1, 2, 3, 4])
    
    print("邏輯環: 0 → 1 → 2 → 3 → 4 → 0")
    print("\n從節點 2 發起選舉...")
    leader = ring.simulate_full_election(2)
    print(f"選出的領導者: {leader}")
    
    # 節點失效情況
    print("\n--- 節點 4 失效 ---")
    ring.nodes[4].active = False
    leader = ring.simulate_full_election(2)
    print(f"選出的領導者: {leader}")
    
    print("\n環狀選舉演算法特點:")
    print("1. 節點按 ID 排序形成邏輯環")
    print("2. ELECTION 訊息繞環傳遞，收集候選 ID")
    print("3. 完成一輪後，選出 ID 最大的節點")
    print("4. COORDINATOR 訊息通知所有節點")
    print("\n訊息複雜度: O(n log n) 到 O(n²) 取決於實作")
