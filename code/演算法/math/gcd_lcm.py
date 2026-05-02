"""
GCD（最大公因數）與 LCM（最小公倍數）演算法

包含歐幾里得演算法、擴展歐幾里得演算法，以及 LCM 計算。
"""

from typing import Tuple, Optional


def gcd(a: int, b: int) -> int:
    """
    使用歐幾里得演算法計算最大公因數

    歐幾里得演算法基於原理：gcd(a, b) = gcd(b, a mod b)
    當餘數為 0 時，除數即為最大公因數。

    時間複雜度：O(log min(a, b))

    參數:
        a: 第一個整數
        b: 第二個整數

    回傳:
        a 和 b 的最大公因數（非負整數）
    """
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b
    return a


def gcd_recursive(a: int, b: int) -> int:
    """
    歐幾里得演算法的遞迴版本

    參數:
        a: 第一個整數
        b: 第二個整數

    回傳:
        a 和 b 的最大公因數
    """
    a = abs(a)
    b = abs(b)
    if b == 0:
        return a
    return gcd_recursive(b, a % b)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    擴展歐幾里得演算法

    找出整數 x, y 使得 ax + by = gcd(a, b)
    這在計算模反元素（Modular Inverse）和中國餘式定理（CRT）中非常有用。

    參數:
        a: 第一個整數
        b: 第二個整數

    回傳:
        (gcd, x, y) 的元組，其中 gcd = ax + by
    """
    a = abs(a)
    b = abs(b)

    if b == 0:
        return a, 1, 0

    gcd_val, x1, y1 = extended_gcd(b, a % b)

    # 根據遞迴關係計算 x, y
    x: int = y1
    y: int = x1 - (a // b) * y1

    return gcd_val, x, y


def lcm(a: int, b: int) -> int:
    """
    計算最小公倍數

    公式：lcm(a, b) = |a * b| / gcd(a, b)

    參數:
        a: 第一個整數
        b: 第二個整數

    回傳:
        a 和 b 的最小公倍數
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def lcm_multiple(numbers: list[int]) -> int:
    """
    計算多個整數的最小公倍數

    參數:
        numbers: 整數列表

    回傳:
        所有數字的最小公倍數
    """
    if not numbers:
        return 0

    result: int = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    計算 a 在模 m 下的反元素

    即找出 x 使得 (a * x) ≡ 1 (mod m)
    當 gcd(a, m) = 1 時，反元素存在。

    參數:
        a: 要計算反元素的數
        m: 模數

    回傳:
        模反元素，如果不存在則回傳 None
    """
    a = a % m
    gcd_val, x, _ = extended_gcd(a, m)

    if gcd_val != 1:
        return None  # 反元素不存在

    return x % m


if __name__ == "__main__":
    # 示範 GCD 和 LCM 演算法
    print("GCD 與 LCM 演算法示範")
    print("=" * 40)

    # GCD 測試
    test_pairs: list[Tuple[int, int]] = [(48, 18), (100, 75), (17, 13), (0, 5), (-12, 8)]
    print("\n最大公因數 (GCD) 測試:")
    for a, b in test_pairs:
        result: int = gcd(a, b)
        result_rec: int = gcd_recursive(a, b)
        print(f"  gcd({a}, {b}) = {result} (遞迴: {result_rec})")

    # 擴展 GCD 測試
    print("\n擴展歐幾里得演算法測試:")
    test_ext: list[Tuple[int, int]] = [(48, 18), (30, 12), (35, 15), (17, 13)]
    for a, b in test_ext:
        g, x, y = extended_gcd(a, b)
        print(f"  gcd({a}, {b}) = {g}, x={x}, y={y}")
        print(f"    驗證: {a}*{x} + {b}*{y} = {a*x + b*y}")

    # LCM 測試
    print("\n最小公倍數 (LCM) 測試:")
    for a, b in [(4, 6), (15, 20), (7, 3), (0, 5)]:
        result: int = lcm(a, b)
        print(f"  lcm({a}, {b}) = {result}")

    # 多數 LCM 測試
    print("\n多個數字的 LCM:")
    numbers: list[int] = [4, 6, 8, 12]
    print(f"  lcm({numbers}) = {lcm_multiple(numbers)}")

    # 模反元素測試
    print("\n模反元素測試:")
    mod_pairs: list[Tuple[int, int]] = [(3, 11), (7, 13), (2, 4), (17, 3120)]
    for a, m in mod_pairs:
        inv = mod_inverse(a, m)
        if inv is not None:
            print(f"  {a}^(-1) mod {m} = {inv} (驗證: {a}*{inv} mod {m} = {(a*inv) % m})")
        else:
            print(f"  {a}^(-1) mod {m} 不存在 (gcd({a}, {m}) != 1)")
