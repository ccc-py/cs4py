"""
Rule 30 細胞自動機

Rule 30 是 Stephen Wolfram 在 1983 年研究的一維細胞自動機，
以簡單的規則產生複雜的混沌行為。

規則定義（依據三個相鄰細胞的狀態）：
左中右 -> 新細胞
0 0 0 -> 0
0 0 1 -> 1
0 1 0 -> 1
0 1 1 -> 1
1 0 0 -> 1
1 0 1 -> 0
1 1 0 -> 0
1 1 1 -> 0

二進位 00011110 = 十進位 30，因此稱為 Rule 30。

歷史背景：
- 1983 年：Stephen Wolfram 開始系統性研究細胞自動機
- Rule 30 被發現能產生偽隨機數
- Wolfram 將其應用於 Mathematica 的隨機數生成器

參考：Wolfram, S. (1983). Statistical mechanics of cellular automata. Reviews of Modern Physics, 55(3), 601-644.
"""

from typing import List


def rule30(left: int, center: int, right: int) -> int:
    """
    計算 Rule 30 的下一個狀態

    規則表：
    111 -> 0, 110 -> 0, 101 -> 0, 100 -> 1
    011 -> 1, 010 -> 1, 001 -> 1, 000 -> 0
    """
    pattern = (left << 2) | (center << 1) | right
    # Rule 30 的二進位表示：00011110
    return (0b00011110 >> pattern) & 1


def evolve(initial: List[int], steps: int) -> List[List[int]]:
    """
    演化細胞自動機

    Args:
        initial: 初始狀態（一維列表，0 或 1）
        steps: 演化步數

    Returns:
        所有代的狀態列表（包含初始狀態）
    """
    height = steps + 1
    width = len(initial)
    grid = [initial.copy()]

    current = initial.copy()
    for _ in range(steps):
        next_row = []
        for i in range(width):
            left = current[i - 1] if i > 0 else 0
            center = current[i]
            right = current[i + 1] if i < width - 1 else 0
            next_row.append(rule30(left, center, right))
        current = next_row
        grid.append(next_row)

    return grid


def evolve_cyclic(initial: List[int], steps: int) -> List[List[int]]:
    """
    演化細胞自動機（週期性邊界條件）

    邊界相連：最左邊的左鄰居是最右邊的細胞
    """
    height = steps + 1
    width = len(initial)
    grid = [initial.copy()]

    current = initial.copy()
    for _ in range(steps):
        next_row = []
        for i in range(width):
            left = current[(i - 1) % width]
            center = current[i]
            right = current[(i + 1) % width]
            next_row.append(rule30(left, center, right))
        current = next_row
        grid.append(next_row)

    return grid


def display(grid: List[List[int]], live: str = '█', dead: str = '·') -> str:
    """將網格轉換為字串表示"""
    lines = []
    for row in grid:
        line = ''.join(live if cell == 1 else dead for cell in row)
        lines.append(line)
    return '\n'.join(lines)


def single_cell(width: int) -> List[int]:
    """建立只有一個細胞的初始狀態（在中間位置）"""
    state = [0] * width
    state[width // 2] = 1
    return state


def random_state(width: int, seed: int = 42) -> List[int]:
    """建立隨機初始狀態"""
    import random
    random.seed(seed)
    return [random.randint(0, 1) for _ in range(width)]


def count_ones(grid: List[List[int]]) -> int:
    """計算所有細胞中 1 的總數"""
    return sum(sum(row) for row in grid)


if __name__ == "__main__":
    print("=== Rule 30 細胞自動機測試 ===")
    print()

    # 測試：單一細胞
    print("測試：單一細胞（寬度 20，演化 10 代）")
    initial = single_cell(20)
    grid = evolve(initial, 10)
    print(display(grid))
    print()

    # 測試：隨機初始狀態
    print("測試：隨機初始狀態（寬度 30，演化 15 代）")
    initial = random_state(30)
    grid = evolve(initial, 15)
    print(display(grid))
    print()

    # 測試：週期性邊界
    print("測試：週期性邊界（寬度 15，演化 10 代）")
    initial = single_cell(15)
    grid = evolve_cyclic(initial, 10)
    print(display(grid))
    print()

    # 測試：規則驗證
    print("測試：規則驗證")
    test_cases = [
        (0, 0, 0, 0),
        (0, 0, 1, 1),
        (0, 1, 0, 1),
        (0, 1, 1, 1),
        (1, 0, 0, 1),
        (1, 0, 1, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 0),
    ]
    for left, center, right, expected in test_cases:
        result = rule30(left, center, right)
        status = "✓" if result == expected else "✗"
        print(f"  {left}{center}{right} -> {result} (預期 {expected}) {status}")
