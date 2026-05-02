"""
歐拉路徑與歐拉迴路 (Eulerian Path and Circuit)

歷史背景：
- 歐拉路徑問題起源於 1736 年 Leonhard Euler 解決的「柯尼斯堡七橋問題」
- Euler 證明了：要在圖中找出經過每條邊恰好一次的閉合路徑，每個節點的度數必須是偶數
- 這是圖論的開端，也是第一個被研究的圖論問題
- Hierholzer's algorithm 由 Carl Hierholzer 於 1873 年提出

歐拉路徑 vs 哈密頓路徑：
- 歐拉路徑：經過每條「邊」恰好一次
- 哈密頓路徑：經過每個「節點」恰好一次
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, deque


def is_eulerian_undirected(graph: Dict[str, List[str]]) -> Tuple[bool, bool, Optional[str]]:
    """
    判斷無向圖是否為歐拉圖

    歐拉迴路存在條件（無向圖）：
    - 圖是連通的
    - 每個節點的度數都是偶數

    歐拉路徑存在條件（無向圖）：
    - 圖是連通的
    - 恰好有 0 個或 2 個節點的度數為奇數
    - 0 個奇數度 = 歐拉迴路
    - 2 個奇數度 = 歐拉路徑（起點和終點是奇數度節點）

    Args:
        graph: 鄰接表表示的無向圖

    Returns:
        (是否存在歐拉路徑, 是否存在歐拉迴路, 起點建議)
    """
    # 計算每個節點的度數
    degree = defaultdict(int)
    for node in graph:
        degree[node] += len(graph[node])
        for neighbor in graph[node]:
            if neighbor not in graph or node not in graph[neighbor]:
                # 確保是無向圖
                degree[neighbor] += 1

    # 重新計算（考慮雙向）
    degree.clear()
    all_nodes = set(graph.keys())
    for node in graph:
        all_nodes.update(graph[node])
        for neighbor in graph[node]:
            degree[node] += 1

    # 統計奇數度節點
    odd_degree_nodes = [node for node in all_nodes if degree[node] % 2 == 1]

    # 檢查連通性（從任意節點開始 DFS）
    if not all_nodes:
        return True, True, None

    start = next(iter(all_nodes))
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        # 也檢查是否有節點將其作為鄰居
        for n in all_nodes:
            if node in graph.get(n, []) and n not in visited:
                dfs(n)

    dfs(start)

    is_connected = visited == all_nodes

    if not is_connected:
        return False, False, None

    has_circuit = len(odd_degree_nodes) == 0
    has_path = len(odd_degree_nodes) == 0 or len(odd_degree_nodes) == 2

    if len(odd_degree_nodes) == 2:
        start_node = odd_degree_nodes[0]
    elif len(odd_degree_nodes) == 0:
        start_node = start if start in graph else next(iter(graph), None)
    else:
        start_node = None

    return has_path, has_circuit, start_node


def is_eulerian_directed(graph: Dict[str, List[str]]) -> Tuple[bool, bool, Optional[str]]:
    """
    判斷有向圖是否為歐拉圖

    歐拉迴路存在條件（有向圖）：
    - 圖是連通的（基於有向邊的連通性）
    - 每個節點的入度 == 出度

    歐拉路徑存在條件（有向圖）：
    - 圖是連通的
    - 最多一個節點的出度 - 入度 = 1（起點）
    - 最多一個節點的入度 - 出度 = 1（終點）
    - 其餘節點的入度 == 出度

    Args:
        graph: 鄰接表表示的有向圖

    Returns:
        (是否存在歐拉路徑, 是否存在歐拉迴路, 起點建議)
    """
    # 計算入度和出度
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    all_nodes = set()

    for node in graph:
        all_nodes.add(node)
        out_degree[node] += len(graph[node])
        for neighbor in graph[node]:
            all_nodes.add(neighbor)
            in_degree[neighbor] += 1

    # 檢查歐拉迴路條件
    has_circuit = all(in_degree[node] == out_degree[node] for node in all_nodes if node in in_degree or node in out_degree)

    # 檢查歐拉路徑條件
    start_nodes = []
    end_nodes = []

    for node in all_nodes:
        delta = out_degree[node] - in_degree[node]
        if delta == 1:
            start_nodes.append(node)
        elif delta == -1:
            end_nodes.append(node)
        elif delta != 0:
            return False, False, None

    has_path = (len(start_nodes) == 0 and len(end_nodes) == 0) or \
               (len(start_nodes) == 1 and len(end_nodes) == 1)

    if has_circuit:
        start_node = next(iter(all_nodes), None)
    elif len(start_nodes) == 1:
        start_node = start_nodes[0]
    else:
        start_node = None

    return has_path, has_circuit, start_node


def hierholzer_undirected(graph: Dict[str, List[str]], start: Optional[str] = None) -> Optional[List[str]]:
    """
    Hierholzer's algorithm 找出無向圖的歐拉路徑/迴路

    原理：
    1. 從起點開始，隨便走（DFS），直到回到起點
    2. 如果還有未訪問的邊，找到一個有未訪問邊的節點
    3. 從該節點開始新的迴路，將其插入到主迴路中

    時間複雜度：O(E)
    空間複雜度：O(E)

    Args:
        graph: 鄰接表表示的無向圖
        start: 起點（可選，如果不提供則自動選擇）

    Returns:
        歐拉路徑的節點序列，如果不存在則返回 None
    """
    # 建立邊的多重集合（允許重複邊）
    edges = defaultdict(list)
    for node in graph:
        for neighbor in graph[node]:
            edges[node].append(neighbor)

    # 選擇起點
    if start is None:
        _, _, start = is_eulerian_undirected(graph)

    if start is None or start not in edges:
        return None

    # 計算總邊數
    total_edges = sum(len(edges[node]) for node in edges)

    # Hierholzer 演算法
    stack = [start]
    path = []

    while stack:
        current = stack[-1]
        if edges[current]:
            # 還有未使用的邊
            next_node = edges[current].pop()
            # 移除反向邊
            edges[next_node].remove(current)
            stack.append(next_node)
        else:
            # 當前節點沒有未使用的邊，加入路徑
            path.append(stack.pop())

    path.reverse()

    # 檢查是否使用了所有邊
    if len(path) != total_edges + 1:
        return None

    return path


def hierholzer_directed(graph: Dict[str, List[str]], start: Optional[str] = None) -> Optional[List[str]]:
    """
    Hierholzer's algorithm 找出有向圖的歐拉路徑/迴路

    Args:
        graph: 鄰接表表示的有向圖
        start: 起點（可選）

    Returns:
        歐拉路徑的節點序列，如果不存在則返回 None
    """
    edges = defaultdict(list)
    for node in graph:
        edges[node].extend(graph[node])

    if start is None:
        _, _, start = is_eulerian_directed(graph)

    if start is None or start not in edges:
        return None

    total_edges = sum(len(edges[node]) for node in edges)

    stack = [start]
    path = []

    while stack:
        current = stack[-1]
        if edges[current]:
            next_node = edges[current].pop()
            stack.append(next_node)
        else:
            path.append(stack.pop())

    path.reverse()

    if len(path) != total_edges + 1:
        return None

    return path


def build_konigsberg_bridge() -> Dict[str, List[str]]:
    """建立柯尼斯堡七橋問題的圖（不存在歐拉迴路）"""
    # 四個區域：A (北岸), B (南岸), C (東島), D (西島)
    # 七座橋：A-C, A-C, A-D, A-D, B-C, B-D, C-D
    return {
        "A": ["C", "C", "D", "D"],
        "B": ["C", "D"],
        "C": ["A", "A", "B", "D"],
        "D": ["A", "A", "B", "C"],
    }


def build_eulerian_example() -> Dict[str, List[str]]:
    """建立有歐拉迴路的圖"""
    return {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C"],
    }


if __name__ == "__main__":
    print("=== 歐拉路徑與歐拉迴路 (Eulerian Path/Circuit) 測試 ===\n")

    # 測試 1：柯尼斯堡七橋問題
    print("1. 柯尼斯堡七橋問題（無解）：")
    konigsberg = build_konigsberg_bridge()
    print(f"圖：{konigsberg}")
    has_path, has_circuit, start = is_eulerian_undirected(konigsberg)
    print(f"存在歐拉路徑？{has_path}")
    print(f"存在歐拉迴路？{has_circuit}")
    print()

    # 測試 2：有歐拉迴路的圖
    print("2. 有歐拉迴路的圖：")
    euler_graph = build_eulerian_example()
    print(f"圖：{euler_graph}")
    has_path, has_circuit, start = is_eulerian_undirected(euler_graph)
    print(f"存在歐拉路徑？{has_path}")
    print(f"存在歐拉迴路？{has_circuit}")
    if has_path:
        path = hierholzer_undirected(euler_graph, start)
        print(f"歐拉迴路：{' -> '.join(path)}")
    print()

    # 測試 3：有歐拉路徑但無迴路
    print("3. 有歐拉路徑但無迴路：")
    path_graph = {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B", "D"],
        "D": ["C"],
    }
    print(f"圖：{path_graph}")
    has_path, has_circuit, start = is_eulerian_undirected(path_graph)
    print(f"存在歐拉路徑？{has_path}")
    print(f"存在歐拉迴路？{has_circuit}")
    if has_path:
        path = hierholzer_undirected(path_graph, start)
        print(f"歐拉路徑：{' -> '.join(path)}")
    print()

    # 測試 4：有向圖
    print("4. 有向圖的歐拉迴路：")
    directed = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    }
    print(f"圖：{directed}")
    has_path, has_circuit, start = is_eulerian_directed(directed)
    print(f"存在歐拉路徑？{has_path}")
    print(f"存在歐拉迴路？{has_circuit}")
    if has_path:
        path = hierholzer_directed(directed, start)
        print(f"歐拉迴路：{' -> '.join(path)}")
    print()

    # 測試 5：較複雜的圖
    print("5. 較複雜的無向圖：")
    complex_graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D"],
        "D": ["A", "B", "C"],
    }
    print(f"圖：完全圖 K4")
    has_path, has_circuit, start = is_eulerian_undirected(complex_graph)
    print(f"存在歐拉迴路？{has_circuit}")
    if has_circuit:
        path = hierholzer_undirected(complex_graph, "A")
        print(f"歐拉迴路（部分）：{' -> '.join(path[:10])}... (共 {len(path)} 個節點)")
