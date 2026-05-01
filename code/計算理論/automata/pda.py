"""
下推自動機 (Pushdown Automaton, PDA)

PDA 是計算理論中比有限狀態自動機更強的計算模型，增加了：
1. 一個堆疊 (stack) 作為輔助記憶體
2. 可以進行推入 (push) 和彈出 (pop) 操作

PDA 能識別的語言類別：上下文無關語言 (Context-Free Languages, CFL)

歷史背景：
下推自動機的概念在 1950 年代末期被提出，用於形式化描述
上下文無關文法的運算模型。PDA 是理解編譯器語法分析的基礎。

重要結論：
- PDA 與上下文無關文法 (CFG) 等價
- 存在確定性和非確定性的 PDA
- NPDA (非確定性) 比 DPDA (確定性) 更強大

參考：Hopcroft, J. E., & Ullman, J. D. (1967). Formal Languages and Their Relation to Automata.
"""


class PDA:
    """下推自動機（非確定性）"""

    def __init__(self, states, input_alphabet, stack_alphabet, transitions, start_state, start_stack, accept_states):
        """
        初始化 PDA

        Args:
            states: 狀態集合 (set)
            input_alphabet: 輸入字母表 (set)
            stack_alphabet: 堆疊字母表 (set)
            transitions: 轉移函數 (list of tuples)
                格式: (state, input_symbol, stack_top) -> [(next_state, stack_operation), ...]
                其中 stack_operation 是字串，如 "A" 表示推入 A，"ε" 表示彈出，"ε" 表示空操作
            start_state: 起始狀態
            start_stack: 起始堆疊符號 (通常是 Z0)
            accept_states: 接受狀態集合 (set)
        """
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack = start_stack
        self.accept_states = accept_states

    def get_transitions(self, state, input_symbol, stack_top):
        """
        獲取所有可能的轉移

        Args:
            state: 當前狀態
            input_symbol: 輸入符號（可以是 '' 表示 ε-轉移）
            stack_top: 堆疊頂端符號（可以是 '' 表示堆疊為空）

        Returns:
            可能的轉移列表 [(next_state, stack_operation), ...]
        """
        results = []
        for (s, inp, top), next_list in self.transitions.items() if isinstance(self.transitions, dict) else []:
            if s == state and (inp == input_symbol or inp == '') and (top == stack_top or top == ''):
                results.extend(next_list)
        return results

    def _get_transitions(self, state, input_symbol, stack_top):
        """內部方法：獲取轉移（處理 dict 格式的 transitions）"""
        results = []
        for (s, inp, top), next_list in self.transitions.items():
            # 匹配狀態
            if s != state:
                continue
            # 匹配輸入符號（'' 表示 ε）
            if inp != input_symbol and inp != '':
                continue
            # 匹配堆疊頂端（'' 表示空堆疊或任意）
            if top != stack_top and top != '':
                continue
            results.extend(next_list)
        return results

    def accepts(self, input_string):
        """
        判斷輸入字串是否被接受（使用非確定性模擬）

        使用 BFS 遍歷所有可能的組態 (configuration)：
        組態 = (狀態, 剩餘輸入, 堆疊)

        Args:
            input_string: 輸入字串

        Returns:
            True 如果字串被接受，否則 False
        """
        from collections import deque

        # 初始組態：(狀態, 剩餘輸入索引, 堆疊)
        initial_stack = [self.start_stack]
        queue = deque([(self.start_state, 0, initial_stack)])

        visited = set()

        while queue:
            state, idx, stack = queue.popleft()

            # 檢查是否訪問過（避免循環）
            config = (state, idx, tuple(stack))
            if config in visited:
                continue
            visited.add(config)

            # 檢查是否接受：到達接受狀態且輸入讀完
            if idx == len(input_string) and state in self.accept_states:
                return True

            # 嘗試 ε-轉移（不消耗輸入）
            for next_state, operation in self._get_transitions(state, '', stack[-1] if stack else ''):
                new_stack = self._apply_operation(stack, operation)
                new_config = (next_state, idx, tuple(new_stack))
                if new_config not in visited:
                    queue.append((next_state, idx, new_stack))

            # 如果能讀入符號
            if idx < len(input_string):
                symbol = input_string[idx]
                for next_state, operation in self._get_transitions(state, symbol, stack[-1] if stack else ''):
                    new_stack = self._apply_operation(stack, operation)
                    new_config = (next_state, idx + 1, tuple(new_stack))
                    if new_config not in visited:
                        queue.append((next_state, idx + 1, new_stack))

            # 如果堆疊非空，也可以嘗試不讀輸入的轉移
            if stack:
                for next_state, operation in self._get_transitions(state, '', stack[-1]):
                    new_stack = self._apply_operation(stack, operation)
                    new_config = (next_state, idx, tuple(new_stack))
                    if new_config not in visited:
                        queue.append((next_state, idx, new_stack))

        return False

    def _apply_operation(self, stack, operation):
        """
        應用堆疊操作

        operation 格式：
        - '': 空操作
        - 'ε': 彈出堆疊頂端
        - 'A': 推入 A（如果長度>1，則依序推入）
        """
        new_stack = stack.copy()
        if operation == '' or operation == 'ε':
            if new_stack:
                new_stack.pop()
        else:
            # 推入：從右到左推入，因為 operation 的第一個字元應該在最頂端
            for ch in reversed(operation):
                new_stack.append(ch)
        return new_stack


def create_pda_balanced_parens():
    """
    建立一個 PDA，接受所有括號平衡的字符串

    語言：{ w | w 中的括號是平衡的 }

    策略：
    - 讀入 '(' 時推入堆疊
    - 讀入 ')' 時彈出堆疊
    - 最後堆疊應該為空
    """
    states = {'q0', 'q1'}
    input_alphabet = {'(', ')'}
    stack_alphabet = {'(', 'Z0'}
    transitions = {
        # 在 q0 讀入 '('，推入 '('
        ('q0', '(', ''): [('q0', '(')],
        ('q0', '(', '('): [('q0', '(')],
        ('q0', '(', 'Z0'): [('q0', '(')],
        # 在 q0 讀入 ')'，彈出 '('
        ('q0', ')', '('): [('q0', 'ε')],
        # 讀完後，彈出 Z0 並進入 q1（接受狀態）
        ('q0', '', 'Z0'): [('q1', 'ε')],
    }
    start_state = 'q0'
    start_stack = 'Z0'
    accept_states = {'q1'}

    return PDA(states, input_alphabet, stack_alphabet, transitions, start_state, start_stack, accept_states)


def create_pda_palindrome():
    """
    建立一個 PDA，接受所有形如 w c w^R 的字串

    其中 w 是任意字串，w^R 是 w 的反轉，c 是中間的分隔符號。
    這是一個非確定性 PDA 的經典例子。

    語言：{ w c w^R | w ∈ {0,1}* }
    """
    states = {'q0', 'q1', 'q2'}
    input_alphabet = {'0', '1', 'c'}
    stack_alphabet = {'0', '1', 'Z0'}
    transitions = {
        # q0: 將 w 的符號推入堆疊
        ('q0', '0', ''): [('q0', '0')],
        ('q0', '0', '0'): [('q0', '0')],
        ('q0', '0', '1'): [('q0', '0')],
        ('q0', '1', ''): [('q0', '1')],
        ('q0', '1', '0'): [('q0', '1')],
        ('q0', '1', '1'): [('q0', '1')],
        # 讀到 c，不消耗堆疊，進入 q1
        ('q0', 'c', ''): [('q1', '')],
        ('q0', 'c', '0'): [('q1', '')],
        ('q0', 'c', '1'): [('q1', '')],
        # q1: 讀入符號，與堆疊頂端匹配則彈出
        ('q1', '0', '0'): [('q1', 'ε')],
        ('q1', '1', '1'): [('q1', 'ε')],
        # q1 讀完後，檢查堆疊是否只剩下 Z0
        ('q1', '', 'Z0'): [('q2', 'ε')],
    }
    start_state = 'q0'
    start_stack = 'Z0'
    accept_states = {'q2'}

    return PDA(states, input_alphabet, stack_alphabet, transitions, start_state, start_stack, accept_states)


if __name__ == "__main__":
    # 測試：括號平衡
    print("=== 測試：括號平衡 ===")
    pda_parens = create_pda_balanced_parens()
    test_cases = ["()", "(())", "()()", "(()", "())", ""]
    for s in test_cases:
        accepted = pda_parens.accepts(s)
        expected = is_balanced(s)
        print(f"'{s}' -> PDA: {accepted}, 預期: {expected}, 正確: {accepted == expected}")

    print()

    # 測試：w c w^R
    print("=== 測試：w c w^R（回文）===")
    pda_pal = create_pda_palindrome()
    test_cases = ["c", "0c0", "1c1", "01c10", "10c01", "0c1", "01c01"]
    for s in test_cases:
        accepted = pda_pal.accepts(s)
        expected = is_palindrome(s)
        print(f"'{s}' -> PDA: {accepted}, 預期: {expected}, 正確: {accepted == expected}")


def is_balanced(s):
    """用來驗證括號平衡（輔助函數）"""
    count = 0
    for ch in s:
        if ch == '(':
            count += 1
        elif ch == ')':
            count -= 1
        if count < 0:
            return False
    return count == 0


def is_palindrome(s):
    """用來驗證 w c w^R 格式（輔助函數）"""
    if 'c' not in s:
        return False
    parts = s.split('c', 1)
    w = parts[0]
    w_rev = parts[1]
    return w == w_rev[::-1]
