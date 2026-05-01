"""
極小化極大演算法與 Alpha-Beta 剪枝 (Minimax with Alpha-Beta Pruning)

歷史背景：
- Minimax 由 John von Neumann 於 1928 年提出，是博弈論的基礎
- Alpha-Beta 剪枝於 1950-60 年代由 Allen Newell, Herbert Simon 等人發展
- 1997 年 IBM Deep Blue 使用此演算法擊敗世界棋王 Garry Kasparov
- 廣泛應用於棋類遊戲 AI：西洋棋、井字遊戲、黑白棋等

核心概念：
- MAX 玩家（己方）嘗試最大化評分
- MIN 玩家（對手）嘗試最小化評分
- Alpha-Beta 剪枝消除不必要搜尋的子樹，大幅提升效率
- 理想情況可將搜尋複雜度從 O(b^d) 降至 O(b^(d/2))
"""

from typing import List, Optional, Tuple
import copy


class TicTacToe:
    """井字遊戲狀態與邏輯"""

    def __init__(self):
        self.board: List[str] = [' '] * 9
        self.current_player = 'X'

    def clone(self) -> 'TicTacToe':
        """建立遊戲狀態副本"""
        new_game = TicTacToe()
        new_game.board = self.board[:]
        new_game.current_player = self.current_player
        return new_game

    def make_move(self, pos: int) -> bool:
        """在指定位置落子"""
        if pos < 0 or pos > 8 or self.board[pos] != ' ':
            return False
        self.board[pos] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def available_moves(self) -> List[int]:
        """返回所有可用的落子位置"""
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def check_winner(self) -> Optional[str]:
        """檢查贏家，返回 'X', 'O', 'draw' 或 None"""
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 橫列
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 直行
            (0, 4, 8), (2, 4, 6),              # 對角線
        ]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]

        if all(cell != ' ' for cell in self.board):
            return 'draw'

        return None

    def is_terminal(self) -> bool:
        """檢查是否為終止狀態"""
        return self.check_winner() is not None

    def evaluate(self, player: str) -> int:
        """
        評估函數
        返回：+1 如果 player 贏，-1 如果對手贏，0 如果平局
        """
        winner = self.check_winner()
        if winner == player:
            return 1
        elif winner == 'draw':
            return 0
        elif winner is not None:
            return -1
        return 0  # 遊戲尚未結束

    def print_board(self) -> str:
        """將棋盤轉換為字串"""
        rows = []
        for i in range(0, 9, 3):
            row = f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} "
            rows.append(row)
        return "\n---+---+---\n".join(rows)


def minimax(
    game: TicTacToe,
    depth: int,
    maximizing: bool,
    player: str,
) -> Tuple[int, int]:
    """
    極小化極大演算法

    返回：(評分, 最佳落子位置)
    """
    if game.is_terminal() or depth == 0:
        return game.evaluate(player), -1

    opponent = 'O' if player == 'X' else 'X'

    if maximizing:
        max_eval = float('-inf')
        best_move = -1
        for move in game.available_moves():
            new_game = game.clone()
            new_game.make_move(move)
            eval_score, _ = minimax(new_game, depth - 1, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = -1
        for move in game.available_moves():
            new_game = game.clone()
            new_game.make_move(move)
            eval_score, _ = minimax(new_game, depth - 1, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


def minimax_alpha_beta(
    game: TicTacToe,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
    player: str,
) -> Tuple[int, int]:
    """
    帶有 Alpha-Beta 剪枝的極小化極大演算法

    參數：
        alpha：MAX 玩家目前的最佳評分下界
        beta：MIN 玩家目前的最佳評分上界

    返回：(評分, 最佳落子位置)
    """
    if game.is_terminal() or depth == 0:
        return game.evaluate(player), -1

    opponent = 'O' if player == 'X' else 'X'

    if maximizing:
        max_eval = float('-inf')
        best_move = -1
        for move in game.available_moves():
            new_game = game.clone()
            new_game.make_move(move)
            eval_score, _ = minimax_alpha_beta(new_game, depth - 1, alpha, beta, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta 剪枝
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = -1
        for move in game.available_moves():
            new_game = game.clone()
            new_game.make_move(move)
            eval_score, _ = minimax_alpha_beta(new_game, depth - 1, alpha, beta, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha 剪枝
        return min_eval, best_move


def get_best_move(game: TicTacToe, player: str) -> int:
    """使用 Minimax + Alpha-Beta 取得最佳落子位置"""
    _, best_move = minimax_alpha_beta(
        game, depth=9, alpha=float('-inf'), beta=float('inf'), maximizing=True, player=player
    )
    return best_move


def play_game_vs_ai():
    """玩家對 AI 的井字遊戲演示"""
    print("=== 井字遊戲 Minimax AI 演示 ===\n")

    game = TicTacToe()
    ai_player = 'X'
    human = 'O'

    print(f"AI 執 {ai_player}，你執 {human}")
    print("位置編號：")
    print(" 0 | 1 | 2 ")
    print("---+---+---")
    print(" 3 | 4 | 5 ")
    print("---+---+---")
    print(" 6 | 7 | 8 ")
    print()

    while not game.is_terminal():
        if game.current_player == ai_player:
            _, best_move = minimax_alpha_beta(
                game, depth=9, alpha=float('-inf'), beta=float('inf'),
                maximizing=True, player=ai_player
            )
            game.make_move(best_move)
            print(f"AI 落子於位置 {best_move}")
        else:
            # 簡化：自動選擇第一個可用位置作為人類玩家的演示
            moves = game.available_moves()
            if moves:
                move = moves[0]
                game.make_move(move)
                print(f"玩家落子於位置 {move}")

        print(game.print_board())
        print()

    winner = game.check_winner()
    if winner == 'draw':
        print("平局！")
    else:
        print(f"{winner} 獲勝！")


def demo_minimax():
    """Minimax 搜尋樹演示"""
    print("\n=== Minimax 搜尋演示 ===\n")

    # 展示 AI 如何選擇最佳落子
    game = TicTacToe()
    game.make_move(0)  # X 下左上角
    game.make_move(4)  # O 下中間

    print("當前棋盤：")
    print(game.print_board())
    print()

    score, move = minimax_alpha_beta(
        game, depth=9, alpha=float('-inf'), beta=float('inf'),
        maximizing=True, player='X'
    )
    print(f"AI (X) 選擇位置 {move}，預期評分：{score}")


def demo_pruning_effect():
    """Alpha-Beta 剪枝效果演示"""
    import time

    print("\n=== Alpha-Beta 剪枝效果比較 ===\n")

    # 較複雜的局面
    game = TicTacToe()
    game.make_move(0)

    start = time.time()
    minimax(game, depth=9, maximizing=True, player='X')
    t_minimax = time.time() - start

    start = time.time()
    minimax_alpha_beta(game, depth=9, alpha=float('-inf'), beta=float('inf'),
                       maximizing=True, player='X')
    t_alpha_beta = time.time() - start

    print(f"Minimax 時間：{t_minimax:.6f} 秒")
    print(f"Alpha-Beta 時間：{t_alpha_beta:.6f} 秒")
    print(f"加速倍數：{t_minimax / max(t_alpha_beta, 0.000001):.1f}x")


if __name__ == "__main__":
    play_game_vs_ai()
    demo_minimax()
    demo_pruning_effect()
