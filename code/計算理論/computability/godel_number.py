"""
哥德尔数编码 (Gödel Numbering)

哥德尔数是哥德尔在 1931 年提出的技术，用于将形式系统的
符号、公式、证明等编码为自然数。

编码方法：
1. 先给每个基本符号分配一个自然数
2. 将公式（符号序列）编码为：2^a1 × 3^a2 × 5^a3 × ... × p_n^an
   （其中 p_i 是第 i 个质数，a_i 是第 i 个符号的编码）

历史背景：
- 1931 年：Gödel 使用哥德尔数证明不完备定理
- 这种编码允许在算术中「谈论」符号、公式、证明
- 是 metamathematics 进入 mathematics 的关键技术

参考：Gödel, K. (1931). Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I.
"""

from typing import List, Dict, Tuple
import sys


# 基本符号的编码（简化版，使用皮亚诺算术）
SYMBOL_CODES = {
    '0': 1,      # 零
    's': 2,      # 后继函数
    '+': 3,      # 加法
    '×': 4,      # 乘法
    '=': 5,      # 等于
    '(': 6,      # 左括号
    ')': 7,      # 右括号
    'x': 8,      # 变量 x
    "'": 9,      # 索引符号（x' = x₁）
    '¬': 10,     # 否定
    '→': 11,     # 蕴含
    '∀': 12,     # 全称量词
    '∃': 13,     # 存在量词
    ',': 14,     # 逗号
    '⊢': 15,     # 证明符号
}

# 反向映射
CODE_TO_SYMBOL = {v: k for k, v in SYMBOL_CODES.items()}


def symbol_to_code(symbol: str) -> int:
    """将符号转换为哥德尔数"""
    if symbol not in SYMBOL_CODES:
        raise ValueError(f"未知符号: {symbol}")
    return SYMBOL_CODES[symbol]


def code_to_symbol(code: int) -> str:
    """将哥德尔数转换为符号"""
    if code not in CODE_TO_SYMBOL:
        raise ValueError(f"未知编码: {code}")
    return CODE_TO_SYMBOL[code]


def formula_to_godel(formula: List[str]) -> int:
    """
    将公式（符号序列）转换为哥德尔数

    公式 = [s1, s2, ..., sn]
    哥德尔数 = 2^code(s1) × 3^code(s2) × ... × p_n^code(sn)
    """
    godel_num = 1
    for i, symbol in enumerate(formula):
        prime = nth_prime(i)
        code = symbol_to_code(symbol)
        godel_num *= prime ** code
    return godel_num


def godel_to_formula(godel_num: int) -> List[str]:
    """
    将哥德尔数转换回公式（符号序列）

    通过质因数分解还原
    """
    formula = []
    prime_idx = 0

    while godel_num > 1:
        prime = nth_prime(prime_idx)
        count = 0
        while godel_num % prime == 0:
            godel_num //= prime
            count += 1
        if count > 0:
            formula.append(code_to_symbol(count))
        prime_idx += 1

    return formula


def nth_prime(n: int) -> int:
    """返回第 n 个质数（n 从 0 开始）"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    if n < len(primes):
        return primes[n]
    # 继续计算更大的质数
    candidate = primes[-1] + 2
    while len(primes) <= n:
        is_prime = all(candidate % p != 0 for p in primes if p * p <= candidate)
        if is_prime:
            primes.append(candidate)
        candidate += 2
    return primes[n]


def proof_to_godel(proof: List[List[str]]) -> int:
    """
    将证明（公式序列）转换为哥德尔数

    证明 = [公式1, 公式2, ..., 公式k]
    每个公式先编码为哥德尔数
    然后整个证明编码为：2^g1 × 3^g2 × ... × p_k^gk
    """
    godel_num = 1
    for i, formula in enumerate(proof):
        prime = nth_prime(i)
        g_formula = formula_to_godel(formula)
        godel_num *= prime ** g_formula
    return godel_num


def godel_to_proof(godel_num: int) -> List[List[str]]:
    """将哥德尔数转换回证明"""
    proof = []
    prime_idx = 0

    while godel_num > 1:
        prime = nth_prime(prime_idx)
        count = 0
        while godel_num % prime == 0:
            godel_num //= prime
            count += 1
        if count > 0:
            proof.append(godel_to_formula(count))
        prime_idx += 1

    return proof


def is_valid_proof_encoding(godel_num: int) -> bool:
    """
    检查哥德尔数是否可能是有效的证明编码

    实际上，这需要检查每个公式是否遵循语法规则，
    以及每个公式是否可以从前面的公式推导出来。
    这里只是简化版本。
    """
    try:
        proof = godel_to_proof(godel_num)
        return len(proof) > 0
    except:
        return False


def demonstrate_encoding():
    """演示哥德尔数编码"""
    print("=== 哥德尔数编码演示 ===")
    print()

    # 编码简单公式：0 = 0
    print("公式：「0 = 0」")
    formula = ['0', '=', '0']
    godel_num = formula_to_godel(formula)
    print(f"  符号序列：{formula}")
    print(f"  哥德尔数：{godel_num}")
    print(f"  质因数分解：{factorize(godel_num)}")
    print()

    # 解码回来
    decoded = godel_to_formula(godel_num)
    print(f"  解码回来：{decoded}")
    print(f"  是否相同：{decoded == formula}")
    print()

    # 更复杂的公式：s(0) + 0 = s(0)
    print("公式：「s(0) + 0 = s(0)」")
    formula = ['s', '(', '0', ')', '+', '0', '=', 's', '(', '0', ')']
    godel_num = formula_to_godel(formula)
    print(f"  符号序列：{formula}")
    print(f"  哥德尔数：{godel_num}")
    print(f"  质因数分解：{factorize(godel_num)[:100]}...")  # 可能很长
    print()

    # 解码回来
    decoded = godel_to_formula(godel_num)
    print(f"  解码回来：{decoded}")
    print(f"  是否相同：{decoded == formula}")
    print()

    # 编码证明
    print("证明：[「0=0」, 「s(0)=s(0)」]")
    proof = [
        ['0', '=', '0'],
        ['s', '(', '0', ')', '=', 's', '(', '0', ')']
    ]
    godel_num = proof_to_godel(proof)
    print(f"  证明的哥德尔数：{godel_num}")
    print()

    # 解码回来
    decoded_proof = godel_to_proof(godel_num)
    print(f"  解码回来：{decoded_proof}")


def factorize(n: int) -> str:
    """将数字分解为质因数乘积的字符串表示"""
    if n <= 1:
        return str(n)

    factors = []
    prime_idx = 0
    while n > 1:
        prime = nth_prime(prime_idx)
        count = 0
        while n % prime == 0:
            n //= prime
            count += 1
        if count > 0:
            factors.append(f"p{prime_idx}^{count}" if count > 1 else f"p{prime_idx}")
        prime_idx += 1

    return " × ".join(factors)


if __name__ == "__main__":
    demonstrate_encoding()

    print("=" * 60)
    print()
    print("=== 符号编码表 ===")
    print()
    for symbol, code in sorted(SYMBOL_CODES.items(), key=lambda x: x[1]):
        print(f"  '{symbol}' → {code}")
