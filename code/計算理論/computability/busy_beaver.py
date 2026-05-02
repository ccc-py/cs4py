"""
忙碌海狸函數 (Busy Beaver Function)

忙碌海狸函數 Σ(n) 定義為：
  Σ(n) = n 狀態圖靈機在停止前所能輸出的 '1' 的最大數量

這個函數由 Tibor Radó 於 1962 年提出，是計算理論中著名的不可計算函數。

已知值：
  Σ(1) = 1
  Σ(2) = 4
  Σ(3) = 6
  Σ(4) = 13
  Σ(5) ≥ 4098 (尚未證明最大值)
  Σ(6) > 3.5 × 10^18 (驚人的增長)

歷史背景：
- 1962 年：Tibor Radó 提出忙碌海狸問題
- 這是第一個被證明的「自然」不可計算函數
- 相關於圖靈停機問題 (Halting Problem)

參考：Radó, T. (1962). On non-computable functions. Bell System Technical Journal, 41(3), 877-884.
"""

from typing import Dict, List, Optional, Tuple


class TuringMachine:
    """圖靈機類別，用於模擬忙碌海狸機"""

    def __init__(self, num_states: int, transitions: Dict[Tuple[int, str], Tuple[int, str, str]]):
        """
        初始化圖靈機

        Args:
            num_states: 狀態數量（不包括停止狀態）
            transitions: 轉移函數，格式為 {(state, read): (new_state, write, move)}
                        move: 'L' 向左, 'R' 向右, 'S' 停止
        """
        self.num_states = num_states
        self.transitions = transitions
        self.reset()

    def reset(self):
        """重設圖靈機到初始狀態"""
        self.tape: Dict[int, str] = {0: '0'}  # 無限紙帶，預設為 '0'
        self.head: int = 0  # 讀寫頭位置
        self.state: int = 1  # 當前狀態，從狀態 1 開始
        self.ones_count: int = 0  # '1' 的數量
        self.steps: int = 0  # 執行步數

    def get_tape_symbol(self, pos: int) -> str:
        """取得紙帶在指定位置的符號"""
        return self.tape.get(pos, '0')

    def write_symbol(self, pos: int, symbol: str):
        """在紙帶指定位置寫入符號，正確更新 ones_count"""
        old = self.get_tape_symbol(pos)
        if old == '1' and symbol != '1':
            self.ones_count -= 1
        elif old != '1' and symbol == '1':
            self.ones_count += 1

        if symbol == '0':
            if pos in self.tape:
                del self.tape[pos]
        else:
            self.tape[pos] = symbol

    def step(self) -> bool:
        """
        執行一個步驟

        Returns:
            True 如果機器繼續執行，False 如果停止
        """
        current_symbol = self.get_tape_symbol(self.head)
        key = (self.state, current_symbol)

        if key not in self.transitions:
            return False  # 沒有轉移規則，停止

        new_state, write_symbol, move = self.transitions[key]

        # 寫入符號（write_symbol 會自動更新 ones_count）
        self.write_symbol(self.head, write_symbol)

        # 移動讀寫頭
        if move == 'L':
            self.head -= 1
        elif move == 'R':
            self.head += 1
        elif move == 'S':
            return False  # 停止

        # 更新狀態
        if new_state == 0:
            return False  # 狀態 0 表示停止狀態
        self.state = new_state

        self.steps += 1
        return True

    def run(self, max_steps: int = 100000) -> Tuple[int, int]:
        """
        執行圖靈機直到停止

        Args:
            max_steps: 最大執行步數（防止無限迴圈）

        Returns:
            (執行步數, '1' 的數量)
        """
        self.reset()
        while self.steps < max_steps:
            if not self.step():
                break
        return self.steps, self.ones_count

    def get_tape_string(self, max_display: int = 20) -> str:
        """取得紙帶內容的字串表示"""
        if not self.tape:
            return "空紙帶"
        min_pos = min(self.tape.keys())
        max_pos = max(self.tape.keys())
        # 擴展顯示範圍
        min_pos = max(min_pos - 1, -max_display)
        max_pos = min(max_pos + 1, max_display)
        result = ""
        for i in range(min_pos, max_pos + 1):
            result += self.get_tape_symbol(i)
        return result


def create_bb_1state() -> TuringMachine:
    """
    1 狀態忙碌海狸機：Σ(1) = 1

    轉移：
    狀態1, 讀0 → 狀態0(停止), 寫1, 不移動(或右移)
    """
    transitions = {
        (1, '0'): (0, '1', 'S'),  # 寫 1 然後停止
    }
    return TuringMachine(1, transitions)


def create_bb_2state() -> TuringMachine:
    """
    2 狀態忙碌海狸機：Σ(2) = 4

    這是 2 狀態的忙碌海狸冠軍機器
    經過 6 步後停止，紙帶上有 4 個 '1'
    """
    transitions = {
        (1, '0'): (2, '1', 'R'),  # 狀態1 讀0: 寫1, 右移, 到狀態2
        (1, '1'): (2, '1', 'L'),  # 狀態1 讀1: 寫1, 左移, 到狀態2
        (2, '0'): (1, '1', 'L'),  # 狀態2 讀0: 寫1, 左移, 到狀態1
        (2, '1'): (0, '1', 'R'),  # 狀態2 讀1: 寫1, 右移, 停止
    }
    return TuringMachine(2, transitions)


def create_bb_3state() -> TuringMachine:
    """
    3 狀態忙碌海狸機：Σ(3) = 6

    這是 3 狀態的忙碌海狸冠軍機器（TNF: 1RB1LC_1RC1RZ_1LA0LB）
    經過 11 步後停止，紙帶上有 6 個 '1'
    """
    transitions = {
        (1, '0'): (2, '1', 'R'),  # A0 → 1,R,B
        (1, '1'): (3, '1', 'L'),  # A1 → 1,L,C
        (2, '0'): (3, '1', 'R'),  # B0 → 1,R,C
        (2, '1'): (0, '1', 'R'),  # B1 → 1,R,H (停止)
        (3, '0'): (1, '1', 'L'),  # C0 → 1,L,A
        (3, '1'): (2, '0', 'L'),  # C1 → 0,L,B
    }
    return TuringMachine(3, transitions)


def create_bb_4state() -> TuringMachine:
    """
    4 狀態忙碌海狸機：Σ(4) = 13

    這是 4 狀態的忙碌海狸冠軍機器
    經過 107 步後停止，紙帶上有 13 個 '1'
    轉移規則（TNF: 1RB1LB_1LA0LC_1RZ1LD_1RD0RA）
    """
    transitions = {
        # 狀態 A (1)
        (1, '0'): (2, '1', 'R'),  # A0 → 1,R,B
        (1, '1'): (2, '1', 'L'),  # A1 → 1,L,B
        # 狀態 B (2)
        (2, '0'): (1, '1', 'L'),  # B0 → 1,L,A
        (2, '1'): (3, '0', 'L'),  # B1 → 0,L,C
        # 狀態 C (3)
        (3, '0'): (0, '1', 'R'),  # C0 → 1,R,H (停止)
        (3, '1'): (4, '1', 'L'),  # C1 → 1,L,D
        # 狀態 D (4)
        (4, '0'): (4, '1', 'R'),  # D0 → 1,R,D
        (4, '1'): (1, '0', 'L'),  # D1 → 0,L,A
    }
    return TuringMachine(4, transitions)


def simulate_bb(machine: TuringMachine, max_steps: int = 10000) -> Tuple[int, int, str]:
    """
    模擬忙碌海狸機並返回結果

    Args:
        machine: 圖靈機
        max_steps: 最大步數

    Returns:
        (步數, '1' 的數量, 紙帶內容)
    """
    steps, ones = machine.run(max_steps)
    tape = machine.get_tape_string()
    return steps, ones, tape


def compute_sigma(n: int) -> Optional[int]:
    """
    計算 Σ(n) 的已知值

    Args:
        n: 狀態數

    Returns:
        Σ(n) 的值，如果未知則返回 None
    """
    known_values = {
        1: 1,
        2: 4,
        3: 6,
        4: 13,
    }
    return known_values.get(n)


if __name__ == "__main__":
    print("=== 忙碌海狸函數 Σ(n) 測試 ===")
    print()

    # 測試 1 狀態
    print("Σ(1) = 1")
    bb1 = create_bb_1state()
    steps, ones, tape = simulate_bb(bb1)
    print(f"  步數: {steps}")
    print(f"  '1' 數量: {ones}")
    print(f"  紙帶: {tape}")
    print(f"  正確: {ones == 1}")
    print()

    # 測試 2 狀態
    print("Σ(2) = 4")
    bb2 = create_bb_2state()
    steps, ones, tape = simulate_bb(bb2)
    print(f"  步數: {steps}")
    print(f"  '1' 數量: {ones}")
    print(f"  紙帶: {tape}")
    print(f"  正確: {ones == 4}")
    print()

    # 測試 3 狀態
    print("Σ(3) = 6")
    bb3 = create_bb_3state()
    steps, ones, tape = simulate_bb(bb3)
    print(f"  步數: {steps}")
    print(f"  '1' 數量: {ones}")
    print(f"  紙帶: {tape}")
    print(f"  正確: {ones == 6}")
    print()

    # 測試 4 狀態
    print("Σ(4) = 13")
    bb4 = create_bb_4state()
    steps, ones, tape = simulate_bb(bb4)
    print(f"  步數: {steps}")
    print(f"  '1' 數量: {ones}")
    print(f"  紙帶: {tape}")
    print(f"  正確: {ones == 13}")
    print()

    # 顯示已知值表格
    print("=== 忙碌海狸函數已知值 ===")
    print()
    print("  n  |  Σ(n)  |  發現年份  |  備註")
    print("  ---|--------|-----------|------")
    print("  1  |   1    |   1962    | Radó")
    print("  2  |   4    |   1962    | Radó")
    print("  3  |   6    |   1965    | Lin & Rado")
    print("  4  |   13   |   1983    | Brady")
    print("  5  |  ≥4098 |   1989    | Marxen & Buntrock")
    print("  6  | >3.5e18|   2022    | Kropitz & Marxen")
    print()
    print("  Σ(n) 增長極快，且已證明是不可計算的！")
