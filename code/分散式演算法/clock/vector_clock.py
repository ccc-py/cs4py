"""
分散式演算法 - 向量時鐘 (Vector Clock)

實作向量時鐘，用於在分散式系統中追蹤因果關係和並發事件。
"""

from typing import List, Dict, Tuple
from enum import Enum


class EventType(Enum):
    """事件類型"""
    LOCAL = "LOCAL"
    SEND = "SEND"
    RECEIVE = "RECEIVE"


class VectorClock:
    """向量時鐘"""
    
    def __init__(self, node_id: int, total_nodes: int):
        """
        初始化向量時鐘
        
        Args:
            node_id: 節點 ID
            total_nodes: 系統中總節點數
        """
        self.node_id = node_id
        self.vector = [0] * total_nodes
        self.total_nodes = total_nodes
        self.event_log: List[Tuple[str, List[int], EventType]] = []
    
    def local_event(self, description: str = "") -> List[int]:
        """
        發生本地事件
        
        Args:
            description: 事件描述
            
        Returns:
            當前向量時鐘副本
        """
        self.vector[self.node_id] += 1
        self.event_log.append((description or f"本地事件@{self.node_id}", 
                              self.vector.copy(), EventType.LOCAL))
        return self.vector.copy()
    
    def send_event(self, msg: str) -> Tuple[List[int], str]:
        """
        發送訊息事件
        
        Args:
            msg: 訊息內容
            
        Returns:
            (向量時鐘副本, 訊息)
        """
        self.vector[self.node_id] += 1
        self.event_log.append((f"發送: {msg}", 
                              self.vector.copy(), EventType.SEND))
        return self.vector.copy(), msg
    
    def receive_event(self, sender_vector: List[int], msg: str, 
                      sender_id: int) -> List[int]:
        """
        接收訊息事件
        
        Args:
            sender_vector: 發送者的向量時鐘
            msg: 訊息內容
            sender_id: 發送者 ID
            
        Returns:
            更新後的向量時鐘副本
        """
        # 逐元素取 max
        for i in range(self.total_nodes):
            self.vector[i] = max(self.vector[i], sender_vector[i])
        self.vector[self.node_id] += 1
        
        self.event_log.append((f"接收自 {sender_id}: {msg}", 
                              self.vector.copy(), EventType.RECEIVE))
        return self.vector.copy()
    
    def get_vector(self) -> List[int]:
        """取得當前向量時鐘"""
        return self.vector.copy()


def compare_vectors(v1: List[int], v2: List[int]) -> str:
    """
    比較兩個向量時鐘的關係
    
    Args:
        v1: 向量時鐘 1
        v2: 向量時鐘 2
        
    Returns:
        '<' 表示 v1 因果先於 v2
        '>' 表示 v2 因果先於 v1
        '=' 表示相等
        '|' 表示並發
    """
    le = all(v1[i] <= v2[i] for i in range(len(v1)))
    ge = all(v1[i] >= v2[i] for i in range(len(v1)))
    eq = all(v1[i] == v2[i] for i in range(len(v1)))
    
    if eq:
        return '='
    elif le:
        return '<'
    elif ge:
        return '>'
    else:
        return '|'  # 並發


def happens_before(v1: List[int], v2: List[int]) -> bool:
    """
    判斷 v1 是否因果先於 v2（嚴格）
    
    Args:
        v1: 向量時鐘 1
        v2: 向量時鐘 2
        
    Returns:
        True 若 v1 因果先於 v2
    """
    le = all(v1[i] <= v2[i] for i in range(len(v1)))
    ne = any(v1[i] < v2[i] for i in range(len(v1)))
    return le and ne


class VectorClockSystem:
    """向量時鐘系統模擬"""
    
    def __init__(self, node_ids: List[int]):
        """
        初始化系統
        
        Args:
            node_ids: 節點 ID 列表
        """
        self.total_nodes = len(node_ids)
        self.nodes: Dict[int, VectorClock] = {}
        for nid in node_ids:
            self.nodes[nid] = VectorClock(nid, self.total_nodes)
        self.messages: List[Tuple[int, int, str, List[int]]] = []
    
    def send_message(self, from_id: int, to_id: int, msg: str) -> None:
        """
        發送訊息
        
        Args:
            from_id: 發送者 ID
            to_id: 接收者 ID
            msg: 訊息內容
        """
        if from_id not in self.nodes or to_id not in self.nodes:
            return
        timestamp, _ = self.nodes[from_id].send_event(msg)
        self.messages.append((from_id, to_id, msg, timestamp))
    
    def deliver_messages(self) -> None:
        """投遞所有訊息"""
        while self.messages:
            from_id, to_id, msg, timestamp = self.messages.pop(0)
            if to_id in self.nodes:
                self.nodes[to_id].receive_event(timestamp, msg, from_id)
    
    def check_concurrent(self, node1: int, event_idx1: int, 
                          node2: int, event_idx2: int) -> bool:
        """
        檢查兩個事件是否並發
        
        Args:
            node1: 節點 1 ID
            event_idx1: 事件 1 的索引
            node2: 節點 2 ID
            event_idx2: 事件 2 的索引
            
        Returns:
            是否並發
        """
        v1 = self.nodes[node1].event_log[event_idx1][1]
        v2 = self.nodes[node2].event_log[event_idx2][1]
        return compare_vectors(v1, v2) == '|'


if __name__ == "__main__":
    print("=== 向量時鐘示範 ===")
    
    # 建立 3 個節點的系統
    system = VectorClockSystem([0, 1, 2])
    
    # 模擬事件
    print("\n--- 事件序列 ---")
    system.nodes[0].local_event("初始化")
    system.nodes[0].local_event("準備資料")
    
    system.send_message(0, 1, "資料 A")
    system.send_message(0, 2, "資料 B")
    
    system.nodes[1].local_event("處理資料")
    system.send_message(1, 2, "處理結果")
    
    system.deliver_messages()
    
    # 顯示所有事件
    print("\n--- 節點事件 ---")
    for nid in [0, 1, 2]:
        print(f"\n節點 {nid}:")
        for desc, vec, etype in system.nodes[nid].event_log:
            print(f"  {vec} - {desc} ({etype.value})")
    
    # 比較事件關係
    print("\n--- 因果關係分析 ---")
    v1 = system.nodes[0].event_log[1][1]  # 節點 0 第二個事件
    v2 = system.nodes[1].event_log[0][1]  # 節點 1 第一個事件
    relation = compare_vectors(v1, v2)
    print(f"節點0事件2 vs 節點1事件1: {relation}")
    print(f"  {v1} vs {v2}")
    
    print("\n向量時鐘特性:")
    print("1. 可檢測並發事件（2PC 無法做到）")
    print("2. 若 v1 < v2，則事件1因果先於事件2")
    print("3. 若 v1 | v2，則兩事件並發")
    print("4. 空間複雜度 O(n)（n = 節點數）")
