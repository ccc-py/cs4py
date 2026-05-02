"""
PageRank 演算法實作

使用冪迭代法計算網頁的 PageRank 分數。
"""

from typing import Dict, List, Tuple, Set
import math


class PageRank:
    """PageRank 演算法實作"""
    
    def __init__(self, damping_factor: float = 0.85, 
                 max_iterations: int = 100, 
                 tolerance: float = 1e-6) -> None:
        """
        初始化 PageRank
        
        Args:
            damping_factor: 阻尼因子 d，通常為 0.85
            max_iterations: 最大迭代次數
            tolerance: 收斂容差
        """
        self.damping_factor = damping_factor
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.graph: Dict[int, List[int]] = {}  # 鄰接表：節點 -> 出鏈列表
        self.pagerank: Dict[int, float] = {}  # 最終 PageRank 分數
        
    def add_edge(self, from_node: int, to_node: int) -> None:
        """新增一條有向邊"""
        if from_node not in self.graph:
            self.graph[from_node] = []
        if to_node not in self.graph:
            self.graph[to_node] = []
        self.graph[from_node].append(to_node)
    
    def build_from_links(self, links: List[Tuple[int, int]]) -> None:
        """從連結列表建立圖"""
        for from_node, to_node in links:
            self.add_edge(from_node, to_node)
    
    def compute(self) -> Dict[int, float]:
        """
        計算 PageRank 分數
        
        使用冪迭代法：
        PR(p) = (1-d)/N + d * Σ(PR(q) / out_degree(q))
                q∈in_links(p)
        
        Returns:
            PageRank 分數字典
        """
        # 所有節點
        all_nodes: Set[int] = set(self.graph.keys())
        for neighbors in self.graph.values():
            all_nodes.update(neighbors)
        all_nodes = set(all_nodes)
        
        N = len(all_nodes)
        if N == 0:
            return {}
        
        # 初始化：均勻分佈
        pr = {node: 1.0 / N for node in all_nodes}
        
        # 建立入鏈映射：節點 -> 指向它的節點列表
        in_links: Dict[int, List[int]] = {node: [] for node in all_nodes}
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                in_links[neighbor].append(node)
        
        # 出度
        out_degree = {node: len(self.graph.get(node, [])) for node in all_nodes}
        
        # 冪迭代
        for iteration in range(self.max_iterations):
            new_pr = {}
            dangling_sum = 0.0  # 懸空節點的 PR 總和
            
            # 計算懸空節點（出度為 0）的貢獻
            for node in all_nodes:
                if out_degree[node] == 0:
                    dangling_sum += pr[node]
            
            # 計算新的 PageRank
            for node in all_nodes:
                # 隨機跳轉部分
                rank = (1.0 - self.damping_factor) / N
                
                # 加上懸空節點的貢獻
                rank += self.damping_factor * dangling_sum / N
                
                # 加上來自入鏈的貢獻
                for in_node in in_links[node]:
                    if out_degree[in_node] > 0:
                        rank += self.damping_factor * pr[in_node] / out_degree[in_node]
                
                new_pr[node] = rank
            
            # 檢查收斂
            diff = sum(abs(new_pr[node] - pr[node]) for node in all_nodes)
            
            pr = new_pr
            
            if diff < self.tolerance:
                break
        
        # 正規化使總和為 1
        total = sum(pr.values())
        if total > 0:
            pr = {node: rank / total for node, rank in pr.items()}
        
        self.pagerank = pr
        return pr
    
    def get_ranking(self) -> List[Tuple[int, float]]:
        """取得按 PageRank 分數排序的列表"""
        return sorted(self.pagerank.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    # 示範用法
    print("=== PageRank 示範 ===\n")
    
    # 建立小型網頁圖
    print("1. 網頁圖結構:")
    links = [
        (1, 2), (1, 3),  # 頁面 1 連到 2 和 3
        (2, 3),          # 頁面 2 連到 3
        (3, 1),          # 頁面 3 連到 1
        (4, 5), (5, 4),  # 頁面 4 和 5 互相連結
        (3, 5)           # 頁面 3 也連到 5
    ]
    
    for from_node, to_node in links:
        print(f"  {from_node} -> {to_node}")
    
    # 計算 PageRank
    pr = PageRank(damping_factor=0.85, max_iterations=100)
    pr.build_from_links(links)
    scores = pr.compute()
    
    print("\n2. PageRank 分數:")
    for node, score in pr.get_ranking():
        print(f"  頁面 {node}: {score:.6f}")
    
    print("\n3. 驗證總和:", sum(scores.values()))
    
    # 測試不同阻尼因子
    print("\n4. 不同阻尼因子的影響:")
    for d in [0.5, 0.85, 0.95]:
        pr_test = PageRank(damping_factor=d, max_iterations=100)
        pr_test.build_from_links(links)
        scores_test = pr_test.compute()
        top_node = pr_test.get_ranking()[0]
        print(f"  d={d}: 最高分頁面 {top_node[0]} = {top_node[1]:.6f}")
