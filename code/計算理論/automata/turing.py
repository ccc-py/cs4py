"""
圖靈機 (Turing Machine)

圖靈機是計算理論中最強大的計算模型，由 Alan Turing 在 1936 年提出。
圖靈機可以模擬任何可計算的函數，是現代計算機的理論基礎。

圖靈機的組成：
1. Q: 有限狀態集合
2. Σ: 輸入字母表（不包含空白符號）
3. Γ: 帶字母表（包含 Σ 和空白符號 B）
4. δ: 轉移函數，Q × Γ → Q × Γ × {L, R, S}
5. q0: 起始狀態
6. q_accept: 接受狀態
7. q_reject: 拒絕狀態

歷史背景：
- 1936 年：Alan Turing 發表《On Computable Numbers》，提出圖靈機概念
- 1936 年：Alonzo Church 提出 Church-Turing Thesis
- 圖靈因此被譽為「計算機科學之父」

參考：Turing, A. M. (1936). On Computable Numbers, with an Application to the Entscheidungsproblem.
"""


class TuringMachine:
    """圖靈機模擬器"""

    def __init__(self, states, input_alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state, blank='B'):
        """
        初始化圖靈機

        Args:
            states: 狀態集合 (set)
            input_alphabet: 輸入字母表 (set)
            tape_alphabet: 帶字母表 (set)，包含輸入字母表和空白符號
            transitions: 轉移函數 (dict)，格式: {(state, symbol): (next_state, write_symbol, direction)}
                direction: 'L' = 左移, 'R' = 右移, 'S' = 靜止
            start_state: 起始狀態
            accept_state: 接受狀態
            reject_state: 拒絕狀態
            blank: 空白符號（預設 'B'）
        """
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank = blank

    def run(self, input_string, max_steps=1000):
        """
        執行圖靈機

        Args:
            input_string: 輸入字串
            max_steps: 最大步數（防止無限循環）

        Returns:
            (accepted, steps, tape_snapshots) 元組
        """
        # 初始化帶子
        tape = list(input_string) + [self.blank]
        head = 0
        state = self.start_state
        steps = 0
        snapshots = [(state, head, ''.join(tape[:20]))]  # 記錄快照

        while steps < max_steps:
            if state == self.accept_state:
                return True, steps, snapshots
            if state == self.reject_state:
                return False, steps, snapshots

            # 獲取當前符號
            symbol = tape[head] if head < len(tape) else self.blank

            # 查詢轉移
            key = (state, symbol)
            if key not in self.transitions:
                # 沒有轉移，進入拒絕狀態
                return False, steps, snapshots

            next_state, write_symbol, direction = self.transitions[key]

            # 寫入符號
            if head < len(tape):
                tape[head] = write_symbol
            else:
                tape.append(write_symbol)

            # 移動讀寫頭
            if direction == 'L':
                head = max(0, head - 1)
            elif direction == 'R':
                head += 1
                if head >= len(tape):
                    tape.append(self.blank)

            state = next_state
            steps += 1
            snapshots.append((state, head, ''.join(tape[:20])))

        # 超過最大步數
        return False, steps, snapshots

    def accepts(self, input_string):
        """判斷輸入字串是否被接受"""
        accepted, _, _ = self.run(input_string)
        return accepted


def create_tm_0n1n():
    """
    建立一個圖靈機，接受語言 {0^n 1^n | n ≥ 1}

    策略：
    1. 將一個 0 標記為 X（已配對）
    2. 向右移動找到一個 1，標記為 Y（已配對）
    3. 回到起點重複
    4. 如果所有 0 和 1 都被標記，則接受

    狀態設計：
    q0: 開始，遇到 0 轉為 X，去 q1；遇到 B（空白）去 q_accept
    q1: 跳過 0 和 X，遇到 1 轉為 Y，去 q2；遇到 B 拒絕
    q2: 跳過 1 和 Y，遇到 X 去 q0（回到起點）
    """
    states = {'q0', 'q1', 'q2', 'q_accept', 'q_reject'}
    input_alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', 'X', 'Y', 'B'}
    transitions = {
        # q0: 處理 0
        ('q0', '0'): ('q1', 'X', 'R'),    # 標記 0 為 X，向右
        ('q0', 'X'): ('q0', 'X', 'R'),    # 跳過已標記的 X
        ('q0', 'Y'): ('q0', 'Y', 'R'),    # 跳過已標記的 Y
        ('q0', 'B'): ('q_accept', 'B', 'S'),  # 空白，接受
        # q1: 找 1
        ('q1', '0'): ('q1', '0', 'R'),    # 跳過未標記的 0
        ('q1', '1'): ('q2', 'Y', 'L'),    # 標記 1 為 Y，向左
        ('q1', 'X'): ('q1', 'X', 'R'),    # 跳過 X
        ('q1', 'Y'): ('q1', 'Y', 'R'),    # 跳過 Y
        ('q1', 'B'): ('q_reject', 'B', 'S'),  # 沒有 1 可配對，拒絕
        # q2: 回到起點
        ('q2', '0'): ('q2', '0', 'L'),    # 向左
        ('q2', '1'): ('q2', '1', 'L'),    # 向左
        ('q2', 'X'): ('q0', 'X', 'R'),    # 找到 X，回到 q0
        ('q2', 'Y'): ('q2', 'Y', 'L'),    # 向左
    }
    start_state = 'q0'
    accept_state = 'q_accept'
    reject_state = 'q_reject'

    return TuringMachine(states, input_alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state)


def create_tm_palindrome():
    """
    建立一個圖靈機，接受所有偶數長度的回文（僅包含 0 和 1）

    策略：
    1. 將第一個符號標記為 X
    2. 掃描到結尾，找到最後一個相同符號，標記為 X
    3. 重複直到所有符號都被標記

    這是一個較複雜的圖靈機，狀態較多。
    """
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q_accept', 'q_reject'}
    input_alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', 'X', 'B'}
    transitions = {
        # q0: 開始，讀第一個符號
        ('q0', '0'): ('q1', 'X', 'R'),    # 標記 0，去找最後一個 0
        ('q0', '1'): ('q3', 'X', 'R'),    # 標記 1，去找最後一個 1
        ('q0', 'X'): ('q0', 'X', 'R'),    # 跳過已標記
        ('q0', 'B'): ('q_accept', 'B', 'S'),  # 空白，接受（空字串是回文）
        # q1: 找最後一個 0
        ('q1', '0'): ('q1', '0', 'R'),    # 向右
        ('q1', '1'): ('q1', '1', 'R'),    # 向右
        ('q1', 'X'): ('q1', 'X', 'R'),    # 向右
        ('q1', 'B'): ('q2', 'B', 'L'),    # 到達空白，向左找
        # q2: 向左找 0
        ('q2', '0'): ('q0', 'X', 'R'),    # 找到 0，標記並回到 q0
        ('q2', '1'): ('q_reject', '1', 'S'),  # 找到 1，不是回文
        ('q2', 'X'): ('q2', 'X', 'L'),    # 向左
        # q3: 找最後一個 1
        ('q3', '0'): ('q3', '0', 'R'),    # 向右
        ('q3', '1'): ('q3', '1', 'R'),    # 向右
        ('q3', 'X'): ('q3', 'X', 'R'),    # 向右
        ('q3', 'B'): ('q4', 'B', 'L'),    # 到達空白，向左找
        # q4: 向左找 1
        ('q4', '1'): ('q0', 'X', 'R'),    # 找到 1，標記並回到 q0
        ('q4', '0'): ('q_reject', '0', 'S'),  # 找到 0，不是回文
        ('q4', 'X'): ('q4', 'X', 'L'),    # 向左
    }
    start_state = 'q0'
    accept_state = 'q_accept'
    reject_state = 'q_reject'

    return TuringMachine(states, input_alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state)


if __name__ == "__main__":
    # 測試：{0^n 1^n}
    print("=== 測試：語言 {0^n 1^n} ===")
    tm = create_tm_0n1n()
    test_cases = ["01", "0011", "000111", "001", "0101", "0", "1"]
    for s in test_cases:
        accepted = tm.accepts(s)
        # 驗證：檢查是否真的是 n 個 0 後跟 n 個 1
        n = len(s) // 2
        expected = len(s) % 2 == 0 and s == '0' * n + '1' * n
        print(f"'{s}' -> TM: {accepted}, 預期: {expected}, 正確: {accepted == expected}")

    print()

    # 測試：回文
    print("=== 測試：偶數長度回文 ===")
    tm_pal = create_tm_palindrome()
    test_cases = ["00", "11", "0110", "1001", "01", "10", "0011", "0101"]
    for s in test_cases:
        accepted = tm_pal.accepts(s)
        expected = len(s) % 2 == 0 and s == s[::-1]
        print(f"'{s}' -> TM: {accepted}, 預期: {expected}, 正確: {accepted == expected}")
