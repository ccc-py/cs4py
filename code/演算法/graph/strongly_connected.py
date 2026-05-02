"""
強連通分量 (Strongly Connected Components, SCC)

歷史背景：
- 強連通分量是圖論中的重要概念
- Kosaraju's algorithm 由 S. Rao Kosaraju 於 1978 年提出
- Tarjan's algorithm 由 Robert Tarjan 於 1972 年提出，效率更高
- 應用於編譯器優化、社群網絡分析、電路設計等領域

定義：
- 強連通分量：有向圖中的一個極大子圖，其中任意兩個節點互相可達
"""

from typing import List, Dict, Set, Optional, Tuple, DefaultDict
from collections import defaultdict, deque


def kosaraju(graph: Dict[str, List[str]]) -> List[List[str]]:
    """
    Kosaraju's algorithm 找出強連通分量

    原理：
    1. 第一次 DFS：對原圖進行後序遍歷，記錄完成順序
    2. 反轉圖：將所有邊的方向反轉
    3. 第二次 DFS：按照第一次 DFS 的逆序，在反轉圖上進行 DFS
       每次 DFS 訪問到的節點構成一個 SCC

    時間複雜度：O(V + E)
    空間複雜度：O(V + E)

    Args:
        graph: 鄰接表表示的圖

    Returns:
        強連通分量列表，每個分量是一個節點列表
    """
    # Step 1: 第一次 DFS，記錄後序順序
    visited = set()
    post_order = []

    def dfs_first(node: str):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_first(neighbor)
        post_order.append(node)

    for node in graph:
        if node not in visited:
            dfs_first(node)

    # Step 2: 建立反轉圖
    reversed_graph = defaultdict(list)
    for node in graph:
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)
        if node not in reversed_graph:
            reversed_graph[node] = []

    # Step 3: 第二次 DFS，按照後序逆序在反轉圖上遍歷
    visited.clear()
    sccs = []

    def dfs_second(node: str, component: List[str]):
        visited.add(node)
        component.append(node)
        for neighbor in reversed_graph.get(node, []):
            if neighbor not in visited:
                dfs_second(neighbor, component)

    for node in reversed(post_order):
        if node not in visited:
            component = []
            dfs_second(node, component)
            sccs.append(component)

    return sccs


def tarjan(graph: Dict[str, List[str]]) -> List[List[str]]:
    """
    Tarjan's algorithm 找出強連通分量

    原理：
    1. 對圖進行 DFS，為每個節點分配 discovery time (disc) 和 low-link value
    2. low-link value 表示從該節點通過樹邊和最多一條後向邊能到達的最早發現的節點
    3. 使用堆疊追踪當前路徑上的節點
    4. 如果某節點的 low == disc，則該節點是一個 SCC 的根

    時間複雜度：O(V + E)（只進行一次 DFS）
    空間複雜度：O(V)

    Args:
        graph: 鄰接表表示的圖

    Returns:
        強連通分量列表
    """
    index_counter = [0]  # 使用列表以便在遞迴中修改
    stack = []
    on_stack = set()
    indices = {}      # disc time
    lowlinks = {}     # low-link value
    sccs = []

    def strongconnect(node: str):
        # 設置節點的 index 和 lowlink
        indices[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        # 遍歷鄰居
        for neighbor in graph.get(node, []):
            if neighbor not in indices:
                # 樹邊
                strongconnect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_stack:
                # 後向邊或交叉邊
                lowlinks[node] = min(lowlinks[node], indices[neighbor])

        # 如果 node 是一個 SCC 的根
        if lowlinks[node] == indices[node]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == node:
                    break
            sccs.append(component)

    for node in graph:
        if node not in indices:
            strongconnect(node)

    return sccs


def build_sample_graph() -> Dict[str, List[str]]:
    """建立示例圖（包含多個 SCC）"""
    # 這個圖包含 3 個 SCC: {A, B, E}, {C, D}, {F, G}
    return {
        "A": ["B", "E"],
        "B": ["A", "C"],
        "C": ["D"],
        "D": ["C"],
        "E": ["A", "F"],
        "F": ["G"],
        "G": ["F"],
    }


if __name__ == "__main__":
    print("=== 強連通分量 (Strongly Connected Components) 測試 ===\n")

    # 測試 1：示例圖
    print("1. 示例圖：")
    graph = build_sample_graph()
    print(f"圖：{graph}")

    print("\nKosaraju's Algorithm:")
    sccs_kosaraju = kosaraju(graph)
    for i, scc in enumerate(sccs_kosaraju, 1):
        print(f"  SCC {i}: {scc}")

    print("\nTarjan's Algorithm:")
    sccs_tarjan = tarjan(graph)
    for i, scc in enumerate(sccs_tarjan, 1):
        print(f"  SCC {i}: {scc}")
    print()

    # 測試 2：簡單的兩個節點循環
    print("2. 兩個節點的循環：")
    simple = {
        "X": ["Y"],
        "Y": ["X"],
    }
    print(f"圖：{simple}")
    print(f"Kosaraju: {kosaraju(simple)}")
    print(f"Tarjan: {tarjan(simple)}")
    print()

    # 測試 3：無循環的圖（每個節點都是獨立的 SCC）
    print("3. DAG（每個節點是獨立的 SCC）：")
    dag = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    print(f"圖：{dag}")
    print(f"Kosaraju: {kosaraju(dag)}")
    print(f"Tarjan: {tarjan(dag)}")
    print()

    # 測試 4：更大的圖
    print("4. 較複雜的圖：")
    complex_graph = {
        "A": ["B", "C"],
        "B": ["C", "D"],
        "C": ["A"],  # A, B, C 形成 SCC
        "D": ["E"],
        "E": ["D", "F"],  # D, E 形成 SCC
        "F": ["G"],
        "G": ["F"],  # F, G 形成 SCC
    }
    print(f"圖：{complex_graph}")
    sccs = tarjan(complex_graph)
    print(f"Tarjan 找到 {len(sccs)} 個 SCC:")
    for i, scc in enumerate(sccs, 1):
        print(f"  SCC {i}: {scc}")
