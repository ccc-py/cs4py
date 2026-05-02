"""
狀態空間搜尋：廣度優先搜尋與深度優先搜尋 (BFS and DFS for State Space Search)

歷史背景：
- BFS 由 Edward F. Moore 於 1959 年提出，用於尋找最短路徑
- DFS 由 Charles Pierce 於 19 世紀末提出概念，20 世紀初應用於迷宮求解
- 兩者皆為人工智慧狀態空間搜尋的基礎演算法
- 不同於圖論中的 BFS/DFS，此處聚焦於「狀態」的轉換與搜尋

核心概念：
- 狀態（State）：問題在某個時刻的具體情況
- 動作（Action）：將一個狀態轉換為另一個狀態的操作
- BFS：使用佇列，保證找到最淺（最短步數）的解
- DFS：使用堆疊，適合深度探索，可加入深度限制避免無限迴圈
"""

from typing import List, Tuple, Dict, Optional, Set, Any, Callable
from collections import deque
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class SearchResult:
    """搜尋結果"""
    path: List[Any]  # 從起點到目標的狀態路徑
    actions: List[Any]  # 執行的動作序列
    nodes_expanded: int  # 擴展的節點數
    found: bool  # 是否找到解

    def __bool__(self) -> bool:
        return self.found


class StateSpaceProblem(ABC):
    """狀態空間問題的抽象基類"""

    @abstractmethod
    def get_initial_state(self) -> Any:
        """返回初始狀態"""
        pass

    @abstractmethod
    def is_goal(self, state: Any) -> bool:
        """檢查是否為目標狀態"""
        pass

    @abstractmethod
    def get_actions(self, state: Any) -> List[Any]:
        """返回在給定狀態下可執行的所有動作"""
        pass

    @abstractmethod
    def get_next_state(self, state: Any, action: Any) -> Any:
        """執行動作後的新狀態"""
        pass

    @abstractmethod
    def state_to_key(self, state: Any) -> Any:
        """將狀態轉換為可用於集合/字典的鍵"""
        pass


def bfs_search(problem: StateSpaceProblem) -> SearchResult:
    """
    廣度優先搜尋（Breadth-First Search）

    使用佇列先進先出，保證找到最短路徑（最少步數）。
    時間複雜度：O(b^d)，b 為分支因子，d 為解的深度
    空間複雜度：O(b^d)

    返回：
        SearchResult 包含路徑、動作序列、擴展節點數
    """
    initial = problem.get_initial_state()
    queue = deque([(initial, [], [])])  # (狀態, 狀態路徑, 動作序列)
    visited: Set[Any] = {problem.state_to_key(initial)}
    nodes_expanded = 0

    while queue:
        state, path, actions = queue.popleft()
        nodes_expanded += 1

        if problem.is_goal(state):
            return SearchResult(
                path=path + [state],
                actions=actions,
                nodes_expanded=nodes_expanded,
                found=True
            )

        for action in problem.get_actions(state):
            next_state = problem.get_next_state(state, action)
            key = problem.state_to_key(next_state)

            if key not in visited:
                visited.add(key)
                queue.append((
                    next_state,
                    path + [state],
                    actions + [action]
                ))

    return SearchResult([], [], nodes_expanded, False)


def dfs_search(
    problem: StateSpaceProblem,
    depth_limit: Optional[int] = None,
) -> SearchResult:
    """
    深度優先搜尋（Depth-First Search）

    使用堆疊後進先出，深度優先探索。
    若指定 depth_limit，則限制搜尋深度避免無限遞迴。
    不保證找到最短路徑，但空間複雜度較低。

    參數：
        problem: 狀態空間問題
        depth_limit: 深度限制，None 表示無限制

    返回：
        SearchResult 包含路徑、動作序列、擴展節點數
    """
    initial = problem.get_initial_state()
    stack = [(initial, [], [], 0)]  # (狀態, 狀態路徑, 動作序列, 當前深度)
    visited: Set[Any] = set()
    nodes_expanded = 0

    while stack:
        state, path, actions, depth = stack.pop()
        key = problem.state_to_key(state)

        if key in visited:
            continue
        visited.add(key)
        nodes_expanded += 1

        if problem.is_goal(state):
            return SearchResult(
                path=path + [state],
                actions=actions,
                nodes_expanded=nodes_expanded,
                found=True
            )

        if depth_limit is not None and depth >= depth_limit:
            continue

        for action in problem.get_actions(state):
            next_state = problem.get_next_state(state, action)
            next_key = problem.state_to_key(next_state)

            if next_key not in visited:
                stack.append((
                    next_state,
                    path + [state],
                    actions + [action],
                    depth + 1
                ))

    return SearchResult([], [], nodes_expanded, False)


class EightPuzzleProblem(StateSpaceProblem):
    """
    8-拼圖問題

    3x3 的棋盤，有 8 個數字和 1 個空格（用 0 表示）。
    每次可以將空格與相鄰的數字交換。
    目標是將數字排列成目標狀態。
    """

    def __init__(self, initial_board: List[int], goal_board: List[int]):
        """
        初始化 8-拼圖

        參數：
            initial_board: 初始棋盤，長度 9 的列表，0 表示空格
            goal_board: 目標棋盤，長度 9 的列表
        """
        self.initial_board = initial_board[:]
        self.goal_board = goal_board[:]

    def get_initial_state(self) -> List[int]:
        return self.initial_board[:]

    def is_goal(self, state: List[int]) -> bool:
        return state == self.goal_board

    def get_actions(self, state: List[int]) -> List[int]:
        """返回空格可以移動的方向：0=上, 1=下, 2=左, 3=右"""
        actions = []
        empty_idx = state.index(0)
        row, col = empty_idx // 3, empty_idx % 3

        if row > 0:  # 上
            actions.append(0)
        if row < 2:  # 下
            actions.append(1)
        if col > 0:  # 左
            actions.append(2)
        if col < 2:  # 右
            actions.append(3)

        return actions

    def get_next_state(self, state: List[int], action: int) -> List[int]:
        """執行移動動作，返回新狀態"""
        new_state = state[:]
        empty_idx = new_state.index(0)
        row, col = empty_idx // 3, empty_idx % 3

        if action == 0:  # 上
            target_idx = (row - 1) * 3 + col
        elif action == 1:  # 下
            target_idx = (row + 1) * 3 + col
        elif action == 2:  # 左
            target_idx = row * 3 + (col - 1)
        else:  # 右
            target_idx = row * 3 + (col + 1)

        # 交換空格與目標位置
        new_state[empty_idx], new_state[target_idx] = new_state[target_idx], new_state[empty_idx]
        return new_state

    def state_to_key(self, state: List[int]) -> Tuple[int, ...]:
        return tuple(state)

    def state_to_string(self, state: List[int]) -> str:
        """將狀態轉換為可讀字串"""
        lines = []
        for i in range(0, 9, 3):
            row = " ".join(str(x) if x != 0 else " " for x in state[i:i+3])
            lines.append(row)
        return "\n".join(lines)


def demo_eight_puzzle():
    """8-拼圖示範"""
    print("=== 8-拼圖問題示範 ===\n")

    # 初始狀態
    initial = [1, 2, 3, 4, 0, 5, 6, 7, 8]
    # 目標狀態
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    print("初始狀態：")
    puzzle = EightPuzzleProblem(initial, goal)
    print(puzzle.state_to_string(initial))
    print("\n目標狀態：")
    print(puzzle.state_to_string(goal))
    print()

    # BFS 搜尋
    print("--- BFS 搜尋 ---")
    result = bfs_search(puzzle)
    if result:
        print(f"找到解！")
        print(f"步數：{len(result.actions)}")
        print(f"擴展節點數：{result.nodes_expanded}")
        print(f"路徑：{result.path}")
    else:
        print("未找到解")

    # DFS 搜尋（帶深度限制）
    print("\n--- DFS 搜尋（深度限制 20）---")
    result = dfs_search(puzzle, depth_limit=20)
    if result:
        print(f"找到解！")
        print(f"步數：{len(result.actions)}")
        print(f"擴展節點數：{result.nodes_expanded}")
        print(f"路徑：{result.path}")
    else:
        print("未找到解（可能超過深度限制）")


class WaterJugProblem(StateSpaceProblem):
    """
    水壺問題（Water Jug Problem）

    給定兩個容量為 3 和 5 的水壺，目標是量出恰好 4 單位的水。
    可執行的動作：
    - 裝滿任一水壺
    - 倒空任一水壺
    - 將一個水壺的水倒入另一個（直到倒空或裝滿）
    """

    def __init__(self, capacity1: int, capacity2: int, goal: int):
        self.capacity1 = capacity1
        self.capacity2 = capacity2
        self.goal = goal

    def get_initial_state(self) -> Tuple[int, int]:
        return (0, 0)

    def is_goal(self, state: Tuple[int, int]) -> bool:
        return state[0] == self.goal or state[1] == self.goal

    def get_actions(self, state: Tuple[int, int]) -> List[str]:
        """返回可執行的動作"""
        actions = []
        x, y = state

        # 裝滿水壺
        if x < self.capacity1:
            actions.append("fill1")
        if y < self.capacity2:
            actions.append("fill2")

        # 倒空水壺
        if x > 0:
            actions.append("empty1")
        if y > 0:
            actions.append("empty2")

        # 互相倒水
        if x > 0 and y < self.capacity2:
            actions.append("pour12")
        if y > 0 and x < self.capacity1:
            actions.append("pour21")

        return actions

    def get_next_state(self, state: Tuple[int, int], action: str) -> Tuple[int, int]:
        x, y = state

        if action == "fill1":
            return (self.capacity1, y)
        elif action == "fill2":
            return (x, self.capacity2)
        elif action == "empty1":
            return (0, y)
        elif action == "empty2":
            return (x, 0)
        elif action == "pour12":
            # 從水壺1倒入水壺2
            amount = min(x, self.capacity2 - y)
            return (x - amount, y + amount)
        elif action == "pour21":
            # 從水壺2倒入水壺1
            amount = min(y, self.capacity1 - x)
            return (x + amount, y - amount)

        return state

    def state_to_key(self, state: Tuple[int, int]) -> Tuple[int, int]:
        return state


def demo_water_jug():
    """水壺問題示範"""
    print("\n=== 水壺問題示範 ===\n")
    print("問題：使用 3 加侖和 5 加侖的水壺，量出恰好 4 加侖的水")
    print("初始狀態：(0, 0)，目標：任一水壺有 4 加侖\n")

    problem = WaterJugProblem(capacity1=3, capacity2=5, goal=4)

    # BFS 搜尋
    print("--- BFS 搜尋 ---")
    result = bfs_search(problem)
    if result:
        print(f"找到解！步數：{len(result.actions)}")
        print(f"擴展節點數：{result.nodes_expanded}")
        print("\n步驟：")
        state = problem.get_initial_state()
        print(f"  (0, 0) - 初始狀態")
        for i, action in enumerate(result.actions):
            state = problem.get_next_state(state, action)
            print(f"  {state} - {action}")
    else:
        print("未找到解")


if __name__ == "__main__":
    demo_eight_puzzle()
    demo_water_jug()
