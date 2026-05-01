"""
NFA 轉 DFA（子集構造法，Subset Construction）

將非確定性有限狀態自動機 (NFA) 轉換為等價的確定性有限狀態自動機 (DFA)。

子集構造法原理：
- DFA 的每個狀態對應 NFA 的一個狀態集合（冪集構造）
- DFA 的起始狀態 = NFA 起始狀態的 ε-閉包
- DFA 的轉移：對於 DFA 狀態 S（NFA 狀態集合）和符號 a，
  DFA 的下一個狀態 = ε-閉包(所有從 S 中狀態透過 a 可達的 NFA 狀態)
- DFA 的接受狀態：任何包含 NFA 接受狀態的 DFA 狀態

歷史背景：
子集構造法由 Rabin 和 Scott 在 1959 年提出，證明了 NFA 和 DFA 的等價性。
雖然 NFA 更簡潔，但轉換後的 DFA 狀態數可能是指數級增長（2^n）。

參考：Rabin, M. O., & Scott, D. (1959). Finite automata and their decision problems.
"""


class DFA:
    """簡化的 DFA 類別，用於 NFA 轉換結果"""

    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if (current_state, symbol) not in self.transitions:
                return False
            current_state = self.transitions[(current_state, symbol)]
        return current_state in self.accept_states

    def __repr__(self):
        return f"DFA(states={len(self.states)}, start={self.start_state}, accept={self.accept_states})"


def nfa_to_dfa(nfa):
    """
    將 NFA 轉換為等價的 DFA（子集構造法）

    Args:
        nfa: NFA 物件

    Returns:
        DFA 物件
    """
    # 計算起始狀態的 ε-閉包
    start_closure = frozenset(nfa.epsilon_closure(nfa.start_state))
    
    dfa_states = {start_closure}
    dfa_transitions = {}
    dfa_accept = set()
    unprocessed = [start_closure]

    # 如果起始狀態的閉包包含 NFA 接受狀態，則 DFA 起始狀態也是接受狀態
    if nfa.accept_states & start_closure:
        dfa_accept.add(start_closure)

    while unprocessed:
        current_set = unprocessed.pop()

        for symbol in nfa.alphabet:
            # 計算從 current_set 中所有狀態透過 symbol 可達的狀態
            next_states = set()
            for state in current_set:
                key = (state, symbol)
                if key in nfa.transitions:
                    next_states.update(nfa.transitions[key])

            # 計算 ε-閉包
            next_closure = frozenset(nfa.epsilon_closure(next_states))

            if not next_closure:
                continue

            # 添加轉移
            dfa_transitions[(current_set, symbol)] = next_closure

            # 如果是新狀態，加入待處理列表
            if next_closure not in dfa_states:
                dfa_states.add(next_closure)
                unprocessed.append(next_closure)

                # 檢查是否為接受狀態
                if nfa.accept_states & next_closure:
                    dfa_accept.add(next_closure)

    return DFA(dfa_states, nfa.alphabet, dfa_transitions, start_closure, dfa_accept)


def nfa_state_to_str(state_set):
    """將 NFA 狀態集合轉換為字串表示"""
    return "{" + ",".join(sorted(state_set)) + "}"


def print_dfa(dfa):
    """印出 DFA 的資訊"""
    print(f"DFA 狀態數: {len(dfa.states)}")
    print(f"字母表: {dfa.alphabet}")
    print(f"起始狀態: {nfa_state_to_str(dfa.start_state)}")
    print(f"接受狀態: {[nfa_state_to_str(s) for s in dfa.accept_states]}")
    print("轉移:")
    for (state, symbol), next_state in sorted(dfa.transitions.items()):
        print(f"  {nfa_state_to_str(state)} --{symbol}--> {nfa_state_to_str(next_state)}")


if __name__ == "__main__":
    from theory.automata.nfa import create_nfa_ends_with_01

    print("=== NFA 轉 DFA 示範 ===")
    print()

    # 建立 NFA（以 '01' 結尾）
    nfa = create_nfa_ends_with_01()
    print("原始 NFA:")
    print(f"  狀態: {nfa.states}")
    print(f"  起始: {nfa.start_state}")
    print(f"  接受: {nfa.accept_states}")
    print()

    # 轉換為 DFA
    dfa = nfa_to_dfa(nfa)
    print("轉換後的 DFA:")
    print_dfa(dfa)
    print()

    # 測試
    print("測試:")
    test_strings = ["01", "101", "001", "0", "1", "0101", "010"]
    for s in test_strings:
        nfa_result = nfa.accepts(s)
        dfa_result = dfa.accepts(s)
        match = nfa_result == dfa_result
        print(f"  '{s}': NFA={nfa_result}, DFA={dfa_result}, 一致={match}")
