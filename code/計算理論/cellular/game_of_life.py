"""
康威生命遊戲 (Conway's Game of Life)

生命遊戲是英國數學家 John Horton Conway 在 1970 年發明的細胞自動機。
它是一個零玩家遊戲，這意味著它的演化只由初始狀態決定。

規則（B3/S23）：
1. 存活：一個活細胞，如果周圍有 2 或 3 個活鄰居，則繼續存活
2. 死亡：一個活細胞，如果周圍少於 2 個（孤獨）或多於 3 個（擁擠）活鄰居，則死亡
3. 繁殖：一個死細胞，如果周圍恰好有 3 個活鄰居，則變成活細胞

歷史背景：
- 1970 年：John Conway 發明生命遊戲，發表於《科學美國人》
- 生命遊戲是圖靈完備的（可以模擬圖靈機）
- 它展示了複雜行為可以從簡單規則湧現

參考：Gardner, M. (1970). Mathematical Games: The fantastic combinations of John Conway's new solitaire game "life". Scientific American.
"""

from typing import List, Tuple


Grid = List[List[int]]


def create_grid(width: int, height: int, fill: int = 0) -> Grid:
    """建立一個空白網格"""
    return [[fill for _ in range(width)] for _ in range(height)]


def get_neighbors(grid: Grid, x: int, y: int) -> int:
    """
    計算 (x, y) 位置的活鄰居數量

    使用週期性邊界條件 (toroidal boundary)
    """
    height = len(grid)
    width = len(grid[0])
    count = 0

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % width
            ny = (y + dy) % height
            count += grid[ny][nx]

    return count


def step(grid: Grid) -> Grid:
    """
    計算下一代

    B3/S23 規則：
    - 活細胞：2 或 3 個鄰居 → 存活
    - 死細胞：恰好 3 個鄰居 → 變活
    """
    height = len(grid)
    width = len(grid[0])
    new_grid = create_grid(width, height)

    for y in range(height):
        for x in range(width):
            neighbors = get_neighbors(grid, x, y)
            if grid[y][x] == 1:  # 活細胞
                new_grid[y][x] = 1 if neighbors in [2, 3] else 0
            else:  # 死細胞
                new_grid[y][x] = 1 if neighbors == 3 else 0

    return new_grid


def display(grid: Grid, live: str = '█', dead: str = '·') -> str:
    """將網格轉換為字串表示"""
    lines = []
    for row in grid:
        line = ''.join(live if cell == 1 else dead for cell in row)
        lines.append(line)
    return '\n'.join(lines)


def run_simulation(grid: Grid, generations: int = 10, delay: float = 0.5):
    """
    執行模擬並顯示每一代

    注意：在實際執行時，這裡只是簡化版本
    """
    current = grid
    for gen in range(generations):
        print(f"Generation {gen}:")
        print(display(current))
        print()
        current = step(current)

    # 最後一代
    print(f"Generation {generations}:")
    print(display(current))


# 經典圖案

def glider() -> Grid:
    """滑翔機 (Glider) - 會移動的圖案"""
    grid = create_grid(10, 10)
    grid[1][2] = 1
    grid[2][3] = 1
    grid[3][1] = 1
    grid[3][2] = 1
    grid[3][3] = 1
    return grid


def blinker() -> Grid:
    """閃爍體 (Blinker) - 週期為 2 的振盪器"""
    grid = create_grid(5, 5)
    grid[1][0] = 1
    grid[1][1] = 1
    grid[1][2] = 1
    return grid


def toad() -> Grid:
    """蟾蜍 (Toad) - 週期為 2 的振盪器"""
    grid = create_grid(6, 6)
    grid[1][1] = 1
    grid[1][2] = 1
    grid[1][3] = 1
    grid[2][2] = 1
    grid[2][3] = 1
    grid[2][4] = 1
    return grid


def beacon() -> Grid:
    """燈塔 (Beacon) - 週期為 2 的振盪器"""
    grid = create_grid(6, 6)
    grid[0][0] = 1
    grid[0][1] = 1
    grid[1][0] = 1
    grid[2][3] = 1
    grid[3][2] = 1
    grid[3][3] = 1
    return grid


def r_pentomino() -> Grid:
    """R-五格骨牌 - 需要 1103 代才會穩定"""
    grid = create_grid(20, 20)
    grid[10][11] = 1
    grid[10][12] = 1
    grid[11][10] = 1
    grid[11][11] = 1
    grid[12][11] = 1
    return grid


def gosper_glider_gun() -> Grid:
    """高斯帕滑翔機槍 - 第一個發現的槍 (gun)"""
    grid = create_grid(40, 20)
    # 左方區塊
    grid[5][1] = 1
    grid[5][2] = 1
    grid[6][1] = 1
    grid[6][2] = 1
    # 右方滑翔機產生器
    grid[5][11] = 1
    grid[6][11] = 1
    grid[7][11] = 1
    grid[4][12] = 1
    grid[8][12] = 1
    grid[3][13] = 1
    grid[9][13] = 1
    grid[3][14] = 1
    grid[9][14] = 1
    grid[6][15] = 1
    grid[4][16] = 1
    grid[8][16] = 1
    grid[5][17] = 1
    grid[6][17] = 1
    grid[7][17] = 1
    grid[6][18] = 1
    # 左下方滑翔機產生器
    grid[3][21] = 1
    grid[4][21] = 1
    grid[5][21] = 1
    grid[3][22] = 1
    grid[4][22] = 1
    grid[5][22] = 1
    grid[2][23] = 1
    grid[6][23] = 1
    grid[1][25] = 1
    grid[2][25] = 1
    grid[6][25] = 1
    grid[7][25] = 1
    # 右下方滑翔機產生器
    grid[3][35] = 1
    grid[4][35] = 1
    grid[3][36] = 1
    grid[4][36] = 1

    return grid


if __name__ == "__main__":
    print("=== 康威生命遊戲測試 ===")
    print()

    # 測試：滑翔機
    print("測試：滑翔機 (Glider)")
    grid = glider()
    print(display(grid))
    print()

    # 執行幾代
    print("執行 5 代...")
    for i in range(5):
        grid = step(grid)
        print(f"Generation {i+1}:")
        print(display(grid))
        print()

    # 測試：閃爍體
    print("測試：閃爍體 (Blinker)")
    grid = blinker()
    print("Generation 0:")
    print(display(grid))
    grid = step(grid)
    print("Generation 1:")
    print(display(grid))
    grid = step(grid)
    print("Generation 2 (回到原狀):")
    print(display(grid))
