"""
非確定性有限狀態自動機 (Nondeterministic Finite Automaton, NFA)

NFA 是計算理論中的另一個基礎計算模型，與 DFA 不同的是：
1. 對於同一個狀態和輸入符號，可以有多個下一個狀態（透過集合表示）
2. 允許 ε-轉移（不需要讀入符號的轉移）

NFA 與 DFA 的等價性：任何 NFA 都可以轉換成等價的 DFA（子集構造法）。

歷史背景：
NFA 的概念由 Rabin 和 Scott 在 1959 年提出，他們證明了
NFA 和 DFA 識別的語言類別相同（都是正規語言）。

參考：Rabin, M. O., & Scott, D. (1959). Finite automata and their decision problems.
"""


class NFA:
    """非確定性有限狀態自動機"""

    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        """
        初始化 NFA

        Args:
            states: 狀態集合 (set)
            alphabet: 字母表 (set)，不包含 ε
            transitions: 轉移函數 (dict)，格式: {(state, symbol): {next_states}}
                        symbol 可以是 ε (空字串) 表示 ε-轉移
            start_state: 起始狀態（單一狀態或集合）
            accept_states: 接受狀態集合 (set)
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state if isinstance(start_state, set) else {start_state}
        self.accept_states = accept_states

    def epsilon_closure(self, states):
        """
        計算給定狀態集合的 ε-閉包

        ε-閉包定義：從 states 中的任何狀態出發，透過零個或多個 ε-轉移
        可以到達的所有狀態的集合。

        Args:
            states: 狀態集合 (set)

        Returns:
            ε-閉包 (set)
        """
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            # 檢查是否有 ε-轉移
            key = (state, '')
            if key in self.transitions:
                for next_state in self.transitions[key]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    def process(self, input_string):
        """
        處理輸入字串，返回所有可能的最終狀態集合

        Args:
            input_string: 輸入字串

        Returns:
            所有可能的最終狀態集合 (set)
        """
        # 初始狀態：起始狀態的 ε-閉包
        current_states = self.epsilon_closure(self.start_state)

        for symbol in input_string:
            if symbol not in self.alphabet and symbol != '':
                raise ValueError(f"符號 '{symbol}' 不在字母表中")

            next_states = set()
            for state in current_states:
                key = (state, symbol)
                if key in self.transitions:
                    next_states.update(self.transitions[key])

            # 對所有新狀態計算 ε-閉包
            current_states = self.epsilon_closure(next_states)

        return current_states

    def accepts(self, input_string):
        """
        判斷輸入字串是否被接受

        NFA 接受字串的條件：存在至少一條路徑從起始狀態到達接受狀態

        Args:
            input_string: 輸入字串

        Returns:
            True 如果字串被接受，否則 False
        """
        final_states = self.process(input_string)
        return bool(final_states & self.accept_states)


def create_nfa_contains_01():
    """
    建立一個 NFA，接受所有包含 '01' 作為子字串的字串

    使用 ε-轉移來簡化構造：
    - 先建構識別 '01' 的 NFA
    - 在前面和後面加上 ε-轉移，允許任意前綴和後綴
    """
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'0', '1'}
    transitions = {
        # 起始狀態 q0 可以透過 ε-轉移到 q1（開始匹配 '01'）
        # 或者透過讀入 0 或 1 保持在 q0（跳過前綴）
        ('q0', '0'): {'q0', 'q1'},
        ('q0', '1'): {'q0'},
        # 讀入 1 後，如果之前讀入 0，則到達 q2
        ('q1', '1'): {'q2'},
        # 在 q2 可以透過 ε-轉移到 q3（接受狀態）
        # 也可以在 q2 繼續讀入任意符號
        ('q2', '0'): {'q2'},
        ('q2', '1'): {'q2'},
        ('q2', ''): {'q3'},  # ε-轉移
        # q3 是接受狀態，可以讀入任意符號
        ('q3', '0'): {'q3'},
        ('q3', '1'): {'q3'},
    }
    start_state = 'q0'
    accept_states = {'q3'}

    return NFA(states, alphabet, transitions, start_state, accept_states)


def create_nfa_ends_with_01():
    """
    建立一個 NFA，接受所有以 '01' 結尾的字串

    這個 NFA 比等價的 DFA 更簡潔
    """
    states = {'q0', 'q1', 'q2'}
    alphabet = {'0', '1'}
    transitions = {
        # q0 可以讀入任意符號（包括透過 ε-轉移保持在 q0）
        ('q0', '0'): {'q0', 'q1'},
        ('q0', '1'): {'q0'},
        # 讀入 1 到達接受狀態 q2
        ('q1', '1'): {'q2'},
    }
    start_state = 'q0'
    accept_states = {'q2'}

    return NFA(states, alphabet, transitions, start_state, accept_states)


if __name__ == "__main__":
    # 測試：包含 '01' 的字串
    print("=== 測試：包含 '01' 的字串 ===")
    nfa_contains = create_nfa_contains_01()
    test_strings = ["01", "101", "001", "0", "1", "0101", "111", "010"]
    for s in test_strings:
        accepted = nfa_contains.accepts(s)
        expected = '01' in s
        print(f"'{s}' -> NFA: {accepted}, 預期: {expected}, 正確: {accepted == expected}")

    print()

    # 測試：以 '01' 結尾的字串
    print("=== 測試：以 '01' 結尾的字串 ===")
    nfa_ends = create_nfa_ends_with_01()
    test_strings = ["01", "101", "001", "0", "1", "0101", "010"]
    for s in test_strings:
        accepted = nfa_ends.accepts(s)
        expected = s.endswith("01")
        print(f"'{s}' -> NFA: {accepted}, 預期: {expected}, 正確: {accepted == expected}")

    print()

    # 比較 NFA 和 DFA 的處理結果
    print("=== 比較 NFA 和 DFA（以 '01' 結尾）===")
    from theory.automata.dfa import create_dfa_ends_with_01
    dfa = create_dfa_ends_with_01()
    nfa = create_nfa_ends_with_01()
    test_strings = ["01", "101", "001", "0", "1", "0101", "010"]
    for s in test_strings:
        dfa_result = dfa.accepts(s)
        nfa_result = nfa.accepts(s)
        match = dfa_result == nfa_result
        print(f"'{s}' -> DFA: {dfa_result}, NFA: {nfa_result}, 一致: {match}")
