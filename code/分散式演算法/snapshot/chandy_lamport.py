"""
分散式演算法 - Chandy-Lamport 快照演算法

在分散式系統中取得全域一致的狀態快照。
"""

from typing import List, Dict, Tuple, Optional
from enum import Enum


class MessageType(Enum):
    """訊息類型"""
    NORMAL = "NORMAL"
    MARKER = "MARKER"


class Channel:
    """通道（用於模擬訊息傳遞）"""
    
    def __init__(self, from_id: int, to_id: int):
        """
        初始化通道
        
        Args:
            from_id: 發送者 ID
            to_id: 接收者 ID
        """
        self.from_id = from_id
        self.to_id = to_id
        self.messages: List[Tuple[str, MessageType]] = []
    
    def send(self, msg: str, msg_type: MessageType = MessageType.NORMAL) -> None:
        """發送訊息"""
        self.messages.append((msg, msg_type))
    
    def deliver(self) -> Optional[Tuple[str, MessageType]]:
        """投遞訊息"""
        if self.messages:
            return self.messages.pop(0)
        return None
    
    def get_state(self) -> List[Tuple[str, MessageType]]:
        """取得通道狀態（快照時的訊息）"""
        return self.messages.copy()


class Process:
    """分散式系統中的行程"""
    
    def __init__(self, pid: int):
        """
        初始化行程
        
        Args:
            pid: 行程 ID
        """
        self.id = pid
        self.state: Optional[int] = None  # 簡化：狀態是一個整數
        self.snapshot_state: Optional[int] = None
        self.snapshot_channels: Dict[int, List] = {}  # from_id -> messages
        self.marker_received: Dict[int, bool] = {}  # 來自哪個通道收到 marker
        self.snapshot_in_progress = False
        self.snapshot_id: Optional[int] = None
    
    def set_state(self, state: int) -> None:
        """設定本地狀態"""
        self.state = state
    
    def initiate_snapshot(self, snapshot_id: int, 
                          channels: Dict[int, 'Channel']) -> None:
        """
        發起快照
        
        Args:
            snapshot_id: 快照 ID
            channels: 所有輸出通道 {to_id: channel}
        """
        self.snapshot_in_progress = True
        self.snapshot_id = snapshot_id
        self.snapshot_state = self.state
        
        # 記錄所有輸入通道為空（尚未收到 marker）
        self.marker_received = {}
        
        # 發送 MARKER 到所有輸出通道
        for to_id, ch in channels.items():
            ch.send(f"MARKER-{snapshot_id}", MessageType.MARKER)
    
    def receive_marker(self, from_id: int, snapshot_id: int,
                       channels: Dict[int, 'Channel']) -> None:
        """
        接收 MARKER 訊息
        
        Args:
            from_id: 發送者 ID
            snapshot_id: 快照 ID
            channels: 輸入通道字典
        """
        if not self.snapshot_in_progress:
            # 第一次收到 marker，啟動快照
            self.snapshot_in_progress = True
            self.snapshot_id = snapshot_id
            self.snapshot_state = self.state
            
            # 記錄此通道狀態（應該是空的，因為剛收到 marker）
            self.snapshot_channels[from_id] = []
            self.marker_received[from_id] = True
            
            # 發送 marker 到所有其他輸出通道
            for to_id, ch in channels.items():
                if to_id != from_id:
                    ch.send(f"MARKER-{snapshot_id}", MessageType.MARKER)
        else:
            # 已經在快照中，記錄該通道狀態
            if from_id not in self.snapshot_channels:
                # 記錄通道中的訊息（簡化：假設還沒傳遞的訊息）
                self.snapshot_channels[from_id] = []
            
            self.marker_received[from_id] = True
        
        # 檢查是否所有輸入通道都收到 marker
        # （簡化：假設已知所有輸入通道）
    
    def get_snapshot(self) -> Tuple[Optional[int], Dict[int, List]]:
        """取得快照結果"""
        return self.snapshot_state, self.snapshot_channels


class ChandyLamportSnapshot:
    """Chandy-Lamport 快照演算法的模擬"""
    
    def __init__(self, process_ids: List[int]):
        """
        初始化模擬
        
        Args:
            process_ids: 行程 ID 列表
        """
        self.processes: Dict[int, Process] = {}
        self.channels: Dict[Tuple[int, int], Channel] = {}
        
        for pid in process_ids:
            self.processes[pid] = Process(pid)
        
        # 建立全連通通道（簡化）
        for p1 in process_ids:
            for p2 in process_ids:
                if p1 != p2:
                    self.channels[(p1, p2)] = Channel(p1, p2)
    
    def get_out_channels(self, pid: int) -> Dict[int, Channel]:
        """取得某行程的輸出通道"""
        return {to_id: ch for (p, to_id), ch in self.channels.items() if p == pid}
    
    def get_in_channels(self, pid: int) -> Dict[int, Channel]:
        """取得某行程的輸入通道"""
        return {from_id: ch for (from_id, p), ch in self.channels.items() if p == pid}
    
    def initiate(self, initiator_id: int, snapshot_id: int = 1) -> None:
        """發起快照"""
        if initiator_id not in self.processes:
            return
        
        out_ch = self.get_out_channels(initiator_id)
        self.processes[initiator_id].initiate_snapshot(snapshot_id, out_ch)
    
    def deliver_all_markers(self) -> None:
        """投遞所有 marker 訊息（簡化模擬）"""
        for (from_id, to_id), ch in self.channels.items():
            msg = ch.deliver()
            if msg and msg[1] == MessageType.MARKER:
                snapshot_id = int(msg[0].split('-')[1])
                in_ch = self.get_in_channels(to_id)
                self.processes[to_id].receive_marker(from_id, snapshot_id, in_ch)


if __name__ == "__main__":
    print("=== Chandy-Lamport 快照演算法示範 ===")
    
    # 建立 3 個行程的系統
    snapshot = ChandyLamportSnapshot([0, 1, 2])
    
    # 設定初始狀態
    snapshot.processes[0].set_state(100)
    snapshot.processes[1].set_state(200)
    snapshot.processes[2].set_state(300)
    
    print("\n初始狀態:")
    for pid in [0, 1, 2]:
        print(f"  行程 {pid}: {snapshot.processes[pid].state}")
    
    # 發起快照（從行程 0）
    print("\n從行程 0 發起快照...")
    snapshot.initiate(0, snapshot_id=1)
    
    # 傳遞 marker 訊息
    snapshot.deliver_all_markers()
    
    print("\n快照結果:")
    for pid in [0, 1, 2]:
        state, channels = snapshot.processes[pid].get_snapshot()
        print(f"  行程 {pid}: 狀態={state}, 通道狀態={channels}")
    
    print("\nChandy-Lamport 特性:")
    print("1. 可取得全域一致的快照")
    print("2. 不需要全域同步")
    print("3. Marker 訊息用於分隔快照前後的訊息")
    print("4. 可處理通道中的 in-transit 訊息")
