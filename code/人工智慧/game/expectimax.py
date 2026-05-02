"""
Expectimax 搜尋演算法 (Expectimax Search Algorithm)

歷史背景：
- 基於 Minimax 演算法擴充，由 Donald Michie 等人在 1960 年代提出
- 用於處理含有機率事件的遊戲決策（如骰子、撲克等）
- 廣泛應用於具有不確定性的遊戲 AI 和決策系統
- 結合機率論與博弈樹搜尋，是處理隨機環境的重要工具

核心概念：
- MAX 節點：玩家試圖最大化期望收益
- CHANCE 節點：代表隨機事件，計算期望值
- 無 MIN 節點（不考慮對手的最差選擇，只看機率）
- 適用於單人 + 隨機事件的遊戲，或雙人但其中一方是「運氣」的情況
"""

from typing import List, Tuple, Optional, Any, Dict, Callable
import random
from abc import ABC, abstractmethod


class ExpectimaxProblem(ABC):
    """Expectimax 搜尋問題的抽象基類"""

    @abstractmethod
    def get_initial_state(self) -> Any:
        """返回初始狀態"""
        pass

    @abstractmethod
    def is_terminal(self, state: Any) -> bool:
        """檢查是否為終止狀態"""
        pass

    @abstractmethod
    def get_player(self, state: Any) -> str:
        """
        返回當前行動的玩家
        返回 'MAX' 表示決策玩家，'CHANCE' 表示隨機事件
        """
        pass

    @abstractmethod
    def get_legal_actions(self, state: Any) -> List[Any]:
        """返回在當前狀態下可執行的動作"""
        pass

    @abstractmethod
    def get_next_state(self, state: Any, action: Any) -> Any:
        """執行動作後的新狀態"""
        pass

    @abstractmethod
    def get_chance_outcomes(self, state: Any) -> List[Tuple[Any, float]]:
        """
        對於 CHANCE 節點，返回可能的結果及其機率
        返回：[(結果狀態, 機率), ...]，機率總和應為 1.0
        """
        pass

    @abstractmethod
    def evaluate(self, state: Any) -> float:
        """評估終止狀態的分數（越高對 MAX 越有利）"""
        pass

    @abstractmethod
    def state_to_key(self, state: Any) -> Any:
        """將狀態轉換為可用於快取的鍵"""
        pass


def expectimax_search(
    problem: ExpectimaxProblem,
    state: Any,
    depth: int,
    memo: Optional[Dict] = None,
) -> Tuple[float, Optional[Any]]:
    """
    Expectimax 搜尋演算法

    參數：
        problem: Expectimax 問題定義
        state: 當前狀態
        depth: 剩餘搜尋深度
        memo: 快取字典（可選）

    返回：
        (期望分數, 最佳動作)
        若為終止狀態或深度為 0，返回 (評分, None)
    """
    if memo is None:
        memo = {}

    # 檢查快取
    key = (problem.state_to_key(state), depth)
    if key in memo:
        return memo[key]

    # 終止條件
    if problem.is_terminal(state) or depth == 0:
        score = problem.evaluate(state)
        memo[key] = (score, None)
        return score, None

    player = problem.get_player(state)

    if player == 'MAX':
        # MAX 節點：選擇分數最高的動作
        best_score = float('-inf')
        best_action = None

        for action in problem.get_legal_actions(state):
            next_state = problem.get_next_state(state, action)
            score, _ = expectimax_search(problem, next_state, depth - 1, memo)

            if score > best_score:
                best_score = score
                best_action = action

        memo[key] = (best_score, best_action)
        return best_score, best_action

    elif player == 'CHANCE':
        # CHANCE 節點：計算期望值
        expected_score = 0.0

        outcomes = problem.get_chance_outcomes(state)
        for next_state, probability in outcomes:
            score, _ = expectimax_search(problem, next_state, depth - 1, memo)
            expected_score += probability * score

        memo[key] = (expected_score, None)
        return expected_score, None

    return 0.0, None


class DiceGameProblem(ExpectimaxProblem):
    """
    簡單骰子遊戲：Pig Game 變體

    規則：
    - 玩家每回合可以選擇「繼續擲骰」或「停手」
    - 擲出 1-6 的點數，累積到當前分數
    - 如果擲出 1，當前回合分數歸零，換下一回合
    - 如果選擇停手，分數加入總分，換下一回合
    - 先達到目標分數（如 20 分）的玩家獲勝

    狀態：(當前玩家, 玩家1總分, 玩家2總分, 當前回合累積分數)
    """

    def __init__(self, target_score: int = 20):
        self.target_score = target_score

    def get_initial_state(self) -> Tuple[str, int, int, int]:
        return ('P1', 0, 0, 0)

    def is_terminal(self, state: Tuple[str, int, int, int]) -> bool:
        _, p1_score, p2_score, _ = state
        return p1_score >= self.target_score or p2_score >= self.target_score

    def get_player(self, state: Tuple[str, int, int, int]) -> str:
        player, _, _, turn_score = state
        if turn_score > 0:
            return 'MAX'  # 可以選擇繼續或停手
        return 'CHANCE'  # 擲骰子的隨機事件

    def get_legal_actions(self, state: Tuple[str, int, int, int]) -> List[str]:
        """MAX 玩家可選擇：繼續擲骰（roll）或停手（hold）"""
        _, _, _, turn_score = state
        actions = ['hold']
        if turn_score > 0:
            actions.append('roll')
        return actions

    def get_next_state(self, state: Tuple[str, int, int, int], action: str) -> Tuple[str, int, int, int]:
        player, p1_score, p2_score, turn_score = state

        if action == 'hold':
            # 停手：將回合分數加入總分，換對手
            if player == 'P1':
                return ('P2', p1_score + turn_score, p2_score, 0)
            else:
                return ('P1', p1_score, p2_score + turn_score, 0)

        elif action == 'roll':
            # 繼續擲骰：回合分數帶入，讓 CHANCE 節點處理
            return (player, p1_score, p2_score, turn_score)

        return state

    def get_chance_outcomes(self, state: Tuple[str, int, int, int]) -> List[Tuple[Tuple[str, int, int, int], float]]:
        """
        擲骰子結果：1-6 各 1/6 機率
        擲出 1 時回合分數歸零並換手
        """
        player, p1_score, p2_score, turn_score = state
        outcomes = []

        for dice in range(1, 7):
            if dice == 1:
                # 擲出 1，回合結束，換對手
                if player == 'P1':
                    next_state = ('P2', p1_score, p2_score, 0)
                else:
                    next_state = ('P1', p1_score, p2_score, 0)
            else:
                # 擲出 2-6，累加分數
                next_state = (player, p1_score, p2_score, turn_score + dice)

            outcomes.append((next_state, 1.0 / 6.0))

        return outcomes

    def evaluate(self, state: Tuple[str, int, int, int]) -> float:
        """
        評估終止狀態
        假設是 P1 的視角：P1 贏為 +1，P2 贏為 -1
        """
        _, p1_score, p2_score, _ = state
        if p1_score >= self.target_score:
            return 1.0
        elif p2_score >= self.target_score:
            return -1.0
        return 0.0

    def state_to_key(self, state: Tuple[str, int, int, int]) -> Tuple[str, int, int, int]:
        return state

    def print_state(self, state: Tuple[str, int, int, int]):
        """印出遊戲狀態"""
        player, p1, p2, turn = state
        print(f"玩家：{player}，P1 分數：{p1}，P2 分數：{p2}，當前回合：{turn}")


def demo_dice_game():
    """骰子遊戲示範"""
    print("=== 骰子遊戲 Expectimax 示範 ===\n")
    print("規則：擲骰子累積分數，擲出 1 則回合分數歸零")
    print("目標：先達到 20 分獲勝\n")

    problem = DiceGameProblem(target_score=20)

    # 模擬一局遊戲
    state = problem.get_initial_state()
    print("初始狀態：")
    problem.print_state(state)
    print()

    while not problem.is_terminal(state):
        player, p1, p2, turn = state

        if turn == 0:
            # 需要擲第一次
            print(f"{player} 擲出：", end="")
            dice = random.randint(1, 6)
            print(dice)
            if dice == 1:
                state = (('P2' if player == 'P1' else 'P1'), p1, p2, 0)
            else:
                state = (player, p1, p2, dice)
        else:
            # 可以使用 expectimax 決定是否繼續
            score, action = expectimax_search(problem, state, depth=4)
            print(f"{player} 回合分數 {turn}，Expectimax 建議：{action}（期望：{score:.3f}）")

            if action == 'hold':
                if player == 'P1':
                    state = ('P2', p1 + turn, p2, 0)
                else:
                    state = ('P1', p1, p2 + turn, 0)
            else:
                # 繼續擲
                dice = random.randint(1, 6)
                print(f"  {player} 選擇繼續，擲出：{dice}")
                if dice == 1:
                    state = (('P2' if player == 'P1' else 'P1'), p1, p2, 0)
                else:
                    state = (player, p1, p2, turn + dice)

        problem.print_state(state)
        print()

    # 結果
    _, p1, p2, _ = state
    if p1 >= 20:
        print("P1 獲勝！")
    else:
        print("P2 獲勝！")


class SimpleGamblingProblem(ExpectimaxProblem):
    """
    簡單賭博問題：示範 CHANCE 節點的期望值計算

    玩家有 100 元，每回合可選擇：
    - 保守：獲得 10 元（確定）
    - 冒險：50% 機會獲得 30 元，50% 機會損失 10 元

    目標：10 回合後總資產最大化
    """

    def __init__(self, initial_money: int = 100, n_rounds: int = 10):
        self.initial_money = initial_money
        self.n_rounds = n_rounds

    def get_initial_state(self) -> Tuple[int, int]:
        return (self.initial_money, 0)  # (目前金額, 已進行回合數)

    def is_terminal(self, state: Tuple[int, int]) -> bool:
        _, rounds = state
        return rounds >= self.n_rounds

    def get_player(self, state: Tuple[int, int]) -> str:
        return 'MAX'

    def get_legal_actions(self, state: Tuple[int, int]) -> List[str]:
        return ['conservative', 'risky']

    def get_next_state(self, state: Tuple[int, int], action: str) -> Tuple[int, int]:
        money, rounds = state
        if action == 'conservative':
            return ('CHANCE', money, rounds, 'conservative')
        else:
            return ('CHANCE', money, rounds, 'risky')

    def get_chance_outcomes(self, state: Tuple) -> List[Tuple[Tuple[int, int], float]]:
        """
        處理 CHANCE 節點
        state: ('CHANCE', money, rounds, action_type)
        """
        _, money, rounds, action_type = state

        if action_type == 'conservative':
            # 確定獲得 10 元
            return [((money + 10, rounds + 1), 1.0)]

        elif action_type == 'risky':
            # 50% 獲得 30 元，50% 損失 10 元
            return [
                ((money + 30, rounds + 1), 0.5),
                ((money - 10, rounds + 1), 0.5),
            ]

        return [((money, rounds + 1), 1.0)]

    def evaluate(self, state: Tuple[int, int]) -> float:
        money, _ = state
        return float(money)

    def state_to_key(self, state: Tuple) -> Tuple:
        if isinstance(state, tuple) and len(state) >= 2:
            return (state[0], state[1]) if len(state) == 2 else (state[1], state[2])
        return state


def demo_gambling():
    """賭博問題示範"""
    print("\n=== 賭博問題 Expectimax 示範 ===\n")
    print("規則：100 元起始，10 回合")
    print("保守：確定 +10 元")
    print("冒險：50% +30 元，50% -10 元\n")

    problem = SimpleGamblingProblem(initial_money=100, n_rounds=10)

    # 使用 expectimax 決定每一步
    state = problem.get_initial_state()
    print(f"初始金額：{state[0]}，回合：{state[1]}")

    while not problem.is_terminal(state):
        expected_value, action = expectimax_search(problem, state, depth=10)
        print(f"\n回合 {state[1] + 1}：Expectimax 建議 {action}（期望值：{expected_value:.1f}）")

        # 執行動作
        if action == 'conservative':
            next_state = (state[0] + 10, state[1] + 1)
        else:
            # 隨機決定結果
            if random.random() < 0.5:
                next_state = (state[0] + 30, state[1] + 1)
                print("  結果：+30 元！")
            else:
                next_state = (state[0] - 10, state[1] + 1)
                print("  結果：-10 元...")

        state = next_state
        print(f"  目前金額：{state[0]}")

    print(f"\n最終金額：{state[0]}")


if __name__ == "__main__":
    # 設定隨機種子以便重現
    random.seed(42)
    demo_dice_game()
    demo_gambling()
