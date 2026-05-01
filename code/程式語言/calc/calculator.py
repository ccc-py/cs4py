"""
簡易計算機語言 (Simple Calculator Language)

歷史背景：
- 1960 年代：Dijkstra 提出 shunting-yard 演算法用於解析中綴表達式
- 1961 年：Tony Hildebrandt 提出遞迴下降解析器概念
- 表達式求值是編譯器前端的核心組件
- 現代計算機、電子表格、腳本語言都依賴此技術

核心概念：
- 詞法分析（Tokenization）：將輸入分解為有意義的單元
- 語法分析（Parsing）：建立抽象語法樹（AST）
- 語義分析（Evaluation）：計算 AST 的值
- 優先順序處理：乘除 > 加減 > 冪次
"""

from typing import List, Tuple, Optional, Any
import math


# ========== Token ==========


class TokenType:
    NUMBER = "NUMBER"
    IDENT = "IDENT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    POW = "POW"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    ASSIGN = "ASSIGN"
    EOF = "EOF"


class Token:
    def __init__(self, type_: str, value: Any = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


# ========== 詞法分析 ==========


def tokenize(text: str) -> List[Token]:
    """將輸入文字分解為 Token 序列"""
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]

        # 跳過空白
        if ch.isspace():
            i += 1
            continue

        # 數字（支援小數）
        if ch.isdigit() or (ch == '.' and i + 1 < len(text) and text[i + 1].isdigit()):
            num = ""
            while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                num += text[i]
                i += 1
            tokens.append(Token(TokenType.NUMBER, float(num) if '.' in num else int(num)))
            continue

        # 識別字（變數名、函數名）
        if ch.isalpha() or ch == '_':
            ident = ""
            while i < len(text) and (text[i].isalnum() or text[i] == '_'):
                ident += text[i]
                i += 1
            tokens.append(Token(TokenType.IDENT, ident))
            continue

        # 運算子
        if ch == '+':
            tokens.append(Token(TokenType.PLUS))
        elif ch == '-':
            tokens.append(Token(TokenType.MINUS))
        elif ch == '*':
            tokens.append(Token(TokenType.MUL))
        elif ch == '/':
            tokens.append(Token(TokenType.DIV))
        elif ch == '^':
            tokens.append(Token(TokenType.POW))
        elif ch == '(':
            tokens.append(Token(TokenType.LPAREN))
        elif ch == ')':
            tokens.append(Token(TokenType.RPAREN))
        elif ch == '=':
            tokens.append(Token(TokenType.ASSIGN))
        else:
            raise SyntaxError(f"未知字元: '{ch}' at position {i}")

        i += 1

    tokens.append(Token(TokenType.EOF))
    return tokens


# ========== AST ==========


class ASTNode:
    pass


class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"


class BinOpNode(ASTNode):
    def __init__(self, op: str, left: ASTNode, right: ASTNode):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"


class UnaryOpNode(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"


class VarNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"


class AssignNode(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assign({self.name}, {self.value})"


class FuncCallNode(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"Call({self.name}, {self.args})"


# ========== 語法分析（遞迴下降） ==========


class Parser:
    """遞迴下降解析器

    文法：
        expr     -> term (('+' | '-') term)*
        term     -> power (('*' | '/') power)*
        power    -> unary ('^' unary)*
        unary    -> ('+' | '-') unary | call
        call     -> primary ('(' expr (',' expr)* ')')?
        primary  -> NUMBER | IDENT | '(' expr ')'
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ASTNode:
        node = self.expr()
        if self.current().type != TokenType.EOF:
            raise SyntaxError(f"意外的 token: {self.current()}")
        return node

    def current(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, type_: str) -> Token:
        token = self.current()
        if token.type != type_:
            raise SyntaxError(f"期望 {type_}，但得到 {token.type}")
        self.pos += 1
        return token

    def expr(self) -> ASTNode:
        """expr -> term (('+' | '-') term)*"""
        node = self.term()
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.current().type)
            right = self.term()
            node = BinOpNode(op.type, node, right)
        return node

    def term(self) -> ASTNode:
        """term -> power (('*' | '/') power)*"""
        node = self.power()
        while self.current().type in (TokenType.MUL, TokenType.DIV):
            op = self.consume(self.current().type)
            right = self.power()
            node = BinOpNode(op.type, node, right)
        return node

    def power(self) -> ASTNode:
        """power -> unary ('^' unary)* （右結合）"""
        node = self.unary()
        if self.current().type == TokenType.POW:
            self.consume(TokenType.POW)
            right = self.power()  # 右結合
            node = BinOpNode(TokenType.POW, node, right)
        return node

    def unary(self) -> ASTNode:
        """unary -> ('+' | '-') unary | call"""
        if self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.current().type)
            operand = self.unary()
            return UnaryOpNode(op.type, operand)
        return self.call()

    def call(self) -> ASTNode:
        """call -> primary ('(' expr (',' expr)* ')')?"""
        node = self.primary()
        if isinstance(node, VarNode) and self.current().type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            args = [self.expr()]
            while self.current().type == TokenType.PLUS:
                # 允許用 + 分隔參數（簡化版）
                pass
            # 支援逗號分隔
            while self.current().type not in (TokenType.RPAREN, TokenType.EOF):
                if self.current().type == TokenType.RPAREN:
                    break
                # 嘗試解析更多參數（支援逗號）
                if self.current().type in (TokenType.NUMBER, TokenType.IDENT,
                                            TokenType.LPAREN, TokenType.MINUS):
                    args.append(self.expr())
                else:
                    break
            self.consume(TokenType.RPAREN)
            node = FuncCallNode(node.name, args)
        return node

    def primary(self) -> ASTNode:
        """primary -> NUMBER | IDENT | '(' expr ')'"""
        token = self.current()

        if token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return NumberNode(token.value)

        if token.type == TokenType.IDENT:
            self.consume(TokenType.IDENT)
            # 檢查是否為賦值
            if self.current().type == TokenType.ASSIGN:
                self.consume(TokenType.ASSIGN)
                value = self.expr()
                return AssignNode(token.value, value)
            return VarNode(token.value)

        if token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            node = self.expr()
            self.consume(TokenType.RPAREN)
            return node

        raise SyntaxError(f"意外的 token: {token}")


# ========== 評估器 ==========


class Calculator:
    """計算機"""

    def __init__(self):
        self.variables: dict = {}
        self.functions: dict = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
            "floor": math.floor,
            "ceil": math.ceil,
            "round": round,
        }

    def evaluate(self, code: str) -> Any:
        """評估表達式"""
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        return self._eval(ast)

    def _eval(self, node: ASTNode) -> Any:
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, BinOpNode):
            left = self._eval(node.left)
            right = self._eval(node.right)

            if node.op == TokenType.PLUS:
                return left + right
            elif node.op == TokenType.MINUS:
                return left - right
            elif node.op == TokenType.MUL:
                return left * right
            elif node.op == TokenType.DIV:
                if right == 0:
                    raise ZeroDivisionError("除以零")
                return left / right
            elif node.op == TokenType.POW:
                return left ** right

        if isinstance(node, UnaryOpNode):
            operand = self._eval(node.operand)
            if node.op == TokenType.MINUS:
                return -operand
            return operand

        if isinstance(node, VarNode):
            name = node.name
            if name in self.variables:
                return self.variables[name]
            if name in self.functions:
                return self.functions[name]
            raise NameError(f"未定義: {name}")

        if isinstance(node, AssignNode):
            value = self._eval(node.value)
            self.variables[node.name] = value
            return value

        if isinstance(node, FuncCallNode):
            func = self.functions.get(node.name)
            if func is None:
                raise NameError(f"未知函數: {node.name}")
            args = [self._eval(arg) for arg in node.args]
            return func(*args)

        raise TypeError(f"未知節點: {type(node)}")


def format_result(value: Any) -> str:
    """格式化輸出"""
    if isinstance(value, float):
        if value == int(value):
            return str(int(value))
        return f"{value:.6g}"
    return str(value)


def demo_basic():
    """基本運算"""
    print("=== 基本運算 ===\n")

    calc = Calculator()

    expressions = [
        "1 + 2",
        "3 * 4 + 5",
        "2 ^ 10",
        "(2 + 3) * (4 - 1)",
        "10 / 3",
        "-5 + 3",
        "2 ^ 3 ^ 2",  # 右結合：2^(3^2) = 2^9 = 512
    ]

    for expr in expressions:
        result = calc.evaluate(expr)
        print(f"  {expr} = {format_result(result)}")


def demo_variables():
    """變數"""
    print("\n=== 變數 ===\n")

    calc = Calculator()

    expressions = [
        "x = 10",
        "y = 20",
        "x + y",
        "x * y - 50",
    ]

    for expr in expressions:
        result = calc.evaluate(expr)
        print(f"  {expr} = {format_result(result)}")


def demo_functions():
    """函數"""
    print("\n=== 數學函數 ===\n")

    calc = Calculator()

    expressions = [
        "sqrt(144)",
        "sin(0)",
        "cos(0)",
        "log10(1000)",
        "exp(1)",
        "floor(3.7)",
        "abs(-42)",
    ]

    for expr in expressions:
        result = calc.evaluate(expr)
        print(f"  {expr} = {format_result(result)}")


def demo_complex():
    """複雜表達式"""
    print("\n=== 複雜表達式 ===\n")

    calc = Calculator()

    # 二次方程求根公式
    print("  二次方程：ax² + bx + c = 0")
    print("  求根公式：x = (-b ± √(b² - 4ac)) / 2a")
    print()

    calc.evaluate("a = 1")
    calc.evaluate("b = -5")
    calc.evaluate("c = 6")

    discriminant = calc.evaluate("b ^ 2 - 4 * a * c")
    print(f"  Δ = b² - 4ac = {format_result(discriminant)}")

    x1 = calc.evaluate("(-b + sqrt(b ^ 2 - 4 * a * c)) / (2 * a)")
    x2 = calc.evaluate("(-b - sqrt(b ^ 2 - 4 * a * c)) / (2 * a)")
    print(f"  x1 = {format_result(x1)}")
    print(f"  x2 = {format_result(x2)}")

    # 複利計算
    print("\n  複利計算：A = P(1 + r)^n")
    print("  P = 1000, r = 0.05, n = 10")
    calc2 = Calculator()
    result = calc2.evaluate("1000 * (1 + 0.05) ^ 10")
    print(f"  A = {format_result(result)}")


def demo_ast():
    """展示 AST"""
    print("\n=== AST 展示 ===\n")

    expressions = [
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "2 ^ 3 ^ 2",
    ]

    for expr in expressions:
        tokens = tokenize(expr)
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"  {expr}")
        print(f"  AST: {ast}\n")


if __name__ == "__main__":
    demo_basic()
    demo_variables()
    demo_functions()
    demo_complex()
    demo_ast()
