"""
回溯法 (Backtracking)
實作經典的回溯演算法：N-皇后問題、數獨求解器
"""

from typing import List, Optional, Tuple


def solve_n_queens(n: int) -> List[List[List[str]]]:
    """
    解 N-皇后問題 - 找出所有解法
    
    Args:
        n: 棋盤大小 (n × n)
        
    Returns:
        所有解的列表，每個解為一個棋盤（二維字串列表）
    """
    solutions = []
    # board[i] 表示第 i 行的皇后放在第幾列（0-indexed）
    board = [-1] * n
    
    def is_safe(row: int, col: int) -> bool:
        """檢查在 (row, col) 放置皇后是否安全"""
        for r in range(row):
            c = board[r]
            # 檢查同一列或同一對角線
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True
    
    def place_queen(row: int) -> None:
        """在第 row 行放置皇后"""
        if row == n:
            # 找到一個解，轉換為棋盤表示
            solution = []
            for r in range(n):
                row_str = ['.'] * n
                row_str[board[r]] = 'Q'
                solution.append(row_str)
            solutions.append(solution)
            return
        
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                place_queen(row + 1)
                board[row] = -1  # 回溯
    
    place_queen(0)
    return solutions


def print_n_queens_solution(solution: List[List[str]], index: int = 0) -> None:
    """印出 N-皇后問題的一個解"""
    print(f"解 {index + 1}:")
    for row in solution:
        print(" " + " ".join(row))
    print()


def count_n_queens(n: int) -> int:
    """
    計算 N-皇后問題的解的數量（只計數，不儲存解）
    
    Args:
        n: 棋盤大小
        
    Returns:
        解的數量
    """
    # 使用位元運算優化
    def backtrack(row: int, cols: int, diag1: int, diag2: int) -> int:
        if row == n:
            return 1
        
        count = 0
        # 可用的位置（0 表示可放）
        available = ~(cols | diag1 | diag2) & ((1 << n) - 1)
        
        while available:
            # 取最低位的 1
            pos = available & -available
            available -= pos
            
            # 遞迴：col 設定為 1，兩個對角線需要 shift
            count += backtrack(
                row + 1,
                cols | pos,
                (diag1 | pos) << 1,
                (diag2 | pos) >> 1
            )
        
        return count
    
    return backtrack(0, 0, 0, 0)


def solve_sudoku(board: List[List[str]]) -> bool:
    """
    數獨求解器 - 使用回溯法
    
    Args:
        board: 9x9 數獨棋盤，空格用 '.' 表示
                會直接修改傳入的 board
        
    Returns:
        是否找到解
    """
    def find_empty() -> Optional[Tuple[int, int]]:
        """找到下一個空格"""
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    return (r, c)
        return None
    
    def is_valid(row: int, col: int, num: str) -> bool:
        """檢查在 (row, col) 放置 num 是否有效"""
        # 檢查行
        for r in range(9):
            if board[r][col] == num:
                return False
        
        # 檢查列
        for c in range(9):
            if board[row][c] == num:
                return False
        
        # 檢查 3x3 宮格
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        
        return True
    
    empty = find_empty()
    if not empty:
        return True  # 所有格子都填完了
    
    row, col = empty
    for num in map(str, range(1, 10)):
        if is_valid(row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = '.'  # 回溯
    
    return False


def print_sudoku(board: List[List[str]]) -> None:
    """印出數獨棋盤"""
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)
        row_str = ""
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row_str += " | "
            row_str += board[r][c] + " "
        print(row_str)


if __name__ == "__main__":
    # 測試 N-皇后問題
    print("=== N-皇后問題 ===")
    for n in [4, 5]:
        solutions = solve_n_queens(n)
        print(f"{n}-皇后問題: 共 {len(solutions)} 個解")
        if solutions:
            print_n_queens_solution(solutions[0], 0)
    
    # 使用位元運算計數
    print("N-皇后問題解的數量:")
    for n in range(1, 11):
        count = count_n_queens(n)
        print(f"  {n}-皇后: {count} 個解")
    
    # 測試數獨求解器
    print("\n=== 數獨求解器 ===")
    sudoku_board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ]
    
    print("原始數獨:")
    print_sudoku(sudoku_board)
    
    if solve_sudoku(sudoku_board):
        print("\n求解結果:")
        print_sudoku(sudoku_board)
    else:
        print("無解！")
