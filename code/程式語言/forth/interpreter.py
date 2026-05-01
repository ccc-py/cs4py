"""
FORTH 解譯器 (FORTH Stack-Based Language Interpreter)

歷史背景：
- 1970 年由 Charles H. Moore 發明
- 基於堆疊的逆向波蘭表示法（Reverse Polish Notation）
- 最初用於天文觀測和儀器控制
- 以其極小的體量和高效的執行速度聞名
- ISO FORTH-83 和 FORTH-94 是標準化版本

核心概念：
- 堆疊是核心數據結構：所有操作都透過推入和彈出
- 逆向波蘭表示法：3 4 + 而非 + 3 4
- 字典：所有詞彙（函數）儲存在字典中
- 即時編譯：可定義新詞彙並即時執行
"""

from typing import List, Dict, Any, Optional, Tuple


class ForthError(Exception):
    """FORTH 執行錯誤"""
    pass


class ForthInterpreter:
    """FORTH 解譯器"""

    def __init__(self):
        self.stack: List[int] = []
        self.dict: Dict[str, Any] = {}
        self.memory: Dict[int, int] = {}
        self._init_builtins()

    def _push(self, n):
        self.stack.append(n)

    def _pop(self):
        if not self.stack:
            raise ForthError("堆疊下溢 (stack underflow)")
        return self.stack.pop()

    def _init_builtins(self):
        """初始化內建詞彙"""
        self.dict = {
            # 堆疊操作
            ".": self._op_dot,
            ".s": self._op_dot_s,
            "drop": self._op_drop,
            "dup": self._op_dup,
            "swap": self._op_swap,
            "over": self._op_over,
            "rot": self._op_rot,
            "?dup": self._op_qdup,

            # 算術
            "+": self._op_add,
            "-": self._op_sub,
            "*": self._op_mul,
            "/": self._op_div,
            "mod": self._op_mod,
            "abs": self._op_abs,
            "negate": self._op_negate,
            "1+": self._op_1plus,
            "1-": self._op_1minus,

            # 比較
            "=": self._op_eq,
            "<>": self._op_neq,
            "<": self._op_lt,
            ">": self._op_gt,
            "<=": self._op_le,
            ">=": self._op_ge,
            "0=": self._op_zero_eq,
            "0<": self._op_zero_lt,
            "0>": self._op_zero_gt,

            # 邏輯
            "and": self._op_and,
            "or": self._op_or,
            "not": self._op_not,

            # 工具
            "depth": self._op_depth,
            "cr": self._op_cr,
            "words": self._op_words,
        }

    # ========== 堆疊操作 ==========

    def _op_dot(self):
        print(self._pop(), end=" ")

    def _op_dot_s(self):
        print(f"<{len(self.stack)}> {self.stack}")

    def _op_drop(self):
        self._pop()

    def _op_dup(self):
        val = self._pop()
        self.stack.append(val)
        self.stack.append(val)

    def _op_swap(self):
        b, a = self._pop(), self._pop()
        self.stack.append(b)
        self.stack.append(a)

    def _op_over(self):
        b, a = self._pop(), self._pop()
        self.stack.append(a)
        self.stack.append(b)
        self.stack.append(a)

    def _op_rot(self):
        c, b, a = self._pop(), self._pop(), self._pop()
        self.stack.append(b)
        self.stack.append(c)
        self.stack.append(a)

    def _op_qdup(self):
        if self.stack and self.stack[-1] != 0:
            self.stack.append(self.stack[-1])

    # ========== 算術 ==========

    def _op_add(self):
        self.stack.append(self._pop() + self._pop())

    def _op_sub(self):
        b, a = self._pop(), self._pop()
        self.stack.append(a - b)

    def _op_mul(self):
        self.stack.append(self._pop() * self._pop())

    def _op_div(self):
        b, a = self._pop(), self._pop()
        if b == 0:
            raise ForthError("除以零")
        self.stack.append(a // b)

    def _op_mod(self):
        b, a = self._pop(), self._pop()
        if b == 0:
            raise ForthError("除以零")
        self.stack.append(a % b)

    def _op_abs(self):
        self.stack.append(abs(self._pop()))

    def _op_negate(self):
        self.stack.append(-self._pop())

    def _op_1plus(self):
        self.stack.append(self._pop() + 1)

    def _op_1minus(self):
        self.stack.append(self._pop() - 1)

    # ========== 比較 ==========

    def _op_eq(self):
        b, a = self._pop(), self._pop()
        self.stack.append(-1 if a == b else 0)

    def _op_neq(self):
        b, a = self._pop(), self._pop()
        self.stack.append(-1 if a != b else 0)

    def _op_lt(self):
        b, a = self._pop(), self._pop()
        self.stack.append(-1 if a < b else 0)

    def _op_gt(self):
        b, a = self._pop(), self._pop()
        self.stack.append(-1 if a > b else 0)

    def _op_le(self):
        b, a = self._pop(), self._pop()
        self.stack.append(-1 if a <= b else 0)

    def _op_ge(self):
        b, a = self._pop(), self._pop()
        self.stack.append(-1 if a >= b else 0)

    def _op_zero_eq(self):
        self.stack.append(-1 if self._pop() == 0 else 0)

    def _op_zero_lt(self):
        self.stack.append(-1 if self._pop() < 0 else 0)

    def _op_zero_gt(self):
        self.stack.append(-1 if self._pop() > 0 else 0)

    # ========== 邏輯 ==========

    def _op_and(self):
        self.stack.append(self._pop() & self._pop())

    def _op_or(self):
        self.stack.append(self._pop() | self._pop())

    def _op_not(self):
        self.stack.append(-1 if self._pop() == 0 else 0)

    # ========== 工具 ==========

    def _op_depth(self):
        self.stack.append(len(self.stack))

    def _op_cr(self):
        print()

    def _op_words(self):
        print(" ".join(self.dict.keys()))

    # ========== 執行引擎 ==========

    def evaluate(self, code: str) -> "ForthInterpreter":
        """執行 FORTH 程式碼"""
        tokens = code.split()
        i = 0
        while i < len(tokens):
            i = self._execute(tokens, i)
        return self

    def _execute(self, tokens: List[str], i: int) -> int:
        """執行從位置 i 開始的 token，返回下一個位置"""
        token = tokens[i]

        # 定義詞彙：: name ... ;
        if token == ":":
            i += 1
            name = tokens[i]
            i += 1
            start = i
            depth = 1
            while i < len(tokens):
                if tokens[i] == ":":
                    depth += 1
                elif tokens[i] == ";":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            body = tokens[start:i]
            self.dict[name] = ("compiled", body[:])
            return i + 1

        # 條件分支：if ... else ... then
        if token == "if":
            cond = self._pop()
            if cond != 0:
                return self._execute_if_body(tokens, i + 1)
            else:
                return self._skip_if_body(tokens, i + 1)

        # 循環：limit start do ... loop
        if token == "do":
            start_idx = self._pop()
            limit = self._pop()
            i += 1
            body_start = i
            # 找到對應的 loop
            depth = 1
            while i < len(tokens) and depth > 0:
                if tokens[i] == "do":
                    depth += 1
                elif tokens[i] == "loop":
                    depth -= 1
                if depth > 0:
                    i += 1
            body = tokens[body_start:i]

            # 執行循環
            for idx in range(start_idx, limit):
                # 替換循環體中的 i 為當前索引
                exec_tokens = []
                for t in body:
                    if t == "i":
                        exec_tokens.append(str(idx))
                    else:
                        exec_tokens.append(t)
                j = 0
                while j < len(exec_tokens):
                    j = self._execute(exec_tokens, j)
            return i + 1

        # 數字
        try:
            self.stack.append(int(token))
            return i + 1
        except ValueError:
            pass

        # 查字典
        if token in self.dict:
            entry = self.dict[token]
            if callable(entry):
                entry()
            elif entry[0] == "compiled":
                body = entry[1]
                j = 0
                while j < len(body):
                    j = self._execute(body, j)
            return i + 1

        raise ForthError(f"未知詞彙: {token}")

    def _skip_if_body(self, tokens: List[str], i: int) -> int:
        """跳過 if 分支，處理 else"""
        depth = 1
        while i < len(tokens) and depth > 0:
            if tokens[i] == "if":
                depth += 1
            elif tokens[i] == "then":
                depth -= 1
                if depth == 0:
                    return i + 1
            elif tokens[i] == "else" and depth == 1:
                i += 1
                # 執行 else 分支
                while i < len(tokens):
                    if tokens[i] == "if":
                        depth += 1
                    elif tokens[i] == "then":
                        depth -= 1
                        if depth == 0:
                            return i + 1
                    i = self._execute(tokens, i)
                return i
            i += 1
        return i

    def _execute_if_body(self, tokens: List[str], i: int) -> int:
        """執行 if 分支"""
        depth = 1
        while i < len(tokens) and depth > 0:
            if tokens[i] == "if":
                depth += 1
            elif tokens[i] == "else" and depth == 1:
                # 跳到 then
                depth = 1
                i += 1
                while i < len(tokens) and depth > 0:
                    if tokens[i] == "if":
                        depth += 1
                    elif tokens[i] == "then":
                        depth -= 1
                    i += 1
                return i
            elif tokens[i] == "then":
                depth -= 1
                if depth == 0:
                    return i + 1
            i = self._execute(tokens, i)
        return i

    def run(self, code: str) -> str:
        """執行並返回結果字串"""
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            self.evaluate(code)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        output = output.strip()
        if self.stack:
            return f"  輸出: {output}\n  堆疊: {self.stack}"
        elif output:
            return f"  輸出: {output}"
        else:
            return f"  堆疊: {self.stack}"


def demo_basic():
    """基本堆疊操作"""
    print("=== FORTH 基本操作 ===\n")

    programs = [
        ("3 4 + .", "3 + 4"),
        ("10 2 - .", "10 - 2"),
        ("5 6 * .", "5 * 6"),
        ("20 4 / .", "20 / 4"),
        ("3 dup * .", "3² (dup)"),
        ("1 2 swap .s", "swap"),
        ("1 2 3 rot .s", "rot"),
        ("5 0> .", "5 > 0"),
        ("-3 abs .", "|-3|"),
    ]

    for code, desc in programs:
        f = ForthInterpreter()
        result = f.run(code)
        print(f"  {desc}: {code}")
        print(f"  {result}\n")


def demo_definitions():
    """使用者定義詞彙"""
    print("=== 使用者定義詞彙 ===\n")

    forth = ForthInterpreter()

    # 定義平方
    forth.evaluate(": sq dup * ;")
    print("  : sq dup * ;  (定義平方)")
    forth.evaluate("7 sq .")
    print(f"  7 sq => 堆疊: {forth.stack}\n")

    # 定義立方
    forth.evaluate(": cube dup dup * * ;")
    print("  : cube dup dup * * ;  (定義立方)")
    forth.evaluate("3 cube .")
    print(f"  3 cube => 堆疊: {forth.stack}\n")

    # 定義偶數判斷
    forth.evaluate(": even 2 mod 0= ;")
    print("  : even 2 mod 0= ;  (定義偶數判斷)")
    for n in [4, 5, 6, 7, 8]:
        f = ForthInterpreter()
        f.evaluate(": even 2 mod 0= ;")
        f.evaluate(f"{n} even .")
        print(f"  {n} even => 堆疊: {f.stack}")
    print()


def demo_control():
    """控制結構"""
    print("=== 控制結構 ===\n")

    # if-else-then
    f1 = ForthInterpreter()
    f1.evaluate("5 3 > if 10 else 20 then .")
    print(f"  5 > 3 ? 10 : 20 => 堆疊: {f1.stack}")

    f2 = ForthInterpreter()
    f2.evaluate("1 3 > if 10 else 20 then .")
    print(f"  1 > 3 ? 10 : 20 => 堆疊: {f2.stack}")

    # 循環
    f3 = ForthInterpreter()
    f3.evaluate("0 5 0 do i + loop .")
    print(f"\n  0+1+2+3+4 = 堆疊: {f3.stack}")


def demo_factorial():
    """階乘"""
    print("\n=== 階乘 ===\n")

    print("  : fact 1 swap 1 + 1 do i * loop ;")

    for n in range(1, 11):
        f = ForthInterpreter()
        f.evaluate(": fact 1 swap 1 + 1 do i * loop ;")
        f.evaluate(f"{n} fact .")
        print(f"  {n}! = {f.stack}")


def demo_nested():
    """巢狀定義"""
    print("\n=== 巢狀定義 ===\n")

    forth = ForthInterpreter()

    # 遞迴：用循環方式計算斐波那契
    forth.evaluate(": fib2 0 1 rot 0 do over + swap loop drop ;")
    print("  : fib2 0 1 rot 0 do over + swap loop drop ;  (迭代版斐波那契)")

    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        f = ForthInterpreter()
        f.evaluate(": fib2 0 1 rot 0 do over + swap loop drop ;")
        f.evaluate(f"{n} fib2 .")
        print(f"  fib({n}) = {f.stack}")


if __name__ == "__main__":
    demo_basic()
    demo_definitions()
    demo_control()
    demo_factorial()
    demo_nested()
