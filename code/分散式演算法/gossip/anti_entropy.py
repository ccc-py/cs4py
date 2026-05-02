"""
分散式演算法 - 反熵同步 (Anti-Entropy)

Gossip 協定的變體，用於資料同步和修復，參考 Dynamo/Cassandra 的實作。
"""

from typing import Dict, Set, List, Tuple
import random


class DataStore:
    """簡化的鍵值儲存，包含版本向量"""
    
    def __init__(self, node_id: int):
        """
        初始化資料儲存
        
        Args:
            node_id: 節點 ID
        """
        self.node_id = node_id
        self.data: Dict[str, Tuple[str, int]] = {}  # key -> (value, version)
    
    def put(self, key: str, value: str, version: int = None) -> None:
        """
        寫入資料
        
        Args:
            key: 鍵
            value: 值
            version: 版本號（None 表示自增）
        """
        if version is None:
            old_ver = self.data[key][1] if key in self.data else 0
            version = old_ver + 1
        self.data[key] = (value, version)
    
    def get(self, key: str) -> Tuple[str, int]:
        """讀取資料"""
        return self.data.get(key, (None, 0))
    
    def get_keys(self) -> Set[str]:
        """取得所有鍵"""
        return set(self.data.keys())
    
    def get_digest(self) -> Dict[str, int]:
        """取得摘要（鍵到版本的映射）"""
        return {k: v[1] for k, v in self.data.items()}
    
    def merge(self, other_data: Dict[str, Tuple[str, int]]) -> List[str]:
        """
        合併其他節點的資料（取版本較新的）
        
        Args:
            other_data: 其他節點的資料
            
        Returns:
            新增/更新的鍵列表
        """
        updated = []
        for key, (value, version) in other_data.items():
            if key not in self.data or self.data[key][1] < version:
                self.data[key] = (value, version)
                updated.append(key)
        return updated


class AntiEntropyNode:
    """反熵同步的節點"""
    
    def __init__(self, node_id: int, all_nodes: List[int]):
        """
        初始化節點
        
        Args:
            node_id: 節點 ID
            all_nodes: 所有節點 ID
        """
        self.id = node_id
        self.store = DataStore(node_id)
        self.all_nodes = all_nodes
        self.sync_count = 0
    
    def anti_entropy_sync(self, nodes: Dict[int, 'AntiEntropyNode'], 
                          strategy: str = 'push-pull') -> Tuple[int, int]:
        """
        執行反熵同步
        
        Args:
            nodes: 所有節點字典
            strategy: 策略 ('push', 'pull', 'push-pull')
            
        Returns:
            (發送數, 接收更新數)
        """
        # 選擇隨機節點
        candidates = [nid for nid in self.all_nodes 
                      if nid != self.id and nid in nodes]
        if not candidates:
            return 0, 0
        
        target_id = random.choice(candidates)
        target = nodes[target_id]
        
        sent = 0
        received = 0
        
        if strategy in ['push', 'push-pull']:
            # Push: 發送摘要，對方回傳需要更新的
            my_digest = self.store.get_digest()
            # 簡化：直接發送全部資料
            received += target.store.merge(self.store.data)
            sent = len(self.store.data)
        
        if strategy in ['pull', 'push-pull']:
            # Pull: 請求對方的資料
            target_digest = target.store.get_digest()
            # 簡化：直接合併
            updated = self.store.merge(target.store.data)
            received += len(updated)
        
        self.sync_count += 1
        return sent, received


class AntiEntropy:
    """反熵同步的模擬"""
    
    def __init__(self, node_ids: List[int]):
        """
        初始化反熵同步模擬
        
        Args:
            node_ids: 節點 ID 列表
        """
        self.nodes: Dict[int, AntiEntropyNode] = {}
        for nid in node_ids:
            self.nodes[nid] = AntiEntropyNode(nid, node_ids)
        self.round = 0
        self.log: List[str] = []
    
    def write_data(self, node_id: int, key: str, value: str) -> None:
        """在某節點寫入資料"""
        if node_id in self.nodes:
            self.nodes[node_id].store.put(key, value)
    
    def run_round(self, strategy: str = 'push-pull') -> int:
        """
        執行一輪反熵同步
        
        Args:
            strategy: 同步策略
            
        Returns:
            總更新數
        """
        self.round += 1
        total_updates = 0
        
        for nid, node in self.nodes.items():
            _, updates = node.anti_entropy_sync(self.nodes, strategy)
            total_updates += updates
        
        # 檢查資料一致性
        consistency = self.check_consistency()
        self.log.append(f"Round {self.round}: {total_updates} 更新, "
                       f"一致性 {consistency:.1%}")
        
        return total_updates
    
    def check_consistency(self) -> float:
        """檢查所有節點資料是否一致"""
        if not self.nodes:
            return 1.0
        
        # 以第一個節點為基準
        ref_node = list(self.nodes.values())[0]
        ref_keys = ref_node.store.get_keys()
        
        consistent = 0
        total = len(self.nodes)
        
        for nid, node in self.nodes.items():
            node_keys = node.store.get_keys()
            if node_keys == ref_keys:
                # 檢查每個鍵的值和版本
                all_match = all(
                    node.store.get(k) == ref_node.store.get(k)
                    for k in ref_keys
                )
                if all_match:
                    consistent += 1
            else:
                pass  # 鍵不一致
        
        return consistent / total if total > 0 else 1.0
    
    def get_log(self) -> List[str]:
        """取得日誌"""
        return self.log


if __name__ == "__main__":
    random.seed(42)
    
    print("=== 反熵同步 (Anti-Entropy) 示範 ===")
    print("參考 Dynamo/Cassandra 的資料同步機制\n")
    
    # 建立 5 個節點
    nodes = list(range(5))
    ae = AntiEntropy(nodes)
    
    # 在不同節點寫入資料
    print("初始資料:")
    ae.write_data(0, "user:1", "Alice")
    ae.write_data(1, "user:2", "Bob")
    ae.write_data(2, "user:3", "Charlie")
    print("  節點 0: user:1=Alice")
    print("  節點 1: user:2=Bob")
    print("  節點 2: user:3=Charlie")
    print("  節點 3,4: 空")
    
    # 執行反熵同步
    print("\n執行 Push-Pull 反熵同步:")
    for r in range(3):
        updates = ae.run_round('push-pull')
        print(f"  Round {r+1}: {updates} 個更新")
    
    print("\n最終一致性:")
    for line in ae.get_log():
        print(f"  {line}")
    
    # 不同策略比較
    print("\n--- 策略比較 ---")
    for strategy in ['push', 'pull', 'push-pull']:
        ae2 = AntiEntropy(list(range(10)))
        for i in range(3):
            ae2.write_data(i, f"key:{i}", f"value:{i}")
        
        rounds = 0
        while ae2.check_consistency() < 1.0 and rounds < 20:
            ae2.run_round(strategy)
            rounds += 1
        
        print(f"{strategy:12s}: {rounds} 輪達到一致")
    
    print("\n反熵同步特性:")
    print("1. 逐步修復資料不一致")
    print("2. Push-Pull 比單純 Push 或 Pull 更快")
    print("3. 用於 Dynamo、Cassandra 的副本同步")
    print("4. 可處理網路分區後的資料修復")
