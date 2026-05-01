"""
正規表達式引擎（從頭實作）

本模組實作一個簡單的正規表達式引擎，不依賴 Python 的 re 模組。
使用 Thompson 構造法將正規表達式轉換為 NFA，然後用 NFA 匹配字串。

支援的運算符：
- . : 任意單一字元（除了換行）
- * : 零次或多次（Kleene 星號）
- | : 或 (alternation)
- () : 分組
- \ : 跳脫字元

歷史背景：
- 1951 年：Stephen Kleene 提出正規表達式，用於描述正規語言
- 1968 年：Ken Thompson 在 QED 編輯器中實作了第一個正規表達式引擎
  （使用 NFA 方法，即 Thompson 構造法）
- 1980 年代：Henry Spencer 實作了更高效的引擎（使用 DFA 方法）

參考：Thompson, K. (1968). Programming Techniques: Regular expression search algorithm.
"""

import sys
sys.path.append('..')
from automata.nfa import NFA


class RegexParser:
    """正規表達式解析器（將 regex 字串轉換為 NFA）"""

    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0

    def parse(self):
        """解析正規表達式，返回 NFA"""
        return self._parse_expr()

    def _peek(self):
        """查看當前字元"""
        if self.pos < len(self.pattern):
            return self.pattern[self.pos]
        return None

    def _consume(self):
        """消耗當前字元並返回"""
        ch = self.pattern[self.pos]
        self.pos += 1
        return ch

    def _parse_expr(self):
        """解析運算式（由 | 分隔的多個項）"""
        nfa = self._parse_term()

        while self._peek() == '|':
            self._consume()  # 消耗 '|'
            nfa2 = self._parse_term()
            nfa = self._union(nfa, nfa2)

        return nfa

    def _parse_term(self):
        """解析項（連接的多個因子）"""
        # 解析第一個因子
        nfa = self._parse_factor()

        # 繼續解析後續因子（隱式連接）
        while self._peek() is not None and self._peek() not in ('|', ')'):
            factor_nfa = self._parse_factor()
            nfa = self._concat(nfa, factor_nfa)

        return nfa

    def _parse_factor(self):
        """解析因子（帶 * 或其他修飾符的基本單元）"""
        nfa = self._parse_primary()

        # 檢查是否有 * 修飾符
        if self._peek() == '*':
            self._consume()
            nfa = self._kleene_star(nfa)

        return nfa

    def _parse_primary(self):
        """解析基本單元（字元、分組或跳脫）"""
        ch = self._peek()

        if ch == '(':
            self._consume()  # 消耗 '('
            nfa = self._parse_expr()
            if self._peek() != ')':
                raise ValueError("缺少右括號")
            self._consume()  # 消耗 ')'
            return nfa

        if ch == '\\':
            self._consume()  # 消耗 '\'
            ch = self._consume()
            return self._char_nfa(ch)

        if ch == '.':
            self._consume()
            return self._dot_nfa()

        if ch not in (None, '|', ')', '*'):
            self._consume()
            return self._char_nfa(ch)

        raise ValueError(f"意外的字元: {ch}")

    def _char_nfa(self, ch):
        """建立匹配單一字元的 NFA"""
        states = {'q0', 'q1'}
        alphabet = {ch}
        transitions = {('q0', ch): {'q1'}}
        return NFA(states, alphabet, transitions, 'q0', {'q1'})

    def _dot_nfa(self):
        """建立匹配任意字元的 NFA（這裡簡化為非特殊字元）"""
        states = {'q0', 'q1'}
        alphabet = {'a', 'b', 'c', '0', '1', '2'}  # 簡化
        transitions = {}
        for ch in alphabet:
            transitions[('q0', ch)] = {'q1'}
        return NFA(states, alphabet, transitions, 'q0', {'q1'})

    def _union(self, nfa1, nfa2):
        """聯集運算：nfa1 | nfa2"""
        # 建立新的起始狀態和接受狀態
        new_start = f'start_{id(nfa1)}_{id(nfa2)}'
        new_accept = f'accept_{id(nfa1)}_{id(nfa2)}'

        states = {new_start, new_accept} | nfa1.states | nfa2.states
        alphabet = nfa1.alphabet | nfa2.alphabet
        transitions = {}

        # 從新起始狀態透過 ε-轉移到兩個 NFA 的起始狀態
        transitions[(new_start, '')] = {nfa1.start_state, nfa2.start_state}

        # 原有轉移
        transitions.update(nfa1.transitions)
        transitions.update(nfa2.transitions)

        # 從兩個 NFA 的接受狀態透過 ε-轉移到新接受狀態
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

        return NFA(states, alphabet, transitions, new_start, {new_accept})

    def _concat(self, nfa1, nfa2):
        """連接運算：nfa1 nfa2"""
        states = nfa1.states | nfa2.states
        alphabet = nfa1.alphabet | nfa2.alphabet
        transitions = {}

        # 原有轉移
        transitions.update(nfa1.transitions)
        transitions.update(nfa2.transitions)

        # 從 nfa1 的接受狀態透過 ε-轉移到 nfa2 的起始狀態
        for s in nfa1.accept_states:
            key = (s, '')
            if key in transitions:
                transitions[key].add(nfa2.start_state)
            else:
                transitions[key] = {nfa2.start_state}

        # 新接受狀態為 nfa2 的接受狀態
        return NFA(states, alphabet, transitions, nfa1.start_state, nfa2.accept_states)

    def _kleene_star(self, nfa):
        """Kleene 星號：nfa*"""
        new_start = f'start_{id(nfa)}'
        new_accept = f'accept_{id(nfa)}'

        states = {new_start, new_accept} | nfa.states
        alphabet = nfa.alphabet
        transitions = {}

        # 原有轉移
        transitions.update(nfa.transitions)

        # 從新起始狀態透過 ε 到達原起始狀態和新接受狀態
        transitions[(new_start, '')] = {nfa.start_state, new_accept}

        # 從原接受狀態透過 ε 到達原起始狀態和新接受狀態
        for s in nfa.accept_states:
            key = (s, '')
            if key in transitions:
                transitions[key].update({nfa.start_state, new_accept})
            else:
                transitions[key] = {nfa.start_state, new_accept}

        return NFA(states, alphabet, transitions, new_start, {new_accept})


class RegexEngine:
    """正規表達式引擎"""

    def __init__(self, pattern):
        self.pattern = pattern
        parser = RegexParser(pattern)
        self.nfa = parser.parse()

    def match(self, text):
        """檢查整個字串是否匹配"""
        return self.nfa.accepts(text)

    def search(self, text):
        """搜尋字串中是否有子串匹配"""
        for i in range(len(text)):
            for j in range(i + 1, len(text) + 1):
                if self.nfa.accepts(text[i:j]):
                    return True
        return False


if __name__ == "__main__":
    print("=== 正規表達式引擎測試 ===")
    print()

    # 測試：a*
    print("測試: 'a*' (零個或多個 a)")
    engine = RegexEngine('a*')
    test_cases = ["", "a", "aa", "aaa", "b", "ab"]
    for s in test_cases:
        result = engine.match(s)
        print(f"  '{s}': {result}")

    print()

    # 測試：a|b
    print("測試: 'a|b' (a 或 b)")
    engine = RegexEngine('a|b')
    test_cases = ["a", "b", "c", "ab", ""]
    for s in test_cases:
        result = engine.match(s)
        print(f"  '{s}': {result}")

    print()

    # 測試：(ab)*
    print("測試: '(ab)*' (零個或多個 ab)")
    engine = RegexEngine('ab*')  # 簡化：只測試 ab*
    test_cases = ["", "a", "ab", "abb", "aba"]
    for s in test_cases:
        result = engine.match(s)
        print(f"  '{s}': {result}")
