"""
CYK 演算法 (Cocke-Younger-Kasami Algorithm)

CYK 是判定字串是否屬於上下文無關語言的經典演算法。

演算法原理：
- 輸入：字串 w = a₁a₂...aₙ 和 CNF 形式的 CFG
- CNF (Chomsky Normal Form)：所有產生規則為 A → BC 或 A → a
- 時間複雜度：O(n³)

歷史背景：
- 1965 年：John Cocke 首次提出
- 1967 年：Younger 和 Kasami 獨立重新發現
- 是編譯器中語法分析的基礎演算法之一

參考：Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation.
"""

from typing import Dict, List, Set, Tuple


class CNFGrammar:
    """轉換為 Chomsky Normal Form (CNF) 的上下文無關文法"""

    def __init__(self, nonterminals: Set[str], terminals: Set[str],
                 productions: Dict[str, List[List[str]]], start_symbol: str):
        """
        初始化 CNF 文法

        CNF 要求所有產生規則為：
        1. A → BC  (其中 B, C 是非終端符號)
        2. A → a   (其中 a 是終端符號)
        3. S → ε    (只有起始符號可以有空產生)
        """
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def get_binary_productions(self, b: str, c: str) -> List[str]:
        """找出所有 A 使得 A → BC"""
        result = []
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) == 2 and rhs[0] == b and rhs[1] == c:
                    result.append(lhs)
        return result

    def get_terminal_production(self, terminal: str) -> List[str]:
        """找出所有 A 使得 A → terminal"""
        result = []
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == terminal:
                    result.append(lhs)
        return result


def cyk(string: str, grammar: CNFGrammar) -> bool:
    """
    CYK 演算法：判定字串是否屬於 CFL

    Args:
        string: 要檢查的字串
        grammar: CNF 形式的文法

    Returns:
        True 如果字串屬於該語言
    """
    n = len(string)
    if n == 0:
        # 檢查 S → ε
        return any(len(rhs) == 0 for rhs in grammar.productions.get(grammar.start_symbol, []))

    # table[i][j] = 在位置 i 開始，長度為 j 的子字串的非終端符號集合
    # 實際上我們用 table[i][j] 表示從 i 開始長度 j 的子字串
    table: List[List[Set[str]]] = [[set() for _ in range(n + 1)] for _ in range(n)]

    # 初始化：長度為 1 的子字串
    for i in range(n):
        symbol = string[i]
        nonterminals = grammar.get_terminal_production(symbol)
        table[i][1] = set(nonterminals)

    # 對於長度 >= 2 的子字串
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            for k in range(1, length):
                # 將子字串分成兩部分：長度 k 和 length-k
                left_set = table[i][k]
                right_set = table[i + k][length - k]

                for b in left_set:
                    for c in right_set:
                        a_list = grammar.get_binary_productions(b, c)
                        for a in a_list:
                            table[i][length].add(a)

    # 檢查起始符號是否在整個字串的集合中
    return grammar.start_symbol in table[0][n]


def create_grammar_anbn() -> CNFGrammar:
    """
    建立 {a^n b^n | n ≥ 0} 的 CNF 文法

    CNF:
    S → AB | ε
    A → a
    B → b
    """
    nonterminals = {'S', 'A', 'B'}
    terminals = {'a', 'b'}
    productions = {
        'S': [['A', 'B'], []],  # [] 表示 ε
        'A': [['a']],
        'B': [['b']],
    }
    return CNFGrammar(nonterminals, terminals, productions, 'S')


def create_grammar_balanced_parens() -> CNFGrammar:
    """
    建立平衡括號的 CNF 文法

    CNF:
    S → AB | ε
    A → (
    B → SB)
    """
    nonterminals = {'S', 'A', 'B'}
    terminals = {'(', ')'}
    productions = {
        'S': [['A', 'B'], []],
        'A': [['(']],
        'B': [['S', 'B2']],
        'B2': [[')']],
    }
    return CNFGrammar(nonterminals, terminals, productions, 'S')


if __name__ == "__main__":
    print("=== CYK 演算法測試 ===")
    print()

    # 測試：{a^n b^n}
    print("測試：{a^n b^n | n ≥ 0}")
    grammar = create_grammar_anbn()
    test_cases = ["", "ab", "aabb", "abab", "aaabbb", "aab"]
    for s in test_cases:
        result = cyk(s, grammar)
        expected = (len(s) % 2 == 0 and
                    s == 'a' * (len(s) // 2) + 'b' * (len(s) // 2))
        print(f"  '{s}': CYK={result}, 預期={expected}, 正確={result == expected}")

    print()

    # 測試：平衡括號
    print("測試：平衡括號")
    grammar = create_grammar_balanced_parens()
    test_cases = ["", "()", "(())", "()()", "(()", "())"]
    for s in test_cases:
        result = cyk(s, grammar)
        # 簡單檢查：括號是否平衡
        count = 0
        balanced = True
        for ch in s:
            if ch == '(':
                count += 1
            elif ch == ')':
                count -= 1
            if count < 0:
                balanced = False
                break
        expected = balanced and count == 0
        print(f"  '{s}': CYK={result}, 預期={expected}, 正確={result == expected}")
