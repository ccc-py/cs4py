"""
Lisp 解譯器 (Minimal Lisp Interpreter)

歷史背景：
- 1958 年由 John McCarthy 在 MIT 發明
- 基於 Lambda 演算，是最古老的函數式程式語言之一
- 原始定義僅用 7 個核心形式：quote, atom, eq, car, cdr, cons, cond
- 1960 年 McCarthy 發表「Recursive Functions of Symbolic Expressions」
- 深刻影響了後續的函數式語言：Scheme, Common Lisp, Clojure 等

核心概念：
- 萬物皆為 S-expression（符號表達式）
- Code is data, data is code（同像性）
- 核心評估規則：eval + apply 遞迴
- 閉包（closure）：函數 + 環境
"""

from typing import Any, Dict, List, Optional, Callable
import math


# ========== S-Expression 解析器 ==========


class Symbol:
    """符號：Lisp 中的變數名"""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Quoted:
    """引用表達式：'(...)" """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"'{self.value}"


def tokenize(text: str) -> List[str]:
    """將輸入文字分解為 tokens"""
    # 處理引號
    text = text.replace("'", " ' ")
    text = text.replace("(", " ( ").replace(")", " ) ")
    return text.split()


def parse(tokens: List[str]) -> Any:
    """將 tokens 解析為 S-expression"""
    if not tokens:
        raise ValueError("意外的 EOF")

    token = tokens.pop(0)

    if token == "'":
        return Quoted(parse(tokens))

    if token == "(":
        lst = []
        while tokens[0] != ")":
            lst.append(parse(tokens))
        tokens.pop(0)  # 消耗 ")"
        return lst

    if token == ")":
        raise ValueError("意外的 )")

    # 嘗試解析為數字
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def parse_expression(text: str) -> Any:
    """解析完整的 S-expression"""
    tokens = tokenize(text)
    return parse(tokens)


# ========== 環境 ==========


class Environment:
    """Lisp 運行環境"""

    def __init__(self, params=None, args=None, outer=None):
        self.vars: Dict[str, Any] = {}
        self.outer = outer

        if params and args:
            for param, arg in zip(params, args):
                self.define(param.name, arg)

    def define(self, name: str, value: Any) -> None:
        self.vars[name] = value

    def find(self, name: str) -> 'Environment':
        if name in self.vars:
            return self
        elif self.outer:
            return self.outer.find(name)
        else:
            raise NameError(f"未定義的變數: {name}")

    def get(self, name: str) -> Any:
        return self.find(name).vars[name]

    def set(self, name: str, value: Any) -> None:
        self.find(name).vars[name] = value


def global_env() -> Environment:
    """建立全域環境"""
    env = Environment()

    # 基本運算
    env.define("+", lambda *args: sum(args))
    env.define("-", lambda *args: args[0] - sum(args[1:]) if len(args) > 1 else -args[0])
    env.define("*", lambda *args: math.prod(args))
    env.define("/", lambda *args: args[0] / math.prod(args[1:]) if len(args) > 1 else 1 / args[0])
    env.define("=", lambda x, y: x == y)
    env.define("<", lambda x, y: x < y)
    env.define(">", lambda x, y: x > y)
    env.define("<=", lambda x, y: x <= y)
    env.define(">=", lambda x, y: x >= y)
    env.define("not", lambda x: not x)
    env.define("null?", lambda x: x is None or x == [])
    env.define("list", lambda *args: list(args))
    env.define("cons", lambda x, y: [x] + (y if isinstance(y, list) else [y]))
    env.define("car", lambda x: x[0] if isinstance(x, list) else None)
    env.define("cdr", lambda x: x[1:] if isinstance(x, list) else [])
    env.define("append", lambda *args: [item for arg in args for item in arg])
    env.define("length", lambda x: len(x) if isinstance(x, list) else 0)
    env.define("display", lambda *args: print(" ".join(str(a) for a in args)))
    env.define("newline", lambda: print())
    env.define("abs", abs)
    env.define("max", max)
    env.define("min", min)

    return env


# ========== 評估器 ==========


class Procedure:
    """使用者定義的函數（閉包）"""

    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval_body(self.body, Environment(self.params, args, self.env))


def eval_body(body, env):
    """評估函數體（多個表達式，返回最後一個）"""
    result = None
    for expr in body:
        result = lisp_eval(expr, env)
    return result


def lisp_eval(expr, env: Environment) -> Any:
    """
    Lisp 評估器

    核心規則：
    1. 數字/字串：返回自身
    2. 符號：查找變數
    3. 引用：返回未評估的表達式
    4. 列表：特殊形式或函數呼叫
    """
    # 原子值
    if isinstance(expr, (int, float, str, bool)):
        return expr

    if isinstance(expr, Quoted):
        return expr.value

    # 符號：查變數
    if isinstance(expr, Symbol):
        return env.get(expr.name)

    # 列表：特殊形式或函數呼叫
    if isinstance(expr, list):
        if not expr:
            return []

        head = expr[0]

        # quote: 引用
        if head == "quote" or head == Symbol("quote"):
            return expr[1]

        # if: 條件分支
        if head == "if" or head == Symbol("if"):
            _, test, consequent, *alternative = expr
            if lisp_eval(test, env):
                return lisp_eval(consequent, env)
            elif alternative:
                return lisp_eval(alternative[0], env)
            else:
                return None

        # define: 定義變數
        if head == "define" or head == Symbol("define"):
            _, name, value = expr
            if isinstance(name, Symbol):
                env.define(name.name, lisp_eval(value, env))
            else:
                # (define (f x) body) => (define f (lambda (x) body))
                func_name = name[0].name
                params = name[1:]
                body = expr[2:]
                env.define(func_name, Procedure(params, body, env))
            return None

        # set!: 賦值
        if head == "set!" or head == Symbol("set!"):
            _, name, value = expr
            env.set(name.name, lisp_eval(value, env))
            return None

        # lambda: 匿名函數
        if head == "lambda" or head == Symbol("lambda"):
            _, params, *body = expr
            return Procedure(params, body, env)

        # begin: 序列執行
        if head == "begin" or head == Symbol("begin"):
            return eval_body(expr[1:], env)

        # let: 局部綁定
        if head == "let" or head == Symbol("let"):
            _, bindings, *body = expr
            new_env = Environment(outer=env)
            for binding in bindings:
                name, value = binding
                new_env.define(name.name, lisp_eval(value, env))
            return eval_body(body, new_env)

        # cond: 多重條件
        if head == "cond" or head == Symbol("cond"):
            for clause in expr[1:]:
                test, *result_exprs = clause
                if test == "else" or lisp_eval(test, env):
                    return eval_body(result_exprs, env)
            return None

        # and/or: 邏輯運算
        if head == "and" or head == Symbol("and"):
            for arg in expr[1:]:
                if not lisp_eval(arg, env):
                    return False
            return True

        if head == "or" or head == Symbol("or"):
            for arg in expr[1:]:
                result = lisp_eval(arg, env)
                if result:
                    return result
            return False

        # 一般函數呼叫
        func = lisp_eval(head, env)
        args = [lisp_eval(arg, env) for arg in expr[1:]]

        if callable(func):
            return func(*args)
        elif isinstance(func, Procedure):
            return func(*args)
        else:
            raise TypeError(f"不可呼叫: {func}")

    raise TypeError(f"未知表達式: {expr}")


def run(code: str, env: Optional[Environment] = None) -> Any:
    """執行 Lisp 程式碼"""
    if env is None:
        env = global_env()
    expr = parse_expression(code)
    return lisp_eval(expr, env)


def to_string(val: Any) -> str:
    """將 Lisp 值轉換為字串"""
    if isinstance(val, list):
        return "(" + " ".join(to_string(x) for x in val) + ")"
    elif isinstance(val, bool):
        return "#t" if val else "#f"
    elif val is None:
        return "#<void>"
    elif isinstance(val, Symbol):
        return val.name
    else:
        return str(val)


# ========== 互動式直譯 ==========


def repl():
    """Lisp 互動式直譯器"""
    env = global_env()
    print("Mini Lisp Interpreter (輸入 'exit' 離開)\n")

    while True:
        try:
            code = input("lisp> ")
            if code.strip() == "exit":
                break
            if not code.strip():
                continue

            result = run(code, env)
            if result is not None:
                print(f"  => {to_string(result)}")
        except EOFError:
            break
        except Exception as e:
            print(f"  錯誤: {e}")


# ========== 演示 ==========


def demo_basic():
    """基本運算演示"""
    print("=== Lisp 基本運算 ===\n")

    env = global_env()

    programs = [
        "(+ 1 2 3)",
        "(* 3 4 5)",
        "(< 3 5)",
        "(define x 10)",
        "(+ x 5)",
        "(define (square n) (* n n))",
        "(square 7)",
        "(if (> 5 3) 'yes 'no)",
        "(cons 1 (cons 2 (cons 3 '())))",
        "(car '(1 2 3))",
        "(cdr '(1 2 3))",
    ]

    for program in programs:
        result = run(program, env)
        print(f"  {program}")
        print(f"  => {to_string(result)}\n")


def demo_recursion():
    """遞迴函數演示"""
    print("=== 遞迴函數 ===\n")

    env = global_env()

    # 階乘
    run("(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1)))))", env)
    print(f"  (factorial 5) => {to_string(run('(factorial 5)', env))}")
    print(f"  (factorial 10) => {to_string(run('(factorial 10)', env))}")

    # Fibonacci
    run("(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))", env)
    print(f"\n  (fib 10) => {to_string(run('(fib 10)', env))}")


def demo_higher_order():
    """高階函數演示"""
    print("\n=== 高階函數 ===\n")

    env = global_env()

    # map 函數
    run("(define (map fn lst) (if (null? lst) '() (cons (fn (car lst)) (map fn (cdr lst)))))", env)
    run("(define (double n) (* n 2))", env)
    result = run("(map double '(1 2 3 4 5))", env)
    print(f"  (map double '(1 2 3 4 5)) => {to_string(result)}")

    # lambda
    result = run("((lambda (x y) (+ (* x x) (* y y))) 3 4)", env)
    print(f"\n  ((lambda (x y) (+ (* x x) (* y y))) 3 4) => {to_string(result)}")

    # 閉包
    run("(define (make-adder n) (lambda (x) (+ x n)))", env)
    run("(define add5 (make-adder 5))", env)
    result = run("(add5 10)", env)
    print(f"\n  (define add5 (make-adder 5)) => 建立閉包")
    print(f"  (add5 10) => {to_string(result)}")


def demo_let():
    """let 綁定演示"""
    print("\n=== let 綁定 ===\n")

    env = global_env()

    result = run("(let ((x 10) (y 20)) (+ x y))", env)
    print(f"  (let ((x 10) (y 20)) (+ x y)) => {to_string(result)}")

    result = run("(let ((x 5)) (let ((y (* x 2))) (+ x y)))", env)
    print(f"  (let ((x 5)) (let ((y (* x 2))) (+ x y))) => {to_string(result)}")


if __name__ == "__main__":
    demo_basic()
    demo_recursion()
    demo_higher_order()
    demo_let()
