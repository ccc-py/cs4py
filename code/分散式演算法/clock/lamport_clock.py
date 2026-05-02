"""
分散式演算法 - Lamport 邏輯時鐘

實作 Lamport 邏輯時鐘，用於在分散式系統中建立事件的全序關係。
"""

from typing import List, Dict, Tuple
from enum import Enum


class EventType(Enum):
    """事件類型"""
    LOCAL = "LOCAL"
    SEND = "SEND"
    RECEIVE = "RECEIVE"


class LamportClock:
    """Lamport 邏輯時鐘"""
    
    def __init__(self, node_id: int):
        """
        初始化 Lamport 時鐘
        
        Args:
            node_id: 節點 ID
        """
        self.node_id = node_id
        self.time = 0
        self.event_log: List[Tuple[str, int, EventType]] = []
    
    def local_event(self, description: str = "") -> int:
        """
        發生本地事件
        
        Args:
            description: 事件描述
            
        Returns:
            當前邏輯時間
        """
        self.time += 1
        self.event_log.append((description or f"本地事件@{self.node_id}", 
                              self.time, EventType.LOCAL))
        return self.time
    
    def send_event(self, msg: str) -> Tuple[int, str]:
        """
        發送訊息事件
        
        Args:
            msg: 訊息內容
            
        Returns:
            (時間戳, 訊息)
        """
        self.time += 1
        self.event_log.append((f"發送: {msg}", self.time, EventType.SEND))
        return self.time, msg
    
    def receive_event(self, sender_time: int, msg: str, 
                      sender_id: int) -> int:
        """
        接收訊息事件
        
        Args:
            sender_time: 發送者的時間戳
            msg: 訊息內容
            sender_id: 發送者 ID
            
        Returns:
            更新後的邏輯時間
        """
        self.time = max(self.time, sender_time) + 1
        self.event_log.append((f"接收自 {sender_id}: {msg}", 
                              self.time, EventType.RECEIVE))
        return self.time


class DistributedSystem:
    """簡化的分散式系統模擬"""
    
    def __init__(self, node_ids: List[int]):
        """
        初始化分散式系統
        
        Args:
            node_ids: 節點 ID 列表
        """
        self.nodes: Dict[int, LamportClock] = {}
        for nid in node_ids:
            self.nodes[nid] = LamportClock(nid)
        self.messages: List[Tuple[int, int, str, int]] = []  # (from, to, msg, timestamp)
    
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
    
    def get_all_events(self) -> List[Tuple[int, str, int, EventType]]:
        """
        取得所有節點的事件（按邏輯時間排序）
        
        Returns:
            事件列表 (node_id, description, time, type)
        """
        events = []
        for nid, node in self.nodes.items():
            for desc, time, etype in node.event_log:
                events.append((nid, desc, time, etype))
        return sorted(events, key=lambda x: x[2])


def happens_before(time1: int, node1: int, time2: int, node2: int) -> bool:
    """
    判斷事件 1 是否 happens-before 事件 2
    
    Lamport 定義：
    - 若 time1 < time2，則事件 1 可能 happens-before 事件 2
    - 若 time1 == time2，則按節點 ID 排序
    
    Args:
        time1: 事件 1 的邏輯時間
        node1: 事件 1 的節點 ID
        time2: 事件 2 的邏輯時間
        node2: 事件 2 的節點 ID
        
    Returns:
        是否可能 happens-before
    """
    if time1 < time2:
        return True
    elif time1 == time2:
        return node1 < node2
    return False


if __name__ == "__main__":
    print("=== Lamport 邏輯時鐘示範 ===")
    
    # 建立 3 個節點的系統
    system = DistributedSystem([0, 1, 2])
    
    # 模擬事件序列
    print("\n--- 事件序列 ---")
    system.nodes[0].local_event("初始化")
    system.nodes[0].local_event("準備資料")
    
    system.send_message(0, 1, "資料 A")
    system.send_message(0, 2, "資料 B")
    
    system.nodes[1].local_event("處理資料")
    system.send_message(1, 2, "處理結果")
    
    system.deliver_messages()
    
    # 顯示所有事件（按邏輯時間排序）
    print("\n--- 全域事件排序 ---")
    events = system.get_all_events()
    for nid, desc, time, etype in events:
        print(f"  [{time:2d}] 節點 {nid}: {desc} ({etype.value})")
    
    # 演示 happens-before 關係
    print("\n--- Happens-Before 關係 ---")
    print(f"事件(2,節點0) happens-before 事件(3,節點1)? {happens_before(2, 0, 3, 1)}")
    print(f"事件(3,節點1) happens-before 事件(3,節點0)? {happens_before(3, 1, 3, 0)}")
    
    print("\nLamport 時鐘特性:")
    print("1. 若 a happens-before b，則 time(a) < time(b)")
    print("2. 反之不一定成立（可能並發）")
    print("3. 提供全序，但無法分辨並發事件")
