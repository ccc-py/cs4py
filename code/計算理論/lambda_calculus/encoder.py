"""
Lambda 演算編碼 (Lambda Calculus Encoder)

使用 Church 編碼 (Church Encoding) 將各種資料型態表示為 Lambda 項。

Church 編碼是 Alonzo Church 在 1930 年代提出的，用 Lambda 項表示：
- 數字 (Church Numerals)
- 布林值 (Church Booleans)
- 有序對 (Church Pairs)
- 列表 (Church Lists)
- 遞迴 (Y Combinator)

歷史背景：
- 1930 年代：Alonzo Church 提出 Church 編碼
- 1936 年：Church 使用 Lambda 演算證明 Entscheidungsproblem 不可判定
- Y Combinator：由 Haskell Curry 發現，用於實作遞迴

參考：Church, A. (1936). An unsolvable problem of elementary number theory.
"""

from theory.lambda_calculus.parser import parse_lambda, Variable, Abstraction, Application
from theory.lambda_calculus.reducer import reduce


# Church 數字 (Church Numerals)
# n = λf.λx.f^n x  (f 應用 n 次)

def church_zero():
    """Church 數字 0: λf.λx.x"""
    return parse_lambda("λf.λx.x")


def church_one():
    """Church 數字 1: λf.λx.f x"""
    return parse_lambda("λf.λx.f x")


def church_two():
    """Church 數字 2: λf.λx.f (f x)"""
    return parse_lambda("λf.λx.f (f x)")


def church_succ():
    """後繼函數: λn.λf.λx.f (n f x)"""
    return parse_lambda("λn.λf.λx.f ((n f) x)")


def church_add():
    """加法: λm.λn.λf.λx.((m f) (n f x))"""
    return parse_lambda("λm.λn.λf.λx.((m f) ((n f) x))")


def church_mult():
    """乘法: λm.λn.λf.m (n f)"""
    return parse_lambda("λm.λn.λf.m (n f)")


def church_to_int(term):
    """
    將 Church 數字轉換為 Python 整數

    透過將 f 設為 (lambda x: x + 1)，x 設為 0 來求值
    """
    # 建立求值函數
    def f(x):
        return x + 1

    def apply_term(term, arg):
        """將 Lambda 項應用於 Python 值"""
        if isinstance(term, Abstraction):
            # λx.M 應用於 arg → M[x := arg]
            from theory.lambda_calculus.reducer import substitute
            return substitute(term.body, term.param, Variable(str(arg)))
        elif isinstance(term, Application):
            # M N → 先化簡 M，再應用
            func = reduce(term.func)
            return apply_term(func, arg)
        return term

    # 應用 f 和 x
    result = apply_term(term, 0)
    # 計算 f 的應用次數
    count = 0
    current = result
    while isinstance(current, Application):
        if isinstance(current.func, Application):
            count += 1
        current = current.arg
    return count


# Church 布林值 (Church Booleans)

def church_true():
    """Church True: λx.λy.x (選擇第一個)"""
    return parse_lambda("λx.λy.x")


def church_false():
    """Church False: λx.λy.y (選擇第二個)"""
    return parse_lambda("λx.λy.y")


def church_and():
    """And: λp.λq.p q p"""
    return parse_lambda("λp.λq.p q p")


def church_or():
    """Or: λp.λq.p p q"""
    return parse_lambda("λp.λq.p p q")


def church_not():
    """Not: λp.p False True"""
    return parse_lambda("λp.p (λx.λy.y) (λx.λy.x)")


# Church 有序對 (Church Pairs)

def church_pair():
    """建立有序對: λx.λy.λf.f x y"""
    return parse_lambda("λx.λy.λf.f x y")


def church_first():
    """取出第一個元素: λp.p (λx.λy.x)"""
    return parse_lambda("λp.p (λx.λy.x)")


def church_second():
    """取出第二個元素: λp.p (λx.λy.y)"""
    return parse_lambda("λp.p (λx.λy.y)")


# Y Combinator (用於遞迴)

def y_combinator():
    """
    Y Combinator: λf.(λx.f (x x)) (λx.f (x x))

    用於在無遞迴定義的語言中實作遞迴
    """
    return parse_lambda("λf.(λx.f (x x)) (λx.f (x x))")


def church_is_zero():
    """檢查是否為零: λn.n (λx.False) True"""
    return parse_lambda("λn.n (λx.λx.λy.y) (λx.λy.x)")


if __name__ == "__main__":
    print("=== Church 編碼測試 ===")
    print()

    # 測試：Church 數字
    print("測試：Church 數字")
    zero = church_zero()
    one = church_one()
    two = church_two()
    print(f"  Zero: {zero}")
    print(f"  One: {one}")
    print(f"  Two: {two}")

    # 測試：後繼
    print()
    print("測試：後繼函數")
    succ = church_succ()
    # 將 succ 應用於 zero，應該得到 one
    result = reduce(Application(succ, zero))
    print(f"  succ zero: {result}")
    print(f"  預期: {one}")
    print(f"  是否相同: {str(result) == str(one)}")

    # 測試：加法
    print()
    print("測試：加法")
    add = church_add()
    # 1 + 2 = 3
    one_plus_two = Application(Application(add, one), two)
    result = reduce(one_plus_two)
    print(f"  1 + 2 = {result}")

    # 測試：乘法
    print()
    print("測試：乘法")
    mult = church_mult()
    # 2 * 3
    two = church_two()
    three = reduce(Application(succ, church_two()))  # 簡化：用 succ 產生 3
    two_times_three = Application(Application(mult, two), three)
    result = reduce(two_times_three)
    print(f"  2 * 3 = {result}")

    print()
    print("測試：Church 布林值")
    true_val = church_true()
    false_val = church_false()
    print(f"  True: {true_val}")
    print(f"  False: {false_val}")

    print()
    print("測試：Church 有序對")
    pair = church_pair()
    first = church_first()
    second = church_second()
    # 建立 pair 3 5，取出 first 應該是 3
    three = church_two()  # 簡化
    five = church_two()   # 簡化
    p = Application(Application(pair, three), five)
    fst = Application(first, p)
    result = reduce(fst)
    print(f"  first (pair 3 5) = {result}")

    print()
    print("測試：Y Combinator")
    y = y_combinator()
    print(f"  Y = {y}")
    print("  (Y 可以用於實作遞迴)")
