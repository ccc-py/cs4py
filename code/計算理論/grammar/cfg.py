"""
上下文無關文法 (Context-Free Grammar, CFG)

上下文無關文法是形式語言理論中的重要概念，用於描述程式語言的語法。

CFG 是一個四元組 G = (V, Σ, R, S)：
- V: 非終端符號集合（變數）
- Σ: 終端符號集合（字母表）
- R: 產生規則集合（形式：A → α，其中 A ∈ V，α ∈ (V ∪ Σ)*）
- S: 起始符號（S ∈ V）

歷史背景：
- 1956 年：Noam Chomsky 提出變換生成文法（Transformational-Generative Grammar）
- 1960 年代：CFG 成為程式語言語法描述的標準
- 應用：BNF（巴科斯-諾爾范式）就是 CFG 的一種表示

參考：Chomsky, N. (1956). Three models for the description of language.
"""

from typing import Dict, List, Set, Tuple
from collections import deque


class CFG:
    """上下文無關文法"""

    def __init__(self, nonterminals: Set[str], terminals: Set[str],
                 productions: Dict[str, List[List[str]]], start_symbol: str):
        """
        初始化 CFG

        Args:
            nonterminals: 非終端符號集合（大寫字母或尖括號）
            terminals: 終端符號集合（小寫字母、符號等）
            productions: 產生規則，格式: {左側: [[右側1], [右側2], ...]}
            start_symbol: 起始符號
        """
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def generate(self, symbol: str = None, max_depth: int = 10) -> List[str]:
        """
        生成該文法能產生的字串（窮舉法）

        Args:
            symbol: 起始符號，預設為 start_symbol
            max_depth: 最大遞迴深度（防止無限遞迴）

        Returns:
            能產生的字串列表
        """
        if symbol is None:
            symbol = self.start_symbol

        if max_depth <= 0:
            return []

        # 如果是終端符號，直接返回
        if symbol in self.terminals:
            return [symbol]

        # 如果是非終端符號，展開所有產生規則
        if symbol in self.productions:
            results = []
            for rhs in self.productions[symbol]:
                if not rhs:  # 空字串
                    results.append('')
                    continue

                # 遞迴生成每個部分的字串
                parts = [self.generate(s, max_depth - 1) for s in rhs]
                # 計算笛卡爾積
                for combo in self._cartesian_product(parts):
                    results.append(''.join(combo))
            return results

        return []

    def _cartesian_product(self, lists: List[List[str]]) -> List[List[str]]:
        """計算多個列表的笛卡爾積"""
        if not lists:
            return [[]]
        result = []
        for item in lists[0]:
            for rest in self._cartesian_product(lists[1:]):
                result.append([item] + rest)
        return result

    def is_in_language(self, string: str, max_steps: int = 1000) -> bool:
        """
        檢查字串是否屬於該文法產生的語言

        使用 CYK 演算法（需要 CNF 形式，這裡用簡化版本）

        注意：這是一個簡化版本，只適用於簡單文法
        """
        # 簡化方法：嘗試窮舉所有可能的推導（僅適用於簡短文法）
        return self._derive(self.start_symbol, string, max_steps)

    def _derive(self, symbol: str, target: str, max_steps: int) -> bool:
        """嘗試從 symbol 推導出 target"""
        if max_steps <= 0:
            return False

        # 如果是終端符號
        if symbol in self.terminals:
            return symbol == target

        # 如果是非終端符號
        if symbol in self.productions:
            for rhs in self.productions[symbol]:
                if not rhs:  # 空產生規則
                    if target == '':
                        return True
                    continue

                # 嘗試不同的分割方式
                if self._can_derive_sequence(rhs, target, max_steps - 1):
                    return True

        return False

    def _can_derive_sequence(self, symbols: List[str], target: str, max_steps: int) -> bool:
        """檢查一系列符號是否能推導出 target"""
        if len(symbols) == 1:
            return self._derive(symbols[0], target, max_steps)

        # 嘗試所有分割點
        for i in range(1, len(target) + 1):
            if self._derive(symbols[0], target[:i], max_steps):
                if self._can_derive_sequence(symbols[1:], target[i:], max_steps):
                    return True

        return False


def create_grammar_balanced_parens() -> CFG:
    """
    建立生成平衡括號的文法

    S → (S)S | ε
    """
    nonterminals = {'S'}
    terminals = {'(', ')'}
    productions = {
        'S': [['(', 'S', ')', 'S'], ['ε']]  # ε 表示空字串
    }
    return CFG(nonterminals, terminals, productions, 'S')


def create_grammar_anbn() -> CFG:
    """
    建立生成 {a^n b^n | n ≥ 0} 的文法

    S → aSb | ε
    """
    nonterminals = {'S'}
    terminals = {'a', 'b'}
    productions = {
        'S': [['a', 'S', 'b'], ['ε']]
    }
    return CFG(nonterminals, terminals, productions, 'S')


def create_grammar_simple_arithmetic() -> CFG:
    """
    建立簡單算術表達式的文法

    E → E + T | T
    T → T * F | F
    F → (E) | number
    """
    nonterminals = {'E', 'T', 'F'}
    terminals = {'+', '*', '(', ')', 'number'}
    productions = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['number']]
    }
    return CFG(nonterminals, terminals, productions, 'E')


if __name__ == "__main__":
    print("=== 上下文無關文法測試 ===")
    print()

    # 測試：平衡括號
    print("測試：平衡括號文法")
    cfg = create_grammar_balanced_parens()
    print(f"  非終端符號: {cfg.nonterminals}")
    print(f"  終端符號: {cfg.terminals}")
    print(f"  起始符號: {cfg.start_symbol}")
    print(f"  產生規則: {cfg.productions}")
    print()

    # 生成一些字串
    print("  生成字串:")
    strings = cfg.generate(max_depth=5)
    for s in set(strings):
        if s:
            print(f"    '{s}'")
    print()

    # 測試：a^n b^n
    print("測試：{a^n b^n | n ≥ 0} 文法")
    cfg = create_grammar_anbn()
    test_cases = ["", "ab", "aabb", "abab", "aaabbb"]
    for s in test_cases:
        result = cfg.is_in_language(s)
        print(f"  '{s}': {result}")
    print()

    # 測試：簡單算術
    print("測試：簡單算術表達式文法")
    cfg = create_grammar_simple_arithmetic()
    print(f"  非終端符號: {cfg.nonterminals}")
    print(f"  終端符號: {cfg.terminals}")
    print(f"  產生規則:")
    for lhs, rhs_list in cfg.productions.items():
        for rhs in rhs_list:
            print(f"    {lhs} → {' '.join(rhs)}")
