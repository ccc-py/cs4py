"""
蒙特卡洛樹搜尋 (Monte Carlo Tree Search, MCTS)

歷史背景：
- 2006 年被 Rémi Coulom 首次應用於棋類遊戲（命名為 "Monte Carlo Graph Search"）
- 同年 Levente Kocsis 和 Csaba Szepesvári 提出 UCT 演算法
- 2016 年 DeepMind AlphaGo 結合 MCTS 與深度神經網路擊敗李世乭
- 2017 年 AlphaGo Zero 完全依賴 MCTS + 自我對弈超越人類

核心概念：
- 不需要完整的遊戲樹，透過隨機模擬估算節點價值
- 四步驟循環：選擇（Selection）→ 擴展（Expansion）→ 模擬（Simulation）→ 回溯（Backpropagation）
- UCT 公式平衡探索與開發：
  UCT = Q/N + C × √(ln(parent_N) / N)
"""

from typing import List, Optional, Dict, Tuple
import math
import random
from abc import ABC, abstractmethod


class MCTSNode:
    """MCTS 樹節點"""

    def __init__(self, state=None, parent=None, action=None):
        self.state = state          # 遊戲狀態
        self.parent = parent        # 父節點
        self.action = action        # 到達此節點的動作
        self.children: List['MCTSNode'] = []
        self.visits = 0             # 訪問次數
        self.wins = 0.0             # 勝利次數
        self.untried_actions = []   # 尚未嘗試的動作

    @property
    def value(self) -> float:
        """平均回報值"""
        if self.visits == 0:
            return 0.0
        return self.wins / self.visits

    def is_fully_expanded(self) -> bool:
        """是否所有動作都已嘗試"""
        return len(self.untried_actions) == 0

    def best_child(self, exploration_weight: float = 1.414) -> 'MCTSNode':
        """使用 UCT 公式選擇最佳子節點"""
        return max(
            self.children,
            key=lambda child: child.value + exploration_weight * math.sqrt(
                math.log(self.visits) / (child.visits + 1e-10)
            )
        )


def uct_select(node: MCTSNode, exploration_weight: float = 1.414) -> MCTSNode:
    """
    UCT 選擇策略

    UCT = Q(s,a) + C × √(ln N(s) / N(s,a))

    其中：
    - Q(s,a)：動作價值（平均回報）
    - N(s)：父節點訪問次數
    - N(s,a)：子節點訪問次數
    - C：探索常數
    """
    return max(
        node.children,
        key=lambda child: child.wins / (child.visits + 1e-10)
        + exploration_weight * math.sqrt(
            math.log(node.visits) / (child.visits + 1e-10)
        )
    )


def mcts_search(
    root_state,
    get_legal_actions,
    make_action,
    simulate,
    is_terminal,
    root_player,
    n_iterations: int = 1000,
    exploration_weight: float = 1.414,
    seed: Optional[int] = None,
) -> int:
    """
    蒙特卡洛樹搜尋主函數

    參數：
        root_state: 初始遊戲狀態
        get_legal_actions: 函數，返回合法動作列表
        make_action: 函數，(state, action) → new_state
        simulate: 函數，從當前狀態隨機模擬到結束，返回勝利的玩家
        is_terminal: 函數，檢查狀態是否為終止
        root_player: 根節點的玩家
        n_iterations: 搜尋迭代次數
        exploration_weight: UCT 探索常數
        seed: 隨機種子

    返回：最佳動作索引
    """
    if seed is not None:
        random.seed(seed)

    root = MCTSNode(state=root_state)
    root.untried_actions = get_legal_actions(root_state)

    for _ in range(n_iterations):
        node = root

        # 階段 1：選擇 — 沿最佳子節點下行直到未完全擴展的節點
        while node.is_fully_expanded() and node.children:
            node = uct_select(node, exploration_weight)

        # 階段 2：擴展 — 添加一個新子節點
        if node.untried_actions:
            action = random.choice(node.untried_actions)
            node.untried_actions.remove(action)
            new_state = make_action(node.state, action)
            child = MCTSNode(state=new_state, parent=node, action=action)
            child.untried_actions = get_legal_actions(new_state)
            node.children.append(child)
            node = child

        # 階段 3：模擬 — 隨機玩到遊戲結束
        winner = simulate(node.state)

        # 階段 4：回溯 — 更新路徑上所有節點的統計
        while node:
            node.visits += 1
            if winner == root_player:
                node.wins += 1.0
            elif winner == "draw":
                node.wins += 0.5
            node = node.parent

    # 返回訪問次數最多的子節點的動作
    if not root.children:
        return root.untried_actions[0] if root.untried_actions else -1

    best = max(root.children, key=lambda c: c.visits)
    return best.action


# ========== Tic-Tac-Toe 實作範例 ==========


class TicTacToeState:
    """井字遊戲狀態"""

    def __init__(self):
        self.board: List[str] = [' '] * 9
        self.current_player = 'X'

    def clone(self) -> 'TicTacToeState':
        new = TicTacToeState()
        new.board = self.board[:]
        new.current_player = self.current_player
        return new

    def is_terminal(self) -> bool:
        winner = self.check_winner()
        return winner is not None

    def check_winner(self) -> Optional[str]:
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        if all(cell != ' ' for cell in self.board):
            return 'draw'
        return None

    def get_legal_actions(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def make_action(self, action: int) -> 'TicTacToeState':
        new = self.clone()
        new.board[action] = new.current_player
        new.current_player = 'O' if new.current_player == 'X' else 'X'
        return new

    def simulate_random(self) -> str:
        """隨機模擬到遊戲結束"""
        state = self
        while not state.is_terminal():
            actions = state.get_legal_actions()
            if not actions:
                break
            action = random.choice(actions)
            state = state.make_action(action)
        return state.check_winner() or 'draw'

    def print_board(self) -> str:
        rows = []
        for i in range(0, 9, 3):
            rows.append(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
        return "\n---+---+---\n".join(rows)


def get_current_player(state: TicTacToeState) -> str:
    return state.current_player


def mcts_play_tic_tac_toe():
    """使用 MCTS 玩井字遊戲"""
    print("=== MCTS 井字遊戲 ===\n")

    state = TicTacToeState()

    while not state.is_terminal():
        if state.current_player == 'X':
            # MCTS AI
            action = mcts_search(
                root_state=state,
                get_legal_actions=lambda s: s.get_legal_actions(),
                make_action=lambda s, a: s.make_action(a),
                simulate=lambda s: s.simulate_random(),
                is_terminal=lambda s: s.is_terminal(),
                root_player='X',
                n_iterations=1000,
                seed=random.randint(0, 10000),
            )
            print(f"AI (X) 落子於 {action}")
        else:
            # 隨機對手
            actions = state.get_legal_actions()
            if actions:
                action = random.choice(actions)
                print(f"隨機玩家 (O) 落子於 {action}")

        state = state.make_action(action)
        print(state.print_board())
        print()

    winner = state.check_winner()
    if winner == 'draw':
        print("平局！")
    else:
        print(f"{winner} 獲勝！")


def mcts_analysis():
    """MCTS 搜尋分析"""
    print("\n=== MCTS 搜尋分析 ===\n")

    state = TicTacToeState()
    state.board[0] = 'X'
    state.board[4] = 'O'
    state.current_player = 'X'

    print("當前棋盤：")
    print(state.print_board())
    print()

    # 執行 MCTS 並分析子節點
    root = MCTSNode(state=state)
    root.untried_actions = state.get_legal_actions()

    n_iterations = 3000
    for _ in range(n_iterations):
        node = root
        while node.is_fully_expanded() and node.children:
            node = uct_select(node)

        if node.untried_actions:
            action = random.choice(node.untried_actions)
            node.untried_actions.remove(action)
            new_state = state.make_action(action)
            child = MCTSNode(state=new_state, parent=node, action=action)
            child.untried_actions = new_state.get_legal_actions()
            node.children.append(child)
            node = child

        winner = node.state.simulate_random()

        while node:
            node.visits += 1
            if winner == 'X':
                node.wins += 1.0
            elif winner == 'draw':
                node.wins += 0.5
            node = node.parent

    print(f"MCTS 分析（{n_iterations} 次迭代）：")
    print(f"{'位置':>5} | {'訪問次數':>8} | {'勝率':>6} | 柱狀圖")
    print("-" * 50)

    for child in sorted(root.children, key=lambda c: c.visits, reverse=True):
        action = child.action
        row, col = action // 3, action % 3
        win_rate = child.wins / child.visits if child.visits > 0 else 0
        bar = "█" * int(child.visits / 30)
        print(f"({row},{col}) | {child.visits:>8} | {win_rate:>5.1%} | {bar}")


def demo_uct_formula():
    """UCT 公式示範"""
    print("\n=== UCT 公式示範 ===\n")

    # 模擬三個子節點的狀態
    parent_visits = 100
    exploration_weight = 1.414

    children_data = [
        ("節點 A", 50, 60),
        ("節點 B", 20, 25),
        ("節點 C", 5, 15),
    ]

    print(f"父節點訪問次數：{parent_visits}")
    print(f"{'':>6} | {'Q/N':>6} | {'探索項':>8} | {'UCT':>6}")
    print("-" * 45)

    for name, wins, visits in children_data:
        q_value = wins / visits
        exploration = exploration_weight * math.sqrt(
            math.log(parent_visits) / visits
        )
        uct = q_value + exploration
        print(f"{name:>6} | {q_value:>6.3f} | {exploration:>8.3f} | {uct:>6.3f}")


if __name__ == "__main__":
    demo_uct_formula()
    mcts_analysis()
    mcts_play_tic_tac_toe()
