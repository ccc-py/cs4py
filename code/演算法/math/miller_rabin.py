"""
Miller-Rabin 質數測試 (Miller-Rabin Primality Test)

歷史背景：
- 由 Gary L. Miller 於 1976 年提出（確定性版本，依賴未證明的 Riemann 猜想）
- Michael O. Rabin 於 1980 年將其改進為概率性演算法
- 是實務上最常用的質數測試演算法之一
- 廣泛應用於密碼學中的大質數生成

特性：
- 概率性測試：不確定性，但錯誤機率可以任意小
- 對於 64 位元以下的整數，使用特定基底可以達到確定性
- 時間複雜度：O(k * log³ n)，k 是測試輪數
"""

from typing import List, Tuple, Optional
import random


def modular_pow(base: int, exponent: int, modulus: int) -> int:
    """輔助函數：模冪運算（square-and-multiply）"""
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    exp = exponent
    while exp > 0:
        if exp & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exp >>= 1
    return result


def miller_rabin_test(n: int, a: int) -> bool:
    """
    對 n 進行 Miller-Rabin 測試，使用基底 a

    原理：
    將 n-1 寫為 d * 2^s，其中 d 是奇數
    計算 a^d mod n
    如果結果是 1 或 -1 (n-1)，則 n 可能是質數
    否則，重複平方 s-1 次，檢查是否出現 -1

    Args:
        n: 待測數（奇數，> 2）
        a: 基底（witness）

    Returns:
        True 表示 n 可能是質數，False 表示 n 一定是合數
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # 將 n-1 寫為 d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # 計算 a^d mod n
    x = modular_pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    # 重複平方 s-1 次
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
        if x == 1:
            return False

    return False


def is_prime_probabilistic(n: int, k: int = 5) -> bool:
    """
    概率性 Miller-Rabin 質數測試

    Args:
        n: 待測數
        k: 測試輪數（越大越準確）

    Returns:
        True 表示很可能是質數，False 表示一定是合數
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # 選擇隨機基底
    for _ in range(k):
        a = random.randrange(2, n - 1)
        if not miller_rabin_test(n, a):
            return False

    return True


def is_prime_deterministic_64bit(n: int) -> bool:
    """
    對於 64 位元以下的整數，使用確定性 Miller-Rabin 測試

    根據研究，對於 n < 2^64，使用以下基底即可確定：
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    Args:
        n: 待測數（< 2^64）

    Returns:
        True 表示質數，False 表示合數
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # 用於 64 位元整數的確定性基底集
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for a in witnesses:
        if a >= n:
            break
        if not miller_rabin_test(n, a):
            return False

    return True


def trial_division(n: int) -> bool:
    """試除法質數測試（用於比較）"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def compare_with_trial_division(limit: int = 1000) -> None:
    """比較 Miller-Rabin 與試除法的結果"""
    print(f"  比較 2 到 {limit} 的質數檢測：")
    mr_errors = 0
    for n in range(2, limit):
        mr_result = is_prime_deterministic_64bit(n)
        td_result = trial_division(n)
        if mr_result != td_result:
            print(f"    不一致：n={n}, MR={mr_result}, TD={td_result}")
            mr_errors += 1
    if mr_errors == 0:
        print(f"  所有結果一致！")


if __name__ == "__main__":
    print("=== Miller-Rabin 質數測試 測試 ===\n")

    # 測試 1：小質數測試
    print("1. 小質數測試：")
    test_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for n in test_nums:
        mr = is_prime_deterministic_64bit(n)
        td = trial_division(n)
        print(f"  {n}: Miller-Rabin={mr}, 試除法={td}")
    print()

    # 測試 2：合數測試
    print("2. 合數測試：")
    composites = [4, 6, 8, 9, 10, 15, 21, 25, 49, 91, 121]
    for n in composites:
        mr = is_prime_deterministic_64bit(n)
        print(f"  {n}: Miller-Rabin={mr} {'(正確檢測為合數)' if not mr else '(錯誤!)'}")
    print()

    # 測試 3：大數測試
    print("3. 大數測試：")
    large_nums = [104729, 1000003, 999983, 1000000007, 9999999967]
    for n in large_nums:
        mr = is_prime_deterministic_64bit(n)
        print(f"  {n}: {'質數' if mr else '合數'}")
    print()

    # 測試 4：概率性 vs 確定性
    print("4. 概率性測試（k=5）vs 確定性：")
    test_num = 999983
    prob = is_prime_probabilistic(test_num, 5)
    det = is_prime_deterministic_64bit(test_num)
    print(f"  n={test_num}")
    print(f"  概率性 (k=5): {prob}")
    print(f"  確定性: {det}")
    print()

    # 測試 5：與試除法比較
    print("5. 與試除法比較（2-1000）：")
    compare_with_trial_division(1000)
