"""
確定性有限狀態自動機 (Deterministic Finite Automaton, DFA)

DFA 是計算理論中最基礎的計算模型之一，由五個元素組成：
1. Q: 有限狀態集合
2. Σ: 有限字母表（輸入符號集合）
3. δ: 轉移函數 Q × Σ → Q
4. q0: 起始狀態 (q0 ∈ Q)
5. F: 接受狀態集合 (F ⊆ Q)

歷史背景：
DFA 的概念源自於 1943 年 McCulloch 和 Pitts 的神經網路模型，
隨後在 1956 年由 Kleene 形式化，並在 1959 年由 Rabin 和 Scott
證明了 DFA 與 NFA 的等價性（獲得圖靈獎）。

參考：Rabin, M. O., & Scott, D. (1959). Finite automata and their decision problems.
"""


class DFA:
    """確定性有限狀態自動機"""

    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        初始化 DFA

        Args:
            states: 狀態集合 (set)
            alphabet: 字母表 (set)
            transitions: 轉移函數 (dict)，格式: {(state, symbol): next_state}
            start_state: 起始狀態
            accept_states: 接受狀態集合 (set)
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def process(self, input_string):
        """
        處理輸入字串，返回最終狀態

        Args:
            input_string: 輸入字串

        Returns:
            最終狀態
        """
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"符號 '{symbol}' 不在字母表中")
            if (current_state, symbol) not in self.transitions:
                raise ValueError(f"狀態 '{current_state}' 沒有符號 '{symbol}' 的轉移")
            current_state = self.transitions[(current_state, symbol)]
        return current_state

    def accepts(self, input_string):
        """
        判斷輸入字串是否被接受

        Args:
            input_string: 輸入字串

        Returns:
            True 如果字串被接受，否則 False
        """
        final_state = self.process(input_string)
        return final_state in self.accept_states

    def get_all_reachable_states(self):
        """獲取所有可達狀態"""
        reachable = {self.start_state}
        changed = True
        while changed:
            changed = False
            for (state, symbol), next_state in self.transitions.items():
                if state in reachable and next_state not in reachable:
                    reachable.add(next_state)
                    changed = True
        return reachable


def create_dfa_divisible_by_3():
    """
    建立一個 DFA，接受所有二進位表示且能被 3 整除的數字

    狀態代表除以 3 的餘數：
    q0: 餘數 0 (接受狀態)
    q1: 餘數 1
    q2: 餘數 2

    轉移規則：讀入 bit b，新餘數 = (舊餘數 * 2 + b) % 3
    """
    states = {'q0', 'q1', 'q2'}
    alphabet = {'0', '1'}
    transitions = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q2',
        ('q1', '1'): 'q0',
        ('q2', '0'): 'q1',
        ('q2', '1'): 'q2',
    }
    start_state = 'q0'
    accept_states = {'q0'}

    return DFA(states, alphabet, transitions, start_state, accept_states)


def create_dfa_ends_with_01():
    """
    建立一個 DFA，接受所有以 '01' 結尾的字串

    狀態：
    q0: 起始狀態，尚未看到 0
    q1: 最後看到 0
    q2: 最後看到 01 (接受狀態)
    """
    states = {'q0', 'q1', 'q2'}
    alphabet = {'0', '1'}
    transitions = {
        ('q0', '0'): 'q1',
        ('q0', '1'): 'q0',
        ('q1', '0'): 'q1',
        ('q1', '1'): 'q2',
        ('q2', '0'): 'q1',
        ('q2', '1'): 'q0',
    }
    start_state = 'q0'
    accept_states = {'q2'}

    return DFA(states, alphabet, transitions, start_state, accept_states)


if __name__ == "__main__":
    # 測試：能被 3 整除的二進位數
    print("=== 測試：能被 3 整除的二進位數 ===")
    dfa_div3 = create_dfa_divisible_by_3()
    test_cases = ["0", "11", "110", "1001", "1010", "1111"]
    for binary in test_cases:
        decimal = int(binary, 2) if binary else 0
        accepted = dfa_div3.accepts(binary)
        divisible = decimal % 3 == 0
        print(f"{binary} (十進位: {decimal}) -> DFA: {accepted}, 實際: {divisible}, 正確: {accepted == divisible}")

    print()

    # 測試：以 '01' 結尾的字串
    print("=== 測試：以 '01' 結尾的字串 ===")
    dfa_01 = create_dfa_ends_with_01()
    test_strings = ["01", "101", "001", "0", "1", "0101", "010"]
    for s in test_strings:
        accepted = dfa_01.accepts(s)
        expected = s.endswith("01")
        print(f"'{s}' -> DFA: {accepted}, 預期: {expected}, 正確: {accepted == expected}")
