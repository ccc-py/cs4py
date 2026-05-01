"""
正規表達式轉 NFA（Thompson 構造法）

將正規表達式轉換為等價的 NFA，使用 Thompson 構造法。

支援的運算符：
- 連接 (concatenation): ab
- 聯集 (union): a|b
- Kleene 星號 (Kleene star): a*
- 括號: (...)

歷史背景：
Thompson 構造法由 Ken Thompson 在 1968 年提出，用於將正規表達式
轉換為 NFA。這是現代正規表達式引擎的基礎方法之一。

參考：Thompson, K. (1968). Programming Techniques: Regular expression search algorithm.
"""

import sys
sys.path.append('..')
from automata.nfa import NFA


class NFAFragment:
    """NFA 片段，用於 Thompson 構造法的中間表示"""

    def __init__(self, states, start_state, accept_states, transitions, alphabet):
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.alphabet = alphabet

    @staticmethod
    def from_char(ch):
        """從單一字元建立 NFA 片段"""
        states = {f'q0_{ch}', f'q1_{ch}'}
        start_state = f'q0_{ch}'
        accept_states = {f'q1_{ch}'}
        transitions = {(f'q0_{ch}', ch): {f'q1_{ch}'}}
        alphabet = {ch}
        return NFAFragment(states, start_state, accept_states, transitions, alphabet)

    def to_nfa(self):
        """轉換為 NFA 物件"""
        return NFA(self.states, self.alphabet, self.transitions, self.start_state, self.accept_states)


def thompson_concat(nfa1, nfa2):
    """
    連接運算：nfa1 後接 nfa2

    Thompson 構造法：
    從 nfa1 的接受狀態透過 ε-轉移到 nfa2 的起始狀態
    """
    states = nfa1.states | nfa2.states
    alphabet = nfa1.alphabet | nfa2.alphabet
    transitions = {}

    # 合併轉移
    transitions.update(nfa1.transitions)
    transitions.update(nfa2.transitions)

    # 從 nfa1 的接受狀態透過 ε-轉移到 nfa2 的起始狀態
    for s in nfa1.accept_states:
        key = (s, '')
        if key in transitions:
            transitions[key].add(nfa2.start_state)
        else:
            transitions[key] = {nfa2.start_state}

    return NFAFragment(states, nfa1.start_state, nfa2.accept_states, transitions, alphabet)


def thompson_union(nfa1, nfa2):
    """
    聯集運算：nfa1 | nfa2

    Thompson 構造法：
    1. 建立新的起始狀態，透過 ε-轉移到兩個 NFA 的起始狀態
    2. 建立新的接受狀態，從兩個 NFA 的接受狀態透過 ε-轉移到它
    """
    new_start = f'start_{id(nfa1)}_{id(nfa2)}'
    new_accept = f'accept_{id(nfa1)}_{id(nfa2)}'

    states = {new_start, new_accept} | nfa1.states | nfa2.states
    alphabet = nfa1.alphabet | nfa2.alphabet
    transitions = {}

    # 合併原有轉移
    transitions.update(nfa1.transitions)
    transitions.update(nfa2.transitions)

    # 新起始狀態透過 ε 到兩個 NFA 的起始狀態
    transitions[(new_start, '')] = {nfa1.start_state, nfa2.start_state}

    # 兩個 NFA 的接受狀態透過 ε 到新接受狀態
    for s in nfa1.accept_states:
        key = (s, '')
        if key in transitions:
            transitions[key].add(new_accept)
        else:
            transitions[key] = {new_accept}

    for s in nfa2.accept_states:
        key = (s, '')
        if key in transitions:
            transitions[key].add(new_accept)
        else:
            transitions[key] = {new_accept}

    return NFAFragment(states, new_start, {new_accept}, transitions, alphabet)


def thompson_star(nfa):
    """
    Kleene 星號運算：nfa*

    Thompson 構造法：
    1. 建立新的起始狀態和接受狀態
    2. 起始狀態透過 ε 到原起始狀態和接受狀態
    3. 原接受狀態透過 ε 到原起始狀態和接受狀態
    """
    new_start = f'start_{id(nfa)}'
    new_accept = f'accept_{id(nfa)}'

    states = {new_start, new_accept} | nfa.states
    alphabet = nfa.alphabet
    transitions = {}

    # 原有轉移
    transitions.update(nfa.transitions)

    # 新起始狀態透過 ε 到原起始狀態和新接受狀態（零次匹配）
    transitions[(new_start, '')] = {nfa.start_state, new_accept}

    # 原接受狀態透過 ε 到原起始狀態（循環）和新接受狀態
    for s in nfa.accept_states:
        key = (s, '')
        if key in transitions:
            transitions[key].update({nfa.start_state, new_accept})
        else:
            transitions[key] = {nfa.start_state, new_accept}

    return NFAFragment(states, new_start, {new_accept}, transitions, alphabet)


class RegexToNFA:
    """將正規表達式轉換為 NFA（使用 Thompson 構造法）"""

    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0

    def parse(self):
        """解析並返回 NFA"""
        return self._parse_expr().to_nfa()

    def _peek(self):
        if self.pos < len(self.pattern):
            return self.pattern[self.pos]
        return None

    def _consume(self):
        ch = self.pattern[self.pos]
        self.pos += 1
        return ch

    def _parse_expr(self):
        """解析運算式（由 | 分隔）"""
        nfa = self._parse_term()

        while self._peek() == '|':
            self._consume()  # 消耗 '|'
            nfa2 = self._parse_term()
            nfa = thompson_union(nfa, nfa2)

        return nfa

    def _parse_term(self):
        """解析項（連接）"""
        nfa = self._parse_factor()

        while self._peek() is not None and self._peek() not in ('|', ')'):
            factor_nfa = self._parse_factor()
            nfa = thompson_concat(nfa, factor_nfa)

        return nfa

    def _parse_factor(self):
        """解析因子（帶 *）"""
        nfa = self._parse_primary()

        if self._peek() == '*':
            self._consume()
            nfa = thompson_star(nfa)

        return nfa

    def _parse_primary(self):
        """解析基本單元"""
        ch = self._peek()

        if ch == '(':
            self._consume()  # 消耗 '('
            nfa = self._parse_expr()
            if self._peek() != ')':
                raise ValueError("缺少右括號")
            self._consume()  # 消耗 ')'
            return nfa

        if ch not in (None, '|', ')', '*'):
            self._consume()
            return NFAFragment.from_char(ch)

        raise ValueError(f"意外的字元: {ch}")


if __name__ == "__main__":
    print("=== Thompson 構造法測試 ===")
    print()

    # 測試：連接 ab
    print("測試: 'ab' (連接)")
    regex = RegexToNFA('ab')
    nfa = regex.parse()
    print(f"  狀態數: {len(nfa.states)}")
    print(f"  起始態: {nfa.start_state}")
    print(f"  接受態: {nfa.accept_states}")
    test_cases = ["ab", "a", "b", "aba"]
    for s in test_cases:
        result = nfa.accepts(s)
        print(f"  '{s}': {result}")

    print()

    # 測試：a|b
    print("測試: 'a|b' (聯集)")
    regex = RegexToNFA('a|b')
    nfa = regex.parse()
    test_cases = ["a", "b", "c", ""]
    for s in test_cases:
        result = nfa.accepts(s)
        print(f"  '{s}': {result}")

    print()

    # 測試：a*
    print("測試: 'a*' (Kleene 星號)")
    regex = RegexToNFA('a*')
    nfa = regex.parse()
    test_cases = ["", "a", "aa", "aaa", "b"]
    for s in test_cases:
        result = nfa.accepts(s)
        print(f"  '{s}': {result}")
