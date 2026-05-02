"""
分散式演算法 - Gossip 協定（流言協定）

實作流行病協定（epidemic protocol），用於資訊傳播和狀態同步。
"""

from typing import List, Dict, Set, Tuple
import random


class GossipNode:
    """Gossip 協定的節點"""
    
    def __init__(self, node_id: int, all_nodes: List[int]):
        """
        初始化節點
        
        Args:
            node_id: 節點 ID
            all_nodes: 所有節點 ID 列表
        """
        self.id = node_id
        self.all_nodes = all_nodes
        self.data: Set[str] = set()  # 節點知道的資訊
        self.rounds_participated = 0
    
    def add_data(self, item: str) -> None:
        """加入新資訊"""
        self.data.add(item)
    
    def gossip_round(self, nodes: Dict[int, 'GossipNode'], 
                      fanout: int = 3) -> List[Tuple[int, int]]:
        """
        執行一輪 gossip
        
        Args:
            nodes: 所有節點字典
            fanout: 每次傳播給幾個鄰居
            
        Returns:
            傳播的 (from, to) 列表
        """
        if not self.data:
            return []
        
        self.rounds_participated += 1
        
        # 隨機選擇 fanout 個節點
        candidates = [nid for nid in self.all_nodes 
                      if nid != self.id and nid in nodes]
        targets = random.sample(candidates, min(fanout, len(candidates)))
        
        transmissions = []
        for target_id in targets:
            # 發送自己的資料
            nodes[target_id].receive_gossip(self.data)
            transmissions.append((self.id, target_id))
        
        return transmissions
    
    def receive_gossip(self, incoming_data: Set[str]) -> None:
        """接收 gossip 資訊"""
        self.data.update(incoming_data)
    
    def get_data_count(self) -> int:
        """取得已知資訊數量"""
        return len(self.data)


class GossipProtocol:
    """Gossip 協定的事件驅動模擬"""
    
    def __init__(self, node_ids: List[int], fanout: int = 3):
        """
        初始化 Gossip 模擬
        
        Args:
            node_ids: 節點 ID 列表
            fanout: 扇出（每次傳播給幾個鄰居）
        """
        self.fanout = fanout
        self.nodes: Dict[int, GossipNode] = {}
        for nid in node_ids:
            self.nodes[nid] = GossipNode(nid, node_ids)
        self.round = 0
        self.log: List[str] = []
    
    def add_initial_data(self, node_id: int, data: str) -> None:
        """給某節點加入初始資訊"""
        if node_id in self.nodes:
            self.nodes[node_id].add_data(data)
    
    def run_round(self) -> int:
        """
        執行一輪 gossip
        
        Returns:
            本輪傳播次數
        """
        self.round += 1
        total_transmissions = 0
        
        for nid, node in self.nodes.items():
            transmissions = node.gossip_round(self.nodes, self.fanout)
            total_transmissions += len(transmissions)
        
        # 統計
        coverage = self.get_coverage()
        self.log.append(f"Round {self.round}: {total_transmissions} 次傳播, "
                       f"覆蓋率 {coverage:.1%}")
        
        return total_transmissions
    
    def run_until_converged(self, target_coverage: float = 0.95, 
                              max_rounds: int = 100) -> int:
        """
        執行直到收斂
        
        Args:
            target_coverage: 目標覆蓋率
            max_rounds: 最大輪數
            
        Returns:
            執行的輪數
        """
        for r in range(max_rounds):
            self.run_round()
            coverage = self.get_coverage()
            if coverage >= target_coverage:
                self.log.append(f"已達到 {target_coverage:.0%} 覆蓋率")
                return r + 1
        return max_rounds
    
    def get_coverage(self) -> float:
        """計算資訊覆蓋率"""
        total_nodes = len(self.nodes)
        if total_nodes == 0:
            return 0.0
        
        # 假設有資料表示已覆蓋
        covered = sum(1 for node in self.nodes.values() if node.get_data_count() > 0)
        return covered / total_nodes
    
    def get_log(self) -> List[str]:
        """取得日誌"""
        return self.log


if __name__ == "__main__":
    random.seed(42)
    
    print("=== Gossip 協定（流言協定）示範 ===")
    
    # 建立 20 個節點的系統
    nodes = list(range(20))
    gossip = GossipProtocol(nodes, fanout=3)
    
    # 節點 0 有初始資訊
    gossip.add_initial_data(0, "新聞A")
    print(f"\n初始：只有節點 0 知道 '新聞A'")
    print(f"節點數: {len(nodes)}, fanout: 3")
    
    # 執行 gossip
    print("\n執行 gossip 傳播:")
    rounds = gossip.run_until_converged(target_coverage=0.9, max_rounds=50)
    print(f"收斂所需輪數: {rounds}")
    
    for line in gossip.get_log()[:10]:  # 顯示前 10 輪
        print(f"  {line}")
    
    # 分析傳播速度
    print("\n--- 傳播分析 ---")
    gossip2 = GossipProtocol(list(range(50)), fanout=3)
    gossip2.add_initial_data(0, "新聞")
    gossip2.run_until_converged(target_coverage=0.9, max_rounds=50)
    
    print(f"50 個節點的傳播日誌:")
    for line in gossip2.get_log()[:5]:
        print(f"  {line}")
    
    print("\nGossip 協定特性:")
    print("1. 去中心化，魯棒性高")
    print("2. 傳播速度約 O(log n) 輪")
    print("3. 可處理動態加入/離開")
    print("4. 應用：會員發現、狀態同步")
