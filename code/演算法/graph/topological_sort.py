"""
拓撲排序 (Topological Sort)

歷史背景：
- 拓撲排序的概念最早由拓撲學引入
- Kahn's algorithm 由 Arthur B. Kahn 於 1962 年提出
- DFS-based 方法由 Robert Tarjan 等人在圖論演算法中推廣
- 廣泛應用於編譯器依賴分析、課程排程、任務排程等領域

應用場景：
- 課程先修關係規劃
- 編譯器中的相依性分析
- 建構系統中的編譯順序
- 工作流程排程
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import deque


def topological_sort_kahn(graph: Dict[str, List[str]]) -> Optional[List[str]]:
    """
    使用 Kahn's algorithm 進行拓撲排序（基於入度的 BFS）

    原理：
    1. 計算所有節點的入度
    2. 將入度為 0 的節點加入佇列
    3. 取出節點，加入結果，減少其鄰居的入度
    4. 重複直到佇列為空

    時間複雜度：O(V + E)
    空間複雜度：O(V)
    若檢測到循環，返回 None

    Args:
        graph: 鄰接表表示的圖，{節點: [鄰居列表]}

    Returns:
        拓撲排序結果，若存在循環則返回 None
    """
    # 計算入度
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1

    # 初始化佇列（入度為 0 的節點）
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        # 減少鄰居的入度
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 檢查是否存在循環
    if len(result) != len(in_degree):
        return None  # 存在循環

    return result


def topological_sort_dfs(graph: Dict[str, List[str]]) -> Optional[List[str]]:
    """
    使用 DFS 進行拓撲排序

    原理：
    1. 對每個未訪問的節點進行 DFS
    2. 完成對節點的 DFS 後，將其加入結果（後序遍歷）
    3. 最後反轉結果

    時間複雜度：O(V + E)
    空間複雜度：O(V)

    Args:
        graph: 鄰接表表示的圖

    Returns:
        拓撲排序結果，若存在循環則返回 None
    """
    visited = set()
    rec_stack = set()  # 遞迴堆疊，用於檢測循環
    result = []

    def dfs(node: str) -> bool:
        """返回 True 表示無循環，False 表示檢測到循環"""
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if not dfs(neighbor):
                    return False
            elif neighbor in rec_stack:
                return False  # 檢測到循環

        rec_stack.remove(node)
        result.append(node)
        return True

    # 對每個未訪問的節點進行 DFS
    for node in graph:
        if node not in visited:
            if not dfs(node):
                return None  # 檢測到循環

    result.reverse()
    return result


def has_cycle(graph: Dict[str, List[str]]) -> bool:
    """
    檢測有向圖中是否存在循環

    使用 DFS + 遞迴堆疊檢測

    Args:
        graph: 鄰接表表示的圖

    Returns:
        是否存在循環
    """
    visited = set()
    rec_stack = set()

    def dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False


def course_scheduling_example():
    """課程排程範例"""
    # 課程先修關係：key 表示課程，value 表示需要先修的課程
    # 圖結構：edge 從先修課指向後修課
    courses = {
        "CS101": [],           # 計算機概論，無先修
        "CS201": ["CS101"],    # 資料結構，需先修 CS101
        "CS301": ["CS201"],    # 演算法，需先修 CS201
        "CS302": ["CS201"],    # 作業系統，需先修 CS201
        "CS401": ["CS301", "CS302"],  # 編譯器，需先修演算法和作業系統
        "MATH101": [],         # 微積分，無先修
        "MATH201": ["MATH101"], # 線性代數，需先修微積分
        "CS303": ["CS201", "MATH201"],  # 電腦圖學，需先修資料結構和線性代數
    }

    # 建立鄰接表（先修課 -> 後修課）
    graph = {course: [] for course in courses}
    for course, prereqs in courses.items():
        for prereq in prereqs:
            graph[prereq].append(course)

    # 移除空的先修課（如果沒有後修課的話）
    for course in courses:
        if course not in graph:
            graph[course] = []

    return graph


if __name__ == "__main__":
    print("=== 拓撲排序 (Topological Sort) 測試 ===\n")

    # 測試 1：課程排程
    print("1. 課程排程範例（Kahn's Algorithm）：")
    graph = course_scheduling_example()
    print(f"課程圖：{graph}")
    result = topological_sort_kahn(graph)
    if result:
        print(f"修課順序：{' -> '.join(result)}")
    else:
        print("檢測到循環，無法排程！")
    print()

    # 測試 2：DFS 方法
    print("2. 課程排程範例（DFS-based）：")
    result = topological_sort_dfs(graph)
    if result:
        print(f"修課順序：{' -> '.join(result)}")
    else:
        print("檢測到循環，無法排程！")
    print()

    # 測試 3：存在循環的情況
    print("3. 存在循環的圖：")
    cyclic_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],  # 循環：A -> B -> C -> A
    }
    print(f"圖：{cyclic_graph}")
    print(f"Kahn's: {topological_sort_kahn(cyclic_graph)}")
    print(f"DFS: {topological_sort_dfs(cyclic_graph)}")
    print(f"有循環？{has_cycle(cyclic_graph)}")
    print()

    # 測試 4：簡單無循環圖
    print("4. 簡單 DAG：")
    simple_graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    print(f"圖：{simple_graph}")
    print(f"Kahn's: {topological_sort_kahn(simple_graph)}")
    print(f"DFS: {topological_sort_dfs(simple_graph)}")
    print()

    # 測試 5：空圖
    print("5. 單節點圖：")
    single = {"X": []}
    print(f"圖：{single}")
    print(f"Kahn's: {topological_sort_kahn(single)}")
    print(f"DFS: {topological_sort_dfs(single)}")
