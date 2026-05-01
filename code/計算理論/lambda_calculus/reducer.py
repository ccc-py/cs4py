"""
Lambda 演算化簡器 (Lambda Calculus Reducer)

實作 Lambda 項的 β-化簡 (beta reduction)。

β-化簡規則：(λx.M) N → M[x := N]
意思是：將函數體 M 中所有的 x 替換為 N。

化簡策略：
- 最左最外 (Leftmost-outermost): 總是化簡最左邊、最外層的可化簡項
- 這對應於非嚴格求值 (lazy evaluation)

歷史背景：
- 1930 年代：Alonzo Church 提出 Lambda 演算和 β-化簡
- 1970 年代：Lambda 演算成為函數式程式設計的理論基礎
- 1936 年：Church 和 Rosser 證明了化簡的收斂性（Church-Rosser 定理）

參考：Church, A. (1936). An unsolvable problem of elementary number theory.
"""

from theory.lambda_calculus.parser import LambdaTerm, Variable, Abstraction, Application, parse_lambda


def free_variables(term: LambdaTerm) -> set:
    """找出 Lambda 項中的自由變數"""
    if isinstance(term, Variable):
        return {term.name}
    elif isinstance(term, Abstraction):
        return free_variables(term.body) - {term.param}
    elif isinstance(term, Application):
        return free_variables(term.func) | free_variables(term.arg)
    return set()


def bound_variables(term: LambdaTerm) -> set:
    """找出 Lambda 項中的綁定變數"""
    if isinstance(term, Variable):
        return set()
    elif isinstance(term, Abstraction):
        return {term.param} | bound_variables(term.body)
    elif isinstance(term, Application):
        return bound_variables(term.func) | bound_variables(term.arg)
    return set()


def fresh_variable(term: LambdaTerm, base: str) -> str:
    """產生一個在 term 中未出現的新變數名"""
    all_vars = free_variables(term) | bound_variables(term)
    new_name = base
    counter = 0
    while new_name in all_vars:
        new_name = f"{base}{counter}"
        counter += 1
    return new_name


def substitute(term: LambdaTerm, var: str, value: LambdaTerm) -> LambdaTerm:
    """
    替換：將 term 中所有的自由變數 var 替換為 value

    term[var := value]
    """
    if isinstance(term, Variable):
        if term.name == var:
            return value
        return term

    elif isinstance(term, Abstraction):
        if term.param == var:
            # var 被綁定在這個抽象中，不替換
            return term
        else:
            # 需要檢查 value 中的自由變數是否會被捕捉
            fv_value = free_variables(value)
            if term.param in fv_value:
                # 發生變數捕捉，需要 α-轉換
                new_param = fresh_variable(value, term.param)
                # 將函數體中的 param 替換為 new_param
                new_body = substitute(term.body, term.param, Variable(new_param))
                return Abstraction(new_param, substitute(new_body, var, value))
            else:
                return Abstraction(term.param, substitute(term.body, var, value))

    elif isinstance(term, Application):
        return Application(
            substitute(term.func, var, value),
            substitute(term.arg, var, value)
        )

    return term


def beta_reduce(term: LambdaTerm) -> LambdaTerm:
    """
    進行一次 β-化簡（最左最外策略）

    返回 (new_term, reduced)
    - new_term: 化簡後的項
    - reduced: 是否進行了化簡
    """
    if isinstance(term, Variable):
        return term, False

    elif isinstance(term, Abstraction):
        # 嘗試化簡函數體
        new_body, reduced = beta_reduce(term.body)
        if reduced:
            return Abstraction(term.param, new_body), True
        return term, False

    elif isinstance(term, Application):
        # 檢查是否為 redex (λx.M) N
        if isinstance(term.func, Abstraction):
            # 進行 β-化簡
            func = term.func
            arg = term.arg
            new_term = substitute(func.body, func.param, arg)
            return new_term, True
        else:
            # 嘗試化簡函數部分
            new_func, reduced = beta_reduce(term.func)
            if reduced:
                return Application(new_func, term.arg), True
            # 嘗試化簡參數部分
            new_arg, reduced = beta_reduce(term.arg)
            if reduced:
                return Application(term.func, new_arg), True
            return term, False

    return term, False


def reduce(term: LambdaTerm, max_steps: int = 100) -> LambdaTerm:
    """
    完全化簡 Lambda 項（進行多次 β-化簡）

    Args:
        term: 要化簡的 Lambda 項
        max_steps: 最大化簡步數（防止無限循環）

    Returns:
        化簡後的項
    """
    current = term
    steps = 0

    while steps < max_steps:
        new_term, reduced = beta_reduce(current)
        if not reduced:
            break
        current = new_term
        steps += 1

    return current


def reduce_and_trace(term: LambdaTerm, max_steps: int = 100):
    """
    化簡並追蹤每一步

    Yields: (step_number, term_before, term_after)
    """
    current = term
    steps = 0

    while steps < max_steps:
        new_term, reduced = beta_reduce(current)
        if not reduced:
            break
        yield steps + 1, current, new_term
        current = new_term
        steps += 1


if __name__ == "__main__":
    print("=== Lambda 演算化簡器測試 ===")
    print()

    # 測試：恆等函數應用
    print("測試：恆等函數 (λx.x) y")
    expr = parse_lambda("(λx.x) y")
    result = reduce(expr)
    print(f"  原始: {expr}")
    print(f"  化簡: {result}")
    print()

    # 測試：常數函數
    print("測試：常數函數 (λx.λy.x) a b")
    expr = parse_lambda("(λx.λy.x) a b")
    result = reduce(expr)
    print(f"  原始: {expr}")
    print(f"  化簡: {result}")
    print()

    # 測試：追蹤化簡過程
    print("測試：追蹤化簡過程 (λx.λy.x y) a b")
    expr = parse_lambda("(λx.λy.x y) a b")
    print(f"  原始: {expr}")
    for step, before, after in reduce_and_trace(expr):
        print(f"  步驟 {step}: {before} → {after}")
    print()

    # 測試：Church 數 2 應用
    print("測試：Church 數 2 (λf.λx.f (f x)) 應用於 s 和 z")
    expr = parse_lambda("(λf.λx.f (f x)) s z")
    print(f"  原始: {expr}")
    result = reduce(expr)
    print(f"  化簡: {result}")
    print()

    # 測試：自由變數
    print("測試：自由變數")
    expr = parse_lambda("λx.x y")
    fv = free_variables(expr)
    print(f"  '{expr}' 的自由變數: {fv}")
