"""
Lambda 演算解析器 (Lambda Calculus Parser)

Lambda 演算是阿隆佐·邱奇 (Alonzo Church) 在 1930 年代提出的計算模型，
比圖靈機更早。任何可計算的函數都可以用 Lambda 演算表示。

Lambda 演算的語法：
- 變數 (Variable): x, y, z 等
- 抽象 (Abstraction): λx.M （其中 M 是 Lambda 項，表示接受參數 x 的函數）
- 應用 (Application): M N （將 M 應用於 N）

歷史背景：
- 1930 年代：Alonzo Church 提出 Lambda 演算
- 1936 年：Alan Turing 證明 Lambda 演算與圖靈機等價 (Church-Turing Thesis)
- 1958 年：John McCarthy 基於 Lambda 演算設計了 Lisp 語言

參考：Church, A. (1936). An unsolvable problem of elementary number theory.
"""

import re
from typing import Union


class LambdaTerm:
    """Lambda 項的基礎類別"""
    pass


class Variable(LambdaTerm):
    """變數"""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __repr__(self):
        return f"Var({self.name})"

    def __str__(self):
        return self.name


class Abstraction(LambdaTerm):
    """抽象（函數定義）: λx.M"""

    def __init__(self, param: str, body: LambdaTerm):
        self.param = param
        self.body = body

    def __eq__(self, other):
        return (isinstance(other, Abstraction) and
                self.param == other.param and
                self.body == other.body)

    def __repr__(self):
        return f"Abs({self.param}, {self.body})"

    def __str__(self):
        return f"λ{self.param}.{self.body}"


class Application(LambdaTerm):
    """應用（函數呼叫）: M N"""

    def __init__(self, func: LambdaTerm, arg: LambdaTerm):
        self.func = func
        self.arg = arg

    def __eq__(self, other):
        return (isinstance(other, Application) and
                self.func == other.func and
                self.arg == other.arg)

    def __repr__(self):
        return f"App({self.func}, {self.arg})"

    def __str__(self):
        # 為了可讀性，適當添加括號
        func_str = f"({self.func})" if isinstance(self.func, Application) else str(self.func)
        arg_str = f"({self.arg})" if isinstance(self.arg, (Application, Abstraction)) else str(self.arg)
        return f"{func_str} {arg_str}"


class LambdaParser:
    """Lambda 演算表達式解析器"""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def parse(self) -> LambdaTerm:
        """解析 Lambda 表達式"""
        return self._parse_expr()

    def _peek(self) -> str:
        """查看當前字元"""
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def _consume(self) -> str:
        """消耗當前字元"""
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def _skip_whitespace(self):
        """跳過空白字元"""
        while self._peek() and self._peek().isspace():
            self._consume()

    def _parse_expr(self) -> LambdaTerm:
        """解析表達式"""
        self._skip_whitespace()
        term = self._parse_term()

        # 檢查是否有應用（後續的項）
        while True:
            self._skip_whitespace()
            if self._peek() is None or self._peek() == ')':
                break
            # 解析下一個項，與當前 term 形成應用
            next_term = self._parse_term()
            term = Application(term, next_term)

        return term

    def _parse_term(self) -> LambdaTerm:
        """解析項（變數或抽象或括號）"""
        self._skip_whitespace()
        ch = self._peek()

        if ch == '(':
            self._consume()  # 消耗 '('
            expr = self._parse_expr()
            self._skip_whitespace()
            if self._peek() != ')':
                raise ValueError("缺少右括號")
            self._consume()  # 消耗 ')'
            return expr

        if ch == 'λ' or ch == '\\':  # 支援 λ 和 \ 兩種表示
            return self._parse_abstraction()

        if ch and ch.isalpha():
            return self._parse_variable()

        raise ValueError(f"意外的字元: {ch}")

    def _parse_variable(self) -> Variable:
        """解析變數"""
        name = ""
        while self._peek() and self._peek().isalnum():
            name += self._consume()
        return Variable(name)

    def _parse_abstraction(self) -> Abstraction:
        """解析抽象: λx.M"""
        self._consume()  # 消耗 'λ' 或 '\'
        self._skip_whitespace()

        # 解析參數名
        param = ""
        while self._peek() and self._peek().isalnum():
            param += self._consume()

        self._skip_whitespace()

        # 消耗 '.'
        if self._peek() != '.':
            raise ValueError("抽象缺少 '.'")
        self._consume()

        # 解析函數體
        body = self._parse_expr()

        return Abstraction(param, body)


def parse_lambda(text: str) -> LambdaTerm:
    """便利函數：解析 Lambda 表達式"""
    return LambdaParser(text).parse()


if __name__ == "__main__":
    print("=== Lambda 演算解析器測試 ===")
    print()

    # 測試：變數
    print("測試：變數")
    expr = parse_lambda("x")
    print(f"  'x' -> {expr}")
    print(f"  類型: {type(expr).__name__}")
    print()

    # 測試：抽象（函數定義）
    print("測試：抽象 (λx.x)")
    expr = parse_lambda("λx.x")
    print(f"  'λx.x' -> {expr}")
    print(f"  類型: {type(expr).__name__}")
    print()

    # 測試：應用（函數呼叫）
    print("測試：應用 ((λx.x) y)")
    expr = parse_lambda("(λx.x) y")
    print(f"  '(λx.x) y' -> {expr}")
    print(f"  類型: {type(expr).__name__}")
    print()

    # 測試：複雜表達式
    print("測試：複雜表達式 (λx.λy.x y)")
    expr = parse_lambda("λx.λy.x y")
    print(f"  'λx.λy.x y' -> {expr}")
    print(f"  repr: {repr(expr)}")
    print()

    # 測試：使用 \ 代替 λ
    print("測試：使用 \\ 代替 λ")
    expr = parse_lambda("\\x.x")
    print(f"  '\\x.x' -> {expr}")
    print()

    # 測試：巢狀抽象
    print("測試：巢狀抽象 (λx.λy.λz.x (y z))")
    expr = parse_lambda("λx.λy.λz.x (y z)")
    print(f"  'λx.λy.λz.x (y z)' -> {expr}")
    print(f"  repr: {repr(expr)}")
