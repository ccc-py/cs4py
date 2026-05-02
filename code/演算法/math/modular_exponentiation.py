"""
模冪運算 (Modular Exponentiation)

歷史背景：
- 模冪運算在數論和密碼學中極為重要
- Square-and-multiply（平方乘）演算法是經典的快速冪算法
- 廣泛應用於 RSA 加密、Diffie-Hellman 金鑰交換等密碼學協定

定義：
- 計算 (base^exponent) mod modulus
- 當指數很大時（如 RSA 中的 2048 位元指數），不能直接計算再取模
"""

from typing import List, Tuple, Optional


def modular_pow_iterative(base: int, exponent: int, modulus: int) -> int:
    """
    迭代版 square-and-multiply 演算法

    原理：
    將指數表示為二進位，利用：
    - base^(2k) = (base^k)²
    - base^(2k+1) = (base^k)² * base

    時間複雜度：O(log exponent)
    空間複雜度：O(1)

    Args:
        base: 底數
        exponent: 指數（非負整數）
        modulus: 模數

    Returns:
        (base^exponent) mod modulus
    """
    if modulus == 1:
        return 0

    result = 1
    base = base % modulus
    exp = exponent

    while exp > 0:
        if exp & 1:  # 指數為奇數
            result = (result * base) % modulus
        base = (base * base) % modulus
        exp >>= 1  # 指數右移一位（除以 2）

    return result


def modular_pow_recursive(base: int, exponent: int, modulus: int) -> int:
    """
    遞迴版 square-and-multiply 演算法

    原理：
    - 若 exponent = 0，返回 1
    - 若 exponent 為偶數：result = modular_pow(base² mod m, exp/2, m)
    - 若 exponent 為奇數：result = base * modular_pow(base² mod m, (exp-1)/2, m)

    時間複雜度：O(log exponent)
    空間複雜度：O(log exponent)（呼叫堆疊）

    Args:
        base: 底數
        exponent: 指數
        modulus: 模數

    Returns:
        (base^exponent) mod modulus
    """
    if modulus == 1:
        return 0
    if exponent == 0:
        return 1

    base = base % modulus

    if exponent % 2 == 0:
        temp = modular_pow_recursive(base, exponent // 2, modulus)
        return (temp * temp) % modulus
    else:
        temp = modular_pow_recursive(base, (exponent - 1) // 2, modulus)
        return (base * temp * temp) % modulus


def fermat_test(n: int, a: int) -> bool:
    """
    費馬小定理測試

    費馬小定理：若 p 是質數，則對於任意 a 使得 gcd(a, p) = 1，
    有 a^(p-1) ≡ 1 (mod p)

    這可以用來檢測質數（但只是必要條件，非充分）

    Args:
        n: 待測數（奇數，> 2）
        a: 基底

    Returns:
        若 a^(n-1) ≡ 1 (mod n) 返回 True，否則 False
    """
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    return modular_pow_iterative(a, n - 1, n) == 1


def rsa_demo() -> None:
    """RSA 加密中的模冪運算示例"""
    # 簡化版 RSA 示例
    # 選擇兩個質數
    p = 61
    q = 53
    n = p * q  # 3233
    phi = (p - 1) * (q - 1)  # 3120

    # 選擇 e（公鑰）
    e = 17
    # 計算 d（私鑰），使得 e * d ≡ 1 (mod phi)
    # 這裡簡化，假設 d = 2753

    # 加密：c = m^e mod n
    m = 65  # 明文 'A'
    c = modular_pow_iterative(m, e, n)
    print(f"  RSA 加密示例：")
    print(f"  明文: {m}")
    print(f"  公鑰 (e, n): ({e}, {n})")
    print(f"  密文: {c}")

    # 解密：m = c^d mod n
    d = 2753
    decrypted = modular_pow_iterative(c, d, n)
    print(f"  私鑰 (d, n): ({d}, {n})")
    print(f"  解密後: {decrypted}")


if __name__ == "__main__":
    print("=== 模冪運算 (Modular Exponentiation) 測試 ===\n")

    # 測試 1：基本範例
    print("1. 基本範例：")
    test_cases = [
        (2, 10, 1000),   # 1024 mod 1000 = 24
        (3, 5, 7),       # 243 mod 7 = 5
        (5, 0, 13),      # 1 mod 13 = 1
        (7, 256, 13),    # 大指數測試
    ]

    for base, exp, mod in test_cases:
        result = modular_pow_iterative(base, exp, mod)
        result_r = modular_pow_recursive(base, exp, mod)
        print(f"  {base}^{exp} mod {mod} = {result} (遞迴：{result_r})")
    print()

    # 測試 2：大指數測試
    print("2. 大指數測試：")
    base, exp, mod = 123456789, 987654321, 1000000007
    result = modular_pow_iterative(base, exp, mod)
    print(f"  {base}^{exp} mod {mod}")
    print(f"  結果：{result}")
    print()

    # 測試 3：費馬小定理
    print("3. 費馬小定理測試：")
    test_nums = [17, 15, 97]
    for n in test_nums:
        a = 2
        result = fermat_test(n, a)
        print(f"  n={n}, a={a}: {result} {'(可能是質數)' if result else '(合數)'}")
    print()

    # 測試 4：RSA 示例
    print("4. RSA 加密示例：")
    rsa_demo()
    print()

    # 測試 5：與內建 pow 比較
    print("5. 與 Python 內建 pow 比較：")
    test = (123, 456, 789)
    builtin = pow(test[0], test[1], test[2])
    ours = modular_pow_iterative(test[0], test[1], test[2])
    print(f"  pow{test} = {builtin}")
    print(f"  our_pow{test} = {ours}")
    print(f"  結果相同：{builtin == ours}")
